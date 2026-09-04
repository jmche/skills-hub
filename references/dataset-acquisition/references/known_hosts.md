# Known hosts and landings

Concrete facts worked out on real runs. The method is in `SKILL.md` and does not depend on
anything here; this file exists so nobody has to rediscover a file id.

**Add to it when you work one out.** One entry: what was wanted, which host served it, what the
identifiers are, and what surprised you.

---

## figshare

**API** — `https://api.figshare.com/v2`, no authentication.

| what | call |
|---|---|
| search | `POST /articles/search` with `{"search_for": "...", "page_size": N}` |
| entry + files | `GET /articles/{id}` → `files[].{name,size,download_url,computed_md5}` |
| file list only | `GET /articles/{id}/files?page_size=200` |

**Search does not index every tier.** Institutional deposits (figshare+, DOI prefix `10.25452`)
are absent from `articles/search` results but retrieve normally by id. If you know a dataset is
on figshare and search returns nothing, the entry id is still worth trying directly.

**Search by file name, not product name.** Verified: `"<Product> Public"` returned unrelated
papers; `"<a file name from the release>"` returned every release entry with its publication
date, in one call.

**Downloads stage on first request and answer `202 Accepted` meanwhile.**
`ndownloader.figshare.com/files/{id}` returns **202 with an empty body** for a file that is not
staged; the request itself is what starts the staging. Once the object is ready it 302s to a
presigned object-store URL (`s3-*.amazonaws.com/pstorage-...`) and serves the bytes.

Three things learned the hard way:

- **It is not a client or header problem.** Four different header sets (including a bare request
  with no custom headers) all returned 202 while the file was cold and all returned 200 once it
  was warm. Chasing this by switching from `urllib` to `requests` proves nothing — a `requests`
  call that "worked" had simply arrived after a dozen earlier requests finished the staging.
- **Do not poll fast.** A file polled every three seconds sat at 202 for fifteen minutes, while an
  untouched sibling file in the same entry served on its first request. Trigger once, then check
  again in tens of seconds, a few times.
- **Warm does not stay warm.** A file that served immediately was back to 202 later. Fetch what you
  need in the same pass rather than assuming a second visit is cheap.

## Zenodo

**API** — `https://zenodo.org/api`, no authentication.
`GET /records?q=...&size=N&sort=mostrecent`, then `GET /records/{id}` →
`files[].{key,size,checksum,links.self}`.

---

## Cancer Dependency Map (DepMap)

**The portal is closed to machines.** Every `depmap.org/portal/...` endpoint tried returns
**HTTP 200 with an HTML page titled `DepMap — Verification`** — a bot wall that a status-code
check reads as success:

```
200  https://depmap.org/portal/api/download/files
200  https://depmap.org/portal/download/api/downloads
200  https://depmap.org/portal/api/download/all
200  https://depmap.org/portal/download/all/
```

**Releases are on figshare.** Search `CRISPRGeneEffect` (a file name present in every release):

| release | figshare id | published |
|---|---|---|
| 24Q4 Public | `27993248` | 2024-12-10 |
| 24Q2 Public | `25880521` | 2024-05-23 |
| 23Q4 Public | `24667905` | 2023-12-19 |
| 23Q2 Public | `22765112` | 2023-06-02 |
| 22Q4 Public | `21637199` | 2022-12-07 |

`27993248` = *DepMap 24Q4 Public*, DOI `10.25452/figshare.plus.27993248.v1`, **73 files**. It is
the newest **complete** release on figshare — checked 2026-07-31. The portal advertises newer
releases; the archive does not carry them, and that gap belongs in your provenance.

**A partial newer entry exists.** `31660582` = *Chronos parameters (Public 26Q1)*, DOI
`10.6084/m9.figshare.31660582.v1`, published 2026-03-11 — **5 files only** (`t0_offset.csv`,
`library_effect.csv`, `guide_efficacy.csv`, …). These are Chronos model parameters, not a release.
A run that used them paired them with `Model.csv` from 24Q4 for row annotation. If you do that,
say so: two versions in one analysis is a fact about the analysis.

Useful files in a full release, by size class:

- small, take whole: `Model.csv` (~0.6 MB, cell-line metadata), `ScreenSequenceMap.csv`,
  `CRISPRScreenMap.csv`, `OmicsProfiles.csv`, `OmicsDefaultModelProfiles.csv`,
  `CRISPRInferredCommonEssentials.csv`, `PortalCompounds.csv`
- wide, stream with `columns`: `CRISPRGeneEffect.csv` (~429 MB), `CRISPRGeneDependency.csv`,
  `ScreenGeneEffect.csv`, `OmicsExpressionProteinCodingGenesTPMLogp1.csv` (~507 MB),
  `OmicsSomaticMutationsMatrixDamaging.csv`, `OmicsSomaticMutationsMatrixHotspot.csv`

Gene columns are labelled `SYMBOL (ENTREZ)`; `columns` already matches on the symbol.
`ScreenGeneEffect.csv` + `ScreenSequenceMap.csv` give per-screen, library-resolved gene effect —
that is what makes a cross-library concordance check possible.

---

## Sources that answered normally

Checked 2026-07-31, plain `GET`, no wall: `api.crossref.org`, `clinicaltrials.gov`,
`eutils.ncbi.nlm.nih.gov`, `api.figshare.com`, `zenodo.org/api`, `www.cbioportal.org/api`.

A portal being walled says nothing about its neighbours — probe each one rather than concluding
that "this environment has no network access to databases."
