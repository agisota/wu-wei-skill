#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 ~/.ai-agent-hub/skill-quality/validate_skill.py --skill skill
bash skill/scripts/run_evals.sh --dry-run --limit 5
bash skill/scripts/run_evals.sh --dry-run --case gs_ru_v2_001
python3 - <<'PY'
import json
from pathlib import Path
for path in [Path('skill/evals/golden_set.jsonl'), Path('skill/evals/golden_set_ru.jsonl')]:
    rows = 0
    ids = set()
    for i, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if row['id'] in ids:
            raise SystemExit(f'duplicate id {row["id"]} in {path}:{i}')
        ids.add(row['id'])
        rows += 1
    print(f'{path}: {rows} valid rows')
PY
bash scripts/package.sh >/dev/null
unzip -t dist/wu-wei-rewriter.skill >/dev/null
