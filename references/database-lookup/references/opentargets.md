# Open Targets Platform API

## Base URLs

**GraphQL API (primary, recommended):**
```
https://api.platform.opentargets.org/api/v4/graphql
```

**Important:** The GraphQL endpoint requires HTTP POST with `Content-Type: application/json`. WebFetch (GET-only) will not work — use `curl` via shell instead:
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"{ target(ensemblId: \"ENSG00000157764\") { approvedSymbol approvedName } }"}' \
  https://api.platform.opentargets.org/api/v4/graphql
```

**No REST API.** Open Targets retired its REST API; the platform is GraphQL-only
now (confirmed against the current official docs and by live testing — the old
REST paths and the GraphQL-as-GET shortcut shown in older examples both return
404/500). Always use POST to the GraphQL endpoint above.

## Authentication

No API key required. All endpoints are public.

## Genetics Evidence (GWAS, L2G, Credible Sets)

This reference covers basic target/disease/drug queries only (sections 1-9
below). For GWAS studies, Locus-to-Gene (L2G) causal-gene predictions,
fine-mapped credible sets, or confidence-star ratings, use the dedicated
`opentargets-database` skill instead — it wraps these endpoints with
pagination reconciliation and retry logic that this generic reference does
not implement. Hand-rolling those queries here risks silently incomplete
results.

## GraphQL API

All GraphQL queries are sent as POST requests to the GraphQL endpoint.

```
POST https://api.platform.opentargets.org/api/v4/graphql
Content-Type: application/json

