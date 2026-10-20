#!/usr/bin/env bash
# 扫描 git 索引里所有文件中形似 API key 的字符串；ci.yml 和 upstream-sync.yml 共用
set -u
pattern='sk-[A-Za-z0-9]{30,}|ghp_[A-Za-z0-9]{30,}|gho_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}'
status=0
matches=$(git grep --cached -ahoE -e "$pattern") || status=$?
if [ "$status" -eq 1 ]; then exit 0; fi
if [ "$status" -ne 0 ]; then exit "$status"; fi
if printf '%s\n' "$matches" | grep -qv '^sk-abcdefghijklmnopqrstuvwxyz'; then
  echo "files containing key-shaped strings:"
  git grep --cached -alE -e "$pattern"
  exit 1
fi
