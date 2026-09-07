#!/usr/bin/env python3
"""install_env.py - idempotent shell-environment installer.

Does three things (all repeatable; existing items are skipped):
  1. ~/.bashrc and ~/.profile: ensure the core line
        [ -f "$HOME/.shell_env" ] && . "$HOME/.shell_env"
     exists, placed BEFORE the interactive guard ("case $- in" /
     "If not running interactively"). Skipped when already present.
     A .bak.TIMESTAMP copy is made before any edit.
  2. Merge missing KEY=VALUE pairs from source env files (~/.agents/.env,
     then ~/.agents/skills/.env) into ~/.shell_env: existing keys are
     kept as-is; new keys appended with a dated comment. Creates
     ~/.shell_env if missing; forces 0600 permissions.
  3. Verify: `bash -lc` checks that imported keys are non-empty
     (values are never printed).
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
    """Returns the action taken: skipped|inserted|appended|absent."""
    if not os.path.isfile(path):
        ts(); print(f'{os.path.basename(path)}: file missing; skipped (create it by hand if wanted)'); return 'absent'
    txt = open(path, encoding='utf-8', errors='replace').read()
    if CORE in txt:
        ts(); print(f'{os.path.basename(path)}: core line already present -> skipped'); return 'skipped'
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
    ts(); print(f'{os.path.basename(path)}: core line {action} (backup: {os.path.basename(bak)})')
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
                    ts(); print(f'key already present, skipped: {key}')
                    continue
                f.write(f'\n# merged from {os.path.basename(src)} @ {DATE} (by install.sh)\n')
                f.write(f'export {key}="{val}"\n')
                ts(); print(f'key added: {key} (from {src})')
                added += 1
                existing.add(key)
    os.chmod(shell_env, 0o600)
    return added

def verify(keys):
    ts(); print('verifying key visibility under bash -lc ...')
    for k in keys:
        r = subprocess.run(['bash', '-lc', f'test -n "${{{k}:-}}" && echo yes'],
                           capture_output=True, text=True)
        mark = 'OK ' if r.stdout.strip() == 'yes' else 'MISS'
        print(f'        {mark} {k}')

def main(dry=False):
    ts(); print('-- 1/3 shell startup files --')
    if dry:
        print('  [dry] (dry) would check ~/.bashrc ~/.profile')
    else:
        ensure_core_line(os.path.join(HOME, '.bashrc'))
        ensure_core_line(os.path.join(HOME, '.profile'))
    ts(); print('-- 2/3 merge env into ~/.shell_env --')
    added = 0 if dry else merge_into_shell_env()
    if dry:
        for src in sources:
            for k, _ in parse_env_lines(src):
                print(f'  [dry] candidate key: {k}')
    ts(); print('-- 3/3 verification --')
    sample = []
    for src in sources:
        for k, _ in parse_env_lines(src):
            if k not in sample:
                sample.append(k)
        if sample:
            break
    if dry or not sample:
        print('  (dry-run or no candidate keys; verification skipped)')
    else:
        verify(sample[:8])
    ts(); print('DONE')

if __name__ == '__main__':
    main(dry='--dry-run' in sys.argv)
