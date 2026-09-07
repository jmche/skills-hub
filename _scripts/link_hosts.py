#!/usr/bin/env python3
"""link_hosts.py - distribute canonical skills to detected hosts via per-skill symlinks.

Policy (purely additive / idempotent / never destroys host-local versions):
  Top-level skill dirs canonical/<name>/ (containing SKILL.md):
    host skills dir absent  -> create the dir, symlink canonical -> host/skills
    host already has <name> -> skip (host-local version kept)
    otherwise               -> symlink host/skills/<name> -> canonical/<name>
  Roles canonical/roles/:
    host agents dir absent  -> symlink roles -> host/agents
    host already has agents -> skip
  A single failure is isolated and reported; --dry-run just prints.
"""
import os, sys, pathlib

ROOT = pathlib.Path('/home/jmche/.agents/skills').resolve()
DRY = '--dry-run' in sys.argv

HOSTS = {
    'claude':   dict(skills='~/.claude/skills',        roles='~/.claude/agents'),
    'codex':    dict(skills='~/.codex/skills',        roles=None),          # roles need toml rendering; handled separately
    'hermes':   dict(skills='~/.hermes/skills',       roles=None),          # roles go through the host plugin / delegate mechanism
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
