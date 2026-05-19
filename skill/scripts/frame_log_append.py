#!/usr/bin/env python3
"""Append a Wu-Wei Frame Log entry to a local JSONL file.

Usage:
  echo '{"name":"frame-id", ...}' | python scripts/frame_log_append.py
  python scripts/frame_log_append.py --file /path/to/entry.json

Default output: ~/.ai-agent-hub/frame-log/wu-wei.jsonl
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sys

DEFAULT_PATH = Path.home() / ".ai-agent-hub" / "frame-log" / "wu-wei.jsonl"
REQUIRED = ["name", "date", "domain", "artifact_type", "kill_condition"]


def load_entry(args: argparse.Namespace) -> dict:
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("No JSON entry supplied on stdin or --file")
    entry = json.loads(text)
    if not isinstance(entry, dict):
        raise SystemExit("Frame Log entry must be a JSON object")
    return entry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="JSON file containing one Frame Log entry")
    parser.add_argument("--out", default=os.environ.get("WU_WEI_FRAME_LOG", str(DEFAULT_PATH)))
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()

    entry = load_entry(args)
    missing = [k for k in REQUIRED if not entry.get(k)]
    if missing and not args.allow_incomplete:
        raise SystemExit(f"Missing required fields: {', '.join(missing)}")

    entry.setdefault("logged_at", dt.datetime.now(dt.timezone.utc).isoformat())
    entry.setdefault("source", "wu-wei-rewriter")

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
