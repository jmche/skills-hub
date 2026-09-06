#!/usr/bin/env bash
# link_skills.sh — 把 canonical (~/.agents/skills) 的技能以"技能级软链"方式分发到各宿主
# 策略（保守、幂等、纯增量）：
#   1. 对每个候选宿主 H（目录 skills 存在）：
#      - canonical 技能 S：若 H 下没有 S  → 建软链 H/S -> canonical/S
#      - H 下已有 S             → 跳过（尊重宿主本地版本，通常同源）
#      - H 下 S 是断链/坏链    → 重建
#   2. 整目录级软链（H/skills -> canonical）仅在 H/skills 不存在或为空时启用
#   3. roles 分发：H/agents -> canonical/roles（仅当 H/agents 不存在或为空）
# 用法:
#   link_skills.sh --dry-run
#   link_skills.sh [--host claude|codex|hermes|opencode|cursor|gemini|copilot|all]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY=0; HOST=all
while [[ $# -gt 0 ]]; do case "$1" in
  --dry-run) DRY=1; shift;; --host) HOST="$2"; shift 2;; *) echo "unknown arg $1"; exit 2;; esac; done

run(){ if [[ $DRY -eq 1 ]]; then echo "DRY $*"; else eval "$@"; fi; }

make_link(){ # target linkname
  local target="$1" link="$2"
  if [[ -L "$link" ]]; then
    local cur; cur="$(readlink "$link" || true)"
    if [[ "$cur" == "$target" ]]; then return 0; fi
    run 'rm "$0"' "$link"
  elif [[ -e "$link" ]]; then
    echo "SKIP  $link already exists (non-symlink), keeping host-local version"
    return 0
  fi
  run 'ln -s "$0" "$1"' "$target" "$link"
  echo "LINK  $link -> $target"
}

host_map(){ # host -> skills_dir
 case "$1" in
  claude)   echo "$HOME/.claude/skills" ;;
  codex)    echo "$HOME/.codex/skills" ;;
  hermes)   echo "$HOME/.hermes/skills" ;;
  opencode) echo "$HOME/.config/opencode/skills" ;;
  cursor)   echo "$HOME/.cursor/skills" ;;
  gemini)   echo "$HOME/.gemini/skills" ;;
  copilot)  echo "$HOME/.copilot/skills" ;;
 esac
}
host_roles(){ # host -> agents/roles dir
 case "$1" in
  claude)   echo "$HOME/.claude/agents" ;;
  codex)    return 1 ;;   # codex roles are rendered toml, handled separately
  hermes)   return 1 ;;   # hermes uses plugins/delegate, handled separately
  cursor)   echo "$HOME/.cursor/agents" ;;
  gemini)   echo "$HOME/.gemini/agents" ;;
  *)        return 1 ;;
 esac
}

if [[ "$HOST" == "all" ]]; then HOSTS="claude codex hermes opencode cursor gemini copilot"; else HOSTS="$HOST"; fi

for H in $HOSTS; do
  S="$(host_map "$H")"
  if [[ ! -d "$S" && ! -L "$S" ]]; then
    echo "[$H] skills dir absent, creating symlink to canonical"
    run 'mkdir -p "'"$(dirname "$S")"'"'
    make_link "$ROOT" "$S"
    continue
  fi
  [[ -d "$S" ]] || { echo "[$H] skills path not a directory, skipping"; continue; }
  n=0; m=0
  for SK in "$ROOT"/*/; do
    name="$(basename "$SK")"
    [[ -f "$ROOT/$name/SKILL.md" ]] || continue
    if [[ -e "$S/$name" || -L "$S/$name" ]]; then m=$((m+1)); else
      make_link "$ROOT/$name" "$S/$name"; run 'true'; echo "  + $name" >/dev/null; n=$((n+1))
    fi
  done
  # roles (md-native hosts only)
  R="$(host_roles "$H" 2>/dev/null || true)"
  if [[ -n "${R:-}" && -d "$ROOT/roles" ]]; then
    if [[ ! -d "$R" && ! -L "$R" ]]; then
      make_link "$ROOT/roles" "$R"
    elif [[ -L "$R" ]]; then :; else
      echo "  roles: $R exists as real dir, NOT touching (populate per-role if needed)"
    fi
  fi
  echo "[$H] $n new skill links, $m kept host-local"
done
echo OK
