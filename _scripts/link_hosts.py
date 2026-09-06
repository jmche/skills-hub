#!/usr/bin/env python3
"""link_hosts.py — 把 canonical 技能以"技能级软链"分发到已装宿主。

策略（纯增量 / 幂等 / 不丢宿主本地版本）：
  顶层技能目录 canonical/<name>/（含 SKILL.md）：
    宿主 skills 目录不存在  → 建目录，整目录软链 canonical -> host/skills
    宿主已有 <name>        → 跳过（保留宿主本地版本）
    否则                  → 建软链 host/skills/<name> -> canonical/<name>
  角色 canonical/roles/：
    宿主 agents 目录不存在 → 整目录软链 -> host/agents
    宿主已有 agents        → 跳过
  单个失败隔离记录，不中断。--dry-run 只打印。
"""
import os, sys, pathlib

ROOT = pathlib.Path('/home/jmche/.agents/skills').resolve()
DRY = '--dry-run' in sys.argv

HOSTS = {
    'claude':   dict(skills='~/.claude/skills',        roles='~/.claude/agents'),
    'codex':    dict(skills='~/.codex/skills',        roles=None),          # roles 需渲染 toml，单独处理
    'hermes':   dict(skills='~/.hermes/skills',       roles=None),          # roles 走插件/delegate
    'opencode': dict(skills='~/.config/opencode/skills', roles=None),
    'cursor':   dict(skills='~/.cursor/skills',       roles='~/.cursor/agents'),
    'gemini':   dict(skills='~/.gemini/skills',       roles='~/.gemini/agents'),
    'copilot':  dict(skills='~/.copilot/skills',      roles='~/.copilot/agents'),
}
only = [a for a in sys.argv[1:] if a not in ('--dry-run',)]
HOSTS = {k: v for k, v in HOSTS.items() if not only or k in only}

skills = sorted(p.name for p in ROOT.iterdir()
                if p.is_dir() and (p / 'SKILL.md').is_file())
print(f'canonical top skills: {len(skills)}')

def link(d: pathlib.Path, target: pathlib.Path):
    if DRY:
        print(f'  [dry] ln -s {target} {d}')
    else:
        try:
            d.parent.mkdir(parents=True, exist_ok=True)
            d.symlink_to(target)
            print(f'  + {d.name} -> {target}')
        except Exception as e:
            print(f'  ! {d.name}: {e}')

summary = {}
for host, spec in HOSTS.items():
    sk = os.path.expanduser(spec['skills'])
    skp = pathlib.Path(sk)
    made = kept = 0
    if not skp.exists():
        if DRY: print(f'[{host}] (dry) mkdir + link whole dir')
        else:
            skp.parent.mkdir(parents=True, exist_ok=True)
            skp.symlink_to(ROOT)
        print(f'[{host}] whole-dir link (absent)')
        continue
    for s in skills:
        dst = skp / s
        if dst.exists() or dst.is_symlink():
            kept += 1
        else:
            link(dst, ROOT / s); made += 1
    rr = spec['roles']
    if rr:
        rp = pathlib.Path(os.path.expanduser(rr))
        if not rp.exists() and not rp.is_symlink():
            link(rp, ROOT / 'roles')
    summary[host] = (made, kept)
    print(f'[{host}] +{made} new links, {kept} kept host-local')

print('OK' if not DRY else 'DRY OK')
