# USPTO Public APIs

## 1. USPTO Open Data Portal — Patent Search (Primary Patent Search)

**Verified 2026-07-15:** PatentsView was absorbed into USPTO's own Open Data
Portal (ODP). Both previously-documented PatentsView hosts are dead:
`api.patentsview.org` returns 410 Gone (already known), and
`search.patentsview.org` now fails DNS resolution entirely (`NXDOMAIN`) —
`patentsview.org` itself redirects to
`https://data.uspto.gov/support/transition-guide/patentsview`. Patent search
now lives directly under USPTO's own API host, `api.uspto.gov`. Confirmed
live via curl: an unauthenticated request to the endpoint below returns
`{"message":"Unauthorized"}` (HTTP 401), and a request with a bogus key
returns `{"message":"Forbidden"}` (HTTP 403) — i.e. the `X-API-KEY` header is
recognized and validated by a real, current endpoint (not a dead domain).

### Base URL

```
https://api.uspto.gov/api/v1/patent
```

**API key required** — register and generate a key ("My Api Key") at
`https://data.uspto.gov` (the Open Data Portal). Docs/getting started:
`https://data.uspto.gov/apis/getting-started`, query syntax reference:
`https://data.uspto.gov/apis/api-syntax-examples`.

Pass as header: `X-API-KEY: YOUR_KEY` (not a query parameter — this is a
change from the old PatentsView `?api_key=` convention).

### Key Endpoints

#### Search patent applications (free-text or field-specific)
```
GET /applications/search?q={query}
```

`q` accepts either a free-text term (searched across all fields) or an
Elasticsearch-style simple query string for field-specific search, e.g.
`applicationMetaData.applicationTypeLabelName:Design`. Spaces and quotes in
`q` must be percent-encoded. Full query DSL: see
`https://data.uspto.gov/documents/documents/ODP-API-Query-Spec.pdf`.

#### Lookup by application number
```
GET /applications/{applicationNumberText}
```

Returns prosecution/status metadata for a specific application — this also
replaces the legacy PEDS use case (see note below).

### Example Calls
```bash
# Keyword search
curl -H "X-API-KEY: ${PATENTSVIEW_API_KEY}" \
  "https://api.uspto.gov/api/v1/patent/applications/search?q=autonomous%20vehicle"

# Field-specific search
curl -H "X-API-KEY: ${PATENTSVIEW_API_KEY}" \
  "https://api.uspto.gov/api/v1/patent/applications/search?q=applicationMetaData.inventorNameText:Tesla"

# Lookup by application number
curl -H "X-API-KEY: ${PATENTSVIEW_API_KEY}" \
  "https://api.uspto.gov/api/v1/patent/applications/16123456"
```

### Rate Limits

Not published for the new ODP API as of this verification; treat conservatively (a few requests/second) and back off on 429s.

### Important Note

The user must have a USPTO ODP API key for this endpoint. If they don't have
one, let them know to register at `https://data.uspto.gov`. Continue loading
the key from `.env` as `PATENTSVIEW_API_KEY` (env var name kept for
continuity even though the issuing system changed).

## 3. PEDS — Patent Examination Data System

**BROKEN as of 2026-07-15 — verified via testing.** `ped.uspto.gov` no
longer resolves (DNS `NXDOMAIN`); this was not a rate-limit/availability
issue, the host is gone. Use the ODP endpoint in section 1 instead —
`GET https://api.uspto.gov/api/v1/patent/applications/{applicationNumberText}`
(same base/auth as the search endpoint above) now covers prosecution
status/filing-date lookups by application number.

**URL** (dead): `https://ped.uspto.gov/api/queries`

**Method**: POST

For patent prosecution data (application status, filing dates, examiner info).

```json
{
  "searchText": "applicationNumberText:16123456",
  "fl": "*",
  "mm": "100%",
  "df": "patentTitle",
  "facet": "false",
  "sort": "applId asc",
  "start": 0
}
```

No API key required but heavily rate limited. Availability can be unreliable.

## 4. TSDR — Trademark Status & Document Retrieval

For trademark lookup by serial or registration number (not full-text search).

```
GET https://tsdr.uspto.gov/documentxml/status/{serial_number}
GET https://tsdr.uspto.gov/documentxml/status/rn{registration_number}
```

Returns XML with mark details, status, owner, goods/services, prosecution history.

No API key. Rate limited. No JSON endpoint — responses are XML.

## 5. Limitations

- **No public REST API for trademark full-text search** (TESS is web-only)
- USPTO ODP API requires registration for an API key
- PEDS is dead (see section 3) — use the ODP application-data endpoint instead
- TSDR requires knowing the serial/registration number already
