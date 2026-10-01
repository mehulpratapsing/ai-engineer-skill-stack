#!/usr/bin/env bash
set -eu

usage() {
  printf 'Usage: %s {opencode|codex|claude} {--project|--global}\n' "$0" >&2
  exit 2
}

[ "$#" -eq 2 ] || usage
target=$1
scope=$2
script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
source_root="$script_dir/../.agents/skills"

[ -d "$source_root" ] || { printf 'Skill source not found: %s\n' "$source_root" >&2; exit 1; }

case "$target" in
  opencode|codex|claude) ;;
  *) usage ;;
esac

case "$scope" in
  --project)
    if [ "$target" = "claude" ]; then
      destination="$PWD/.claude/skills"
    else
      destination="$PWD/.agents/skills"
    fi
    ;;
  --global)
    case "$target" in
      opencode) destination="$HOME/.agents/skills" ;;
      codex)
        codex_home=${CODEX_HOME:-$HOME/.codex}
        destination="$codex_home/skills"
        ;;
      claude) destination="$HOME/.claude/skills" ;;
    esac
    ;;
  *) usage ;;
esac

mkdir -p "$destination"
copied=0
skipped=0
for skill in "$source_root"/*; do
  [ -d "$skill" ] || continue
  name=$(basename "$skill")
  if [ -e "$destination/$name" ]; then
    printf 'Skipped existing skill: %s\n' "$destination/$name"
    skipped=$((skipped + 1))
  else
    cp -R "$skill" "$destination/$name"
    printf 'Installed: %s\n' "$destination/$name"
    copied=$((copied + 1))
  fi
done
printf 'Done. Installed %s skill(s); skipped %s existing skill(s).\n' "$copied" "$skipped"
