#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 ~/.ai-agent-hub/skill-quality/validate_skill.py --skill skill
bash skill/scripts/run_evals.sh --dry-run --limit 5
python3 -m json.tool < <(head -n 1 skill/evals/golden_set.jsonl) >/dev/null
bash scripts/package.sh >/dev/null
unzip -t dist/wu-wei-rewriter.skill >/dev/null
