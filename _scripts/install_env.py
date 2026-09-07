#!/usr/bin/env python3
"""install_env.py — 幂等的 shell 环境安装器。

做三件事（全部可重复执行，已存在的项直接跳过）：
  1. ~/.bashrc 与 ~/.profile：确保存在核心行
        [ -f "$HOME/.shell_env" ] && . "$HOME/.shell_env"
     且位于交互式守卫（case $- in / # If not running interactively）之前；
     已存在则跳过。修改前先备份 .bak.YYYYmmdd-HHMMSS。
  2. 把源 env 文件（默认 ~/.agents/.env，其次 ~/.agents/skills/.env）里缺失的
     KEY=VALUE 合并进 ~/.shell_env：已存在的 key 跳过；新 key 带日期注释追加。
     ~/.shell_env 不存在则创建；权限强制 600。
  3. 校验：用 bash -lc 检查关键 key 非空（不打印值）。
"""
import datetime
import os
import re
import shutil
import subprocess
import sys

HOME = os.path.expanduser('~')
CORE = '[ -f "$HOME/.shell_env" ] && . "$HOME/.shell_env"'
STAMP = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
DATE = datetime.date.today().isoformat()
shell_env = os.path.join(HOME, '.shell_env')
sources = [os.path.join(HOME, '.agents', '.env'),
           os.path.join(HOME, '.agents', 'skills', '.env')]

def ts():
    print(f'  [{datetime.datetime.now().strftime("%H:%M:%S")}]', end=' ')

def ensure_core_line(path: str) -> str:
    """返回 action: skipped|inserted|appended|absent-skip"""
    if not os.path.isfile(path):
        ts(); print(f'{os.path.basename(path)}: 文件不存在，跳过（新建 shell 环境时可手建）'); return 'absent'
    txt = open(path, encoding='utf-8', errors='replace').read()
    if CORE in txt:
        ts(); print(f'{os.path.basename(path)}: 核心行已存在 → 跳过'); return 'skipped'
    lines = txt.splitlines(keepends=True)
    insert_at = None
    guard = re.compile(r'^(case \$- in|# If not running interactively|#.*interactive guard|export PS1=)', re.I)
    for i, ln in enumerate(lines):
        if guard.match(ln):
            insert_at = i
            break
    block = ['# --- API keys: centralized in ~/.shell_env (before interactive guard) ---\n',
             CORE + '\n', '\n']
    if insert_at is None:
        if lines and not lines[-1].endswith('\n'):
            lines[-1] += '\n'
        lines += block
        action = 'appended'
    else:
        lines[insert_at:insert_at] = block
        action = 'inserted'
    bak = f'{path}.bak.{STAMP}'
    shutil.copy2(path, bak)
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    ts(); print(f'{os.path.basename(path)}: 核心行{action}（备份 {os.path.basename(bak)}）')
    return action

def parse_env_lines(path: str):
    """yield (key, value) for real KEY=VALUE lines (export optional)."""
    if not os.path.isfile(path):
        return
    for raw in open(path, encoding='utf-8', errors='replace'):
        ln = raw.strip()
        if not ln or ln.startswith('#'):
            continue
        if ln.startswith('export '):
            ln = ln[len('export '):].strip()
        if '=' not in ln:
            continue
        key, _, val = ln.partition('=')
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
            continue
        v = val.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
            v = v[1:-1]
        yield key, v

def merge_into_shell_env() -> int:
    os.umask(0o077)
    if not os.path.exists(shell_env):
        open(shell_env, 'w').close()
    if os.path.exists(shell_env):
        cur = open(shell_env, encoding='utf-8', errors='replace').read()
        existing = set(re.findall(r'^(?:export[ \t]+)?([A-Za-z_][A-Za-z0-9_]*)=', cur, re.M))
    else:
        existing = set()
    added = 0
    with open(shell_env, 'a+', encoding='utf-8') as f:
        for src in sources:
            for key, val in parse_env_lines(src):
                if key in existing:
                    ts(); print(f'key 已存在，跳过: {key}')
                    continue
                f.write(f'\n# merged from {os.path.basename(src)} @ {DATE} (by install.sh)\n')
                f.write(f'export {key}="{val}"\n')
                ts(); print(f'key 新增: {key}（来源 {src}）')
                added += 1
                existing.add(key)
    os.chmod(shell_env, 0o600)
    return added

def verify(keys):
    ts(); print('校验 bash -lc 环境可见性 …')
    for k in keys:
        r = subprocess.run(['bash', '-lc', f'test -n "${{{k}:-}}" && echo yes'],
                           capture_output=True, text=True)
        mark = 'OK ' if r.stdout.strip() == 'yes' else 'MISS'
        print(f'        {mark} {k}')

def main(dry=False):
    ts(); print('── 1/3 shell 启动文件 ──')
    if dry:
        print('  [dry] 会检查 ~/.bashrc ~/.profile')
    else:
        ensure_core_line(os.path.join(HOME, '.bashrc'))
        ensure_core_line(os.path.join(HOME, '.profile'))
    ts(); print('── 2/3 合并 env 到 ~/.shell_env ──')
    added = 0 if dry else merge_into_shell_env()
    if dry:
        for src in sources:
            for k, _ in parse_env_lines(src):
                print(f'  [dry] 候选 key: {k}')
    ts(); print('── 3/3 校验 ──')
    sample = []
    for src in sources:
        for k, _ in parse_env_lines(src):
            if k not in sample:
                sample.append(k)
        if sample:
            break
    if dry or not sample:
        print('  (dry-run 或无候选 key，跳过校验)')
    else:
        verify(sample[:8])
    ts(); print('DONE')

if __name__ == '__main__':
    main(dry='--dry-run' in sys.argv)
