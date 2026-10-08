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
| dask | Scales pandas, NumPy, and custom Python research workflows beyond memory or across clusters with Dask. Covers… |
| polars | High-performance DataFrame library for Python ETL, analytics, and pandas migration. It supports… |
| vaex | Processes large tabular scientific datasets with Vaex expressions, filtered views, streamed statistics,… |
| zarr-python | Stores and queries chunked N-D scientific arrays with Zarr-Python 3, including codecs, sharding, S3/GCS… |
| lamindb | Manages biological datasets and models with LaminDB, including artifact registration, lineage tracking,… |
| exploratory-data-analysis | "Performs bounded, local exploratory analysis of explicitly supported scientific files. Supports redacted… |
| scikit-learn | Supports machine learning in Python with scikit-learn. Applies when working with supervised learning… |
| shap | Explain and audit machine-learning predictions with SHAP. Use for selecting SHAP explainers and maskers,… |
| statsmodels | Fits and diagnoses Python statistical models including OLS, GLM, discrete and mixed models, ARIMA and… |
| scikit-survival | Builds, evaluates, and audits right-censored or competing-risk survival workflows with scikit-survival,… |
| aeon | This skill should be used for time series machine learning tasks including classification, regression,… |
| timesfm-forecasting | Performs zero-shot time-series forecasting with Google's TimesFM, including regular-grid CSV preparation,… |
| transformers | Hugging Face Transformers for loading Hub models, running pipeline inference, text generation, and Trainer… |
| pytorch-lightning | Deep learning framework (PyTorch Lightning / lightning package). Organize PyTorch code into LightningModules,… |
| torch-geometric | Supports PyTorch Geometric (PyG) graph neural networks — node/link/graph classification, message passing… |
| stable-baselines3 | Trains and evaluates single-agent reinforcement learning with Stable Baselines3 (PPO, SAC, DQN, TD3, DDPG,… |
| networkx | Creates, analyzes, and visualizes complex networks and graphs in Python with NetworkX. Use when working with… |
| geopandas | Guidance and local audit tools for Python workflows that directly use GeoPandas GeoSeries, GeoDataFrame,… |
| geomaster | Supports geospatial research workflows for remote sensing, vector and raster GIS, spatial statistics, terrain… |
| umap-learn | Applies UMAP-learn to nonlinear dimensionality reduction, 2D/3D embeddings, clustering preprocessing,… |
| get-available-resources | Detects host inventory and effective CPU, memory, disk, scheduler, container, and accelerator limits when a… |

## Cross-hub handoff
- Domain (single-cell / protein / genomics) work -> scientific
- Publication-grade output -> docs-figures

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
