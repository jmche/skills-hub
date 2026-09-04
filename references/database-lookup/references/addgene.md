# Addgene (Plasmid Repository)

## Base URL
```
https://api.developers.addgene.org
```

**Verified 2026-07-15:** the old `www.addgene.org/api/` path documented below is
gone (404 on everything, including bare `/api/`). Addgene relaunched API access
under a separate "Developers Portal" with a new domain and new paths. Confirmed
live via curl: unauthenticated requests to the new domain return a normal JSON
auth challenge (`{"detail":"Authentication credentials were not provided."}`,
HTTP 401), not a 404 — i.e. the domain and routes below are real and current.
Full spec: `https://docs.developers.addgene.org/docs/` (OpenAPI source at
`https://api.developers.addgene.org/docs/schema/`).

## Auth
API key required, and access is **gated by manual approval** (not instant
self-service): request an access token at `https://developers.addgene.org/`
(log in, request a scope, accept the data license). Addgene states review
takes up to 5 business days.

Pass as: `Authorization: Token <your_api_key>` (same header format as before).

Load from `.env` as `ADDGENE_API_KEY`.

## Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/catalog/plasmid/{id}/` | Get plasmid details by Addgene ID |
| `/catalog/plasmid/` | List/search plasmids — filter via query params (see below) |
| `/catalog/plasmid-with-sequences/{id}/` | Plasmid details including sequence data |
| `/catalog/viral-prep/{id}/` | Viral prep details by ID |
| `/catalog/viral-prep/` | List/search viral preps |
| `/download/plasmids/` | Bulk JSON export of all plasmids (refreshed daily) |
| `/download/plasmids_with_sequences/` | Bulk JSON export including sequences |
| `/download/genbank/{id}/` | GenBank file for a plasmid |
| `/auth/test/` | Verify your token is valid |

`/catalog/plasmid/` list search accepts: `name`, `genes`, `gene_ids`, `pis`,
`pi_id`, `article_authors`, `article_title`, `article_pmid`, `article_so`,
`article_published`, `backbone`, `bacterial_resistance`, `resistance_marker`,
`cloning_method`, `expression`, `plasmid_type`, `vector_types`, `promoters`,
`species`, `mutations`, `tags`, `purpose`, `experimental_use`,
`catalog_item_id`, `material_code`, `is_industry`, `first_available_time`,
`sort_by`, `page`, `page_size`. There is no separate `/depositors/` or
`/articles/` endpoint anymore — depositor (`pis`/`pi_id`) and publication
(`article_*`) fields are query filters on `/catalog/plasmid/` itself.

## Example Calls
```bash
# Get plasmid details (e.g., pSpCas9, Addgene ID 12260)
curl -H "Authorization: Token ${ADDGENE_API_KEY}" \
  https://api.developers.addgene.org/catalog/plasmid/12260/

# Search plasmids by name
curl -H "Authorization: Token ${ADDGENE_API_KEY}" \
  "https://api.developers.addgene.org/catalog/plasmid/?name=GFP"
```

## Response Format
JSON with plasmid name, backbone, inserts, resistance markers, depositor (PI), sequences, publications.

## Rate Limits
No published limits. Reasonable use expected.

## No API key / not yet approved
If the user has no Addgene API key and can't wait for approval, there is no
public unauthenticated alternative for structured plasmid metadata — fall back
to a targeted web search/fetch of the plasmid's page at
`https://www.addgene.org/{addgene_id}/` (the web UI itself works fine and is
not gated), or point the user to the bulk data download options at
`https://developers.addgene.org/access-options/` if they need many records.
