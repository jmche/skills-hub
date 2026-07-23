# gnomAD (Genome Aggregation Database) API Reference

## Overview
gnomAD aggregates exome and genome sequencing data to provide allele frequencies
and variant annotations across diverse populations.

## API Type: GraphQL
- **Endpoint**: `https://gnomad.broadinstitute.org/api`
- **Method**: POST with JSON body containing GraphQL query
- **Auth**: None required (public, unauthenticated)
- **Response format**: JSON (`data` wrapper with GraphQL structure)

## Key Queries

### Variant lookup by variant ID
Variant IDs use format: `{chrom}-{pos}-{ref}-{alt}`, and the coordinates are
build-specific: GRCh38 for `gnomad_r4`/`gnomad_r3`, GRCh37 for `gnomad_r2_1`.

```
POST https://gnomad.broadinstitute.org/api
Content-Type: application/json

{
  "query": "{ variant(variantId: \"1-55516090-C-A\", dataset: gnomad_r4) { variant_id rsids chrom pos ref alt exome { ac an af } genome { ac an af } } }"
}
```

**Warning:** the same `variantId` string means different physical positions
depending on genome build, and gnomAD does **not** reject a build/dataset
mismatch. Querying a GRCh38 variant ID against `gnomad_r2_1` (GRCh37) usually
returns `"data": {"variant": null}` with an `errors: [{"message": "Variant not
found"}]` note -- easy to misread as "this gene/variant has no data" rather
than "you queried the wrong build." Worse, if the raw numeric position happens
to coincide with a *real, different* variant under the other build, gnomAD
returns that unrelated variant's real allele counts with **no error at all**
(verified live: `1-55516888-G-A` against `dataset: gnomad_r4` returns "Variant
not found", but the identical string against `dataset: gnomad_r2_1` silently
returns a real, unrelated GRCh37 variant, `rs527413419`, with populated
`exome` frequencies). Always confirm `chrom`/`pos` in the response match your
intended build, and prefer `gnomad_r4` (GRCh38) or `gnomad_r3` (GRCh38) unless
you specifically need the legacy GRCh37 exome data in `gnomad_r2_1`.

### Gene lookup
```json
{
  "query": "{ gene(gene_symbol: \"BRCA1\", reference_genome: GRCh38) { gene_id symbol chrom start stop strand } }"
}
```

### Variants in a gene
```json
{
  "query": "{ gene(gene_symbol: \"PCSK9\", reference_genome: GRCh38) { variants(dataset: gnomad_r4) { variant_id consequence rsids exome { ac an af } genome { ac an af } } } }"
}
```

### Variants in a region
```json
{
  "query": "{ region(chrom: \"1\", start: 55505222, stop: 55530526, reference_genome: GRCh38) { variants(dataset: gnomad_r4) { variant_id rsids consequence exome { ac af } genome { ac af } } } }"
}
```

### Transcript lookup
```json
{
  "query": "{ transcript(transcript_id: \"ENST00000357654\", reference_genome: GRCh38) { transcript_id gene_id chrom start stop strand } }"
}
```

## Dataset values
- `gnomad_r4` -- gnomAD v4 (GRCh38, latest major release)
- `gnomad_r3` -- gnomAD v3.1.2 (GRCh38, genomes only)
- `gnomad_r2_1` -- gnomAD v2.1.1 (GRCh37, exomes + genomes)

## Population frequency fields
Within `exome` or `genome` objects, population-specific frequencies are available via
`populations { id ac an af }` where `id` values include: `afr`, `amr`, `asj`, `eas`,
`fin`, `mid`, `nfe`, `oth`, `sas`.

## Response example (variant, verified live)
```json
{
  "data": {
    "variant": {
      "variant_id": "1-55516090-C-A",
      "rsids": ["rs1695955"],
      "chrom": "1",
      "pos": 55516090,
      "ref": "C",
      "alt": "A",
      "exome": null,
      "genome": { "ac": 36454, "an": 152076, "af": 0.2397090928220101 }
    }
  }
}
```

## Rate Limits
- No published rate limits, but aggressive querying will be throttled
- Use reasonable request pacing (~1 req/sec recommended)
- For bulk downloads, use gnomAD's Hail tables on Google Cloud or download VCFs

## Notes
- The GraphQL schema is not versioned separately; it tracks the gnomAD web interface
- Use the browser's network inspector on gnomad.broadinstitute.org to discover
  additional query fields and structures
- Structural variants (SV) have a separate query structure (`structural_variant`)
- Constraint metrics (pLI, LOEUF) are available on gene queries via `gnomad_constraint`
