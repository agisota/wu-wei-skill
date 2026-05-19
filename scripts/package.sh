#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/dist"
PKG="$OUT/wu-wei-rewriter.skill"
rm -rf "$OUT"
mkdir -p "$OUT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/wu-wei-rewriter"
rsync -a \
  --exclude '.venv' \
  --exclude 'evals/results' \
  --exclude 'evals/.cache' \
  --exclude '__pycache__' \
  "$ROOT/skill/" "$TMP/wu-wei-rewriter/"
( cd "$TMP" && zip -qr "$PKG" wu-wei-rewriter )
echo "$PKG"
