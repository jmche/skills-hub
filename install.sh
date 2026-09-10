#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# skills-hub installer
#
#   curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash
#   bash install.sh --select     # pick skills interactively
#
# What it does (idempotent, safe to re-run):
#   1. Ensure a canonical library at ~/.agents/skills (this repo; clone if missing,
#      otherwise git pull unless --no-pull).
#   2. Apply the publish whitelist (publish.json). Entries that are NOT
#      whitelisted (e.g. private project skills) are moved to
#      ~/.agents/skills-hidden (never deleted). Restore with: install.sh enable <name>
#      Selection (--select): unselected entries go to skills-hidden as well.
#   3. Detect installed coding agents and ask which hosts to link (or link all
#      in non-interactive mode). Symlinks are purely additive and idempotent.
#   4. Offer API-key setup (~/.shell_env; see env.example for the key list).
#
# Flags:
#   --yes            non-interactive: install everything public, link all
#                    detected hosts (this is the curl|bash default)
#   --select         interactive skill selection (all / by-hub / individual)
#   --skip-hosts     do not create host symlinks
#   --skip-env       do not offer API-key setup
#   --no-pull        do not git-pull an existing local clone
#   --repo URL       clone from a different repository
#   -h, --help       print this help
#
# Subcommands:
#   install.sh enable <name>   restore a hidden skill into ~/.agents/skills
#   install.sh hidden          list hidden (unpublished) skills
#   install.sh update          git pull the local clone
#   install.sh status          show install state
# Usage: one-command installer for the skills-hub library.
# ============================================================================

VERSION=0.1.0
REPO="https://github.com/jmche/skills-hub.git"
YES=0; SELECT=0; SKIP_HOSTS=0; SKIP_ENV=0; NOPULL=0
SUB=""

usage() { awk 'NR==1{next} /^# =/{next} /^$/{next} sub{exit} {sub(/^# ?/,""); print} {sub=1}' "$0"; }

# ---- arg parsing -----------------------------------------------------------
while [ $# -gt 0 ]; do
  case "$1" in
    --yes) YES=1; shift ;;
    --select) SELECT=1; shift ;;
    --skip-hosts) SKIP_HOSTS=1; shift ;;
    --skip-env) SKIP_ENV=1; shift ;;
    --no-pull) NOPULL=1; shift ;;
    --repo) shift; REPO="${1:-$REPO}"; shift ;;
    -h|--help) usage; exit 0 ;;
    enable|hidden|update|status) SUB="$1"; shift ;;
    *) echo "unknown argument: $1 (try --help)" >&2; exit 2 ;;
  esac
done
# positional after subcommand (e.g. enable <name>)
SUBARG="${1:-}"

H="$HOME/.agents"
CANON="$H/skills"
HIDDEN="$H/skills-hidden"

