---
name: docs-figures
description: 发表级交付物样式簇（docs-figures hub）：发表级图（figure-style/scientific-visualization/ scientific-schematics）、快速探索图（seaborn/matplotlib）、幻灯片/演示 （scientific-slides/pptx-posters/latex-posters）、infographic（infographics）、 Mermaid 工作流图（markdown-mermaid-writing/archify）、科学示意图 （scientific-schematics）、AI 生图（generate-image，顶层直用不走本簇）。 触发 = 出发表级图/画幻灯片/做海报/生成 infographic/Mermaid 流程图/科学示意图。 非触发 = 快速 EDA 图（直接用 seaborn/matplotlib）、UI 设计（→dev）、写论文正文（→research）。 
---

# docs-figures hub

## 判据
- 目标是产出交付物样式的图/幻灯片/海报/示意图 → 本簇
- 快速探索性图表 → 直接用 seaborn/matplotlib（仍在 docs-figures 簇内可查）
- 写论文正文 → research

## 子技能索引

| 子技能 | 说明 |
|---|---|
| scientific-visualization | Meta-skill for publication-ready figures. Use when creating journal submission figures requiring multi-panel… |
| figure-style | "Publication-grade figure correctness and legibility rules for final-deliverable figures — not every plot.… |
| scientific-schematics | Create publication-quality scientific diagrams using Nano Banana 2 AI with smart iterative refinement. Uses… |
| scientific-slides | Build slide decks and presentations for research talks. Use this for making PowerPoint slides, conference… |
| infographics | "Create professional infographics using Nano Banana Pro AI with smart iterative refinement. Uses Gemini 3 Pro… |
| latex-posters | "Create professional research posters in LaTeX using beamerposter, tikzposter, or baposter. Support for… |
| pptx-posters | Create research posters using HTML/CSS that can be exported to PDF or PPTX. Use this skill ONLY when the user… |
| markdown-mermaid-writing | Comprehensive markdown and Mermaid diagram writing skill. Use when creating any scientific document, report,… |
| archify | Create polished, validated architecture, workflow, sequence, data-flow, and lifecycle/state diagrams as… |
| seaborn | Statistical visualization with pandas integration. Use for quick exploration of distributions, relationships,… |
| matplotlib | Low-level plotting library for full customization. Use when you need fine-grained control over every plot… |

## 跳簇规则
- 要 EDA 快图 → 直接用 seaborn/matplotlib，不必加载发表级 checklist

## 使用方式

1. 按上表选中子技能；2. 读 `skills/docs-figures/<name>/INSTRUCTIONS.md`；3. 其内部脚本/资源相对该文件所在目录解析。
