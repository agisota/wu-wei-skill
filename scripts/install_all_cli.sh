#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="${WU_WEI_SKILL_SOURCE:-$ROOT/skill}"
NAME="wu-wei-rewriter"

if [[ ! -f "$SOURCE/SKILL.md" ]]; then
  echo "ERROR: SOURCE does not look like a skill: $SOURCE" >&2
  exit 2
fi

# Strict named CLI roots requested by the operator. These are created if absent.
CREATE_ROOTS=(
  "$HOME/.codex/skills"
  "$HOME/.claude/skills"
  "$HOME/.config/opencode/skills"
  "$HOME/.kimi/skills"
  "$HOME/.gemini/skills"
  "$HOME/.hermes/skills"
  "$HOME/.droid/skills"
  "$HOME/.pi/skills"
  "$HOME/.config/pi/skills"
  "$HOME/.agents/skills.shared-archive"
)

# Extra direct CLI skill roots discovered on this workstation. These are used only if already present.
OPTIONAL_ROOTS=(
  "$HOME/.agent/skills"
  "$HOME/.agents/skills"
  "$HOME/.adal/skills"
  "$HOME/.ai-agent-hub/skills"
  "$HOME/.ai-agent-hub/mirror/claude/skills"
  "$HOME/.ai-agent-hub/mirror/codex/skills"
  "$HOME/.ai-agent-hub/mirror/kimi/skills"
  "$HOME/.amp/skills"
  "$HOME/.antigravity/skills"
  "$HOME/.augment/skills"
  "$HOME/.bob/skills"
  "$HOME/.cline/skills"
  "$HOME/.codebuddy/skills"
  "$HOME/.codeium/windsurf/skills"
  "$HOME/.codmate/skills"
  "$HOME/.commandcode/skills"
  "$HOME/.config/agents/skills"
  "$HOME/.config/crush/skills"
  "$HOME/.config/goose/skills"
  "$HOME/.config/zed/skills"
  "$HOME/.continue/skills"
  "$HOME/.counter/skills"
  "$HOME/.craft/skills"
  "$HOME/.cursor/skills"
  "$HOME/.factory/skills"
  "$HOME/.gemini/antigravity/skills"
  "$HOME/.sandbox-home/.pi/skills"
)

ROOTS=()
for r in "${CREATE_ROOTS[@]}"; do
  mkdir -p "$r"
  ROOTS+=("$r")
done
for r in "${OPTIONAL_ROOTS[@]}"; do
  [[ -d "$r" ]] && ROOTS+=("$r")
done

if [[ -n "${EXTRA_SKILL_ROOTS:-}" ]]; then
  IFS=':' read -r -a extra <<< "$EXTRA_SKILL_ROOTS"
  for r in "${extra[@]}"; do
    [[ -n "$r" ]] || continue
    mkdir -p "$r"
    ROOTS+=("$r")
  done
fi

# Deduplicate while preserving order.
DEDUPED=()
seen=""
for r in "${ROOTS[@]}"; do
  key="|$r|"
  [[ "$seen" == *"$key"* ]] && continue
  seen+="$key"
  DEDUPED+=("$r")
done

installed=0
for root in "${DEDUPED[@]}"; do
  target="$root/$NAME"
  if [[ -L "$target" || -e "$target" ]]; then
    if [[ -L "$target" && "$(readlink "$target")" == "$SOURCE" ]]; then
      status="already"
    else
      backup="$target.backup.$(date -u +%Y%m%dT%H%M%SZ)"
      mv "$target" "$backup"
      ln -s "$SOURCE" "$target"
      status="replaced backup=$backup"
    fi
  else
    ln -s "$SOURCE" "$target"
    status="linked"
  fi
  if [[ ! -f "$target/SKILL.md" ]]; then
    echo "ERROR: install verification failed for $target" >&2
    exit 3
  fi
  printf '%s\t%s\t%s\n' "$status" "$root" "$target"
  installed=$((installed+1))
done

echo "installed_roots=$installed"
