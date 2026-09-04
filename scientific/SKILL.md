---
name: scientific
description: 生物/化学/医学计算簇（scientific hub）：结构预测与序列设计（AlphaFold2/Boltz/Chai-1/ ESMFold2/ESMFold/OpenFold3/Pymol/MD）、序列与基因组工具（Biopython/Clustal Omega/ IQ-TREE/ETE）、30+ 数据库查询（UniProt/Ensembl/PDB/PubChem/ChEMBL/gnomAD/clinVar/ DepMap/1000Genomes/STRING/Reactome/KEGG-JASPAR/QuickGO…）、单细胞与转录组（Scanpy/ anndata/scvi-tools/cellxgene-census/scVelo/bulk RNA-seq/DESeq2/DEEPTools/GRN/ 通路富集/geniml/gtars/pysam/TileDB-VCF）、临床医学（CDS/临床报告/适应症综述/ ISO13485/治疗方案/PyHealth/影像 BIDS/病理 WSI/神经电生理）、化学与药物发现 （RDKit/datamol/medchem/molfeat/DeepChem/TorchDrug/PyOpenMS/COBRA/DiffDock/ 材料 pymatgen）、实验室与云平台集成（Benchling/LabArchive/DNAnexus/LatchBio/ Ginkgo/Opentrons/pylabrobot/protocols.io/Nextflow/pacsomatic）、量子与通用模拟 （Qiskit/cirq/PennyLane/QuTiP/SimPy/PyMC/Astropy/FluidSim/MATLAB）。 触发 = 蛋白质折叠/查 UniProt PDB ChEMBL/跑 Scanpy/跑 RNA-seq/Dock 分子/写 Opentrons 协议/ 查基因变异/跑分子动力学/查结构相似性/GRN/单细胞/药物分子。 非触发 = 统计方法论与假说设计（→research）、找文献与引文（→references）、 通用 ML 框架（transformers/polars/pytorch-lightning →data-ml）、 发表级图与幻灯片（→docs-figures）、UI 工程与 GPU 云（→dev）。 
---

# scientific hub

## 判据
- 目标 = 跑具体生物计算 / 查具体数据库 / 结构预测 / 分子设计 → 本簇
- 目标是方法论层面（实验设计、统计推断、假说）→ research
- 文献查找/引文/专利/法规文本 → references
- 纯通用数据与 ML 库（无生物领域色彩）→ data-ml
- 发表级出图/幻灯片/海报 → docs-figures

## 子技能索引

### A 结构预测与序列设计

