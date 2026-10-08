---
name: references
description: Literature / citation / formatting / regulatory hub: paper search (arXiv / bioRxiv / Europe PMC / OpenAlex / PubMed / Semantic Scholar / CORE / Unpaywall / Crossref), literature review, citation management and BibTeX, manuscript formatting (Nature/ Cell/CONSORT/STROBE/PRISMA), Zotero integration, patents and regulatory text (US fiscal data / openFDA / database availability), document extraction (MarkItDown / liteparse), parallel web search (Exa / parallel-cli / research-lookup). TRIGGER = find papers / look up a DOI / format BibTeX / literature review / check a citation / patents / regulations / extract PDF text / bulk fetch datasets. SKIP = synthesizing or critiquing paper claims (-> research), publication-grade figures (-> docs-figures), bio-computation (-> scientific). 
---

# references hub

## Routing rules
- Paper retrieval, citation formatting, patents / regulatory text -> this hub
- Synthesizing or critiquing claims INSIDE papers -> research
- Querying structured databases (non-literature) -> scientific

## Sub-skill index

| skill | description |
|---|---|
| paper-lookup | Searches 18 scholarly APIs for papers, preprints, citations, open-access full text, repository records, and… |
| literature-review | Conducts systematic, scoping, and narrative literature reviews using PubMed, arXiv, bioRxiv, Semantic… |
| literature-search-arxiv | Search for scientific papers, preprints, and publications on arXiv. Extract metadata, abstracts, and download… |
| literature-search-biorxiv | Browse, filter, and download life sciences, biology, and medical preprints from bioRxiv and medRxiv. Supports… |
| literature-search-europepmc | Search Europe PMC for scientific literature and download open-access full texts and PDFs. Retrieve full-text… |
| literature-search-openalex | Query the OpenAlex scholarly database for research papers, authors, institutions, topics, sources,… |
| pubmed-database | Search PubMed for scientific literature, including published clinical trials. Fetch abstracts and full text.… |
| research-lookup | "Compiles current scholarly evidence for a scientific manuscript or research brief when the user explicitly… |
| exa-search | "Searches scientific and technical web content with Exa and extracts page or PDF text from URLs in batches.… |
| parallel-web | "Uses Parallel CLI for web search, URL extraction, deep research, structured data enrichment, entity… |
| database-lookup | Queries documented public database APIs with explicit endpoints, filters, pagination, and provenance. Used… |
| dataset-acquisition | Acquire a public dataset when the project's own portal will not serve a machine — probe response bodies… |
| citation-management | Comprehensive citation management for academic research. Search OpenAlex, PubMed, and Google Scholar for… |
| venue-templates | Prepares journal manuscripts, conference papers, research posters, and grant documents using venue-specific… |
| pyzotero | Manages Zotero reference libraries using the pyzotero Python client: retrieves, creates, updates, and deletes… |
| open-notebook | Organizes research with the self-hosted Open Notebook alternative to NotebookLM. Supports source ingestion… |
| usfiscaldata | Queries the U.S. Treasury Fiscal Data REST API for federal financial data. No API key required. Use for… |
| openfda-database | Query, search, and download data from the openFDA API for drugs, devices, foods, tobacco, cosmetics, animal… |
| liteparse | Local document and PDF parsing that returns spatial text with bounding boxes. Use for extracting text from… |
| markitdown | Converts heterogeneous documents and selected URIs to Markdown with Microsoft MarkItDown for text analysis,… |

## Cross-hub handoff
- Critiquing literature's claims -> research (scientific-critical-thinking)
- Writing a review or manuscript -> research (scientific-writing)

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
