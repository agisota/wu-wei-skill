#!/usr/bin/env python3
"""
Wu-Wei Rewriter — autograder.

Pipeline:
  1. Load evals/golden_set.jsonl and evals/golden_set_ru.jsonl when present
  2. For each case: invoke the rewriter (Anthropic API, system_prompt_v1.3.md)
  3. Invoke the LLM judge (separate model) with grader_prompt_v2.md
  4. Compute structural assertions deterministically
  5. Merge judge JSON + structural assertions
  6. Write results jsonl + summary md to evals/results/<timestamp>/

Dry runs do not require anthropic or ANTHROPIC_API_KEY.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import anthropic  # type: ignore
except ImportError:  # dry-run and structural-only workflows should still work
    anthropic = None  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
SYS_PROMPT_PATH = Path(os.environ.get(
    "WU_WEI_SYSTEM_PROMPT",
    str(ROOT / "system_prompt_v1.3.md" if (ROOT / "system_prompt_v1.3.md").exists() else ROOT / "system_prompt_v1.2.md"),
))
JUDGE_PROMPT_PATH = Path(os.environ.get(
    "WU_WEI_GRADER_PROMPT",
    str(ROOT / "evals" / "grader_prompt_v2.md" if (ROOT / "evals" / "grader_prompt_v2.md").exists() else ROOT / "evals" / "grader_prompt.md"),
))
BASE_GOLDEN_PATH = ROOT / "evals" / "golden_set.jsonl"
RU_GOLDEN_PATH = ROOT / "evals" / "golden_set_ru.jsonl"
RESULTS_DIR = ROOT / "evals" / "results"
CACHE_DIR = ROOT / "evals" / ".cache"

REWRITER_MODEL = os.environ.get("REWRITER_MODEL", "claude-opus-4-7")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-sonnet-4-6")

SECTION_ALIASES = {
    "rewrite": ["## REWRITE", "## Переписанная версия", "## 改写", "## 改写后", "## 重写"],
    "boundary": ["## BOUNDARY", "## Граница", "## Область применимости", "## 边界"],
    "prediction": ["## ONE TESTABLE PREDICTION", "## PREDICTIONS", "## Проверка", "## Проверяемые прогнозы", "## 可验证预测"],
    "polarity": ["## POLARITY NOTES", "## Риски обратного эффекта", "## Риски разворота", "## Полярность"],
    "killed": ["## KILLED CLAIMS", "## KILLED / WEAK CLAIMS", "## Убрано или ослаблено", "## Снятые утверждения", "## Что я бы убрал", "## 被删除的主张"],
    "elegance": ["## ELEGANCE AUDIT", "## Аудит красивых фраз", "## Аудит языка"],
    "frame_log": ["## FRAME LOG ENTRY", "## Запись для журнала рамки", "## Frame Log"],
    "next_check": ["## NEXT CHECK", "## Следующая проверка", "## 下一次检查"],
    "diagnosis": ["## DIAGNOSIS", "## Диагноз", "## 诊断"],
    "repair": ["## REPAIR PATH", "## Что надо уточнить", "## Минимальная ремонтная версия", "repair path", "ремонт", "минимальная рабочая версия"],
    "kill_condition": ["## KILL CONDITION", "## Условие снятия", "kill_condition:"],
}

PREDICTION_LABELS = {
    "metric": ["metric", "метрика", "指标"],
    "source": ["source", "источник", "来源"],
    "threshold": ["threshold", "порог", "阈值"],
    "check_date": ["check_date", "check date", "дата проверки", "срок проверки", "到 ", "日期"],
    "confirmed_if": ["confirmed_if", "confirmed if", "подтвердится", "confirmed"],
    "weakened_if": ["weakened_if", "weakened if", "ослабнет", "weakened"],
    "falsified_if": ["falsified_if", "falsified if", "опровергнется", "falsified"],
}

OBJECTION_RE = re.compile(
    r"STRUCTURAL OBJECTION|СТРУКТУРНОЕ ВОЗРАЖЕНИЕ|##\s*OBJECTION|##\s*Возражение|结构性反对",
    re.IGNORECASE,
)


@dataclass
class StructuralAssertions:
    expected_outcome_matched: Optional[bool] = None
    refusal_type_correct: Optional[bool] = None
    repair_path_present_if_objection: Optional[bool] = None
    kills_count_ok: Optional[bool] = None
    predictions_count_ok: Optional[bool] = None
    prediction_contract_complete: Optional[bool] = None
    polarity_flag_present_as_expected: Optional[bool] = None
    frame_log_present_when_required: Optional[bool] = None
    schema_mode_correct: Optional[bool] = None
    language_integrity_required_met: Optional[bool] = None
    must_not_contain_clean: Optional[bool] = None
    must_contain_present: Optional[bool] = None


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


def selected_output_mode(case: dict) -> str:
    modes = case.get("modes", {}) or {}
    return (case.get("expected_output_mode") or modes.get("output_mode") or "decision")


def selected_strict_schema(case: dict) -> bool:
    if "strict_schema" in case:
        return bool(case["strict_schema"])
    # Old base golden-set rows predate localized schemas; keep them strict for continuity.
    return case.get("expected_output_mode") is None


def call_rewriter(client, system_prompt: str, case: dict) -> str:
    modes = case.get("modes", {}) or {}
    user_payload = {
        "artifact_text": case["input"],
        "artifact_type": case["artifact_type"],
        "domain": case.get("domain"),
        "intended_use": case.get("intended_use"),
        "author_confidence": case.get("author_confidence"),
        "pitch_mode": modes.get("pitch_mode", "strict"),
        "creative_mode": modes.get("creative_mode", "ship"),
        "output_mode": selected_output_mode(case),
        "strict_schema": selected_strict_schema(case),
        "output_language": case.get("output_language", "artifact"),
        "prior_versions": case.get("prior_versions", []),
    }
    user_msg = (
        "Process the following artifact through the Wu-Wei Rewriter v1.3 pipeline.\n\n"
        f"```json\n{json.dumps(user_payload, ensure_ascii=False, indent=2)}\n```\n\n"
        "Emit the selected output mode only. No preamble."
    )
    resp = client.messages.create(
        model=REWRITER_MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def call_judge(client, judge_prompt: str, case: dict, rewriter_output: str) -> dict:
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


def _low(text: str) -> str:
    return text.casefold()


def has_section(output: str, category: str) -> bool:
    low = _low(output)
    return any(_low(alias) in low for alias in SECTION_ALIASES[category])


def section_position(output: str, category: str) -> int:
    low = _low(output)
    positions = [low.find(_low(alias)) for alias in SECTION_ALIASES[category]]
    positions = [p for p in positions if p >= 0]
    return min(positions) if positions else -1


def extract_block(output: str, category: str) -> str:
    pos = section_position(output, category)
    if pos < 0:
        return ""
    rest = output[pos:]
    m = re.search(r"\n##\s+", rest[1:])
    return rest[: m.start() + 1] if m else rest


def has_prediction_label(output: str, label: str) -> bool:
    low = _low(output)
    return any(_low(token) in low for token in PREDICTION_LABELS[label])


def prediction_contract_complete(output: str, required: list[str] | None = None) -> bool:
    required = required or ["metric", "source", "threshold", "check_date"]
    return all(has_prediction_label(output, r) for r in required)


def count_predictions(output: str) -> int:
    count = len(re.findall(r"(?m)^\s*-?\s*P\d+\s*:", output))
    if count == 0 and re.search(r"Prediction\s*:|Прогноз\s*:|可验证预测", output, re.IGNORECASE):
        count = 1
    return count


def contains_near_kill_context(output: str, term: str) -> bool:
    low = _low(output)
    t = _low(term)
    idx = low.find(t)
    if idx < 0:
        return True
    while idx >= 0:
        window = low[max(0, idx - 180): idx + len(t) + 180]
        if re.search(r"убра|снят|kill|killed|removed|запрещ|не использ|метафор|slop|weak|слаб", window):
            return True
        idx = low.find(t, idx + len(t))
    return False


def has_repair_path(output: str) -> bool:
    low = _low(output)
    return (
        has_section(output, "repair")
        or "repair path" in low
        or "что нужно добавить" in low
        or "что надо уточнить" in low
        or "операционное определение" in low
        or "минимальная рабочая версия" in low
        or "weaker version" in low
    )


def schema_mode_correct(case: dict, output: str) -> bool:
    mode = selected_output_mode(case)
    if mode == "full":
        mode = "decision"
    if mode == "quick":
        mode = "compact"
    if mode == "frame_log_only":
        mode = "frame_log"

    if mode == "compact":
        return all(has_section(output, k) for k in ["rewrite", "boundary", "prediction", "killed", "next_check"])
    if mode == "decision":
        return all(has_section(output, k) for k in ["rewrite", "boundary", "prediction", "polarity", "killed", "elegance", "frame_log"])
    if mode == "frame_log":
        return has_section(output, "frame_log") and has_section(output, "kill_condition")
    if mode == "critique_only":
        return has_section(output, "diagnosis") and has_repair_path(output)
    return True


def extract_refusal_type(output: str) -> Optional[int]:
    patterns = [
        r"(?:Type|Condition|condition|#)\s*:?\s*#?\s*(\d+)",
        r"(?:Тип|Условие|условие)\s*:?\s*#?\s*(\d+)",
        r"#\s*(\d+)\s*[—-]",
    ]
    for pat in patterns:
        m = re.search(pat, output, re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except ValueError:
                pass
    return None


def check_structure(case: dict, output: str) -> StructuralAssertions:
    a = StructuralAssertions()
    expected = case["expected_outcome"]
    is_objection = bool(OBJECTION_RE.search(output))

    if expected == "objection":
        a.expected_outcome_matched = is_objection
        expected_type = case.get("expected_refusal_type")
        if expected_type is not None and is_objection:
            a.refusal_type_correct = extract_refusal_type(output) == expected_type
        else:
            a.refusal_type_correct = None
        a.repair_path_present_if_objection = has_repair_path(output) if is_objection else False
        a.kills_count_ok = None
        a.predictions_count_ok = None
        a.prediction_contract_complete = None
        a.polarity_flag_present_as_expected = None
        a.frame_log_present_when_required = None
        a.schema_mode_correct = None
    else:
        a.expected_outcome_matched = not is_objection
        a.refusal_type_correct = None
        a.repair_path_present_if_objection = None

        killed_block = extract_block(output, "killed")
        kill_lines = [ln for ln in killed_block.splitlines() if re.match(r"^\s*[-*]|^\s*(Removed|Убрано|Снято)", ln, re.IGNORECASE)]
        a.kills_count_ok = len(kill_lines) >= case.get("expected_kills_min", 0)

        min_preds = case.get("expected_predictions_min", 0)
        pred_count = count_predictions(output)
        speculative = "SPECULATIVE" in output.upper() or "СПЕКУЛЯТИВ" in output.upper()
        a.predictions_count_ok = pred_count >= min_preds or (min_preds == 0 and speculative)
        if min_preds > 0:
            a.prediction_contract_complete = prediction_contract_complete(output, case.get("prediction_requirements"))
        else:
            a.prediction_contract_complete = None

        if case.get("expected_polarity_flag"):
            pol_block = extract_block(output, "polarity")
            a.polarity_flag_present_as_expected = bool(
                pol_block.strip()
                or re.search(r"reversal|polarity|обратн|разворот|слишком|риск", output, re.IGNORECASE)
            )
        else:
            a.polarity_flag_present_as_expected = True

        mode = selected_output_mode(case)
        a.frame_log_present_when_required = has_section(output, "frame_log") if mode in {"decision", "frame_log", "full", "frame_log_only"} else True
        a.schema_mode_correct = schema_mode_correct(case, output)

    must_not = case.get("must_not_contain") or []
    a.must_not_contain_clean = all(contains_near_kill_context(output, term) for term in must_not)
    must = case.get("must_contain") or []
    out_low = _low(output)
    a.must_contain_present = all(_low(term) in out_low for term in must)
    if case.get("language_integrity_required"):
        a.language_integrity_required_met = bool(a.must_not_contain_clean)
    else:
        a.language_integrity_required_met = None

    return a


def aggregate_from_judge(judge: dict) -> str:
    if "_judge_parse_error" in judge:
        return "FAIL"
    grades = [v.get("grade") for v in judge.get("scores", {}).values()]
    if any(g == "FAIL" for g in grades):
        return "FAIL"
    if grades and all(g == "PASS" for g in grades):
        return "PASS"
    return "WEAK"


def run_case(client, system_prompt: str, judge_prompt: str, case: dict, use_cache: bool, skip_rewriter: bool) -> CaseResult:
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


def load_cases(selection: str) -> tuple[list[dict], list[Path]]:
    paths: list[Path]
    if selection == "base":
        paths = [BASE_GOLDEN_PATH]
    elif selection == "ru":
        paths = [RU_GOLDEN_PATH]
    else:
        paths = [BASE_GOLDEN_PATH, RU_GOLDEN_PATH]

    cases: list[dict] = []
    used: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        used.append(path)
        with path.open(encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                if row["id"] in seen:
                    raise ValueError(f"duplicate case id {row['id']} in {path}:{line_no}")
                seen.add(row["id"])
                cases.append(row)
    return cases, used


def write_summary(results: list[CaseResult], out_path: Path, used_files: list[Path]) -> None:
    from collections import Counter

    by_agg = Counter(r.aggregate for r in results)
    by_type = {}
    for r in results:
        by_type.setdefault(r.artifact_type, Counter())[r.aggregate] += 1

    lines = [
        "# Wu-Wei Rewriter — Eval Summary",
        f"_Run: {datetime.now(timezone.utc).isoformat()}_",
        f"_System prompt: {SYS_PROMPT_PATH.name}_",
        f"_Judge prompt: {JUDGE_PROMPT_PATH.name}_",
        f"_Golden files: {', '.join(p.name for p in used_files)}_",
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
    ap.add_argument("--golden", choices=["all", "base", "ru"], default="all", help="which golden-set file(s) to load")
    ap.add_argument("--use-cache", action="store_true", help="reuse cached rewriter outputs if present")
    ap.add_argument("--skip-rewriter", action="store_true", help="never call the rewriter; require cache")
    ap.add_argument("--dry-run", action="store_true", help="print plan, do not call any API")
    args = ap.parse_args()

    if not SYS_PROMPT_PATH.exists():
        print(f"ERROR: missing system prompt: {SYS_PROMPT_PATH}", file=sys.stderr)
        return 2
    if not JUDGE_PROMPT_PATH.exists():
        print(f"ERROR: missing judge prompt: {JUDGE_PROMPT_PATH}", file=sys.stderr)
        return 2

    if not os.environ.get("ANTHROPIC_API_KEY") and not args.dry_run:
        print("ERROR: set ANTHROPIC_API_KEY", file=sys.stderr)
        return 2
    if anthropic is None and not args.dry_run:
        print("ERROR: pip install anthropic (or use --dry-run)", file=sys.stderr)
        return 2

    system_prompt = SYS_PROMPT_PATH.read_text(encoding="utf-8")
    judge_prompt = JUDGE_PROMPT_PATH.read_text(encoding="utf-8")

    try:
        cases, used_files = load_cases(args.golden)
    except Exception as e:
        print(f"ERROR: failed loading golden set: {e}", file=sys.stderr)
        return 2

    if args.case:
        cases = [c for c in cases if c["id"] == args.case]
    if args.type:
        cases = [c for c in cases if c["artifact_type"] == args.type]
    if args.domain:
        cases = [c for c in cases if c.get("domain") == args.domain]
    if args.limit:
        cases = cases[: args.limit]

    if not cases:
        print("ERROR: no cases matched filters", file=sys.stderr)
        return 4

    print(
        f"plan: {len(cases)} cases | rewriter={REWRITER_MODEL} | judge={JUDGE_MODEL} | "
        f"system={SYS_PROMPT_PATH.name} | grader={JUDGE_PROMPT_PATH.name} | "
        f"golden={','.join(p.name for p in used_files)}",
        file=sys.stderr,
    )
    if args.dry_run:
        for c in cases:
            print(
                f"  {c['id']}  {c['artifact_type']}/{c.get('domain','-')}  mode={selected_output_mode(c)} strict_schema={selected_strict_schema(c)}",
                file=sys.stderr,
            )
        return 0

    client = anthropic.Anthropic()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = RESULTS_DIR / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    results_path = out_dir / "results.jsonl"
    summary_path = out_dir / "summary.md"

    results = []
    with results_path.open("w", encoding="utf-8") as f:
        for i, case in enumerate(cases, 1):
            print(f"[{i}/{len(cases)}] {case['id']}", file=sys.stderr)
            r = run_case(client, system_prompt, judge_prompt, case, use_cache=args.use_cache, skip_rewriter=args.skip_rewriter)
            results.append(r)
            f.write(json.dumps({**asdict(r), "structural": asdict(r.structural)}, ensure_ascii=False) + "\n")
            f.flush()

    write_summary(results, summary_path, used_files)
    print(f"\n=> {results_path}", file=sys.stderr)
    print(f"=> {summary_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
