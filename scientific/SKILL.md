---
name: scientific
description: Biology / chemistry / medicine computation hub: structure prediction and sequence design (AlphaFold2/Boltz/Chai-1/ESMFold2/ESMFold/OpenFold3/PyMOL/MD), sequence and genomics tooling (Biopython/Clustal Omega/IQ-TREE/ETE), 30+ database queries (UniProt/Ensembl/PDB/PubChem/ChEMBL/gnomAD/clinVar/DepMap/1000Genomes/STRING/ Reactome/KEGG-JASPAR/QuickGO ...), single-cell and transcriptomics (Scanpy/anndata/ scvi-tools/cellxgene-census/scVelo/bulk RNA-seq/DESeq2/DEEPTools/GRN/pathway enrichment/geniml/gtars/pysam/TileDB-VCF), clinical (CDS/clinical reporting/ indication dossier/ISO13485/treatment plans/PyHealth/imaging BIDS/pathology WSI/ electrophysiology), cheminformatics and drug discovery (RDKit/datamol/medchem/ molfeat/DeepChem/TorchDrug/PyOpenMS/COBRApy/DiffDock/pymatgen), lab & cloud platform integration (Benchling/LabArchive/DNAnexus/LatchBio/Ginkgo/Opentrons/ pylabrobot/protocols.io/Nextflow/pacsomatic), quantum & general simulation (Qiskit/cirq/PennyLane/QuTiP/SimPy/PyMC/Astropy/FluidSim/MATLAB). TRIGGER = protein folding / UniProt-PDB-ChEMBL-gnomAD lookups / run Scanpy or RNA-seq / dock molecules / write Opentrons protocols / query a gene variant / MD simulation / structural similarity search / single-cell analysis / drug molecules. SKIP = statistical methodology and hypothesis design (-> research), literature and citation (-> references), generic ML frameworks (transformers/polars/ pytorch-lightning -> data-ml), publication figures and slides (-> docs-figures), UI engineering and GPU clouds (-> dev). 
---

# scientific hub

## Routing rules
- Goal = RUN a concrete bio-computation / query a concrete database / predict structure / design a molecule -> this hub
- Goal = methodology (experimental design, statistical inference, hypothesis) -> research
- Paper retrieval / citations / patents / regulatory text -> references
- Pure generic data & ML libraries (no domain flavor) -> data-ml
- Publication-grade figure / slide / poster -> docs-figures

## Sub-skill index

### A Structure prediction & sequence design

