---
name: dataset-acquisition
description: Acquire a public dataset when the project's own portal will not serve a machine — probe response bodies rather than status codes, find the archive host behind a blocked front door, resolve the current release instead of hardcoding one, and record provenance. Use when an analysis needs bulk data files (matrices, releases, supplementary tables) rather than single API facts, or when a documented endpoint returns something that is not the data.
allowed-tools: Read Bash
license: MIT
metadata:
  version: "1.0"
---

# Dataset Acquisition

`database-lookup` queries a documented endpoint for a fact. This skill is for the other case:
you need the **files** — a release matrix, a full table, a supplementary archive — and the
front door is not cooperating.

## The four failures this exists to prevent

Each has been observed in real runs, and each is invisible unless you look for it.

**1. Trusting the status code.** A bot wall answers **200** with an HTML verification page. A
cold-storage archive answers **202** with an empty body. Both read as success to
`curl -o file -w "%{http_code}"`. What follows is an HTML file parsed as JSON, or a zero-byte
file cited as a dataset.

> Read the body. `fetch_dataset.py probe <url>` does this and returns `usable`,
> `blocked_html_body`, `not_ready`, `http_error`, or `unreachable`.

**2. Treating a blocked portal as "the data is unavailable."** The portal is one host. Public
datasets are almost always deposited somewhere built to serve machines — a research archive
(figshare, Zenodo, Dryad), an object store, an institutional mirror, an FTP endpoint, a GEO/SRA
accession. A run that reports "no live API access in this environment" after trying **one** host
has not established that the data is unavailable; it has established that it tried once.

**3. Remembering a version instead of resolving one.** A release number written into a script is
correct on the day it is written and wrong forever after. Worse, a skill or a comment that says
"update as needed" guarantees the version drifts silently.

**4. Downloading the whole matrix.** Release matrices run 150–500 MB. You usually want tens of
columns out of tens of thousands. Streaming and keeping only what you asked for turns 500 MB into
a few hundred KB, and nothing large touches the disk.

## Order of work

### 1. Probe before planning

```bash
python3 scripts/fetch_dataset.py probe "https://<portal>/api/whatever"
```

`ok: false, verdict: blocked_html_body` means the front door is closed **to machines**. This is
not a reason to stop; it is the signal to go to step 2.

`verdict: not_ready` is a different thing entirely: the archive is staging the file out of cold
storage, and your request is what started it. That one only needs time — `get` waits for you.
**Do not poll it hard.** Fast polling does not speed staging up and appears to prolong it; check
again in tens of seconds, a few times. Minutes for a large file is normal, and a run that treats
"still 202" as "unavailable" is throwing away a file that was on its way.

### 2. Find the archive host

```bash
python3 scripts/fetch_dataset.py search figshare "<distinctive file name>"
python3 scripts/fetch_dataset.py search zenodo   "<dataset name> <version>"
```

**Search for a distinctive FILE NAME, not the product name.** Release entries are titled after
the product, but the file names are indexed with the entry's contents — so a file-name query
finds the release entries that a product-name query misses entirely. This is not a quirk of one
archive; it follows from how deposit metadata is indexed.

When the archive's search does not index a host at all (institutional tiers often are not
indexed publicly), entries are still retrievable **by id**:

```bash
python3 scripts/fetch_dataset.py files figshare <entry_id>
```

That returns every file with its `download_url`, size and upstream checksum.

### 3. Resolve the version — do not assume it

List what the archive actually has and sort by publication date. Two things to check before you
pick one:

- **The newest complete release is not always the newest entry.** An archive may carry a partial
  update (one component of a release) published after the last full release. Combining them can
  be correct — say which parts came from which, and why.
- **The machine-reachable mirror may lag the portal.** If the portal advertises a newer release
  than the archive carries, that gap is a fact about your evidence, not a detail to omit.

If a specific version was requested, use that version or fail. Quietly falling back to an older
release is how an analysis ends up describing data it did not use.

### 4. Transfer, and prove what you got

```bash
# whole file, verified against the listing
python3 scripts/fetch_dataset.py get "<download_url>" data/Model.csv \
    --expect-bytes 645696 --expect-md5 <md5> --provenance data/provenance.jsonl

# wide matrix: stream it, keep only the columns you need, write long format
python3 scripts/fetch_dataset.py columns "<download_url>" data/panel.csv \
    --keep GENE_A,GENE_B,GENE_C --provenance data/provenance.jsonl
```

`get` refuses a zero-byte result and verifies size and checksum when you pass them — always pass
them, the listing already told you both. `columns` reports which requested columns were **not**
found rather than silently returning fewer.

Wide matrices often label columns `SYMBOL (ID)`; `columns` matches on the symbol.

### 5. Record provenance

Every acquisition appends one line: host, entry id, DOI, version, publication date, upstream
checksum, locally computed sha256, retrieval time. A number that cannot be traced back to a
released version is not evidence, and the first person to ask "which release is this?" will be a
reviewer, not you.

Record the negative results too — which hosts were tried, what each returned. That is what makes
"this data could not be obtained" a finding rather than an assertion.

## What not to do

- Do not report "no API access in this environment" until you have tried more than one host and
  recorded what each returned.
- Do not hardcode a release identifier in analysis code. Resolve it, then record what you
  resolved.
- Do not accept a downgrade on your own authority. If the analysis was specified against a named
  source or version and you could not obtain it, that is a failure to report, not a limitation to
  absorb into the write-up.
- Do not scrape a JavaScript portal page. If the API behind it is walled, the page is walled too;
  the archive is the answer.

## Host-specific landings

Method is above; the concrete things learned about particular hosts and datasets live in
`references/known_hosts.md`. Add to it whenever you work out a new one — the next run should not
have to rediscover a file id.
