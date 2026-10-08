# DISGENET — Gene/variant–disease associations

Use the current [DISGENET documentation](https://www.disgenet.com/docs) and
[API/tools page](https://www.disgenet.com/Tools). The old disgenet.org API and
email/password login recipes are not the current integration contract.

Access is plan-dependent: the [Academic plan](https://www.disgenet.com/Plans)
exposes the curated subset; full-dataset API access requires an appropriate
subscription. Obtain a key from the account dashboard before running requests.
The base URL and endpoint shapes are listed under "API base and endpoints"
below; they come from the public OpenAPI spec, and authenticated responses were
not exercised.

For a reproducible retrieval, choose gene–disease (GDA) or variant–disease (VDA),
resolve the input identifier, and save source filters, release, evidence rows,
PMIDs, score fields and pagination metadata. Summary rows aggregate evidence;
inspect supporting evidence before making a mechanistic claim.

[Current score guidance](https://support.disgenet.com/support/solutions/articles/202000100283-what-are-the-gda-score-vda-score-disgenet-score-)
removes the former cap at 1. Do not treat the raw DISGENET score as a probability,
clamp it to [0,1], or confuse it with a normalized score. DSI measures disease
specificity and DPI pleiotropy; neither is causal evidence.

## API base and endpoints

```
https://api.disgenet.com/api/v1
```

`disgenet.org` redirects to the `disgenet.com` web app; the API is served from
the `api.disgenet.com` subdomain. An unauthenticated request there returns a JSON
auth error (`"Missing or invalid API Key"`, HTTP 401). The OpenAPI spec is
readable without login at `https://api.disgenet.com/v2/api-docs`. The endpoint
shapes below come from that spec; authenticated responses were not exercised.

Pass the key as `Authorization: Bearer <token>`; load it from `.env` as
`DISGENET_API_KEY`. Identifiers are query parameters, not path segments.

| Endpoint | Description |
|----------|-------------|
| `/gda/summary` | Gene-disease associations |
| `/gda/evidence` | Evidence-level GDA data |
| `/vda/summary` | Variant-disease associations |
| `/vda/evidence` | Evidence-level VDA data |
| `/entity/gene`, `/entity/disease`, `/entity/variant` | Entity lookup/resolution |
| `/enrichment/gene` | Gene set disease-enrichment |

Parameters on `/gda/summary` and `/vda/summary`:
- `gene_ncbi_id`, `gene_ensembl_id`, `gene_symbol` — up to 100 comma-separated
- `disease` — vocabulary-prefixed ID, e.g. `UMLS_C0006142`, `MONDO_...`, `OMIM_...`
- `variant` — dbSNP rsID (on `/vda/summary`)
- `source` — e.g. `CURATED`, `CLINVAR`, `CLINGEN`, `ALL`
- `min_score` / `max_score`, `min_ei` / `max_ei` — score and evidence-index bounds
- `page_number` — pagination

```bash
# Gene-disease for TP53 (NCBI gene ID 7157)
curl -H "Authorization: Bearer ${DISGENET_API_KEY}" \
  "https://api.disgenet.com/api/v1/gda/summary?gene_ncbi_id=7157&source=CURATED"

# Variant-disease for rs1042522
curl -H "Authorization: Bearer ${DISGENET_API_KEY}" \
  "https://api.disgenet.com/api/v1/vda/summary?variant=rs1042522"
```
