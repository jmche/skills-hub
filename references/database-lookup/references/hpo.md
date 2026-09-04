# HPO (Human Phenotype Ontology)

## Base URLs — two separate services

**Verified 2026-07-15:** the previously documented `/api/hp/hpo/...` path
prefix 404s on every endpoint — there is no `/hpo/` segment. The base domain
(`ontology.jax.org/api/hp`) is correct, but pure-ontology operations
(search/term/hierarchy) and gene/disease annotations live on two different
backend services, confirmed by pulling each service's live OpenAPI spec
(`https://ontology.jax.org/api/hp/ontology-service-hp-0.5.20.yml` and
`https://ontology.jax.org/api/network/ontology-annotation-network-latest.yml`)
and verifying responses with `HP:0001250` (seizure) and `NCBIGene:6323` (SCN1A).

**Ontology term service** (search, term details, hierarchy):
```
https://ontology.jax.org/api/hp
```

**Annotation network service** (genes/diseases linked to a term, and vice versa):
```
https://ontology.jax.org/api/network
```

## Auth
No API key required.

## Note on HP ID formatting
The colon does **not** need URL-encoding against the current API —
`https://ontology.jax.org/api/hp/terms/HP:0001250` works with a literal colon
(verified live). `%3A` also works if you prefer to encode it defensively.

## Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/hp/search?q={query}&page=0&limit={n}` | Search HPO terms by name (`page` and `limit` are both required params) |
| `/api/hp/terms/{id}` | Term details |
| `/api/hp/terms/{id}/children` | Child terms in hierarchy |
| `/api/hp/terms/{id}/parents` | Parent terms |
| `/api/hp/terms/{id}/ancestors` | All ancestor terms |
| `/api/hp/terms/{id}/descendants` | All descendant terms |
| `/api/network/annotation/{id}` | Genes, diseases, assays, medical actions linked to an HP term ID, **or** diseases/phenotypes linked to a `NCBIGene:{id}` gene ID |
| `/api/network/search/{entity}?q={query}&page=0&limit={n}` | Search within an entity type (`entity` = `gene`, `disease`, `hp`, etc.) |

There is no dedicated `/hpo/gene/{id}` or `/hpo/disease/{id}` path anymore —
gene- and disease-side lookups both go through `/api/network/annotation/{id}`,
which infers the entity type from the ID prefix (`HP:...`, `NCBIGene:...`,
`OMIM:...`, `ORPHA:...`).

## Example Calls
```bash
# Search for "seizure"
curl "https://ontology.jax.org/api/hp/search?q=seizure&page=0&limit=5"

# Term details for Seizure
curl "https://ontology.jax.org/api/hp/terms/HP:0001250"

# Parent/child terms
curl "https://ontology.jax.org/api/hp/terms/HP:0001250/parents"
curl "https://ontology.jax.org/api/hp/terms/HP:0001250/children"

# Genes + diseases associated with Seizure
curl "https://ontology.jax.org/api/network/annotation/HP:0001250"

# Diseases (and other annotations) for SCN1A (NCBI Gene 6323)
curl "https://ontology.jax.org/api/network/annotation/NCBIGene:6323"
```

## Response Format
Ontology service: `id`, `name`, `definition`, `synonyms`, `xrefs`. Annotation
network service returns one object with `diseases[]`, `genes[]`, `assays[]`,
`medicalActions[]` arrays (each item has its own `id`/`name`/`mondoId` etc.
depending on entity type) — not a flat list, so check which array is
populated for your query.

## Rate Limits
No published limits. Bulk annotation files at https://hpo.jax.org/data/annotations
