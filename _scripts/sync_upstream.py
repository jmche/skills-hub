#!/usr/bin/env python3
"""sync_upstream.py - pull a vendored skill's latest stable version from its upstream repo.

Usage:
  python3 _scripts/sync_upstream.py <name>            # sync to latest stable tag
  python3 _scripts/sync_upstream.py <name> --ref v2.16.0
  python3 _scripts/sync_upstream.py <name> --commit   # also git commit the result

Driven by upstreams.json. For each entry:
  1. resolve the latest stable semver tag of <repo> (prereleases skipped)
  2. download the tag tarball (codeload) and extract only <subdir>/
  3. mirror it over the vendored dir:
       - SKILL.md is renamed per `rename` (our convention: INSTRUCTIONS.md)
       - `exclude` globs are dropped
       - files removed upstream are removed locally too (true mirror)
  4. print the version bump and a diff stat, then run check.py (hard gate)
  5. with --commit, create a git commit

This is a MAINTAINER command: vendored third-party content is reviewed once by
you at sync time, then shipped to users through the normal skills-hub update.
"""
import json, os, subprocess, sys, tarfile, tempfile, urllib.request, shutil, fnmatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True, **kw)

def gh_json(url):
    r = subprocess.run(["gh", "api", url], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"gh api failed: {url}\n{r.stderr}")
    return json.loads(r.stdout)

def latest_tag(repo):
    tags = gh_json(f"repos/{repo}/tags?per_page=50")
    for t in tags:
        name = t["name"].lstrip("v")
        parts = name.split(".")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            return t["name"]                      # first (newest) stable tag
    sys.exit("no stable semver tag found")

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    cfg_all = json.load(open(os.path.join(ROOT, "upstreams.json")))
    if name not in cfg_all:
        sys.exit(f"unknown upstream '{name}'. known: {', '.join(cfg_all)}")
    cfg = cfg_all[name]
    ref = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else latest_tag(cfg["repo"])
    commit = "--commit" in sys.argv

    vendored = os.path.join(ROOT, cfg["vendored"])
    # current version, for the report
    old_ver = "?"
    pkg = os.path.join(vendored, "package.json")
    if os.path.isfile(pkg):
        old_ver = json.load(open(pkg)).get("version", "?")

    print(f"[{name}] syncing {cfg['repo']}@{ref} -> {cfg['vendored']}")
    url = f"https://codeload.github.com/{cfg['repo']}/tar.gz/refs/tags/{ref}"
    tmp = tempfile.mkdtemp()
    tgz = os.path.join(tmp, "src.tar.gz")
    urllib.request.urlretrieve(url, tgz)
    prefix = f"{cfg['repo'].split('/')[-1]}-{ref.lstrip('v')}/"
    src_prefix = prefix + cfg["subdir"].strip("/") + "/"
    staging = os.path.join(tmp, "stage")
    with tarfile.open(tgz) as tf:
        members = [m for m in tf.getmembers() if m.name.startswith(src_prefix) and m.isfile()]
        if not members:
            sys.exit(f"no files under {src_prefix} in {ref}")
        for m in members:
            m.name = m.name[len(src_prefix):]      # strip the tarball prefix
            tf.extract(m, staging)

    # mirror: wipe vendored (keep nothing - upstream is the source of truth),
    # then copy staged files, applying renames/excludes
    new_ver = "?"
    stage_pkg = os.path.join(staging, "package.json")
    if os.path.isfile(stage_pkg):
        new_ver = json.load(open(stage_pkg)).get("version", "?")

    shutil.rmtree(vendored)
    shutil.copytree(staging, vendored)
    for src, dst in cfg.get("rename", {}).items():
        s = os.path.join(vendored, src)
        if os.path.isfile(s):
            os.replace(s, os.path.join(vendored, dst))
    for pat in cfg.get("exclude", []):
        for f in os.listdir(vendored):
            if fnmatch.fnmatch(f, pat):
                shutil.rmtree(os.path.join(vendored, f)) if os.path.isdir(os.path.join(vendored, f)) else os.remove(os.path.join(vendored, f))

    print(f"  version: {old_ver} -> {new_ver}")
    st = sh("git status --porcelain -- " + cfg["vendored"]).stdout.strip().splitlines()
    print(f"  changed files: {len(st)}")
    for ln in st[:12]:
        print("   ", ln)
    if len(st) > 12:
        print(f"    ... and {len(st)-12} more")

    gate = sh("python3 _scripts/check.py")
    tail = [l for l in gate.stdout.splitlines() if l.strip()][-1:]
    print("  gates:", tail[0] if tail else "?")
    if gate.returncode != 0:
        print(gate.stdout, gate.stderr)
        sys.exit("check.py failed - NOT committing. Resolve and retry.")

    if commit:
        msg = f"sync {name}: {old_ver} -> {new_ver} ({cfg['repo']}@{ref})"
        c = sh(f'git add -A "{cfg["vendored"]}" && git commit -m "{msg}"')
        print("  committed:", msg)
        if "--push" in sys.argv:
            p = sh("git push origin HEAD")
            print("  pushed" if p.returncode == 0 else f"  push failed: {p.stderr.strip()[:120]}")
    else:
        print("  (dry: pass --commit to commit)")
    shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
