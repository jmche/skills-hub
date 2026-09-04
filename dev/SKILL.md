---
name: dev
description: 工程/UI/云/GPU 簇（dev hub）：前端设计（frontend-design）、UI/UX 风格库 （ui-ux-pro-max，84 种风格/192 配色/74 字号/192 产品类型/98 条 UX 指南/104 图标/GSAP 动画/ 25 种图表 × 22 栈）、Web 界面规范审查（web-design-guidelines）、Modal 无服务器 云（GPU/批量/端点）、NVIDIA/CUDA 加速（optimize-for-gpu：CuPy/Numba/CuDF/cuML/cuGraph/Warp）、 Pi 极简 agent harness（pi-agent：安装/配置/skills/extensions/MCP/RPC）。 触发 = 写前端/做 UI/审查界面/部署 GPU/跑批量云加速/NVIDIA 优化/装 Pi harness。 非触发 = 生物领域计算（→scientific）、发表级图（→docs-figures）、统计/ML 方法论（→research）。 
---

# dev hub

## 判据
- 写代码 / 做 UI / 部署云 / GPU 加速 → 本簇
- 领域计算（生物/化学）→ scientific
- 通用数据与 ML 库 → data-ml

## 子技能索引

| 子技能 | 说明 |
|---|---|
| frontend-design | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps… |
| ui-ux-pro-max | "UI/UX design intelligence for web and mobile. Searchable local database with 84 styles, 192 color palettes,… |
| web-design-guidelines | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check… |
| modal | Modal is a serverless cloud platform for running Python on demand, including on-demand GPUs. Use when… |
| optimize-for-gpu | "GPU-accelerate Python code using CuPy, Numba CUDA, Warp, cuDF, cuML, cuGraph, KvikIO, cuCIM, cuxfilter,… |
| pi-agent | Build with and use Pi, the minimal terminal coding harness. Use for installing Pi, configuring… |

## 跳簇规则
- 出 UI 设计系统 → 本簇（ui-ux-pro-max）；出发表级图 → docs-figures

## 使用方式

1. 按上表选中子技能；2. 读 `skills/dev/<name>/INSTRUCTIONS.md`；3. 其内部脚本/资源相对该文件所在目录解析。
