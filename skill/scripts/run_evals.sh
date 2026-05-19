#!/usr/bin/env bash
# Run Wu-Wei Rewriter evals. Dependencies stay inside skill/.venv.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/run_evals.sh [--dry-run] [--limit N] [--type artifact_type] [--case id]
  bash scripts/run_evals.sh --rejudge [--limit N] [--type artifact_type] [--case id]

Environment:
  ANTHROPIC_API_KEY   required unless --dry-run
  REWRITER_MODEL      default: claude-opus-4-7
  JUDGE_MODEL         default: claude-sonnet-4-6
USAGE
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

if [[ " ${*:-} " == *" --dry-run "* ]]; then
  exec python3 evals/grader.py "$@"
fi

if [[ -z "${ANTHROPIC_API_KEY:-}" && " ${*:-} " != *" --dry-run "* ]]; then
  echo "ERROR: set ANTHROPIC_API_KEY, or use --dry-run" >&2
  exit 2
fi

if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi
.venv/bin/python - <<'PY' >/dev/null 2>&1 || .venv/bin/python -m pip install -q anthropic
import anthropic  # noqa: F401
PY

if [[ "${1:-}" == "--rejudge" ]]; then
  shift
  exec .venv/bin/python evals/grader.py --skip-rewriter --use-cache "$@"
fi

exec .venv/bin/python evals/grader.py "$@"
