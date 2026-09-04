---
name: research
description: 科研方法论簇（research hub）：实验设计、统计检验与推断、样本量/功效分析、假说生成与 检验、科学批判性评估、同行评审、学术写作（IMRAD）、科研头脑风暴、基金标书（NSF/NIH/DARPA/ NSTC）、市场研究报告、HTR 迭代优化、古代文本分析。 触发 = 设计实验/选统计检验/样本量/提出假说/审论文/写论文或标书/科研思路/评估证据质量。 非触发 = 跑具体生物计算与查数据库（→scientific）、找文献与引文格式（→references）、 出发表级图（→docs-figures）、通用 ML 库（→data-ml）、UI/部署工程（→dev）。 
---

# research hub

## 判据
- 目标 = 得出结论 / 设计实验 / 统计决策 / 写学术文本 → 本簇
- 目标是跑具体算法、查一条数据库记录 → scientific
- 涉及文献获取、引文、专利/法规文本 → references
- 需要发表级图片/幻灯片/海报 → docs-figures

## 子技能索引

| 子技能 | 说明 |
|---|---|
| statistical-analysis | Guided statistical analysis for research data - test selection, assumption checking, effect sizes, power… |
| statistical-power | Sample-size and statistical power calculations for planning studies. Use whenever someone asks "how many… |
| experimental-design | Design experiments and studies BEFORE data is collected — choosing a design, randomizing, blocking, and… |
| hypothesis-generation | Structured hypothesis formulation from observations. Use when you have experimental observations or data and… |
| scientific-brainstorming | Creative research ideation and exploration. Use for open-ended brainstorming sessions, exploring… |
| scientific-critical-thinking | Evaluate scientific claims and evidence quality. Use for assessing experimental design validity, identifying… |
| peer-review | Structured manuscript/grant review with checklist-based evaluation. Use when writing formal peer reviews with… |
| scholar-evaluation | Systematically evaluate scholarly work using the ScholarEval framework, providing structured assessment… |
| scientific-writing | Core skill for the deep research and writing tool. Write scientific manuscripts in full paragraphs (never… |
| arbor | Autonomously improve a real artifact (code, training recipe, agent harness, data pipeline, prompt) against an… |
| research-grants | Write competitive research proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC. Agency-specific formatting,… |
| hypogenic | Automated LLM-driven hypothesis generation and testing on tabular datasets. Use when you want to… |
| predictingthepast | > Ancient text restoration, attribution, dating, contextualization, and embedding via Aeneas (Latin) / Ithaca… |
| market-research-reports | Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey,… |

## 跳簇规则
- 选统计方法 → 本簇；在该数据上跑统计代码 → data-ml（statsmodels/scikit-learn/pymc）
- 引用文献 → references；批判文献观点 → 本簇（scientific-critical-thinking）

## 使用方式

1. 按上表选中子技能；2. 读 `skills/research/<name>/INSTRUCTIONS.md`；3. 其内部脚本/资源相对该文件所在目录解析。
