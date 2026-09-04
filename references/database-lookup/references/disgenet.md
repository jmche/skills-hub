# DisGeNET (Gene-Disease Associations)

## Base URL
```
https://api.disgenet.com/api/v1
```

**Verified 2026-07-15:** `disgenet.org` now 308-redirects to `disgenet.com`,
which serves the React web app (HTML) at its root — not the API. The real API
lives on a dedicated subdomain, `api.disgenet.com`, confirmed live via curl:
unauthenticated requests return a clean JSON auth error
(`{"status":"BAD_REQUEST","payload":{"details":"UNAUTHORIZED","message":"Missing or invalid API Key"},"httpStatus":400}`),
not a 404 or an HTML page — i.e. this is a normal auth wall on a real,
current endpoint. Live OpenAPI spec: `https://api.disgenet.com/v2/api-docs`
(no login required to fetch the spec itself, despite the human-readable
Swagger UI at `api.disgenet.com/doc/swagger` requiring account login).

Path structure also changed: there is no more `/gda/gene/{id}` /
`/gda/disease/{id}` REST-path style. Identifiers are now **query parameters**
on a smaller set of endpoints (`/gda/summary`, `/vda/summary`, etc.).

## Auth
**API key required.** The old email/password → token POST flow
(`disgenet.org/api/auth/`) is gone; that path now 401s. Keys are now issued
from your account dashboard at `https://disgenet.com` (no self-serve POST
auth endpoint found). Pass the key as:
```
Authorization: Bearer <token>
```
Load token from `.env` as `DISGENET_API_KEY`.

## Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/gda/summary` | Gene-disease associations (query params, not path segments) |
| `/gda/evidence` | Evidence-level GDA data |
| `/vda/summary` | Variant-disease associations |
| `/vda/evidence` | Evidence-level VDA data |
| `/entity/gene` | Gene entity lookup/resolution |
| `/entity/disease` | Disease entity lookup/resolution |
| `/entity/variant` | Variant entity lookup/resolution |
| `/enrichment/gene` | Gene set disease-enrichment |

## Parameters (on `/gda/summary`, `/vda/summary`)
- `gene_ncbi_id`, `gene_ensembl_id`, `gene_symbol` — up to 100 comma-separated
- `disease` — vocabulary-prefixed ID, e.g. `UMLS_C0006142`, `MONDO_...`, `OMIM_...`, `HPO_HP:...` (see full prefix list in the spec)
- `variant` — dbSNP rsID (on `/vda/summary`)
- `source` — array, e.g. `CURATED`, `CLINVAR`, `CLINGEN`, `ALL`
- `min_score` / `max_score` — GDA/VDA score threshold (0-1)
- `min_ei` / `max_ei` — evidence index threshold
- `page_number` — pagination

## Example Calls
```bash
# Gene-disease for TP53 (NCBI gene ID 7157)
curl -H "Authorization: Bearer ${DISGENET_API_KEY}" \
  "https://api.disgenet.com/api/v1/gda/summary?gene_ncbi_id=7157&source=CURATED&min_score=0.3"

# Disease-gene for Breast Cancer (UMLS CUI C0006142)
curl -H "Authorization: Bearer ${DISGENET_API_KEY}" \
  "https://api.disgenet.com/api/v1/gda/summary?disease=UMLS_C0006142"

# Variant-disease for rs1042522
curl -H "Authorization: Bearer ${DISGENET_API_KEY}" \
  "https://api.disgenet.com/api/v1/vda/summary?variant=rs1042522"
```

## Rate Limits
Free academic tier: ~few hundred requests/day. Paid tiers available.

## Free alternative
If no API key: use **Open Targets** for disease-gene associations.
