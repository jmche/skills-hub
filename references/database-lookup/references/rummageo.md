# RummaGEO (GEO Gene Set Enrichment Search)

## Base URL
```
https://rummageo.com/
```

## Auth
No auth required.

## API Type: GraphQL (not the REST `/api/enrich` shown in older docs)

**Verified 2026-07-15:** `POST /api/enrich` and `GET /api/table` return HTTP
200 with a completely empty body — those REST paths don't exist server-side;
RummaGEO is served by PostGraphile over Postgres, exposing a GraphQL endpoint
at `/graphql`. Confirmed working end-to-end with a live query (see below).

```
POST https://rummageo.com/graphql
Content-Type: application/json
```

### 1. List available backgrounds (species/background IDs needed for enrichment)

```bash
curl -s -X POST "https://rummageo.com/graphql" -H "Content-Type: application/json" \
  -d '{"query":"{ backgrounds { nodes { id species nGeneIds } } }"}'
```

As of 2026-07-15 this returns two backgrounds: `species: "human"` id
`e604830d-62e3-426f-bfd3-1f065f057bfe` (62,237 genes) and
`species: "mouse"` id `c010707b-8f5a-402e-8e5f-19647d78d250` (52,771 genes).
Look these IDs up live rather than hardcoding — they can change when
RummaGEO ships a new release.

### 2. Run enrichment against a gene list (verified working)

```bash
curl -s -X POST "https://rummageo.com/graphql" -H "Content-Type: application/json" \
  -d '{
    "query": "query Enrich($id: UUID!, $genes: [String]) { background(id: $id) { enrich(genes: $genes, first: 5, sortBy: \"pvalue\", sortByDir: \"asc\") { totalCount nodes { nOverlap oddsRatio pvalue adjPvalue geneSet { id term } } } } }",
    "variables": { "id": "e604830d-62e3-426f-bfd3-1f065f057bfe", "genes": ["STAT3","JAK1","JAK2","SOCS3","IL6","IL6R","IL6ST","PTPN11","MYC","BCL2"] }
  }'
```

Live-verified response (truncated): `{"data":{"background":{"enrich":{"totalCount":18214,"nodes":[{"nOverlap":9,"oddsRatio":32.7,"pvalue":8.57e-14,"adjPvalue":1.5e-8,"geneSet":{"id":"...","term":"GSE124636-1-vs-11-human dn"}}, ...]}}}}`.

`enrich` args: `genes` (list of symbols), `first`/`offset` (pagination),
`overlapGe`, `pvalueLe`, `adjPvalueLe` (filters), `sortBy`/`sortByDir`
(`"pvalue"`, `"adjPvalue"`, `"oddsRatio"`, `"nOverlap"`).

### 3. (Optional) Save a gene set first via mutation

If you want a persistent, shareable gene-set ID (as the RummaGEO UI does),
create one before enriching:

```bash
curl -s -X POST "https://rummageo.com/graphql" -H "Content-Type: application/json" \
  -d '{"query":"mutation M($genes: [String], $desc: String) { addUserGeneSet(input: {genes: $genes, description: $desc}) { userGeneSet { id genes description } } }", "variables": {"genes": ["STAT3","JAK1","JAK2","SOCS3","IL6"], "desc": "my gene set"}}'
```

Returns a `userGeneSet.id` (UUID); this step is not required to call
`background(id).enrich(genes)` directly as in step 2.

## Response Format
JSON (standard GraphQL envelope: `{"data": {...}}` or `{"errors": [...]}`).

## Note
POST-only GraphQL endpoint — use `curl` via shell, not WebFetch. Use the
GraphiQL explorer at `https://rummageo.com/graphiql` to develop/test queries
interactively before scripting them.

## Rate Limits
No published limits. Designed for interactive/programmatic use.

## Fallback
If GraphQL access is impractical for a given workflow, GEO's own tools or
the `pathway-enrichment` skill (Enrichr, GSEApy, etc.) cover general gene
set enrichment, though not RummaGEO's GEO-signature-specific background.
