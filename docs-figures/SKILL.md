---
name: docs-figures
description: Publication-grade visual deliverables hub: publication figures (figure-style / scientific-visualization / scientific-schematics), quick exploratory plots (seaborn/matplotlib), slide decks & presentations (scientific-slides / pptx-posters / latex-posters), infographics (infographics), Mermaid workflow diagrams (markdown-mermaid-writing / archify), scientific schematics (scientific-schematics), AI image generation (generate-image, top-level, NOT routed through this hub). TRIGGER = produce a publication figure / build slides / make a poster / generate an infographic / draw a Mermaid flow / technical schematic. SKIP = quick exploratory plots (use seaborn/matplotlib directly), UI design (-> dev), writing the paper body (-> research). 
---

# docs-figures hub

## Routing rules
- Goal = deliverable-style figure / slides / poster / schematic -> this hub
- Exploratory charting -> plain seaborn/matplotlib (still inside this hub, but no checklist needed)
- Writing the paper body -> research

## Sub-skill index

| skill | description |
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

## Cross-hub handoff
- Quick exploratory plot -> plain seaborn/matplotlib, skip the checklist

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
