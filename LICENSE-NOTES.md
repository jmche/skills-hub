# Licensing notes

This repository is a **curated skill library**. The library content — routing
hubs (`research`, `scientific`, `references`, `dev`, `data-ml`,
`docs-figures`, `team`), role personas (curated from `agency-agents`),
routing metadata, and the installer/maintenance tooling — is released under
**MIT** (see `LICENSE`).

## Upstream attribution

Skills in this collection were curated from an upstream "scientific agent
skills" ecosystem. The most prominent upstream sources detected in the
content (full machine-readable breakdown in `LICENSE-AUDIT.csv`):

| Upstream | License | Used by (examples) |
|---|---|---|
| `mattpocock/skills` | MIT | `grill-me`, `grill-with-docs` |
| `msitarzewski/agency-agents` | MIT | `roles/` (33 personas) |
| `SuperiorByteWorks-LLC/agent-project` | Apache-2.0 | several docs-figures templates |
| `google-deepmind/science-skills` | Apache-2.0 | hypothesis-generation related |
| Anthropic ecosystem skills (`anthropics/skills`) | MIT (inferred) | `pdf`, `docx`, `xlsx`, `pptx`, `generate-image` |
| Tooling docs (Biohub/esm, sokrypton/ColabFold, dauparas/ProteinMPNN, ...) | MIT / other | scientific sub-skill references |

## Upstream tooling called by some sub-skills (all permissive; tools installed separately by users)

These sub-skills document how to call third-party libraries. The sub-skill
documents themselves are part of this MIT-licensed library; the underlying
tools keep their own permissive licenses (confirmed against each upstream
`LICENSE` file) and are installed separately on the user's machine:

| Sub-skill | Upstream library | Upstream license |
|---|---|---|
| `scientific/proteinmpnn` | dauparas/ProteinMPNN | MIT |
| `scientific/solublempnn` | dauparas/ProteinMPNN | MIT |
| `scientific/ligandmpnn` | dauparas/LigandMPNN | MIT |
| `scientific/pyopenms` | OpenMS/OpenMS | BSD-3-Clause |

## What is NOT published

- `gov-*` (14 skills) — private project skills (autogov, not yet public).
  They live on disk inside this directory and remain fully usable locally,
  but are excluded from version control (`.gitignore`) and from the publish
  whitelist (`publish.json`).
- Real secrets (`.env`, `~/.shell_env`) — never committed; only `env.example`
  (key names, no values) is published.
