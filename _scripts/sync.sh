#!/usr/bin/env bash
# sync.sh — 一键拉齐：重新生成 hub 索引 → 一致性门禁 → 宿主分发
# 用法: sync.sh [--hub <name>]   (只重生成某 hub 的索引表)
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