# ---- subcommands -----------------------------------------------------------
case "$SUB" in
  enable)
    [ -n "$SUBARG" ] || { echo "usage: install.sh enable <skill-name>"; exit 2; }
    [ -d "$HIDDEN/$SUBARG" ] || { echo "no hidden skill named '$SUBARG'"; ls "$HIDDEN" 2>/dev/null; exit 1; }
    mv "$HIDDEN/$SUBARG" "$CANON/$SUBARG"
    echo "enabled: $SUBARG (now in $CANON/$SUBARG)"; [ -f "$CANON/_scripts/link_hosts.py" ] && python3 "$CANON/_scripts/link_hosts.py" || true
    exit 0 ;;
  hidden)
    [ -d "$HIDDEN" ] || { echo "(nothing hidden)"; exit 0; }
    echo "hidden skills (restore with: bash install.sh enable <name>):"
    ls -1 "$HIDDEN"
    exit 0 ;;
  update)
    [ -d "$CANON/.git" ] || { echo "no git repo at $CANON"; exit 1; }
    git -C "$CANON" pull
    git -C "$CANON" submodule update --init --recursive
    exit 0 ;;
  sync-upstream)
    [ -n "$SUBARG" ] || { echo "usage: install.sh sync-upstream <name>   (see upstreams.json)"; exit 2; }
    exec python3 "$CANON/_scripts/sync_upstream.py" "$SUBARG" ;;

  status)
    if [ -d "$CANON" ]; then echo "canonical:  $CANON (present)"; else echo "canonical:  $CANON (missing)"; fi
    if [ -d "$HIDDEN" ]; then n=$(ls "$HIDDEN" | wc -l | tr -d ' '); echo "hidden:     $HIDDEN ($n skills)"; else echo "hidden:     $HIDDEN (none)"; fi
    [ -f "$CANON/install.sh" ] && echo "skills:     $(ls "$CANON" | grep -c .) top-level entries"
    for h in claude codex opencode cursor gemini copilot hermes; do
      p="$HOME/.$h/skills"; [ "$h" = opencode ] && p="$HOME/.config/opencode/skills"
      [ -d "$(dirname "$p")" ] && echo "host $h:   linked=$(find "$(dirname "$p")" -maxdepth 1 -type l 2>/dev/null | grep -c "skills/$h\|/skills" 2>/dev/null || echo '?')"
    done
    exit 0 ;;
esac

echo "=== skills-hub v$VERSION"

# ---- 1/4 canonical library -------------------------------------------------
if [ ! -f "$CANON/install.sh" ]; then
  [ -e "$CANON" ] && { echo "ERROR: $CANON exists but is not skills-hub. Move it away first."; exit 1; }
  echo "[1/4] no local clone found — cloning $REPO"
  mkdir -p "$H"
  git clone --depth 1 --recurse-submodules "$REPO" "$CANON"
else
  echo "[1/4] local clone at $CANON"
  if [ -d "$CANON/.git" ] && [ "$NOPULL" -eq 0 ]; then
    git -C "$CANON" pull --quiet && echo "      updated" || echo "      pull skipped/failed; using local state"
  fi
  # ensure submodules (grounded-build) are checked out
  [ -d "$CANON/.git" ] && git -C "$CANON" submodule update --init --recursive --quiet 2>/dev/null || true
fi
cd "$CANON"

# ---- 2/4 whitelist + selection ----------------------------------------------
echo "[2/4] applying publish whitelist (publish.json)"
python3 - <<'PYEOF' || true
import json, os, shutil, subprocess, sys
canon = os.path.abspath(os.environ['H']) + '/skills' if False else os.getcwd()
hidden = os.path.expanduser('~/.agents/skills-hidden')
wl = json.load(open('publish.json'))
whitelist = set(wl.get('top', [])) | set(wl.get('hubs', []))
os.makedirs(hidden, exist_ok=True)
kept, moved = [], []
for e in sorted(os.listdir(canon)):
    p = os.path.join(canon, e)
    if not os.path.isdir(p) or e.startswith(('.', '_')):
        continue
    if not os.path.isfile(os.path.join(p, 'SKILL.md')):
        continue
    if e in whitelist:
        kept.append(e)
    else:
        dst = os.path.join(hidden, e)
        if os.path.exists(dst): shutil.rmtree(dst)
        shutil.move(p, dst); moved.append(e)
print(f'      kept:   {len(kept)}')
print(f'      hidden: {len(moved)} -> {hidden}')
if moved:
    print(f'      (restore any with: bash install.sh enable <name>)')
# selection mode: move unselected top-level skills to hidden
if '--select' in os.environ.get('INSTALL_SH_SELECT', ''):
    pass  # selection handled by caller before this step if desired
PYEOF

