---
name: data-ml
description: Generic data / ML / scientific-compute hub: large-memory DataFrames (polars/dask/ vaex/zarr-python/lamindb), scientific data format exploration (exploratory-data- analysis), time series & forecasting (aeon/timesfm), statistics & Bayesian (statsmodels/statistical-analysis/scikit-learn/scikit-survival/shap/pymc/pymoo), deep learning (transformers/pytorch-lightning/torch-geometric/stable-baselines3), graph & geography (networkx/geopandas/geomaster), dimensionality reduction (umap-learn), resource self-check (get-available-resources). TRIGGER = ETL / polars / dask / train an ML model / time-series forecasting / graph algorithms / geospatial / big-memory / run generic scientific compute. SKIP = domain bio/chem computation (-> scientific), publication figures (-> docs-figures), experimental design (-> research). 
---

# data-ml hub

## Routing rules
- Generic data & ML libraries (no domain flavor) -> this hub
- Bio / chem / clinical computation -> scientific
- Publication figures -> docs-figures

## Sub-skill index

| skill | description |
|---|---|
| dask | Distributed computing for larger-than-RAM pandas/NumPy workflows. Use when you need to scale existing… |
| polars | High-performance DataFrame library for Python ETL, analytics, and pandas migration. Use for expression-based… |
| vaex | Use this skill for processing and analyzing large tabular datasets (billions of rows) that exceed available… |
| zarr-python | Chunked N-D arrays for cloud storage (Zarr-Python 3). Compressed arrays, parallel I/O, S3/GCS via fsspec,… |
| lamindb | Use when working with LaminDB, the open-source lineage-native lakehouse for biological datasets and models.… |
| exploratory-data-analysis | Perform comprehensive exploratory data analysis on scientific data files across 200+ file formats. This skill… |
| scikit-learn | Machine learning in Python with scikit-learn. Use when working with supervised learning (classification,… |
| shap | Model interpretability and explainability using SHAP (SHapley Additive exPlanations). Use this skill when… |
| statsmodels | Statistical models library for Python. Use when you need specific model classes (OLS, GLM, mixed models,… |
| scikit-survival | Comprehensive toolkit for survival analysis and time-to-event modeling in Python using scikit-survival. Use… |
| aeon | This skill should be used for time series machine learning tasks including classification, regression,… |
| timesfm-forecasting | Zero-shot time series forecasting with Google's TimesFM foundation model. Use for any univariate time series… |
| transformers | Hugging Face Transformers for loading Hub models, running pipeline inference, text generation, and Trainer… |
| pytorch-lightning | Deep learning framework (PyTorch Lightning / lightning package). Organize PyTorch code into LightningModules,… |
| torch-geometric | PyTorch Geometric (PyG) for graph neural networks — node/link/graph classification, message passing (GCN,… |
| stable-baselines3 | Production-ready reinforcement learning algorithms (PPO, SAC, DQN, TD3, DDPG, A2C) with scikit-learn-like… |
| networkx | Create, analyze, and visualize complex networks and graphs in Python with NetworkX. Use when working with… |
| geopandas | Python library for working with geospatial vector data including shapefiles, GeoJSON, and GeoPackage files.… |
| geomaster | Comprehensive geospatial science skill covering remote sensing, GIS, spatial analysis, machine learning for… |
| umap-learn | Use UMAP-learn for nonlinear dimensionality reduction, 2D/3D embeddings, clustering preprocessing, supervised… |
| get-available-resources | This skill should be used at the start of any computationally intensive scientific task to detect and report… |

## Cross-hub handoff
- Domain (single-cell / protein / genomics) work -> scientific
- Publication-grade output -> docs-figures

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
