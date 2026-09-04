---
name: data-ml
description: 通用数据/ML/科学计算簇（data-ml hub）：大内存 DataFrame（polars/dask/vaex/zarr-python/ lamindb）、科学数据文件格式探查（exploratory-data-analysis）、时序与预测 （aeon/timesfm-forecasting）、统计与贝叶斯（statsmodels/statistical-analysis/ scikit-learn/scikit-survival/shap/pymc/pymoo）、深度学习（transformers/ pytorch-lightning/torch-geometric/stable-baselines3）、图与空间（networkx/ geopandas/geomaster）、降维（umap-learn）、资源自检（get-available-resources）。 触发 = ETL/polars/dask/ML 模型/时序预测/图算法/地理空间/大内存/跑通用科学计算。 非触发 = 生物领域计算（→scientific）、出发表级图（→docs-figures）、设计实验（→research）。 
---

# data-ml hub

## 判据
- 通用数据与 ML 算法（无生物领域色彩）→ 本簇
- 生物/化学/临床计算 → scientific
- 出发表级图 → docs-figures

## 子技能索引

| 子技能 | 说明 |
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

## 跳簇规则
- 生物领域（单细胞/蛋白/基因组）→ scientific
- 要发表级图 → docs-figures

## 使用方式

1. 按上表选中子技能；2. 读 `skills/data-ml/<name>/INSTRUCTIONS.md`；3. 其内部脚本/资源相对该文件所在目录解析。
