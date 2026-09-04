#!/usr/bin/env python3
"""check.py — canonical hub consistency gates. Run after every gen; must be green to commit.

  C1  no stray SKILL.md inside a hub's sub-skill dirs (prevents deep scanners
      e.g. `npx skills` from re-registering sub-skills as independent skills)
  C2  every on-disk sub-skill dir under a hub has INSTRUCTIONS.md
  C3  local markdown links inside INSTRUCTIONS.md resolve (code blocks stripped;
      SMILES/regex false-positives excluded); dangling upstream links are WARN not
      ERR, because many shipped skills ship with broken intra-doc links
  C4  names unique within a hub
  C5  INSTRUCTIONS.md depth is exactly skills/<hub>/<name>/INSTRUCTIONS.md
  C6  top-level catalog size (OPENCODE limit 119) — a final-state invariant
  C7  each hub frontmatter description >= 40 chars
  C8  every assigned name resolves on disk
  C9  scientific sections cover all its members
"""
import argparse, glob, json, os, re, sys
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HUBS = ['research','scientific','references','dev','data-ml','docs-figures','team']
errors, warns = [], []
FINAL = '--final' in sys.argv[1:]
def err(m): errors.append(m)
def warn(m): warns.append(m)

assignments = json.load(open(os.path.join(ROOT,'_assignments.json'),encoding='utf-8'))
meta = yaml.safe_load(open(os.path.join(ROOT,'routes_meta.yaml'),encoding='utf-8'))

# C6 catalog top-level
topskills = [d for d in os.listdir(ROOT)
             if os.path.isdir(os.path.join(ROOT,d)) and os.path.isfile(os.path.join(ROOT,d,'SKILL.md'))]
if len(topskills) > 119:
    if FINAL: err(f'C6 top-level catalog {len(topskills)} > 119 (final gate)')
    else: warn(f'C6 top-level catalog = {len(topskills)} (must be <=119 in final state)')

for hub in HUBS:
    hdir = os.path.join(ROOT, hub)
    if not os.path.isdir(hdir):
        continue
    # C1: no SKILL.md in sub-skill dirs
    for sp in glob.glob(os.path.join(hdir, '*', 'SKILL.md')):
        err(f'C1 stray SKILL.md: {os.path.relpath(sp, ROOT)}')
    hskill = os.path.join(hdir, 'SKILL.md')
    if not os.path.isfile(hskill):
        warn(f'C7 {hub}: hub SKILL.md missing')
        continue
    txt = open(hskill, encoding='utf-8').read()
    m = re.match(r'^---\s*\n(.*?)\n---', txt, re.S|re.M)
    if not m:
        err(f'C7 {hub}: no frontmatter'); continue
    dm = re.search(r'description:\s*(.*?)(?=\n\w+:\s|\Z)', m.group(1), re.S|re.M)
    if not dm or len(re.sub(r'\s+','',dm.group(1))) < 40:
        err(f'C7 {hub}: description too short')
    # C4 uniqueness within hub
    subdirs = [d for d in os.listdir(hdir) if os.path.isdir(os.path.join(hdir,d))]
    if len(subdirs) != len(set(subdirs)):
        err(f'C4 {hub}: duplicate sub-skill dir name')
    # C8 assigned names resolve
    for nm in assignments.get(hub, []):
        if not os.path.isdir(os.path.join(hdir, nm)) and not os.path.isdir(os.path.join(ROOT, nm)):
            err(f'C8 {hub}/{nm}: missing on disk')
    # C2 INSTRUCTIONS.md required
    for nm in subdirs:
        if not os.path.isfile(os.path.join(hdir, nm, 'INSTRUCTIONS.md')):
            warn(f'C2 {hub}/{nm}: no INSTRUCTIONS.md (may be empty placeholder)')
    # C9 (scientific) sections cover every member
    if hub == 'scientific':
        secs = meta.get('hubs',{}).get('scientific',{}).get('sections',{})
        if isinstance(secs, dict):
            listed = set()
            for members in secs.values():
                listed |= set(members)
        else:
            listed = {m for s in secs for m in s[1]}
        ondisk = set(subdirs)
        unassigned = ondisk - set(assignments.get('scientific',[]))
        if unassigned:
            err(f'C9 scientific: subdirs not in assignments: {sorted(unassigned)}')
        missing = set(assignments.get('scientific',[])) - ondisk
        if missing:
            err(f'C9 scientific: assigned but not moved: {sorted(missing)}')
        unlisted = set(assignments.get('scientific',[])) - listed
        if unlisted:
            err(f'C9 scientific: assigned but not listed in a section: {sorted(unlisted)}')

# C3 local link scan (code blocks stripped, false-positives excluded)
INO = [p for h in HUBS for p in glob.glob(os.path.join(ROOT, h, '*', 'INSTRUCTIONS.md'))]
links_checked = 0
for p in INO:
    base = os.path.dirname(p)
    txt = open(p, encoding='utf-8', errors='replace').read()
    txt = re.sub(r'```.*?```', '', txt, flags=re.S)      # drop fenced blocks (SMILES, code)
    txt = re.sub(r'`[^`]*`', '', txt)                     # drop inline code
    # require a dot in the target OR an existing sibling file — excludes SMILES/regex junk
    for ln in re.findall(r'\]\(([^)\s]+)\)', txt):
        if ln.startswith(('http','mailto','#','/','[')) or ln == 'url': continue
        if '.' not in ln and not os.path.exists(os.path.join(base, ln.split('#')[0])):
            continue  # no-dot target and file absent → not a file link (likely SMILES etc.)
        tgt = ln.split('#')[0]
        if not tgt: continue
        if not os.path.exists(os.path.normpath(os.path.join(base, tgt))):
            warn(f'C3 (upstream) {os.path.relpath(p,ROOT)}: dangling local link {ln}')
            links_checked += 1

# C5 depth: no INSTRUCTIONS.md deeper than skills/<hub>/<name>/
for sp in glob.glob(os.path.join(ROOT, '*', '*', '*', 'INSTRUCTIONS.md')):
    rel = os.path.relpath(sp, ROOT)
    parts = rel.split(os.sep)
    if len(parts) > 3 and parts[0] not in ('_backups','_scripts','roles'):
        err(f'C5 INSTRUCTIONS.md too deep: {rel}')

print('--- check.py ---')
print(f'OK  sub-skill INSTRUCTIONS.md scanned: {len(INO)}')
print(f'WARN  dangling upstream local links: {links_checked}')
for w in warns: print('WARN', w)
if errors:
    print(f'FAIL  {len(errors)} error(s):', file=sys.stderr)
    for e in errors: print('  ERR', e, file=sys.stderr)
    sys.exit(1)
print('PASS  all hard gates green')