# ---- 2b interactive selection (only with --select and TTY) -----------------
if [ "$SELECT" -eq 1 ] && [ -t 0 ]; then
  echo "      interactive selection: choose by number (comma-separated, blank = all)"
  i=0
  LIST=""
  for e in $(ls -1 | grep -E . | grep -vE '^(\.|_)' | while read -r d; do [ -f "$d/SKILL.md" ] && echo "$d"; done | sort); do
    i=$((i+1)); LIST="$LIST
  $i) $e"
  done
  echo "$LIST"
  printf "      pick: "
  read -r PICK || PICK=""
  if [ -n "$PICK" ]; then
    SELECTED=""
    IFS=',' read -ra NUMS <<< "$PICK"
    for n in "${NUMS[@]}"; do
      n=$(echo "$n" | tr -d ' ')
      name=$(echo "$LIST" | awk -v n="$n" '$1==n")"{print $2; exit}')
      [ -n "$name" ] && SELECTED="$SELECTED ${name}"
    done
    # move everything NOT selected to hidden (whitelisted only)
    for e in $(ls -1); do
      [ -f "$CANON/$e/SKILL.md" ] || continue
      case " $SELECTED " in *" $e "*) : ;; *) mv "$CANON/$e" "$HIDDEN/$e"; echo "      hidden: $e" ;; esac
    done
  fi
fi

# ---- 3/4 host discovery & linking -------------------------------------------
if [ "$SKIP_HOSTS" -eq 1 ]; then
  echo "[3/4] host linking skipped (--skip-hosts)"
else
  echo "[3/4] detected coding agents:"
  HOSTS=()
  hostdir(){ case "$1" in claude) echo "$HOME/.claude/skills" ;; codex) echo "$HOME/.codex/skills" ;; opencode) echo "$HOME/.config/opencode/skills" ;; cursor) echo "$HOME/.cursor/skills" ;; gemini) echo "$HOME/.gemini/skills" ;; copilot) echo "$HOME/.copilot/skills" ;; hermes) echo "$HOME/.hermes/skills" ;; esac; }
  for h in claude codex opencode cursor gemini copilot hermes; do
    d="$(hostdir "$h")"
    if [ -d "$(dirname "$d")" ]; then echo "      · $h"; HOSTS+=("$h"); fi
  done
  if [ ${#HOSTS[@]} -eq 0 ]; then
    echo "      (none detected; library is still usable by any host that reads ~/.agents/skills)"
  elif [ "$YES" -eq 1 ] || [ ! -t 0 ]; then
    echo "      (non-interactive) linking all detected hosts"
    python3 _scripts/link_hosts.py
  else
    printf "      link to which hosts? [blank = all detected]%s]\n      > " "${HOSTS[*]}"
    read -r CHOICE || CHOICE=""
    if [ -z "$CHOICE" ] || [ "$CHOICE" = "all" ]; then
      python3 _scripts/link_hosts.py
    elif [ "$CHOICE" = "none" ]; then
      echo "      (none selected)"
    else
      IFS=',' read -ra HS <<< "${CHOICE// /}"
      for h in "${HS[@]}"; do python3 _scripts/link_hosts.py --host "$h"; done
    fi
  fi
fi

# ---- 4/4 API keys ------------------------------------------------------------
if [ "$SKIP_ENV" -eq 1 ]; then
  echo "[4/4] API-key setup skipped (--skip-env)"
else
  if [ ! -t 0 ]; then
    echo "[4/4] (non-interactive) API-key check"
  fi
  if [ -f "$HOME/.shell_env" ]; then
    python3 _scripts/install_env.py
  else
    echo "[4/4] ~/.shell_env not found — key template: env.example"
    if [ -t 0 ]; then
      printf "      run key setup now? [y/N] "
      read -r ANS || ANS=n
      case "$ANS" in y|Y) python3 _scripts/install_env.py ;; *) echo "      skipped." ;; esac
    else
      echo "      skipped (run later: bash install.sh --skip-hosts --select)"
    fi
  fi
fi

echo
echo "=== done
  open a new terminal (or: source ~/.profile)
  verify:   bash -lc 'test -n \"\${OPENALEX_API_KEY:-}\" && echo OK'
  hidden:   bash $(basename "$0") hidden
  install:  bash $(basename "$0") enable <name>
  skills:   ls $CANON"
