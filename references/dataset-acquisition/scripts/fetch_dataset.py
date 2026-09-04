#!/usr/bin/env python3
"""Acquire a public dataset when the project's own portal will not serve a machine.

Standard library only — no requests, no pandas. This runs inside headless coding-agent
subprocesses that may have nothing installed.

What it is for, none of it specific to any one dataset:

1. Judge a response by its BODY. A blocked endpoint commonly answers 200 with an HTML
   verification or login page; an archive that has not produced a file yet answers 202 with an
   empty one. Both read as success to a status-code check, and what follows is HTML parsed as
   JSON, or a zero-byte file cited as data.
2. Find the dataset on an ARCHIVE rather than the project's portal. Portals get bot-walled;
   archives exist to serve machines.
3. Transfer in ONE request. ``get`` writes a file, ``columns`` keeps only the columns you asked
   for out of a matrix too large to hold — and neither re-requests, because an archive that
   rations requests will refuse the second one.
4. Prove what arrived: size and checksum against the listing, and a provenance line.

Usage:
  fetch_dataset.py probe   <url>
  fetch_dataset.py search  <host> <query> [--limit N]
  fetch_dataset.py files   <host> <entry_id>
  fetch_dataset.py get     <url> <dest> [--expect-bytes N] [--expect-md5 M] [--wait S]
                                        [--provenance FILE]
  fetch_dataset.py columns <url> <dest.csv> --keep A,B,C [--wait S] [--provenance FILE]

Hosts: datacite (cross-archive index), figshare, zenodo.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

# There is no single User-Agent that works everywhere, and this is not a detail. A bot wall in
# front of a portal refuses a plain client and lets a browser through; an archive API does the
# exact opposite, refusing browser-like agents as scrapers and serving an honest tool string.
# Verified on two hosts on the same day: one served only the browser UA, the other answered 403
# to it and 200 to `curl/8.0`. So: identify honestly first, and only masquerade if refused.
UA_PLAIN = "dataset-acquisition/1.0 (python-urllib)"
UA_BROWSER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/120 Safari/537.36")
TIMEOUT = 60


class HostError(Exception):
    """A host said no, in a way the caller should report rather than crash on."""

    def __init__(self, url: str, status, detail: str):
        super().__init__(detail)
        self.record = {"ok": False, "url": url, "status": status, "verdict": "host_error",
                       "detail": detail, "checked_at": _utc_placeholder()}


def _utc_placeholder() -> str:  # defined before _utc for HostError; kept trivial on purpose
    return datetime.now(timezone.utc).isoformat()

# HTML where data belongs is the signature of a bot wall or a login redirect. Matching the SHAPE
# matters more than matching any one vendor's wording; these markers only sharpen the message.
_WALL_MARKERS = (
    "verification", "checking your browser", "captcha", "cf-browser-verification",
    "attention required", "cloudflare", "enable javascript", "sign in", "log in",
    "access denied", "forbidden",
)


def _req(url: str, data: bytes | None = None, ctype: str | None = None,
         ua: str = UA_PLAIN) -> urllib.request.Request:
    headers = {"User-Agent": ua, "Accept": "application/json, text/csv, */*"}
    if ctype:
        headers["Content-Type"] = ctype
    return urllib.request.Request(url, data=data, headers=headers)


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _open(url: str, data: bytes | None = None, ctype: str | None = None):
    """Open a URL, trying the honest agent first and the browser agent only if refused.

    Raises ``HostError`` rather than a traceback: an agent reading this output needs a verdict it
    can act on, not a stack.
    """
    last = None
    for ua in (UA_PLAIN, UA_BROWSER):
        try:
            return urllib.request.urlopen(_req(url, data, ctype, ua), timeout=TIMEOUT)
        except urllib.error.HTTPError as e:
            last = HostError(url, e.code, f"{e.code} {e.reason} (User-Agent {ua!r})")
            if e.code not in (401, 403, 429):
                raise last            # not an agent-policy refusal; another UA will not help
        except Exception as e:
            raise HostError(url, None, f"{type(e).__name__}: {e}")
    raise last


def _json(url: str, data: bytes | None = None, ctype: str | None = None):
    with _open(url, data, ctype) as r:
        return json.load(r)


# ------------------------------------------------------------------------ classify

def _classify(status: int, ctype: str, head: bytes, url: str) -> dict:
    """Judge a response from its first bytes. Pure: no I/O, so a caller that already opened the
    connection can classify and then keep reading from it."""
    out = {"url": url, "checked_at": _utc()}

    # 202, or any 2xx with an empty body: the archive has not produced the object — staging it
    # out of cold storage, or rationing requests. Not usable, because a caller that treats it as
    # usable writes a zero-byte file and calls it a dataset.
    if status == 202 or (200 <= status < 300 and not head):
        out.update({"ok": False, "status": status, "verdict": "not_ready",
                    "detail": "status %s with an empty body — the archive has not produced the "
                              "file yet" % status,
                    "hint": "wait and retry; requesting harder makes it worse"})
        return out

    text = head.decode("utf-8", errors="replace")
    low = text.lower()
    if low.lstrip().startswith(("<!doctype", "<html")) or "<html" in low[:512]:
        marker = next((m for m in _WALL_MARKERS if m in low), None)
        title = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
        detail = "status %s but the body is HTML" % status
        if marker:
            detail += " containing %r" % marker
        if title:
            detail += " — <title>%s</title>" % title.group(1).strip()
        out.update({"ok": False, "status": status, "verdict": "blocked_html_body",
                    "detail": detail,
                    "hint": "the front door is closed to machines; find the archive copy "
                            "(see references/known_hosts.md)"})
        return out

    out.update({"ok": True, "status": status, "verdict": "usable",
                "content_type": ctype, "body_head": text[:200]})
    return out


def probe(url: str) -> dict:
    """Standalone diagnostic: open, read the head, close.

    ``get``/``columns`` deliberately do NOT call this — they need the response they judged to be
    the one they read from. See ``_open_checked``.
    """
    try:
        r = _open(url)
    except HostError as e:
        return dict(e.record, checked_at=_utc())
    except urllib.error.HTTPError as e:
        return {"url": url, "checked_at": _utc(), "ok": False, "status": e.code,
                "verdict": "http_error", "detail": str(e.reason)}
    except Exception as e:  # DNS, TLS, timeout
        return {"url": url, "checked_at": _utc(), "ok": False, "status": None,
                "verdict": "unreachable", "detail": f"{type(e).__name__}: {e}"}
    with r:
        return _classify(r.status, (r.headers.get("Content-Type") or "").lower(),
                         r.read(4096), url)


# ------------------------------------------------------------------- archive hosts
#
# DataCite indexes datasets across archives — figshare, Zenodo, Dryad, Dataverse, institutional
# repositories — so it is the platform-independent place to start. Verified: a deposit that
# figshare's own search does not return is present in DataCite, with its publisher and landing
# page. Search DataCite for the dataset, take the DOI, then use the publisher's file API.

def _datacite_search(query: str, limit: int) -> list[dict]:
    q = urllib.parse.urlencode({"query": query, "resource-type-id": "dataset",
                                "page[size]": limit})
    rows = (_json("https://api.datacite.org/dois?" + q) or {}).get("data", [])
    out = []
    for x in rows:
        a = x.get("attributes") or {}
        out.append({"doi": a.get("doi"), "publisher": a.get("publisher"),
                    "title": ((a.get("titles") or [{}])[0]).get("title"),
                    "published": str(a.get("publicationYear") or ""),
                    "url": a.get("url")})
    return out


def _datacite_files(doi: str) -> dict:
    """Resolve one DOI to its publisher and landing page, and to a file listing when the
    publisher is one we can read. Otherwise return the landing page — a human-readable answer
    beats a wrong machine one."""
    a = (_json("https://api.datacite.org/dois/" + urllib.parse.quote(doi, safe=""))
         or {}).get("data", {}).get("attributes", {})
    rec = {"host": "datacite", "doi": a.get("doi"), "publisher": a.get("publisher"),
           "title": ((a.get("titles") or [{}])[0]).get("title"), "url": a.get("url")}
    m = re.search(r"(?:figshare|zenodo)\.[^/]*/.*?/(\d+)", str(a.get("url") or ""))
    pub = str(a.get("publisher") or "").lower()
    if m and "figshare" in pub:
        rec["files"] = _figshare_files(m.group(1)).get("files")
    elif m and "zenodo" in pub:
        rec["files"] = _zenodo_files(m.group(1)).get("files")
    else:
        rec["note"] = ("no file adapter for this publisher — open the landing page, or use the "
                       "publisher's own API; the DOI above is the stable handle")
    return rec


def _figshare_search(query: str, limit: int) -> list[dict]:
    payload = json.dumps({"search_for": query, "page_size": limit}).encode()
    rows = _json("https://api.figshare.com/v2/articles/search", data=payload,
                 ctype="application/json")
    return [{"id": a.get("id"), "title": a.get("title"), "doi": a.get("doi"),
             "published": (a.get("published_date") or "")[:10]} for a in rows]


def _figshare_files(entry_id: str) -> dict:
    art = _json(f"https://api.figshare.com/v2/articles/{entry_id}")
    return {"host": "figshare", "id": art.get("id"), "title": art.get("title"),
            "doi": art.get("doi"), "published": (art.get("published_date") or "")[:10],
            "files": [{"name": f.get("name"), "size": f.get("size"),
                       "url": f.get("download_url"), "md5": f.get("computed_md5")}
                      for f in (art.get("files") or [])]}


def _zenodo_search(query: str, limit: int) -> list[dict]:
    url = "https://zenodo.org/api/records?" + urllib.parse.urlencode(
        {"q": query, "size": limit})
    rows = (_json(url) or {}).get("hits", {}).get("hits", [])
    return [{"id": a.get("id"), "title": (a.get("metadata") or {}).get("title"),
             "doi": a.get("doi"),
             "published": ((a.get("metadata") or {}).get("publication_date") or "")[:10]}
            for a in rows]


def _zenodo_files(entry_id: str) -> dict:
    rec = _json(f"https://zenodo.org/api/records/{entry_id}")
    meta = rec.get("metadata") or {}
    return {"host": "zenodo", "id": rec.get("id"), "title": meta.get("title"),
            "doi": rec.get("doi"), "published": (meta.get("publication_date") or "")[:10],
            "files": [{"name": f.get("key"), "size": f.get("size"),
                       "url": (f.get("links") or {}).get("self"),
                       "md5": str(f.get("checksum") or "").replace("md5:", "")}
                      for f in (rec.get("files") or [])]}


_HOSTS = {
    "datacite": (_datacite_search, _datacite_files),
    "figshare": (_figshare_search, _figshare_files),
    "zenodo": (_zenodo_search, _zenodo_files),
}

# Release entries are titled after the PRODUCT, while the FILE NAMES are indexed with the
# entry's content. So a distinctive file name finds release entries that a product-name query
# misses entirely — verified on a real archive where "<Product> Public" returned nothing and the
# file name returned every release with its date.
SEARCH_NOTE = ("start with datacite (cross-archive). If a product-name query returns nothing, "
               "search for a distinctive FILE NAME from the dataset instead")


# ------------------------------------------------------------------------ transfer

def _open_checked(url: str):
    """Open once, judge from the first bytes, hand back the SAME open response.

    Returns ``(response|None, head, verdict)``. A caller with ``verdict["ok"]`` writes ``head``
    and keeps reading ``response``.

    Probe-then-fetch is wrong against an archive that rations requests: the probe spends the
    request that would have succeeded and the fetch gets the refusal. Observed directly — a file
    served 200 to a single request and 202 a minute later to a probe-then-fetch pair.
    """
    try:
        r = _open(url)
    except HostError as e:
        return None, b"", dict(e.record, checked_at=_utc())
    except urllib.error.HTTPError as e:
        return None, b"", {"url": url, "checked_at": _utc(), "ok": False, "status": e.code,
                           "verdict": "http_error", "detail": str(e.reason)}
    except Exception as e:
        return None, b"", {"url": url, "checked_at": _utc(), "ok": False, "status": None,
                           "verdict": "unreachable", "detail": f"{type(e).__name__}: {e}"}
    head = r.read(4096)
    verdict = _classify(r.status, (r.headers.get("Content-Type") or "").lower(), head, url)
    if not verdict["ok"]:
        r.close()
        return None, b"", verdict
    return r, head, verdict


def _open_with_retry(url: str, wait_seconds: int):
    """``_open_checked``, waiting out ``not_ready`` in LONG intervals.

    Requesting harder does not make an archive produce a file sooner and appears to make it
    worse: a file requested every few seconds stayed not-ready for a quarter of an hour, while
    single spaced-out requests to sibling files in the same entry returned bytes immediately.
    Few attempts, far apart.

    A wall, an HTTP error or an unreachable host returns at once — none improve by waiting.
    """
    deadline = time.monotonic() + max(0, wait_seconds)
    r, head, verdict = _open_checked(url)
    delay = 20.0
    while verdict.get("verdict") == "not_ready" and time.monotonic() < deadline:
        time.sleep(min(delay, max(0.0, deadline - time.monotonic())))
        delay = min(delay * 1.5, 60.0)
        r, head, verdict = _open_checked(url)
    if verdict.get("verdict") == "not_ready":
        verdict["hint"] = ("not produced after %ds — normal for a large or cold object, and also "
                           "what rationing looks like; come back later rather than retrying in a "
                           "tight loop" % wait_seconds)
    return r, head, verdict


class _Prefixed(io.RawIOBase):
    """The already-read head, then the rest of the same response.

    Judging a stream costs you its first bytes. Putting them back is what lets a 500 MB matrix be
    judged and read in one request instead of two.
    """

    def __init__(self, head: bytes, rest):
        self._head, self._rest = head, rest

    def readable(self) -> bool:
        return True

    def readinto(self, b) -> int:
        if self._head:
            n = min(len(b), len(self._head))
            b[:n] = self._head[:n]
            self._head = self._head[n:]
            return n
        chunk = self._rest.read(len(b))
        if not chunk:
            return 0
        b[:len(chunk)] = chunk
        return len(chunk)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def get(url: str, dest: str, expect_bytes: int | None = None, expect_md5: str | None = None,
        wait_seconds: int = 300) -> dict:
    """Stream a file to disk, then prove it is the file.

    Refuses an HTML body (a wall, not the dataset) and refuses an empty result — a transfer that
    produced nothing must never report success, because that is how an empty file becomes a
    cited dataset.
    """
    r, head, verdict = _open_with_retry(url, wait_seconds)
    if r is None:
        return {"ok": False, "url": url, "dest": dest, "probe": verdict}
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or ".", exist_ok=True)
    n = 0
    md5 = hashlib.md5()
    with r, open(dest, "wb") as out:
        out.write(head)          # the bytes the judgement was made from
        md5.update(head)
        n += len(head)
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
            md5.update(chunk)
            n += len(chunk)

    problems = []
    if n == 0:
        problems.append("transfer produced 0 bytes")
    if expect_bytes is not None and n != int(expect_bytes):
        problems.append(f"size {n} != expected {expect_bytes}")
    if expect_md5 and md5.hexdigest() != expect_md5:
        problems.append(f"md5 {md5.hexdigest()} != expected {expect_md5}")

    rec = {"ok": not problems, "url": url, "dest": dest, "bytes": n,
           "sha256": _sha256_file(dest), "md5": md5.hexdigest(), "retrieved_at": _utc()}
    if problems:
        rec["errors"] = problems
    return rec


_COL_RE = re.compile(r"^([A-Za-z0-9\-\._]+)\s*\(\d+\)$")


def _col_key(name: str) -> str:
    """Wide matrices often label columns ``SYMBOL (ID)``; match on the symbol."""
    m = _COL_RE.match(name.strip())
    return m.group(1) if m else name.strip()


def columns(url: str, dest: str, keep: list[str], wait_seconds: int = 300) -> dict:
    """Stream a wide CSV, keeping only ``keep`` columns; write long format.

    The point is never to hold the whole matrix. A 500 MB release matrix becomes a few hundred KB
    when you want twenty columns, and nothing large touches the disk.
    """
    r, head, verdict = _open_with_retry(url, wait_seconds)
    if r is None:
        return {"ok": False, "url": url, "dest": dest, "probe": verdict}
    wanted = {k.strip() for k in keep if k.strip()}
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or ".", exist_ok=True)
    kept: list[tuple[int, str]] = []
    row_label, rows_out, first = "row_id", 0, True
    with r, open(dest, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        stream = io.TextIOWrapper(_Prefixed(head, r), encoding="utf-8",
                                  errors="replace", newline="")
        for line in stream:
            if not line.strip():
                continue
            fields = next(csv.reader([line]))
            if first:
                first = False
                row_label = fields[0] or "row_id"
                kept = [(i, _col_key(f)) for i, f in enumerate(fields[1:], start=1)
                        if _col_key(f) in wanted]
                if not kept:
                    return {"ok": False, "url": url, "dest": dest,
                            "error": "none of the requested columns are in the header",
                            "header_sample": [_col_key(f) for f in fields[1:21]]}
                writer.writerow([row_label, "column", "value"])
                continue
            rid = fields[0]
            for i, name in kept:
                if i < len(fields) and fields[i] not in ("", "NA", "NaN", "nan"):
                    writer.writerow([rid, name, fields[i]])
                    rows_out += 1
    found = sorted({name for _, name in kept})
    return {"ok": True, "url": url, "dest": dest, "rows": rows_out, "columns_found": found,
            "columns_missing": sorted(wanted - set(found)), "retrieved_at": _utc()}


def record_provenance(path: str, entry: dict) -> None:
    """Append one line per acquisition. A number nobody can trace to a released version is not
    evidence."""
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ----------------------------------------------------------------------------- cli

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("probe"); s.add_argument("url")

    s = sub.add_parser("search"); s.add_argument("host", choices=sorted(_HOSTS))
    s.add_argument("query"); s.add_argument("--limit", type=int, default=25)

    s = sub.add_parser("files"); s.add_argument("host", choices=sorted(_HOSTS))
    s.add_argument("entry_id", help="archive entry id, or a DOI when host is datacite")

    s = sub.add_parser("get"); s.add_argument("url"); s.add_argument("dest")
    s.add_argument("--expect-bytes", type=int, help="size from the listing; verified")
    s.add_argument("--expect-md5", help="upstream checksum from the listing; verified")
    s.add_argument("--wait", type=int, default=300, help="seconds to wait out a not-ready archive")
    s.add_argument("--provenance")

    s = sub.add_parser("columns"); s.add_argument("url"); s.add_argument("dest")
    s.add_argument("--keep", required=True); s.add_argument("--wait", type=int, default=300)
    s.add_argument("--provenance")

    a = ap.parse_args(argv)
    try:
        out = _dispatch(a)
    except HostError as e:
        out = e.record
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out.get("ok", True) else 1


def _dispatch(a):
    if a.cmd == "probe":
        out = probe(a.url)
    elif a.cmd == "search":
        out = {"host": a.host, "query": a.query, "note": SEARCH_NOTE,
               "results": _HOSTS[a.host][0](a.query, a.limit)}
    elif a.cmd == "files":
        out = _HOSTS[a.host][1](a.entry_id)
    elif a.cmd == "get":
        out = get(a.url, a.dest, expect_bytes=a.expect_bytes, expect_md5=a.expect_md5,
                  wait_seconds=a.wait)
        if a.provenance and out.get("ok"):
            record_provenance(a.provenance, out)
    else:
        out = columns(a.url, a.dest, a.keep.split(","), wait_seconds=a.wait)
        if a.provenance and out.get("ok"):
            record_provenance(a.provenance, out)
    return out


if __name__ == "__main__":
    sys.exit(main())
