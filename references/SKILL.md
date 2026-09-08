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
| paper-lookup | Search 10 academic literature APIs for papers, preprints, citations, and open-access full text, and return… |
| literature-review | Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed, arXiv,… |
| literature-search-arxiv | Search for scientific papers, preprints, and publications on arXiv. Extract metadata, abstracts, and download… |
| literature-search-biorxiv | Browse, filter, and download life sciences, biology, and medical preprints from bioRxiv and medRxiv. Supports… |
| literature-search-europepmc | Search Europe PMC for scientific literature and download open-access full texts and PDFs. Retrieve full-text… |
| literature-search-openalex | Query the OpenAlex scholarly database for research papers, authors, institutions, topics, sources,… |
| pubmed-database | Search PubMed for scientific literature, including published clinical trials. Fetch abstracts and full text.… |
| research-lookup | 'Look up current research and scientific information across three backends: fast web search via parallel-cli… |
| exa-search | "Web toolkit powered by Exa, tuned for scientific and technical content. Use this skill when the user needs… |
| parallel-web | "All-in-one web toolkit powered by parallel-cli, with a strong emphasis on academic and scientific sources.… |
| database-lookup | Query documented public database APIs with explicit endpoints, filters, pagination, and provenance. Use when… |
| dataset-acquisition | Acquire a public dataset when the project's own portal will not serve a machine — probe response bodies… |
| citation-management | Comprehensive citation management for academic research. Search Google Scholar and PubMed for papers, extract… |
| venue-templates | Access comprehensive LaTeX templates, formatting requirements, and submission guidelines for major scientific… |
| pyzotero | Interact with Zotero reference management libraries using the pyzotero Python client. Retrieve, create,… |
| open-notebook | Self-hosted, open-source alternative to Google NotebookLM for AI-powered research and document analysis. Use… |
| usfiscaldata | Query the U.S. Treasury Fiscal Data REST API for federal financial data. No API key required. Use for… |
| openfda-database | Query, search, and download data from the openFDA API for drugs, devices, foods, tobacco, cosmetics, animal… |
| liteparse | Local document and PDF parsing with spatial text and bounding boxes. Use for extracting text from PDFs, DOCX,… |
| markitdown | Convert files and office documents to Markdown. Supports PDF, DOCX, PPTX, XLSX, images (with OCR), audio… |

## Cross-hub handoff
- Critiquing literature's claims -> research (scientific-critical-thinking)
- Writing a review or manuscript -> research (scientific-writing)

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
