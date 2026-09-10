#!/usr/bin/env python3
"""check_upstreams.py - compare vendored skills against their upstream stable tags.

Used by `install.sh update`. For every entry in upstreams.json:
  - read the vendored package.json version
  - resolve the upstream repo's latest stable semver tag (prereleases skipped)
  - report; with --sync, older entries are synced (see sync_upstream.py) and
    committed (+pushed with --push).

Exit codes: 0 = up to date / synced, 1 = failure.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

def ver_tuple(v):
    v = v.lstrip("v").split("-")[0]
    try:
        return tuple(int(p) for p in v.split("."))
    except ValueError:
        return None

def local_version(vendored):
    p = os.path.join(ROOT, vendored, "package.json")
    if not os.path.isfile(p):
        return None
    try:
        return json.load(open(p)).get("version")
    except Exception:
        return None

def main():
    sync = "--sync" in sys.argv
    push = "--push" in sys.argv
    cfg = json.load(open(os.path.join(ROOT, "upstreams.json")))
    import sync_upstream as su

    stale = []
    for name, c in cfg.items():
        local = local_version(c["vendored"])
        try:
            tag = su.latest_tag(c["repo"])
        except SystemExit as e:
            print(f"[{name}] upstream tag lookup failed: {e}")
            continue
        lt = ver_tuple(tag); lv = ver_tuple(local or "")
        if lv is None:
            print(f"[{name}] local version unknown ({c['vendored']}) - skipping")
            continue
        if lt and lv < lt:
            stale.append((name, tag, local))
            print(f"[{name}] UPDATE AVAILABLE: {local} -> {tag}")
        else:
            print(f"[{name}] up to date ({local})")

    if not sync:
        if stale:
            print(f"{len(stale)} upstream update(s) available - run: "
                  f"bash install.sh sync-upstream <name>")
        return 0

    ok = True
    for name, tag, _old in stale:
        args = [sys.executable, os.path.join(HERE, "sync_upstream.py"), name, "--ref", tag, "--commit"]
        if push:
            args.append("--push")
        r = subprocess_r(args)
        if r != 0:
            ok = False
            print(f"[{name}] sync FAILED (gates?) - left uncommitted for review")
    return 0 if ok else 1

def subprocess_r(args):
    import subprocess
    return subprocess.run(args, cwd=ROOT).returncode

if __name__ == "__main__":
    sys.exit(main())