| skill | description |
|---|---|
| alphafold2 | Predict protein structure for monomers and multimers with AlphaFold2 via the ColabFold runner (Mirdita et al.… |
| alphafold-database-fetch-and-analyze | Retrieve and analyze AlphaFold predicted structures for a protein. Use when the user provides a specific… |
| boltz | Structure prediction for protein, nucleic-acid, and small-molecule complexes with Boltz-2 (Passaro & Wohlwend… |
| chai1 | Structure prediction for protein, nucleic-acid, and small-molecule complexes with the Chai-1 foundation model… |
| esm | Uses the Biohub esm Python SDK for ESM3 protein generation, ESMC embeddings, and ESMFold2 all-atom folding.… |
| esmfold2 | Biohub ESMFold2 / ESMFold2-Fast all-atom co-folding (Candido et al. 2026, github.com/Biohub/esm).… |
| openfold3 | Structure prediction using OpenFold3, an open-weights PyTorch reproduction of AlphaFold3 from the AlQuraishi… |
| foldseek-structural-search | Performs 3D structural searches of proteins against various databases (PDB, AlphaFold, CATH, MGnify, etc.)… |
| pymol | Visualize, analyze, and render protein and molecular structures using PyMOL. Use when the user wants to… |
| molecular-dynamics | Runs and analyzes molecular dynamics simulations with OpenMM and MDAnalysis. Sets up protein/small molecule… |
| glycoengineering | Analyzes and engineers protein glycosylation by scanning canonical N-glycosylation sequons, describing… |
| solublempnn | Inverse-fold a backbone with SolubleMPNN — ProteinMPNN retrained on a soluble-PDB subset (Dauparas et al.… |
| ligandmpnn | Inverse-fold a backbone with ligand, nucleic-acid, and metal context using LigandMPNN (Dauparas et al. 2023,… |
| proteinmpnn | Inverse-fold a protein backbone (PDB structure) into amino-acid sequence with ProteinMPNN (Dauparas et al.… |
| diffdock | Predicts protein-small-molecule binding poses with DiffDock and DiffDock-L from PDB or sequence plus… |
| tamarind | Provides access to a collection of open-source molecular design and structural biology tools on the Tamarind… |
| rowan | Rowan is a cloud-native molecular modeling and medicinal-chemistry workflow platform with a Python API. Use… |
| adaptyv | Uses the Adaptyv Bio Foundry API and Python SDK to design protein characterization experiments, estimate… |

### B Sequence & genomics tooling

| skill | description |
|---|---|
| biopython | Provides Biopython workflows for sequence manipulation, file parsing (FASTA/GenBank/PDB), phylogenetics, and… |
| gget | "Queries 20+ bioinformatics resources through CLI/Python. Supports quick lookups of gene info, BLAST/BLAT,… |
| bioservices | Provides a Python interface to bioinformatics services including UniProt, KEGG, ChEMBL, Reactome, QuickGO,… |
| ncbi-sequence-fetch | Retrieve protein and nucleotide sequences from NCBI databases using E-utilities. Supports direct accession… |
| protein-sequence-msa | Performs multiple sequence alignment of proteins with EBI Clustal Omega. Use when you need to align multiple… |
| protein-sequence-similarity-search | Searches for homologous protein sequences using MMseqs2 (fast, default) or BLAST (comprehensive, fallback).… |
| phylogenetics | Builds and analyzes phylogenetic trees using MAFFT multiple sequence alignment, IQ-TREE maximum likelihood… |
| etetoolkit | Analyzes, manipulates, compares, annotates, and visualizes phylogenetic or other hierarchical trees with ETE… |
| scikit-bio | Biological data toolkit. Sequence analysis, alignments, phylogenetic trees, diversity metrics (alpha/beta,… |

### C Database lookup

| skill | description |
|---|---|
| uniprot-database | Access protein metadata, function, taxonomy, and sequences across UniProtKB, UniParc, and UniRef. Use when… |
| ensembl-database | Query the Ensembl database to resolve gene, transcript, and protein IDs, fetch genomic or protein sequences,… |
| pdb-database | Use when you want to search for or download experimentally-determined 3D structures for biomolecules… |
| pubchem-database | Query PubChem, search by name/CID/SMILES, retrieve properties, similarity/substructure searches, bioactivity,… |
| chembl-database | Query the ChEMBL database for bioactive molecules, drug targets, bioactivity data, approved drugs, and… |
| gnomad-database | Query the Genome Aggregation Database (gnomAD). Use when determining the rarity or allele frequency of… |
| onekgpd | Queries the 1000 Genomes Project dataset (3,202 whole-genome-sequenced individuals, GRCh38) at the level of… |
| dbsnp-database | Use when you want to look up, map, and search for short genetic variants (SNPs, indels) in NCBI's dbSNP… |
| clinvar-database | Use when needing clinical significance, pathogenicity classifications (e.g., Pathogenic, Benign, VUS),… |
| depmap | Retrieves and analyzes Cancer Dependency Map (DepMap) release data, including CRISPR Chronos gene effects,… |
| opentargets-database | Query Open Targets Platform for target-disease associations, drug target discovery, tractability/safety data,… |
| primekg | Queries a pinned Precision Medicine Knowledge Graph (PrimeKG) CSV for typed gene, drug, disease, and… |
| string-database | Query the STRING database for protein-protein interactions (PPIs), functional enrichment, and homology. Use… |
| embl-ebi-ols | Query and search the EMBL-EBI Ontology Lookup Service (OLS) for biomedical ontology terms, definitions, and… |
| encode-ccres-database | Query the ENCODE Registry of cis-Regulatory Elements (cCREs) via the SCREEN GraphQL API, or make custom… |
| interpro-database | Identify domains, families, and sites in proteins; find all proteins in a family or sharing a domain; explore… |
| jaspar-database | Query the JASPAR database for Transcription Factor (TF) binding profiles. Use when retrieving Position… |
| quickgo-database | Query the QuickGO and Evidence & Conclusion Ontology (ECO) REST API. Use this when you need to map genes to… |
| reactome-database | Query the Reactome database (Analysis and Content Services). Use when the user asks about pathway analysis,… |
| ucsc-conservation-and-tfbs | Fetch Evolutionary Conservation scores (phyloP, phastCons) and Transcription Factor Binding Sites (TFBS) from… |
| unibind-database | Queries the UniBind database for experimentally validated transcription factor (TF) binding sites. Use when… |
| alphagenome-single-variant-analysis | Analyzes genetic variant effects on gene expression (RNA-seq), chromatin accessibility (DNASE), histone marks… |
| clinical-trials-database | Query ClinicalTrials.gov via APIv2. Use when you want to search for trials by condition, drug, location,… |
| gtex-database | Use when you want to retrieve quantitative RNA expression data and variant eQTL information from the GTEx… |
| human-protein-atlas-database | Use when you want to retrieve semi-quantitative protein expression and spatial localisation data from the… |

### D Single-cell & transcriptomics

| skill | description |
|---|---|
| scanpy | Performs Scanpy single-cell RNA-seq QC, normalization, HVG selection, PCA/UMAP/t-SNE, clustering, exploratory… |
| anndata | Handles annotated matrices in single-cell analysis, .h5ad and Zarr files, and integration with the scverse… |
| scvi-tools | Fits probabilistic models for single-cell omics, including scVI batch integration, scANVI annotation, totalVI… |
| cellxgene-census | Queries the CZ CELLxGENE Census programmatically for versioned public single-cell and spatial transcriptomics… |
| scvelo | Performs RNA velocity analysis with scVelo from spliced and unspliced single-cell RNA counts. Fits… |
| bulk-rnaseq | Prepares bulk RNA-seq FASTQ, Salmon, STAR or featureCounts output for gene-level differential expression.… |
| pydeseq2 | Performs bulk RNA-seq differential expression analysis with PyDESeq2, including count validation, formula… |
| deeptools | NGS analysis toolkit. BAM to bigWig conversion, QC (correlation, PCA, fingerprints), heatmaps/profiles (TSS,… |
| arboreto | Infers candidate gene regulatory networks from bulk or single-cell expression data using AertsLab Arboreto… |
| pathway-enrichment | Performs pathway and gene-set enrichment analysis on gene lists or ranked gene data and interprets the… |
| geniml | "Supports audited local Geniml genomic-interval workflows: validate BED and universe contracts, plan… |
| gtars | Supports Gtars for local genomic interval models and set algebra, overlaps and counts, consensus and… |
| pysam | Provides Python/HTSlib workflows for genomic files. Used when reading, querying, filtering, or writing… |
| polars-bio | Performs genomic interval overlap, nearest, merge, coverage, complement and subtraction on Polars DataFrames,… |
| tiledbvcf | Stores and retrieves genomic variant calls with TileDB-VCF. Use for indexed single-sample VCF/BCF ingestion,… |

### E Chemistry & drug discovery

| skill | description |
|---|---|
| rdkit | Cheminformatics toolkit for fine-grained molecular control. SMILES/SDF parsing, descriptors (MW, LogP, TPSA),… |
| datamol | Pythonic wrapper around RDKit with simplified interface and sensible defaults. Preferred for standard drug… |
| medchem | Applies medicinal chemistry filters for compound triage, using drug-likeness rules (Lipinski, Veber, CNS),… |
| molfeat | Featurizes small molecules with Molfeat for QSAR/QSPR, chemical similarity, virtual screening, and molecular… |
| pytdc | Provides Therapeutics Data Commons workflows through PyTDC for registry discovery, dataset access, task-aware… |
| deepchem | Builds molecular property prediction and MoleculeNet workflows with DeepChem, including SMILES featurization,… |
| torchdrug | Builds and troubleshoots TorchDrug 0.2.1 workflows for molecular graphs, property prediction, self-supervised… |
| matchms | Processes, cleans, compares, and searches tandem mass spectra with matchms. Use for MS/MS file I/O, metadata… |
| pyopenms | Processes mass spectrometry data with pyOpenMS. Supports proteomics and metabolomics workflows—feature… |
| cobrapy | Performs constraint-based metabolic modeling with COBRApy, including FBA, pFBA, FVA, gene knockouts, flux… |
| pymatgen | Analyzes, validates, converts, and transforms materials structures and computed materials data with pymatgen.… |

### F Clinical & medical

| skill | description |
|---|---|
| clinical-decision-support | Prepares and validates research-only clinical decision-support evaluation, evidence-profile, cohort,… |
| clinical-reports | Creates safety-bounded draft structures and runs local deterministic checks for clinical case, diagnostic,… |
| indication-dossier | Generate a therapeutic indication dossier. Covers the patient population, epidemiology, disease biology,… |
| iso-standards-readiness | Prepares and structurally reviews readiness evidence for ISO management-system and laboratory-competence… |
| treatment-plans | Formats and structurally validates local treatment-plan documentation after clinical decisions have already… |
| pyhealth | Builds and validates PyHealth clinical machine-learning pipelines for EHR, signals, imaging, and medical… |
| neurokit2 | Builds and audits reproducible NeuroKit2 research workflows for physiological time-series preprocessing,… |
| imaging-data-commons | Queries and downloads public cancer imaging data from NCI Imaging Data Commons. Supports IDC collection… |
| bids | Organizes, queries, validates, and converts Brain Imaging Data Structure (BIDS) datasets. Supports organizing… |
| flowio | Reads, inspects, and writes Flow Cytometry Standard (FCS) 2.0, 3.0, and 3.1 files with FlowIO. Use for… |
| pydicom | Reads, inspects, writes, transforms, and preflights local DICOM datasets and pixel data. Applies to DICOM… |
| omero-integration | Inspects and automates microscopy data workflows against OMERO.server with omero-py, BlitzGateway, OMERO CLI,… |
| histolab | Extracts and preprocesses whole-slide histology image tiles with Histolab. Use for WSI inspection, tissue… |
| pathml | "Supports local computational pathology research with PathML: slide loading and tiling, preprocessing and QC,… |
| neuropixels-analysis | Analyzes Neuropixels extracellular recordings end-to-end with SpikeInterface. Covers loading SpikeGLX/Open… |

### G Platforms & pipelines

| skill | description |
|---|---|
| benchling-integration | Benchling Python SDK and REST API integration for registry entities, inventory, ELN entries, workflows,… |
| labarchive-integration | Integrates with the official LabArchives ELN REST-like API and Inventory API v1. Supports regional endpoint… |
| dnanexus-integration | Builds and operates reproducible genomics workloads on DNAnexus with the dx CLI, dxpy, apps/applets, native… |
| latchbio-integration | Builds, registers, debugs, and operates bioinformatics workflows on Latch using the Python SDK, CLI, Latch… |
| ginkgo-cloud-lab | Guides protocol selection, input preparation, pricing checks, and browser ordering on Ginkgo Bioworks Cloud… |
| opentrons-integration | Authors, reviews, migrates, simulates, and troubleshoots official Opentrons Python Protocol API v2 protocols… |
| pylabrobot | Develops and reviews PyLabRobot lab-automation resources, liquid-handling plans, offline simulations, and… |
| protocolsio-integration | Reads, validates, and safely exports protocols.io data with current official REST/MCP contracts, or creates… |
| nextflow | Builds, runs, and debugs Nextflow DSL2 pipelines and nf-core workflows. Use for Nextflow, nf-core, .nf files,… |
| pacsomatic | Prepares and launches nf-core/pacsomatic matched tumor-normal PacBio HiFi genomics workflows from unaligned… |
| hugging-science | Discovers and evaluates scientific datasets, models, methodology posts, and Spaces through the Hugging… |

### H Quantum & general simulation

| skill | description |
|---|---|
| cirq | Google quantum computing framework. Use when targeting Google Quantum AI hardware, designing noise-aware… |
| pennylane | Builds and differentiates PennyLane quantum circuits, hybrid PyTorch or JAX models, molecular VQE and QAOA… |
| qiskit | Builds, simulates, transpiles, and executes quantum circuits with Qiskit and IBM Quantum Runtime. Use for… |
| qutip | Simulate and audit closed and open quantum-system models with QuTiP 5, including deterministic, trajectory,… |
| simpy | Builds, inspects, tests, and analyzes bounded process-based discrete-event simulations with SimPy. Use for… |
| sympy | Performs exact symbolic mathematics with SymPy for algebra, calculus, equation solving, symbolic linear… |
| pymc | Builds and checks Bayesian models with PyMC, including hierarchical models, NUTS MCMC, variational inference,… |
| pymoo | Solves and validates single-, multi-, and many-objective optimization with pymoo, including NSGA-II,… |
| astropy | Core Python library for astronomy and astrophysics workflows that need Astropy APIs, including… |
| fluidsim | Plans, configures, inspects, restarts, and analyzes bounded FluidSim computational-fluid-dynamics simulations… |
| matlab | Builds, reviews, migrates, and plans MATLAB or GNU Octave numerical workflows. Use for arrays, tabular/time… |
| pufferlib | Version-aware guidance for PufferLib reinforcement-learning environments, vectorization, policies, PuffeRL… |


## Cross-hub handoff
- Charts & figures -> docs-figures (do not hard-draw matplotlib inside this hub)
- Statistical methodology -> research; the stats libraries themselves -> data-ml
- Writing grants / reports -> research

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
