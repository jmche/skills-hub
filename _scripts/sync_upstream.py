#!/usr/bin/env python3
"""sync_upstream.py - mirror a vendored upstream's skill directories at its latest version.

Usage:
  python3 _scripts/sync_upstream.py <name>            # sync to the latest version
  python3 _scripts/sync_upstream.py <name> --ref v2.16.0
  python3 _scripts/sync_upstream.py <name> --commit   # also git commit the result

Driven by upstreams.json (configuration) and upstreams.lock.json (the ref each
entry is vendored at and the directories it owns; written only by this script).
An entry maps upstream directories to local skill directories:
  - "subdir" + "vendored": one upstream directory -> one local directory
  - "subdir" + "hub":      every child directory of <subdir> holding a SKILL.md
                           -> <hub>/<child>
  - "subdir" + "skills":   only the listed children, {upstream name: local dir};
                           a local dir is <hub>/<name> or a top-level <name>
The version tracked is the newest stable semver tag, or with "branch" the
latest commit on that branch.

Steps:
  1. resolve the ref, download its tarball (codeload), stage the mapped dirs
  2. in each staged dir: rename per `rename` (our convention: SKILL.md ->
     INSTRUCTIONS.md; hub sub-skills only, a top-level skill keeps SKILL.md),
     drop `exclude` globs, copy `license_files` from the upstream repo root
     when the dir has no file of that name; for a skill in `patches`, run its
     probe command on the upstream copy and keep that copy when the probe
     passes, otherwise apply the local patch and require the probe to pass
     (the lock records which patches are in use)
  3. delete the dirs the entry owned before, copy the staged dirs in (a true
     mirror); a target dir that exists but is not owned by the entry stops the
     sync
  4. keep _assignments.json and the LICENSE-AUDIT.csv rows in step with the
     owned dirs, regenerate the hub indexes (gen_routers.py --only-generate),
     write the lock
  5. run check.py (hard gate); with --commit, create a git commit

This is a MAINTAINER command, also run daily by .github/workflows/upstream-sync.yml:
vendored third-party content ships to users through the normal skills-hub update.
"""
import csv, fnmatch, io, json, os, shutil, subprocess, sys, tarfile, tempfile, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = os.path.join(ROOT, "upstreams.lock.json")
ASSIGN = os.path.join(ROOT, "_assignments.json")
AUDIT = os.path.join(ROOT, "LICENSE-AUDIT.csv")

def sh(args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)

def gh_json(url):
    r = subprocess.run(["gh", "api", url], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"gh api failed: {url}\n{r.stderr}")
    try:
        data = json.loads(r.stdout)
    except ValueError:
        sys.exit(f"gh api returned non-JSON for {url}")
    if not isinstance(data, (dict, list)):
        sys.exit(f"gh api returned an unexpected value for {url}")
    return data

def stable_version(tag):
    parts = tag.lstrip("v").split(".")
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        return tuple(int(p) for p in parts)
    return None

