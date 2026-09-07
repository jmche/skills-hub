---
name: dev
description: Engineering / UI / cloud / GPU hub: frontend design (frontend-design), UI/UX style library (ui-ux-pro-max: 84 styles / 192 palettes / 74 type scales / 192 product types / 98 UX guidelines / 104 icons / GSAP motion / 25 chart types x 22 stacks), web UI standard review (web-design-guidelines), Modal serverless clouds (GPU/batch/endpoints), NVIDIA/CUDA acceleration (optimize-for-gpu: CuPy/Numba/CuDF/ cuML/cuGraph/Warp), Pi minimal agent harness (pi-agent: install/configure/skills/ extensions/MCP/RPC). TRIGGER = build frontend / design UI / review an interface / deploy GPU / run batch cloud acceleration / NVIDIA optimization / install the Pi harness. SKIP = domain bio/chem computation (-> scientific), publication figures (-> docs-figures), statistical & ML methodology (-> research). 
---

# dev hub

## Routing rules
- Build web UI / frontend / deploy to cloud / GPU acceleration -> this hub
- Domain (bio/chem) computation -> scientific
- Generic data & ML libraries -> data-ml

## Sub-skill index

| skill | description |
|---|---|
| frontend-design | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps… |
| ui-ux-pro-max | "UI/UX design intelligence for web and mobile. Searchable local database with 84 styles, 192 color palettes,… |
| web-design-guidelines | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check… |
| modal | Modal is a serverless cloud platform for running Python on demand, including on-demand GPUs. Use when… |
| optimize-for-gpu | "GPU-accelerate Python code using CuPy, Numba CUDA, Warp, cuDF, cuML, cuGraph, KvikIO, cuCIM, cuxfilter,… |
| pi-agent | Build with and use Pi, the minimal terminal coding harness. Use for installing Pi, configuring… |

## Cross-hub handoff
- UI design system -> this hub (ui-ux-pro-max); publication-grade figures -> docs-figures

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
