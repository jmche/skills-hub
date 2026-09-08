---
name: research
description: Research methodology hub: experimental design, statistical tests and inference, sample-size / power analysis, hypothesis generation and testing, critical evaluation of scientific claims, peer review, academic writing (IMRAD), research brainstorming, grant proposals (NSF/NIH/DARPA/NSTC), market research reports, HTR iterative optimization, classical text analysis. TRIGGER = design an experiment / pick a statistical test / compute sample size / generate or test a hypothesis / review a paper / write a paper or grant / evaluate evidence quality. SKIP = running concrete bio-computation, database or API lookups (-> scientific), finding papers and citation formatting (-> references), publication-grade figures (-> docs-figures), generic ML libraries (-> data-ml), UI/infrastructure engineering (-> dev). 
---

# research hub

## Routing rules
- Goal = reach a CONCLUSION / design an experiment / statistical decision / academic text -> this hub
- Goal = run a concrete algorithm or fetch a database record -> scientific
- Paper retrieval, citation formatting, patents / regulatory text -> references
- Publication-grade figure, slide, or poster output -> docs-figures

## Sub-skill index

| skill | description |
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
| predictingthepast | Ancient text restoration, attribution, dating, contextualization, and embedding via Aeneas (Latin) / Ithaca… |
| market-research-reports | Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey,… |

## Cross-hub handoff
- Choosing a statistical method -> this hub; RUNNING the stats code on data -> data-ml (statsmodels/scikit-learn/pymc)
- Citing literature -> references; CRITIQUING its claims -> this hub (scientific-critical-thinking)

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