def latest_ref(cfg):
    if "branch" in cfg:
        data = gh_json(f"repos/{cfg['repo']}/commits/{cfg['branch']}")
        if not isinstance(data, dict) or "sha" not in data:
            sys.exit(f"no commit sha for {cfg['repo']}@{cfg['branch']}")
        return data["sha"]
    r = subprocess.run(["gh", "api", "--paginate", f"repos/{cfg['repo']}/tags?per_page=100",
                        "--jq", ".[].name"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"gh api failed: tags of {cfg['repo']}\n{r.stderr}")
    tags = r.stdout.split()
    stable = [t for t in tags if stable_version(t)]
    if not stable:
        sys.exit(f"no stable semver tag found in {cfg['repo']}")
    return max(stable, key=stable_version)

def short(ref):
    return ref[:7] if ref and len(ref) == 40 else ref

def load_lock():
    if not os.path.isfile(LOCK):
        return {}
    return json.load(open(LOCK, encoding="utf-8"))

def download(cfg, ref, tmp):
    kind = ref if "branch" in cfg else f"refs/tags/{ref}"
    tgz = os.path.join(tmp, "src.tar.gz")
    urllib.request.urlretrieve(f"https://codeload.github.com/{cfg['repo']}/tar.gz/{kind}", tgz)
    tree = os.path.join(tmp, "tree")
    with tarfile.open(tgz) as tf:
        sub = cfg["subdir"].strip("/") + "/"
        for m in tf.getmembers():
            rel = os.path.normpath(m.name.split("/", 1)[1]) if "/" in m.name else ""
            if m.isdir() or not rel:
                continue
            if rel.startswith("..") or os.path.isabs(rel):
                sys.exit(f"unsafe path in upstream tarball: {m.name}")
            if not m.isfile():
                if rel.startswith(sub):
                    sys.exit(f"{rel} is not a regular file; the mirror cannot reproduce it")
                continue
            m.name = rel
            tf.extract(m, tree)
    return tree

def targets(cfg, tree):
    """{local dir (relative to ROOT): staged source dir}"""
    base = os.path.join(tree, cfg["subdir"].strip("/"))
    if not os.path.isdir(base):
        sys.exit(f"upstream has no {cfg['subdir']}/")
    if "hub" in cfg:
        names = sorted(d for d in os.listdir(base)
                       if os.path.isfile(os.path.join(base, d, "SKILL.md")))
        return {f"{cfg['hub']}/{d}": os.path.join(base, d) for d in names}
    if "skills" in cfg:
        missing = sorted(n for n in cfg["skills"] if not os.path.isfile(os.path.join(base, n, "SKILL.md")))
        if missing:
            sys.exit(f"upstream no longer has {', '.join(missing)} under {cfg['subdir']}/ - update upstreams.json")
        return {d: os.path.join(base, n) for n, d in cfg["skills"].items()}
    return {cfg["vendored"]: base}

def split_dir(d):
    """local dir -> (_assignments.json key, name); a top-level skill belongs to "top" """
    return tuple(d.split("/")) if "/" in d else ("top", d)

def prepare(cfg, tree, d, src):
    if "/" in d:
        for s, t in cfg.get("rename", {}).items():
            if os.path.isfile(os.path.join(src, s)):
                os.replace(os.path.join(src, s), os.path.join(src, t))
    for pat in cfg.get("exclude", []):
        for f in os.listdir(src):
            if fnmatch.fnmatch(f, pat):
                p = os.path.join(src, f)
                shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    for f in cfg.get("license_files", []):
        if not os.path.exists(os.path.join(src, f)):
            shutil.copy2(os.path.join(tree, f), os.path.join(src, f))

def update_assignments(old_dirs, new_dirs):
    a = json.load(open(ASSIGN, encoding="utf-8"))
    for d in old_dirs:
        if d not in new_dirs:
            hub, nm = split_dir(d)
            a[hub].remove(nm)
    for d in new_dirs:
        hub, nm = split_dir(d)
        if nm not in a[hub]:
            a[hub].append(nm)
    with open(ASSIGN, "w", encoding="utf-8") as f:
        f.write(json.dumps(a, ensure_ascii=False, indent=2))

SPDX_STATUS = {"MIT": "mit", "Apache-2.0": "apache", "BSD-2-Clause": "bsd", "BSD-3-Clause": "bsd",
               "CC-BY-4.0": "cc-by", "CC0-1.0": "cc0"}

def skill_license(d):
    """the `license:` value in the skill's own frontmatter, if any"""
    # 只在同步时需要 PyYAML；install.sh update 只查看更新，不加载它
    import yaml
    for f in ("INSTRUCTIONS.md", "SKILL.md"):
        p = os.path.join(ROOT, d, f)
        if os.path.isfile(p):
            text = open(p, encoding="utf-8", errors="replace").read()
            if text.startswith("---"):
                fm = yaml.safe_load(text.split("\n---", 1)[0][3:]) or {}
                if not isinstance(fm, dict):
                    sys.exit(f"{d}/{f}: frontmatter is not a mapping")
                lic = fm.get("license")
                return str(lic).strip() if lic else None
    return None

def update_audit(name, cfg, old_dirs, new_dirs):
    rows = list(csv.reader(io.StringIO(open(AUDIT, newline="", encoding="utf-8").read())))
    rows = [r for r in rows if r[0] not in old_dirs or r[0] in new_dirs]
    have = {r[0] for r in rows}
    for d in new_dirs:
        if d in have:
            continue
        hub = split_dir(d)[0]
        lic = skill_license(d) or cfg["license"]
        # 只有可识别的 SPDX 标识才写入 raw_status，其余写 unknown，留给人工核对
        row = [d, hub, SPDX_STATUS.get(lic, "unknown"),
               f"{lic} ({cfg['repo']}, vendored; upstream-synced)", cfg["repo"], "publish"]
        last = max((i for i, r in enumerate(rows) if r[1] == hub), default=len(rows) - 1)
        rows.insert(last + 1, row)
    out = io.StringIO()
    csv.writer(out, lineterminator="\r\n").writerows(rows)
    with open(AUDIT, "w", newline="", encoding="utf-8") as f:
        f.write(out.getvalue())

PROBE_ENV = {"PATH", "LANG", "LC_ALL", "TZ", "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE",
             "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "no_proxy"}
PROBE_TIMEOUT = 120

def run_probe(name, p, src):
    """run the probe command in a staged skill copy; returns the exit code"""
    need = tuple(int(x) for x in p["python"].split("."))
    if sys.version_info[:len(need)] < need:
        sys.exit(f"the {name} probe needs Python {p['python']}+, this is {sys.version.split()[0]}")
    with tempfile.TemporaryDirectory() as out:
        args = [sys.executable] + [a.replace("{out}", os.path.join(out, "run")) for a in p["probe"]]
        # the probe runs upstream code: pass only what a network client needs, no tokens or API keys
        env = {k: v for k, v in os.environ.items() if k in PROBE_ENV}
        env.update(HOME=out, PYTHONDONTWRITEBYTECODE="1")
        try:
            r = subprocess.run(args, cwd=src, capture_output=True, text=True, timeout=PROBE_TIMEOUT, env=env)
        except subprocess.TimeoutExpired:
            sys.exit(f"the {name} probe did not finish within {PROBE_TIMEOUT} s - not syncing")
    last = (r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or [""])[-1]
    print(f"  {name} probe: exit {r.returncode} ({last[:120]})")
    return r.returncode

def apply_patches(cfg, staged):
    """for each configured patch: keep the upstream copy if its probe passes, otherwise apply
    the local patch and require the patched copy to pass; returns the patched skill names"""
    patched = []
    for up, p in sorted(cfg.get("patches", {}).items()):
        src = staged[cfg["skills"][up]]
        if run_probe(up, p, src) == 0:
            print(f"  {up}: upstream copy passes its probe - local patch not used")
            continue
        patch = os.path.join(ROOT, p["patch"])
        # keep git from treating an enclosing repository as the patch root
        genv = dict(os.environ, GIT_CEILING_DIRECTORIES=os.path.dirname(src))
        if subprocess.run(["git", "apply", "--check", patch], cwd=src, capture_output=True, env=genv).returncode != 0:
            sys.exit(f"{up}: upstream copy fails its probe and {p['patch']} no longer applies - review the patch")
        subprocess.run(["git", "apply", patch], cwd=src, check=True, env=genv)
        if run_probe(up, p, src) != 0:
            sys.exit(f"{up}: the patched copy fails its probe as well - not syncing")
        print(f"  {up}: upstream copy fails its probe - local patch {p['patch']} applied")
        patched.append(up)
    return patched

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    cfg_all = json.load(open(os.path.join(ROOT, "upstreams.json"), encoding="utf-8"))
    if name not in cfg_all:
        sys.exit(f"unknown upstream '{name}'. known: {', '.join(cfg_all)}")
    cfg = cfg_all[name]
    ref = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else latest_ref(cfg)
    commit = "--commit" in sys.argv
    if commit and sh(["git", "status", "--porcelain"]).stdout.strip():
        sys.exit("working tree has uncommitted changes - commit them first, then sync with --commit")

    lock = load_lock()
    old = lock.get(name, {})
    old_dirs = old.get("dirs", [])
    print(f"[{name}] syncing {cfg['repo']}@{short(ref)}")
    with tempfile.TemporaryDirectory() as tmp:
        tree = download(cfg, ref, tmp)
        staged = targets(cfg, tree)
        for d in staged:
            if d not in old_dirs and os.path.exists(os.path.join(ROOT, d)):
                sys.exit(f"{d} exists but is not owned by '{name}' (upstreams.lock.json) - not overwriting")
        for d, src in staged.items():
            prepare(cfg, tree, d, src)
        patched = apply_patches(cfg, staged)
        for d in old_dirs:
            p = os.path.join(ROOT, d)
            if os.path.isdir(p):
                shutil.rmtree(p)
        for d, src in staged.items():
            shutil.copytree(src, os.path.join(ROOT, d))
        new_dirs = sorted(staged)

    update_assignments(old_dirs, new_dirs)
    update_audit(name, cfg, old_dirs, new_dirs)
    lock[name] = {"ref": ref, "dirs": new_dirs}
    if "patches" in cfg:
        lock[name]["patched"] = patched
    with open(LOCK, "w", encoding="utf-8") as f:
        f.write(json.dumps(lock, indent=2, sort_keys=True) + "\n")
    gen = sh([sys.executable, "_scripts/gen_routers.py", "--only-generate", "--force"])
    if gen.returncode != 0:
        sys.exit(f"gen_routers.py failed:\n{gen.stdout}{gen.stderr}")

    added = sorted(set(new_dirs) - set(old_dirs))
    removed = sorted(set(old_dirs) - set(new_dirs))
    print(f"  ref: {short(old.get('ref')) or '(none)'} -> {short(ref)}")
    print(f"  dirs: {len(new_dirs)} (added {added or 'none'}, removed {removed or 'none'})")
    st = sh(["git", "status", "--porcelain"]).stdout.strip().splitlines()
    print(f"  changed files: {len(st)}")
    for ln in st[:12]:
        print("   ", ln)
    if len(st) > 12:
        print(f"    ... and {len(st)-12} more")

    gate = sh([sys.executable, "_scripts/check.py"])
    tail = [l for l in gate.stdout.splitlines() if l.strip()][-1:]
    print("  gates:", tail[0] if tail else "?")
    if gate.returncode != 0:
        print(gate.stdout, gate.stderr)
        sys.exit("check.py failed - NOT committing. Resolve and retry.")

    if commit:
        if not st:
            print("  nothing to commit")
            return
        msg = f"sync {name}: {short(old.get('ref')) or 'new'} -> {short(ref)} ({cfg['repo']})"
        # the owned dirs were just copied fresh, so everything in them is upstream content;
        # -f also keeps files that a nested upstream .gitignore matches but upstream tracks
        add = sh(["git", "add", "-A", "-f", "--"] + new_dirs)
        if add.returncode == 0:
            add = sh(["git", "add", "-A"])
        c = sh(["git", "commit", "-q", "-m", msg])
        if add.returncode != 0 or c.returncode != 0:
            sys.exit(f"git commit failed:\n{add.stderr}{c.stdout}{c.stderr}")
        print("  committed:", msg)
        if "--push" in sys.argv:
            p = sh(["git", "push", "origin", "HEAD"])
            print("  pushed" if p.returncode == 0 else f"  push failed: {p.stderr.strip()[:120]}")
    else:
        print("  (dry: pass --commit to commit)")

if __name__ == "__main__":
    main()