{
  "query": "...",
  "variables": { ... }
}
```

### 1. Target information (by Ensembl Gene ID)

```graphql
query TargetInfo($ensemblId: String!) {
  target(ensemblId: $ensemblId) {
    id
    approvedSymbol
    approvedName
    biotype
    proteinIds {
      id
      source
    }
    tractability {
      label
      modality
      value
    }
    safetyLiabilities {
      event
      effects {
        direction
        dosing
      }
    }
    pathways {
      pathway
      pathwayId
    }
    functionDescriptions
    subcellularLocations {
      location
    }
  }
}
```

**Variables:** `{ "ensemblId": "ENSG00000141510" }`

---

### 2. Disease information (by EFO ID)

```graphql
query DiseaseInfo($efoId: String!) {
  disease(efoId: $efoId) {
    id
    name
    description
    therapeuticAreas {
      id
      name
    }
    synonyms {
      terms
    }
  }
}
```

**Variables:** `{ "efoId": "EFO_0000311" }` (cancer)

---

### 3. Target-Disease associations

```graphql
query Associations($ensemblId: String!, $page: Pagination!) {
  target(ensemblId: $ensemblId) {
    approvedSymbol
    associatedDiseases(page: $page) {
      count
      rows {
        disease {
          id
          name
        }
        score
        datasourceScores {
          id
          score
        }
      }
    }
  }
}
```

**Variables:**
```json
{
  "ensemblId": "ENSG00000141510",
  "page": { "index": 0, "size": 10 }
}
```

---

### 4. Disease-Target associations (from disease side)

```graphql
query DiseaseAssociations($efoId: String!, $page: Pagination!) {
  disease(efoId: $efoId) {
    name
    associatedTargets(page: $page) {
      count
      rows {
        target {
          id
          approvedSymbol
        }
        score
        datasourceScores {
          id
          score
        }
      }
    }
  }
}
```

**Variables:**
```json
{
  "efoId": "EFO_0000311",
  "page": { "index": 0, "size": 10 }
}
```

---

### 5. Evidence for a target-disease pair

```graphql
query Evidence($ensemblId: String!, $efoId: String!, $size: Int!) {
  disease(efoId: $efoId) {
    evidences(ensemblIds: [$ensemblId], size: $size) {
      count
      rows {
        id
        score
        datasourceId
        datatypeId
        literature
        diseaseFromSource
        targetFromSourceId
        resourceScore
        urls {
          niceName
          url
        }
      }
    }
  }
}
```

**Variables:**
```json
{
  "ensemblId": "ENSG00000141510",
  "efoId": "EFO_0000311",
  "size": 10
}
```

---

### 6. Drug/molecule information

```graphql
query DrugInfo($chemblId: String!) {
  drug(chemblId: $chemblId) {
    id
    name
    drugType
    maximumClinicalTrialPhase
    hasBeenWithdrawn
    mechanismsOfAction {
      rows {
        mechanismOfAction
        targets {
          id
          approvedSymbol
        }
      }
    }
    indications {
      rows {
        disease {
          id
          name
        }
        maxPhaseForIndication
      }
    }
    linkedDiseases {
      count
      rows {
        id
        name
      }
    }
    linkedTargets {
      count
      rows {
        id
        approvedSymbol
      }
    }
  }
}
```

**Variables:** `{ "chemblId": "CHEMBL25" }` (aspirin)

---

### 7. Search across targets, diseases, and drugs

```graphql
query Search($queryString: String!, $entityNames: [String!], $page: Pagination!) {
  search(queryString: $queryString, entityNames: $entityNames, page: $page) {
    total
    hits {
      id
      entity
      name
      description
      score
    }
  }
}
```

**Variables:**
```json
{
  "queryString": "BRAF melanoma",
  "entityNames": ["target", "disease", "drug"],
  "page": { "index": 0, "size": 10 }
}
```

---

### 8. Known drugs for a target

```graphql
query KnownDrugs($ensemblId: String!, $size: Int!) {
  target(ensemblId: $ensemblId) {
    approvedSymbol
    knownDrugs(size: $size) {
      count
      rows {
        drug {
          id
          name
          drugType
          maximumClinicalTrialPhase
        }
        disease {
          id
          name
        }
        phase
        status
        mechanismOfAction
        urls {
          niceName
          url
        }
      }
    }
  }
}
```

**Variables:**
```json
{
  "ensemblId": "ENSG00000157764",
  "size": 10
}
```

(ENSG00000157764 = BRAF)

---

### 9. Tractability (druggability)

Included in the target query (see endpoint 1 above). Modalities include:
- `SM` (small molecule)
- `AB` (antibody)
- `PR` (PROTAC)
- `OC` (other clinical)

---

## Key Identifiers

| Entity  | ID Format | Example |
|---------|-----------|---------|
| Target  | Ensembl Gene ID | `ENSG00000141510` (TP53) |
| Disease | EFO/Mondo/HP/Orphanet | `EFO_0000311` (cancer), `MONDO_0007254` |
| Drug    | ChEMBL ID | `CHEMBL25` (aspirin) |

## Datasource IDs (for filtering evidence)

- `ot_genetics_portal` -- Open Targets Genetics
- `eva` -- ClinVar (via EVA)
- `cancer_gene_census` -- COSMIC Cancer Gene Census
- `chembl` -- ChEMBL (clinical trials)
- `europepmc` -- Literature mining
- `expression_atlas` -- Expression Atlas
- `gene2phenotype` -- Gene2Phenotype
- `genomics_england` -- Genomics England PanelApp
- `intogen` -- IntOGen (cancer drivers)
- `ot_crispr` -- Open Targets CRISPR screens
- `progeny` -- PROGENy (pathway activity)
- `reactome` -- Reactome pathways
- `slapenrich` -- SLAPenrich
- `sysbio` -- Systems biology
- `uniprot_literature` -- UniProt literature

## Pagination

GraphQL uses `page: { index: Int, size: Int }` (0-based index).

## Rate Limits

- No API key required.
- Fair-use rate limiting applies. No hard published limit.
- For bulk data, use the Open Targets data downloads (Parquet files on GCS/FTP) rather than API.
- Respect HTTP 429 and `Retry-After` headers.

## Error Format

GraphQL errors:
```json
{
  "errors": [
    {
      "message": "Variable '$ensemblId' expected value of type 'String!' but got: null",
      "locations": [{"line": 1, "column": 7}]
    }
  ]
}
```

## Tips

- Use the GraphQL API for maximum flexibility -- request only the fields you need.
- Always use POST for GraphQL — GET is not supported (verified: returns HTTP 500).
- Combine target + disease queries to get association scores with evidence breakdown.
- Use `datasourceScores` in association queries to see which evidence sources contribute most.
- The Open Targets Platform web UI at `https://platform.opentargets.org` has a GraphQL playground for testing queries.