| 子技能 | 说明 |
|---|---|
| alphafold2 | > Predict protein structure for monomers and multimers with AlphaFold2 via the ColabFold runner (Mirdita et… |
| alphafold-database-fetch-and-analyze | > Retrieve and analyze AlphaFold predicted structures for a protein. Use when the user provides a specific… |
| boltz | > Structure prediction for protein, nucleic-acid, and small-molecule complexes with Boltz-2 (Passaro &… |
| chai1 | > Structure prediction for protein, nucleic-acid, and small-molecule complexes with the Chai-1 foundation… |
| esm | Use when working directly with the `esm` Python SDK, ESM3 or ESMC model IDs, Forge/Biohub inference clients,… |
| esmfold2 | > Biohub ESMFold2 / ESMFold2-Fast all-atom co-folding (Candido et al. 2026, github.com/Biohub/esm).… |
| openfold3 | > Structure prediction using OpenFold3, an open-weights PyTorch reproduction of AlphaFold3 from the… |
| foldseek-structural-search | > Performs 3D structural searches of proteins against various databases (PDB, AlphaFold, CATH, MGnify, etc.)… |
| pymol | > Visualize, analyze, and render protein and molecular structures using PyMOL. Use when the user wants to… |
| molecular-dynamics | Run and analyze molecular dynamics simulations with OpenMM and MDAnalysis. Set up protein/small molecule… |
| glycoengineering | Analyze and engineer protein glycosylation. Scan sequences for N-glycosylation sequons (N-X-S/T), predict… |
| solublempnn | > Inverse-fold a backbone with SolubleMPNN — ProteinMPNN retrained on a soluble-PDB subset (Dauparas et al.… |
| ligandmpnn | > Inverse-fold a backbone with ligand, nucleic-acid, and metal context using LigandMPNN (Dauparas et al.… |
| proteinmpnn | > Inverse-fold a protein backbone (PDB structure) into amino-acid sequence with ProteinMPNN (Dauparas et al.… |
| diffdock | DiffDock and DiffDock-L molecular docking. Use for protein-small-molecule pose prediction from PDB or… |
| tamarind | Access a collection of open-source molecular design and structural biology tools on the Tamarind Bio… |
| rowan | Rowan is a cloud-native molecular modeling and medicinal-chemistry workflow platform with a Python API. Use… |
| adaptyv | "How to use the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results… |

### B 序列与基因组工具

| 子技能 | 说明 |
|---|---|
| biopython | Comprehensive molecular biology toolkit. Use for sequence manipulation, file parsing (FASTA/GenBank/PDB),… |
| gget | "Fast CLI/Python queries to 20+ bioinformatics databases. Use for quick lookups: gene info, BLAST/BLAT, viral… |
| bioservices | Unified Python interface to 40+ bioinformatics services. Use when querying multiple databases (UniProt, KEGG,… |
| ncbi-sequence-fetch | > Retrieve protein and nucleotide sequences from NCBI databases using E-utilities. Supports direct accession… |
| protein-sequence-msa | > Performs multiple sequence alignment of proteins with EBI Clustal Omega. Use when you need to align… |
| protein-sequence-similarity-search | > Searches for homologous protein sequences using MMseqs2 (fast, default) or BLAST (comprehensive, fallback).… |
| phylogenetics | Build and analyze phylogenetic trees using MAFFT (multiple alignment), IQ-TREE 2 (maximum likelihood), and… |
| etetoolkit | Phylogenetic tree toolkit (ETE). Tree manipulation (Newick/NHX), evolutionary event detection,… |
| scikit-bio | Biological data toolkit. Sequence analysis, alignments, phylogenetic trees, diversity metrics (alpha/beta,… |

### C 数据库查询

| 子技能 | 说明 |
|---|---|
| uniprot-database | >- Access protein metadata, function, taxonomy, and sequences across UniProtKB, UniParc, and UniRef. Use when… |
| ensembl-database | > Query the Ensembl database to resolve gene, transcript, and protein IDs, fetch genomic or protein… |
| pdb-database | > Use when you want to search for or download experimentally-determined 3D structures for biomolecules… |
| pubchem-database | > Query PubChem, search by name/CID/SMILES, retrieve properties, similarity/substructure searches,… |
| chembl-database | > Query the ChEMBL database for bioactive molecules, drug targets, bioactivity data, approved drugs, and… |
| gnomad-database | > Query the Genome Aggregation Database (gnomAD). Use when determining the rarity or allele frequency of… |
| onekgpd | > Query the 1000 Genomes Project dataset (3,202 whole-genome-sequenced individuals, GRCh38) at the level of… |
| dbsnp-database | > Use when you want to look up, map, and search for short genetic variants (SNPs, indels) in NCBI's dbSNP… |
| clinvar-database | > Use when needing clinical significance, pathogenicity classifications (e.g., Pathogenic, Benign, VUS),… |
| depmap | Query the Cancer Dependency Map (DepMap) for cancer cell line gene dependency scores (CRISPR Chronos), drug… |
| opentargets-database | > Query Open Targets Platform for target-disease associations, drug target discovery, tractability/safety… |
| primekg | Query the Precision Medicine Knowledge Graph (PrimeKG) for multiscale biological data including genes, drugs,… |
| string-database | > Query the STRING database for protein-protein interactions (PPIs), functional enrichment, and homology. Use… |
| embl-ebi-ols | > Query and search the EMBL-EBI Ontology Lookup Service (OLS) for biomedical ontology terms, definitions, and… |
| encode-ccres-database | > Query the ENCODE Registry of cis-Regulatory Elements (cCREs) via the SCREEN GraphQL API, or make custom… |
| interpro-database | > Identify domains, families, and sites in proteins; find all proteins in a family or sharing a domain;… |
| jaspar-database | > Query the JASPAR database for Transcription Factor (TF) binding profiles. Use when retrieving Position… |
| quickgo-database | > Query the QuickGO and Evidence & Conclusion Ontology (ECO) REST API. Use this when you need to map genes to… |
| reactome-database | > Query the Reactome database (Analysis and Content Services). Use when the user asks about pathway analysis,… |
| ucsc-conservation-and-tfbs | > Fetch Evolutionary Conservation scores (phyloP, phastCons) and Transcription Factor Binding Sites (TFBS)… |
| unibind-database | >- Queries the UniBind database for experimentally validated transcription factor (TF) binding sites. Use… |
| alphagenome-single-variant-analysis | > Analyzes genetic variant effects on gene expression (RNA-seq), chromatin accessibility (DNASE), histone… |
| clinical-trials-database | > Query ClinicalTrials.gov via APIv2. Use when you want to search for trials by condition, drug, location,… |
| gtex-database | > Use when you want to retrieve quantitative RNA expression data and variant eQTL information from the GTEx… |
| human-protein-atlas-database | > Use when you want to retrieve semi-quantitative protein expression and spatial localisation data from the… |

### D 单细胞与转录组

| 子技能 | 说明 |
|---|---|
| scanpy | Standard single-cell RNA-seq analysis pipeline. Use for QC, normalization, dimensionality reduction… |
| anndata | Data structure for annotated matrices in single-cell analysis. Use when working with .h5ad files or… |
| scvi-tools | Deep generative models for single-cell omics. Use when you need probabilistic batch correction (scVI),… |
| cellxgene-census | Query the CZ CELLxGENE Census programmatically for versioned public single-cell and spatial transcriptomics… |
| scvelo | RNA velocity analysis with scVelo. Estimate cell state transitions from unspliced/spliced mRNA dynamics,… |
| bulk-rnaseq | End-to-end bulk RNA-seq orchestrator — takes raw FASTQ reads through QC and trimming (FastQC, fastp/Trim… |
| pydeseq2 | Differential gene expression analysis for bulk RNA-seq with PyDESeq2, including formulaic designs, Wald… |
| deeptools | NGS analysis toolkit. BAM to bigWig conversion, QC (correlation, PCA, fingerprints), heatmaps/profiles (TSS,… |
| arboreto | Infer gene regulatory networks (GRNs) from gene expression data using scalable algorithms (GRNBoost2,… |
| pathway-enrichment | Run pathway and gene-set enrichment analysis on gene lists or ranked gene data, then interpret the results.… |
| geniml | This skill should be used when working with genomic interval data (BED files) for machine learning tasks. Use… |
| gtars | High-performance toolkit for genomic interval analysis in Rust with Python bindings. Use when working with… |
| pysam | Genomic file toolkit. Read/write SAM/BAM/CRAM alignments, VCF/BCF variants, FASTA/FASTQ sequences, extract… |
| polars-bio | High-performance genomic interval operations and bioinformatics file I/O on Polars DataFrames. Overlap,… |
| tiledbvcf | Efficient storage and retrieval of genomic variant data using TileDB. Scalable VCF/BCF ingestion, incremental… |

### E 化学与药物发现

| 子技能 | 说明 |
|---|---|
| rdkit | Cheminformatics toolkit for fine-grained molecular control. SMILES/SDF parsing, descriptors (MW, LogP, TPSA),… |
| datamol | Pythonic wrapper around RDKit with simplified interface and sensible defaults. Preferred for standard drug… |
| medchem | Medicinal chemistry filters for compound triage. Apply drug-likeness rules (Lipinski, Veber, CNS), structural… |
| molfeat | Molecular featurization for ML (100+ featurizers). ECFP, MACCS, descriptors, pretrained models (ChemBERTa),… |
| pytdc | Therapeutics Data Commons. AI-ready drug discovery datasets (ADME, toxicity, DTI), benchmarks, scaffold… |
| deepchem | Molecular ML with diverse featurizers and pre-built datasets. Use for property prediction (ADMET, toxicity)… |
| torchdrug | PyTorch-native graph neural networks for molecules and proteins. Use when building custom GNN architectures… |
| matchms | Spectral similarity and compound identification for metabolomics. Use for comparing mass spectra, computing… |
| pyopenms | Complete mass spectrometry analysis platform. Use for proteomics and metabolomics workflows—feature… |
| cobrapy | Constraint-based metabolic modeling (COBRA). FBA, FVA, gene knockouts, flux sampling, SBML models, for… |
| pymatgen | Materials science toolkit. Crystal structures (CIF, POSCAR), phase diagrams, band structure, DOS, Materials… |

### F 临床与医学

| 子技能 | 说明 |
|---|---|
| clinical-decision-support | Generate professional clinical decision support (CDS) documents for pharmaceutical and clinical research… |
| clinical-reports | Write comprehensive clinical reports including case reports (CARE guidelines), diagnostic reports… |
| indication-dossier | > Generate a therapeutic indication dossier. Covers the patient population, epidemiology, disease biology,… |
| iso-13485-certification | Comprehensive toolkit for preparing ISO 13485 certification documentation for medical device Quality… |
| treatment-plans | Generate concise (3-4 page), focused medical treatment plans in LaTeX/PDF format for all clinical… |
| pyhealth | Build clinical/healthcare deep-learning pipelines with PyHealth — loading EHR/signal/imaging datasets… |
| neurokit2 | Comprehensive biosignal processing toolkit for analyzing physiological data including ECG, EEG, EDA, RSP,… |
| imaging-data-commons | Query and download public cancer imaging data from NCI Imaging Data Commons using idc-index. Use for… |
| bids | > Use this skill when working with Brain Imaging Data Structure (BIDS) datasets: organizing neuroscience and… |
| flowio | Parse FCS (Flow Cytometry Standard) files v2.0-3.1. Extract events as NumPy arrays, read metadata/channels,… |
| pydicom | Python library for working with DICOM (Digital Imaging and Communications in Medicine) files. Use this skill… |
| omero-integration | Microscopy data management platform. Access images via Python, retrieve datasets, analyze pixels, manage… |
| histolab | Lightweight WSI tile extraction and preprocessing. Use for basic slide processing, tissue detection, tile… |
| pathml | Full-featured computational pathology toolkit. Use for advanced WSI analysis including multiplexed… |
| neuropixels-analysis | Analyze Neuropixels extracellular recordings end-to-end with SpikeInterface. Covers loading SpikeGLX/Open… |

### G 平台与流程

| 子技能 | 说明 |
|---|---|
| benchling-integration | Benchling Python SDK and REST API integration for registry entities, inventory, ELN entries, workflows,… |
| labarchive-integration | Electronic lab notebook API integration. Access notebooks, manage entries/attachments, backup notebooks,… |
| dnanexus-integration | DNAnexus cloud genomics platform. Build apps/applets, manage data (upload/download), dxpy Python SDK, run… |
| latchbio-integration | Latch platform for bioinformatics workflows. Build pipelines with Latch SDK, @workflow/@task decorators,… |
| ginkgo-cloud-lab | Submit and manage protocols on Ginkgo Bioworks Cloud Lab (cloud.ginkgo.bio), a web-based interface for… |
| opentrons-integration | Official Opentrons Protocol API for OT-2 and Flex robots. Use when writing protocols specifically for… |
| pylabrobot | Vendor-agnostic lab automation framework. Use when controlling multiple equipment types (Hamilton, Tecan,… |
| protocolsio-integration | Integration with protocols.io API for managing scientific protocols. This skill should be used when working… |
| nextflow | Build, run, and debug Nextflow data pipelines and nf-core workflows end to end. Use whenever the user… |
| pacsomatic | Operator toolkit for nf-core/pacsomatic matched tumor-normal workflows from BAM inputs. Use this skill when… |
| hugging-science | Use when the user is doing AI/ML work in a scientific domain such as biology, chemistry, physics, astronomy,… |

### H 量子与通用模拟

| 子技能 | 说明 |
|---|---|
| cirq | Google quantum computing framework. Use when targeting Google Quantum AI hardware, designing noise-aware… |
| pennylane | Hardware-agnostic quantum ML framework with automatic differentiation. Use when training quantum circuits via… |
| qiskit | IBM quantum computing framework. Use when targeting IBM Quantum hardware, working with Qiskit Runtime for… |
| qutip | Quantum physics simulation library for open quantum systems. Use when studying master equations, Lindblad… |
| simpy | Process-based discrete-event simulation framework in Python. Use this skill when building simulations of… |
| sympy | Use when you need exact symbolic math in Python — algebra, calculus, equation solving, symbolic linear… |
| pymc | Bayesian modeling with PyMC. Build hierarchical models, MCMC (NUTS), variational inference, LOO/WAIC… |
| pymoo | Multi-objective optimization framework. NSGA-II, NSGA-III, MOEA/D, Pareto fronts, constraint handling,… |
| astropy | Core Python library for astronomy and astrophysics workflows that need Astropy APIs, including… |
| fluidsim | Framework for computational fluid dynamics simulations using Python. Use when running fluid dynamics… |
| matlab | MATLAB and GNU Octave numerical computing for matrix operations, data analysis, visualization, and scientific… |
| pufferlib | High-performance reinforcement learning framework optimized for speed and scale. Use when you need fast… |


## 跳簇规则
- 出图 → docs-figures（别在簇内硬画 matplotlib）
- 统计方法论 → research；统计库本身 → data-ml
- 写标书/报告 → research

## 使用方式

1. 按上表选中子技能；2. 读 `skills/scientific/<name>/INSTRUCTIONS.md`；3. 其内部脚本/资源相对该文件所在目录解析。
