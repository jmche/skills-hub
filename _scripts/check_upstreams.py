#!/usr/bin/env python3
"""check_upstreams.py - compare vendored skills against their upstream versions.

Used by `install.sh update` and .github/workflows/upstream-sync.yml. For every
entry in upstreams.json:
  - read the vendored ref from upstreams.lock.json
  - resolve the upstream's newest stable semver tag, or the latest commit on
    its "branch"; an entry with a local patch in use counts as stale every
    day, so its probe decides again whether upstream works unpatched
  - report; with --sync, stale entries are synced and committed one by one
    (see sync_upstream.py); the first failure stops the run
  - with --stale, print only "<name> <ref>" per stale entry on stdout (the
    report goes to stderr); the workflow syncs each of them separately

Exit codes: 0 = up to date / synced, 1 = failure.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

def main():
    sync = "--sync" in sys.argv
    names_only = "--stale" in sys.argv
    out = sys.stderr if names_only else sys.stdout
    cfg = json.load(open(os.path.join(ROOT, "upstreams.json"), encoding="utf-8"))
    import sync_upstream as su
    lock = su.load_lock()

    stale = []
    lookup_failed = False
    for name, c in cfg.items():
        local = lock.get(name, {}).get("ref")
        if names_only:
            # 一个上游查询失败时，其余上游照常列出，最后以非零码退出
            try:
                latest = su.latest_ref(c)
            except SystemExit as e:
                print(f"[{name}] upstream lookup failed: {e}", file=out)
                lookup_failed = True
                continue
        else:
            latest = su.latest_ref(c)
        patched = lock.get(name, {}).get("patched")
        if local == latest and patched:
            # 使用本地补丁期间每天重新同步一次，由探测结果决定是否回到上游原版
            stale.append((name, latest))
            print(f"[{name}] up to date ({su.short(local)}); re-checking local patches: {', '.join(patched)}", file=out)
            continue
        if local == latest:
            print(f"[{name}] up to date ({su.short(local)})", file=out)
            continue
        lv = su.stable_version(local) if local and "branch" not in c else None
        if lv and lv > su.stable_version(latest):
            print(f"[{name}] vendored {local} is newer than upstream {latest} - skipping", file=out)
            continue
        stale.append((name, latest))
        print(f"[{name}] UPDATE AVAILABLE: {su.short(local) or '(not vendored)'} -> {su.short(latest)}", file=out)

    if names_only:
        for name, ref in stale:
            print(name, ref)
        return 1 if lookup_failed else 0
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
