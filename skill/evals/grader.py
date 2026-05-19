#!/usr/bin/env python3
"""
Wu-Wei Rewriter — autograder.

Pipeline:
  1. Load evals/golden_set.jsonl
  2. For each case: invoke the rewriter (Anthropic API, system_prompt_v1.2.md)
  3. Invoke the LLM judge (separate model) with grader_prompt.md
  4. Compute structural assertions deterministically (regex/section presence)
  5. Merge judge JSON + structural assertions
  6. Write results jsonl + summary md to evals/results/<timestamp>/

Usage:
  python evals/grader.py                              # full run
  python evals/grader.py --type pitch                 # filter by artifact_type
  python evals/grader.py --limit 5                    # smoke test
  python evals/grader.py --case gs_022                # single case
  python evals/grader.py --skip-rewriter --use-cache  # re-judge cached rewrites

Requires:  ANTHROPIC_API_KEY  in env
Optional:  REWRITER_MODEL (default claude-opus-4-7), JUDGE_MODEL (default claude-sonnet-4-6)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import anthropic  # type: ignore
except ImportError:
    print("ERROR: pip install --break-system-packages anthropic", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SYS_PROMPT_PATH = ROOT / "system_prompt_v1.2.md"
JUDGE_PROMPT_PATH = ROOT / "evals" / "grader_prompt.md"
GOLDEN_PATH = ROOT / "evals" / "golden_set.jsonl"
RESULTS_DIR = ROOT / "evals" / "results"
CACHE_DIR = ROOT / "evals" / ".cache"

REWRITER_MODEL = os.environ.get("REWRITER_MODEL", "claude-opus-4-7")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-sonnet-4-6")

REQUIRED_SECTIONS = [
    "## REWRITE", "## BOUNDARY", "## PREDICTIONS",
    "## POLARITY NOTES", "## KILLED CLAIMS", "## ELEGANCE AUDIT",
    "## FRAME LOG ENTRY",
]
OBJECTION_HEADER = "## OBJECTION"


# ---------------------------------------------------------------------------
# data classes
# ---------------------------------------------------------------------------
@dataclass
class StructuralAssertions:
    expected_outcome_matched: Optional[bool] = None
    refusal_type_correct: Optional[bool] = None
    kills_count_ok: Optional[bool] = None
    predictions_count_ok: Optional[bool] = None
    polarity_flag_present_as_expected: Optional[bool] = None
    frame_log_present: Optional[bool] = None
    schema_order_correct: Optional[bool] = None


@dataclass
class CaseResult:
    case_id: str
    artifact_type: str
    domain: str
    rewriter_output: str
    structural: StructuralAssertions
    judge: dict = field(default_factory=dict)
    aggregate: str = "UNKNOWN"
    elapsed_s: float = 0.0
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# rewriter & judge calls
# ---------------------------------------------------------------------------
def call_rewriter(client: anthropic.Anthropic, system_prompt: str, case: dict) -> str:
    """Build the user message from the case and call the rewriter model."""
    user_payload = {
        "artifact_text": case["input"],
        "artifact_type": case["artifact_type"],
        "domain": case.get("domain"),
        "intended_use": case.get("intended_use"),
        "author_confidence": case.get("author_confidence"),
        "pitch_mode": case.get("modes", {}).get("pitch_mode", "strict"),
        "creative_mode": case.get("modes", {}).get("creative_mode", "ship"),
        "prior_versions": case.get("prior_versions", []),
    }
    user_msg = (
        "Process the following artifact through the Wu-Wei Rewriter pipeline.\n\n"
        f"```json\n{json.dumps(user_payload, ensure_ascii=False, indent=2)}\n```\n\n"
        "Emit the strict OUTPUT SCHEMA. No preamble."
    )
    resp = client.messages.create(
        model=REWRITER_MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def call_judge(client: anthropic.Anthropic, judge_prompt: str,
               case: dict, rewriter_output: str) -> dict:
    """Send the case + agent output to the judge model. Expect strict JSON back."""
    user_msg = (
        f"## CASE\n```json\n{json.dumps(case, ensure_ascii=False, indent=2)}\n```\n\n"
        f"## AGENT OUTPUT\n```\n{rewriter_output}\n```\n\n"
        "Return your verdict as strict JSON per the schema in the system prompt. "
        "No preamble. No markdown fences around the JSON."
    )
    resp = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=2048,
        system=judge_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```\s*$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        return {"_judge_parse_error": str(e), "_raw": text[:2000]}


# ---------------------------------------------------------------------------
# structural assertions (deterministic, regex/section checks)
# ---------------------------------------------------------------------------
def check_structure(case: dict, output: str) -> StructuralAssertions:
    a = StructuralAssertions()
    expected = case["expected_outcome"]
    is_objection = OBJECTION_HEADER in output

    if expected == "objection":
        a.expected_outcome_matched = is_objection
        expected_type = case.get("expected_refusal_type")
        if expected_type is not None and is_objection:
            m = re.search(r"Type:\s*(?:condition\s*)?#?(\d+)", output, re.IGNORECASE)
            a.refusal_type_correct = bool(m and int(m.group(1)) == expected_type)
        a.frame_log_present = None
        a.schema_order_correct = None
        a.kills_count_ok = None
        a.predictions_count_ok = None
        a.polarity_flag_present_as_expected = None
        return a

    # expected outcome is rewrite or mixed
    a.expected_outcome_matched = not is_objection

    # frame log
    a.frame_log_present = "## FRAME LOG ENTRY" in output

    # schema order
    positions = [output.find(s) for s in REQUIRED_SECTIONS]
    a.schema_order_correct = all(p > -1 for p in positions) and \
        positions == sorted(positions)

    # kills count
    kills_block = _extract_block(output, "## KILLED CLAIMS", "##")
    kill_lines = [ln for ln in kills_block.splitlines() if ln.strip().startswith("-")]
    a.kills_count_ok = len(kill_lines) >= case.get("expected_kills_min", 0)

    # predictions count
    pred_block = _extract_block(output, "## PREDICTIONS", "##")
    pred_lines = [ln for ln in pred_block.splitlines()
                  if re.match(r"^\s*-?\s*P\d+:", ln)]
    speculative = "SPECULATIVE" in output.upper()
    min_preds = case.get("expected_predictions_min", 0)
    a.predictions_count_ok = len(pred_lines) >= min_preds or (min_preds == 0 and speculative)

    # polarity flag
    pol_block = _extract_block(output, "## POLARITY NOTES", "##")
    has_polarity_content = bool(re.search(r"reversal|too much|polarity|phase",
                                          pol_block, re.IGNORECASE))
    if case.get("expected_polarity_flag"):
        a.polarity_flag_present_as_expected = has_polarity_content
    else:
        a.polarity_flag_present_as_expected = True  # not required

    return a


def _extract_block(text: str, start_header: str, stop_prefix: str) -> str:
    idx = text.find(start_header)
    if idx < 0:
        return ""
    rest = text[idx + len(start_header):]
    # find next header at same level
    m = re.search(rf"\n{re.escape(stop_prefix)} ", rest)
    return rest[:m.start()] if m else rest


# ---------------------------------------------------------------------------
# orchestration
# ---------------------------------------------------------------------------
def aggregate_from_judge(judge: dict) -> str:
    if "_judge_parse_error" in judge:
        return "FAIL"
    grades = [v.get("grade") for v in judge.get("scores", {}).values()]
    if any(g == "FAIL" for g in grades):
        return "FAIL"
    if all(g == "PASS" for g in grades):
        return "PASS"
    return "WEAK"


def run_case(client, system_prompt, judge_prompt, case, use_cache: bool,
             skip_rewriter: bool) -> CaseResult:
    t0 = time.time()
    cache_file = CACHE_DIR / f"{case['id']}.txt"
    output = ""

    try:
        if skip_rewriter or (use_cache and cache_file.exists()):
            output = cache_file.read_text(encoding="utf-8")
        else:
            output = call_rewriter(client, system_prompt, case)
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(output, encoding="utf-8")

        structural = check_structure(case, output)
        judge = call_judge(client, judge_prompt, case, output)
        agg = judge.get("aggregate") or aggregate_from_judge(judge)
        return CaseResult(
            case_id=case["id"],
            artifact_type=case["artifact_type"],
            domain=case.get("domain", ""),
            rewriter_output=output,
            structural=structural,
            judge=judge,
            aggregate=agg,
            elapsed_s=round(time.time() - t0, 2),
        )
    except Exception as e:
        return CaseResult(
            case_id=case["id"],
            artifact_type=case["artifact_type"],
            domain=case.get("domain", ""),
            rewriter_output=output,
            structural=StructuralAssertions(),
            aggregate="ERROR",
            elapsed_s=round(time.time() - t0, 2),
            error=f"{type(e).__name__}: {e}",
        )


def write_summary(results: list[CaseResult], out_path: Path) -> None:
    from collections import Counter
    by_agg = Counter(r.aggregate for r in results)
    by_type = {}
    for r in results:
        by_type.setdefault(r.artifact_type, Counter())[r.aggregate] += 1

    lines = [
        f"# Wu-Wei Rewriter — Eval Summary",
        f"_Run: {datetime.now(timezone.utc).isoformat()}_",
        f"_Rewriter model: {REWRITER_MODEL}_",
        f"_Judge model: {JUDGE_MODEL}_",
        "",
        f"## Aggregate (N={len(results)})",
        "",
        "| Grade | Count | % |",
        "|---|---:|---:|",
    ]
    total = max(len(results), 1)
    for g in ("PASS", "WEAK", "FAIL", "ERROR"):
        c = by_agg.get(g, 0)
        lines.append(f"| {g} | {c} | {c/total*100:.0f}% |")

    lines += ["", "## By artifact type", "", "| Type | PASS | WEAK | FAIL | ERROR |", "|---|---:|---:|---:|---:|"]
    for t, ctr in sorted(by_type.items()):
        lines.append(f"| {t} | {ctr.get('PASS',0)} | {ctr.get('WEAK',0)} | {ctr.get('FAIL',0)} | {ctr.get('ERROR',0)} |")

    lines += ["", "## Failures and weak runs", ""]
    for r in results:
        if r.aggregate not in ("FAIL", "WEAK", "ERROR"):
            continue
        head = r.judge.get("headline", "(no headline)") if isinstance(r.judge, dict) else "(judge error)"
        lines.append(f"- **{r.case_id}** ({r.artifact_type}/{r.domain}) — {r.aggregate} — {head}")
        if r.error:
            lines.append(f"    - error: `{r.error}`")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", help="filter by artifact_type")
    ap.add_argument("--domain", help="filter by domain")
    ap.add_argument("--limit", type=int, help="cap number of cases")
    ap.add_argument("--case", help="run a single case by id")
    ap.add_argument("--use-cache", action="store_true",
                    help="reuse cached rewriter outputs if present")
    ap.add_argument("--skip-rewriter", action="store_true",
                    help="never call the rewriter; require cache")
    ap.add_argument("--dry-run", action="store_true",
                    help="print plan, do not call any API")
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY") and not args.dry_run:
        print("ERROR: set ANTHROPIC_API_KEY", file=sys.stderr)
        return 2

    system_prompt = SYS_PROMPT_PATH.read_text(encoding="utf-8")
    judge_prompt = JUDGE_PROMPT_PATH.read_text(encoding="utf-8")

    cases = []
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cases.append(json.loads(line))

    if args.case:
        cases = [c for c in cases if c["id"] == args.case]
    if args.type:
        cases = [c for c in cases if c["artifact_type"] == args.type]
    if args.domain:
        cases = [c for c in cases if c.get("domain") == args.domain]
    if args.limit:
        cases = cases[: args.limit]

    print(f"plan: {len(cases)} cases | rewriter={REWRITER_MODEL} | judge={JUDGE_MODEL}",
          file=sys.stderr)
    if args.dry_run:
        for c in cases:
            print(f"  {c['id']}  {c['artifact_type']}/{c.get('domain','-')}",
                  file=sys.stderr)
        return 0

    client = anthropic.Anthropic()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = RESULTS_DIR / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    results_path = out_dir / "results.jsonl"
    summary_path = out_dir / "summary.md"

    results = []
    with open(results_path, "w", encoding="utf-8") as f:
        for i, case in enumerate(cases, 1):
            print(f"[{i}/{len(cases)}] {case['id']}", file=sys.stderr)
            r = run_case(client, system_prompt, judge_prompt, case,
                         use_cache=args.use_cache, skip_rewriter=args.skip_rewriter)
            results.append(r)
            f.write(json.dumps({
                **asdict(r),
                "structural": asdict(r.structural),
            }, ensure_ascii=False) + "\n")
            f.flush()

    write_summary(results, summary_path)
    print(f"\n=> {results_path}", file=sys.stderr)
    print(f"=> {summary_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
