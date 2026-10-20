#!/usr/bin/env python3
"""check_upstreams.py - compare vendored skills against their upstream versions.

Used by `install.sh update` and .github/workflows/upstream-sync.yml. For every
entry in upstreams.json:
  - read the vendored ref from upstreams.lock.json
  - resolve the upstream's newest stable semver tag, or the latest commit on
    its "branch"
  - report; with --sync, stale entries are synced and committed one by one
    (see sync_upstream.py); the first failure stops the run

Exit codes: 0 = up to date / synced, 1 = failure.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

def main():
    sync = "--sync" in sys.argv
    cfg = json.load(open(os.path.join(ROOT, "upstreams.json"), encoding="utf-8"))
    import sync_upstream as su
    lock = su.load_lock()

    stale = []
    for name, c in cfg.items():
        local = lock.get(name, {}).get("ref")
        latest = su.latest_ref(c)
        if local == latest:
            print(f"[{name}] up to date ({su.short(local)})")
            continue
        if "branch" not in c and local and su.stable_version(local) > su.stable_version(latest):
            print(f"[{name}] vendored {local} is newer than upstream {latest} - skipping")
            continue
        stale.append((name, latest))
        print(f"[{name}] UPDATE AVAILABLE: {su.short(local) or '(not vendored)'} -> {su.short(latest)}")

    if not sync:
        if stale:
            print(f"{len(stale)} upstream update(s) available - synced daily by the "
                  f"upstream-sync workflow (or: bash install.sh update --commit); users "
                  f"receive the result through the next update's git pull")
        return 0

    for name, ref in stale:
        r = subprocess.run([sys.executable, os.path.join(HERE, "sync_upstream.py"),
                            name, "--ref", ref, "--commit"], cwd=ROOT).returncode
        if r != 0:
            print(f"[{name}] sync FAILED - left uncommitted for review")
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
