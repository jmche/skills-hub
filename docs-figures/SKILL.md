---
name: docs-figures
description: Publication-grade visual deliverables hub: publication figures (figure-style / scientific-visualization / scientific-schematics), quick exploratory plots (seaborn/matplotlib), slide decks & presentations (scientific-slides / pptx-posters / latex-posters), infographics (infographics), Mermaid workflow diagrams (markdown-mermaid-writing / archify), editorial HTML/SVG diagrams (diagram-design), video and motion graphics rendered from HTML (hyperframes and the HyperFrames sub-skills), scientific schematics (scientific-schematics), AI image generation (generate-image, top-level, NOT routed through this hub). TRIGGER = produce a publication figure / build slides / make a poster / generate an infographic / draw a Mermaid flow / draw a diagram / technical schematic / make or edit a video, animation or motion graphic. SKIP = quick exploratory plots (use seaborn/matplotlib directly), UI design (-> dev), writing the paper body (-> research). 
---

# docs-figures hub

## Routing rules
- Goal = deliverable-style figure / slides / poster / schematic -> this hub
- Exploratory charting -> plain seaborn/matplotlib (still inside this hub, but no checklist needed)
- Writing the paper body -> research
- Video, animation, motion graphic, captioned clip, animated or interactive deck, Remotion port -> read hyperframes first; it selects the workflow and the domain sub-skills
- In HyperFrames sub-skills, `/<name>` means `docs-figures/<name>/INSTRUCTIONS.md`. This library ships every HyperFrames skill: keep `HYPERFRAMES_SKIP_SKILLS=1` set (env.example) so `npx hyperframes skills update` and `init` do not install separate copies
- Standalone diagram file: editorial HTML/SVG/PNG across many types (charts, Gantt, Sankey, Wardley, UML, ...), or .drawio / Mermaid / .excalidraw redrawn -> diagram-design; architecture, workflow, sequence, data-flow or state diagrams with trace motion and video export -> archify; Mermaid kept inside Markdown -> markdown-mermaid-writing

## Sub-skill index

| skill | description |
|---|---|
| scientific-visualization | Creates and audits truthful, accessible, publication-ready scientific figures with Matplotlib, Seaborn, or… |
| figure-style | "Publication-grade figure correctness and legibility rules for final-deliverable figures — not every plot.… |
| scientific-schematics | Generates scientific diagram drafts using Nano Banana 2 AI with smart iterative refinement. Uses Gemini 3.7… |
| scientific-slides | Builds slide decks and presentations for research talks. Used for making PowerPoint slides, conference… |
| infographics | "Creates and reviews infographics with Nano Banana 2 via OpenRouter. Use for statistical summaries,… |
| latex-posters | "Creates research posters in LaTeX using beamerposter, tikzposter, or baposter. Use for conference posters,… |
| pptx-posters | Creates and audits editable scientific posters in macro-free PowerPoint (.pptx) from author-approved local… |
| markdown-mermaid-writing | Writes scientific Markdown documentation and Mermaid diagrams for workflows, relationships, timelines, and… |
| archify | "Create validated architecture, workflow, sequence, data-flow, lifecycle/state, ERD, class, tree, timeline,… |
| seaborn | Creates Seaborn statistical visualizations with pandas integration for distributions, relationships,… |
| matplotlib | Creates and customizes scientific plots with Matplotlib. Used for fine-grained control over plot elements,… |
| embedded-captions | Add captions or subtitles to an existing single-subject talking-head video without editing the footage. Use… |
| faceless-explainer | "Turn arbitrary text — an article, notes, a topic, a brief — into a faceless explainer video: there is no… |
| figma | Import Figma content into a HyperFrames composition — rendered assets, brand tokens, components, storyboard… |
| general-video | Author or edit a custom HyperFrames composition when no specialized workflow fits, or when BRIEF.md sets… |
| hyperframes | Mandatory entry point: read this first for any request to make, create, edit, animate, or render a video,… |
| hyperframes-animation | "All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene… |
| hyperframes-audio | Use when audio already placed in a HyperFrames composition needs to be mixed: fade-in/fade-out, crossfade,… |
| hyperframes-cli | Use the HyperFrames CLI development loop: init, add, catalog, capture, lint, check, snapshot, compare,… |
| hyperframes-core | The HyperFrames composition contract — build one renderable project. Use for composition structure, the… |
| hyperframes-creative | Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling,… |
| hyperframes-keyframes | Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe, Ken Burns treatment, camera… |
| hyperframes-registry | Search, install, and wire registry blocks and components into HyperFrames compositions. Use BEFORE… |
| hyperframes-studio | Use when working with a person on a HyperFrames project in Studio: first, whether their message asks for a… |
| media-use | Agent Media OS for a HyperFrames project. Resolve BGM, SFX, image, icon, brand logo, voice, color grade, or… |
| motion-graphics | Use when creating a short, design-led motion graphic where motion is the message — kinetic typography, stat… |
| music-to-video | "Turn a music track (an audio file, a video to pull audio from, or a track generated from a mood brief) into… |
| pr-to-video | "Turn a GitHub pull request (a PR URL, owner/repo#N, or 'this PR' in a checked-out repo) into a code-change… |
| product-launch-video | "Turn a product or marketing URL, pasted script, or brief into a product launch / promo video — SaaS promos,… |
| remotion-to-hyperframes | 'Port an existing Remotion (React) composition''s source to HyperFrames HTML. Use ONLY on an explicit ask to… |
| slideshow | Author a HyperFrames slideshow — a presentation, pitch deck, or interactive deck with discrete slides,… |
| talking-head-recut | Package an existing talking-head / interview / podcast video with timed, designed GRAPHIC OVERLAY cards —… |

## Cross-hub handoff
- Quick exploratory plot -> plain seaborn/matplotlib, skip the checklist

## How to use

1. Pick the sub-skill from the index above; 2. read `<hub>/<name>/INSTRUCTIONS.md`; 3. its scripts/assets resolve relative to that file's directory.
