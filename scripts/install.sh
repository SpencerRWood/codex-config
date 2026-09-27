#!/bin/sh
set -eu

repo_dir=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd -P)

link_if_absent() {
  source_path=$1
  target_path=$2
  if [ -L "$target_path" ] && [ "$(readlink "$target_path")" = "$source_path" ]; then
    return
  fi
  if [ -e "$target_path" ] || [ -L "$target_path" ]; then
    printf 'Existing path needs review: %s\n' "$target_path" >&2
    exit 1
  fi
  ln -s "$source_path" "$target_path"
}

link_managed_file() {
  source_path=$1
  target_path=$2
  if [ -L "$target_path" ] && [ "$(readlink "$target_path")" = "$source_path" ]; then
    return
  fi
  if [ -f "$target_path" ] && [ ! -L "$target_path" ] && cmp -s "$source_path" "$target_path"; then
    rm "$target_path"
  elif [ -e "$target_path" ] || [ -L "$target_path" ]; then
    printf 'Existing path needs review: %s\n' "$target_path" >&2
    exit 1
  fi
  ln -s "$source_path" "$target_path"
}

for codex_dir in "$HOME/.codex" "$HOME/.codex-secondary"; do
  mkdir -p "$codex_dir/skills"
  link_if_absent "$repo_dir/AGENTS.md" "$codex_dir/AGENTS.md"
  for skill_dir in "$repo_dir"/skills/*; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    skill_name=${skill_dir##*/}
    link_if_absent "$skill_dir" "$codex_dir/skills/$skill_name"
  done
done

mkdir -p "$HOME/.wood/scripts"
link_managed_file "$repo_dir/scripts/openproject/wood_openproject_env.py" "$HOME/.wood/scripts/wood_openproject_env.py"

wood_tools_dir="$HOME/Projects/internal/Wood Tools/wood-tools"
if [ -d "$wood_tools_dir/.git" ]; then
  link_if_absent "$repo_dir/overrides/wood-tools/AGENTS.override.md" "$wood_tools_dir/AGENTS.override.md"
  exclude_file="$wood_tools_dir/.git/info/exclude"
  if ! grep -Fxq 'AGENTS.override.md' "$exclude_file"; then
    printf '\nAGENTS.override.md\n' >> "$exclude_file"
  fi
fi
