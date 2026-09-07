#!/usr/bin/env bash
# sync.sh - MAINTAINER-ONLY one-shot: regenerate hub indexes -> consistency gates -> host distribution
# Usage: sync.sh [--hub <name>]   (regenerate only one hub index)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "=== [1/3] gen_routers (indexes + registry) ==="
python3 _scripts/gen_routers.py "$@"
echo "=== [2/3] check gates ==="
python3 _scripts/check.py
echo "=== [3/3] link hosts ==="
python3 _scripts/link_hosts.py
echo "SYNC OK"
