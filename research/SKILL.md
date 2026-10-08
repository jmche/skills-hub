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
| statistical-power | Calculates sample sizes and statistical power for study planning. Applies when someone asks "how many… |
| experimental-design | Designs experiments and studies BEFORE data is collected — choosing a design, randomizing, blocking, and… |
| hypothesis-generation | Formulates evidence-bounded scientific questions, candidate hypotheses, rival explanations, causal or… |
| scientific-brainstorming | Facilitates evidence-aware scientific ideation with independent generation, structured discussion, explicit… |
| scientific-critical-thinking | Evaluates scientific claims and evidence quality. Applies to experimental design validity, biases and… |
| peer-review | Prepares evidence-bounded, constructive peer-review drafts and structured manuscript assessments. Supports… |
| scholar-evaluation | Provides qualitative-first, evidence-traceable developmental review of scholarly works and audit low-stakes… |
| scientific-writing | Drafts, revises, and audits scientific manuscripts or reports with explicit evidence provenance,… |
| arbor | Applies Arbor Hypothesis Tree Refinement to research artifacts with repeatable evaluators, including model… |
| research-grants | Supports research proposal preparation and review for NSF, NIH, DOE, DARPA, and Taiwan NSTC, including… |
| hypogenic | Plans and audits use of ChicagoHAI HypoGeniC/HypoRefine for LLM-assisted hypothesis generation from labeled… |
| predictingthepast | Ancient text restoration, attribution, dating, contextualization, and embedding via Aeneas (Latin) / Ithaca… |
| market-research-reports | Builds evidence-traceable market research reports and assumption-driven market sizing or forecast scenarios.… |

## Cross-hub handoff
- Choosing a statistical method -> this hub; RUNNING the stats code on data -> data-ml (statsmodels/scikit-learn/pymc)
- Citing literature -> references; CRITIQUING its claims -> this hub (scientific-critical-thinking)

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
