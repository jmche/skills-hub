---
name: references
description: 文献/引文/格式/法规簇（references hub）：文献检索（arXiv / bioRxiv / Europe PMC / OpenAlex / PubMed / Semantic Scholar / CORE / Unpaywall / Crossref）、文献综述、 引文管理与 BibTeX、文献格式（Nature/Cell/CONSORT/STROBE/PRISMA）、Zotero 集成、 专利与法规文本（US Fiscal Data / openFDA / 数据库可查性）、文档转换（MarkItDown / liteparse 提取）、并行网络搜索（Exa / parallel-cli / research-lookup）。 触发 = 找文献/查 DOI/引 BibTeX/文献综述/检查引用/专利/法规/提取 PDF 文本/批量获取数据集。 非触发 = 文献观点综合与批判（→research）、出发表级图（→docs-figures）、生物计算（→scientific）。 
---

# references hub

## 判据
- 涉及文献获取、引文格式、专利/法规文本 → 本簇
- 对文献做观点综合/批判 → research
- 查结构化数据库（非文献）→ scientific

## 子技能索引

| 子技能 | 说明 |
|---|---|
| paper-lookup | Search 10 academic literature APIs for papers, preprints, citations, and open-access full text, and return… |
| literature-review | Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed, arXiv,… |
| literature-search-arxiv | > Search for scientific papers, preprints, and publications on arXiv. Extract metadata, abstracts, and… |
| literature-search-biorxiv | > Browse, filter, and download life sciences, biology, and medical preprints from bioRxiv and medRxiv.… |
| literature-search-europepmc | > Search Europe PMC for scientific literature and download open-access full texts and PDFs. Retrieve… |
| literature-search-openalex | > Query the OpenAlex scholarly database for research papers, authors, institutions, topics, sources,… |
| pubmed-database | >- Search PubMed for scientific literature, including published clinical trials. Fetch abstracts and full… |
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
| openfda-database | > Query, search, and download data from the openFDA API for drugs, devices, foods, tobacco, cosmetics, animal… |
| liteparse | Local document and PDF parsing with spatial text and bounding boxes. Use for extracting text from PDFs, DOCX,… |
| markitdown | Convert files and office documents to Markdown. Supports PDF, DOCX, PPTX, XLSX, images (with OCR), audio… |

## 跳簇规则
- 文献内容批判 → research（scientific-critical-thinking）
- 要写综述/论文 → research（scientific-writing）

## 使用方式

1. 按上表选中子技能；2. 读 `skills/references/<name>/INSTRUCTIONS.md`；3. 其内部脚本/资源相对该文件所在目录解析。
