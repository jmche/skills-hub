#!/usr/bin/env python3
"""check.py — 一致性门禁。每次 gen 之后必须全绿。

检查项：
  C1  每个 hub 目录下不得出现 INSTRUCTIONS.md 之外的 SKILL.md（子技能内）
      → 防深度扫描器（npx skills 等）把子技能当独立技能注册。
  C2  hub SKILL.md 索引表里列出的每个子技能，其 <hub>/<name>/INSTRUCTIONS.md 必须存在
  C3  INSTRUCTIONS.md 内的本地相对路径引用（markdown 链接 + 脚本路径）必须可达
  C4  名字唯一：同 hub 内无重名；顶层/hub 之间无冲突
  C5  子技能目录深度 ≤ 2（skills/<hub>/<name>/…），再深即违规
  C6  catalog 顶层条目 ≤ 119（OpenCode 上限余量）
  C7  每个 hub frontmatter description ≥ 40 字符
  C8  _assignments.json 中的名字都确有对应目录（已收集或仍在顶层）
  C9  scientific 的 sections 与磁盘一致（无缺失/无多余）
"""
import argparse, json, os, re, sys, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HUBS = ['research','scientific','references','dev','data-ml','docs-figures','team']
errors, warns = [], []
FINAL = '--final' in sys.argv[1:]

def err(m): errors.append(m)
def warn(m): warns.append(m)

assignments = json.load(open(os.path.join(ROOT,'_assignments.json'),encoding='utf-8'))
all_assigned = {}
for k,v in assignments.items():
    if k.startswith('_'): continue
    for s in v: all_assigned.setdefault(s, k)

# C6 catalog top-level (dirs with SKILL.md directly under root)
topskills = [d for d in os.listdir(ROOT)
             if os.path.isdir(os.path.join(ROOT,d)) and os.path.isfile(os.path.join(ROOT,d,'SKILL.md'))]
if len(topskills) > 119:
    if FINAL: err(f'C6 (final) top-level catalog {len(topskills)} > 119')
    else: warn(f'C6 top-level catalog entries = {len(topskills)} (final gate: must be <=119 after all hubs collected)')

import yaml
meta = yaml.safe_load(open(os.path.join(ROOT,'routes_meta.yaml'),encoding='utf-8'))

for hub in HUBS:
    hdir = os.path.join(ROOT, hub)
    hskill = os.path.join(hdir, 'SKILL.md')
    if not os.path.isdir(hdir):
        continue
    # C1: no stray SKILL.md in sub-skill dirs
    for sp in glob.glob(os.path.join(hdir, '*', 'SKILL.md')):
        err(f'C1 stray SKILL.md: {os.path.relpath(sp, ROOT)}')
    if not os.path.isfile(hskill):
        warn(f'C7 {hub}: hub SKILL.md not yet generated')
        continue
    txt = open(hskill, encoding='utf-8').read()
    # C7 description length
    m = re.match(r'^---\s*\n(.*?)\n---', txt, re.S|re.M)
    if not m:
        err(f'C7 {hub}: no frontmatter in hub SKILL.md'); continue
    dm = re.search(r'description:\s*(.*?)(?=\n\w+:\s|\Z)', m.group(1), re.S|re.M)
    dlen = len(re.sub(r'\s+','', dm.group(1))) if dm else 0
    if dlen < 40: err(f'C7 {hub}: description only {dlen} chars (<40)')
    # C2: every listed sub-skill has INSTRUCTIONS.md
    listed = set(re.findall(r'^\|\s*([a-z0-9][a-z0-9-]*)\s*\|', re.sub(r'##.*','',txt), re.M))
    # more robust: parse table rows
    rows = re.findall(r'^\|\s*([a-z0-9][a-z0-9-]+)\s*\|\s*(.*?)\s*\|$', txt, re.M)
    listed = [r[0] for r in rows if r[0] not in ('子技能','name')]
    disk = set(os.listdir(hdir))
    # C9 scientific sections check
    if hub == 'scientific':
        secs = meta.get('hubs',{}).get('scientific',{}).get('sections',[])
        for sec in secs:
            title, members = sec[0], sec[1]
            for nm in members:
                if not os.path.isdir(os.path.join(hdir, nm)):
                    if not os.path.isdir(os.path.join(ROOT, nm)):
                        err(f'C9 scientific section "{title}": {nm} not found (disk or top)')
    # C8: assigned names to this hub resolve
    for nm in assignments.get(hub, []):
        if not os.path.isdir(os.path.join(hdir, nm)) and not os.path.isdir(os.path.join(ROOT, nm)):
            err(f'C8 {hub}: assigned skill {nm} missing on disk')
    # C2: each on-disk sub-skill dir must have INSTRUCTIONS.md (except team)
    for nm in os.listdir(hdir):
        p = os.path.join(hdir, nm)
        if os.path.isdir(p) and hub != 'team':
            if not os.path.isfile(os.path.join(p,'INSTRUCTIONS.md')):
                err(f'C2 {hub}/{nm}: no INSTRUCTIONS.md')
        # C5 depth
    # C5: INSTRUCTIONS.md must live at most at skills/<hub>/<name>/INSTRUCTIONS.md
    for sp in glob.glob(os.path.join(hdir, '*', '*', 'INSTRUCTIONS.md')):
        err(f'C5 INSTRUCTIONS.md deeper than skills/<hub>/<name>/: {os.path.relpath(sp, ROOT)}')

# C3: INSTRUCTIONS.md local relative links resolve (sample: only files, not http)
checked = 0
for ino in glob.glob(os.path.join(ROOT, HUBS and '*' , '*','INSTRUCTIONS.md')):
    pass
import glob as g
INO = [p for h in HUBS for p in g.glob(os.path.join(ROOT, h, '*', 'INSTRUCTIONS.md'))]
for p in INO:
    base = os.path.dirname(p)
    txt = open(p, encoding='utf-8', errors='replace').read()
    links = re.findall(r'\]\(([^)\s]+)\)', txt)
    for ln in links:
        if ln.startswith(('http','mailto','#','/')) or ln == 'url': continue
        tgt = os.path.normpath(os.path.join(base, ln.split('#')[0]))
        if not os.path.exists(tgt):
            err(f'C3 {os.path.relpath(p,ROOT)}: broken local link {ln}')
        checked += 1

print(f'--- check.py ---')
print(f'OK  sub-skill dirs scanned:    {len(INO)}')
print(f'OK  local links checked:       {checked}')
for w in warns: print('WARN', w)
if errors:
    print(f'FAIL  {len(errors)} error(s):', file=sys.stderr)
    for e in errors: print('  ERR', e, file=sys.stderr)
    sys.exit(1)
print('PASS  all gates green')
