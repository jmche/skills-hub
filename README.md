# skills-hub

A curated agent-skill library with **routing hubs**: 200+ sub-skills grouped into
7 large hubs so hosts (Claude Code, Codex, OpenCode, Cursor, Gemini, Copilot,
Hermes, DSH) load a small catalog and pull the full instructions on demand.

> **v0.1.0** — pre-1.0 release; versioning policy below.
>Languages: [English](README.md) · [中文](README_zh.md) · [한국어](README_ko.md)

## What you get

| Hub | Sub-skills | Covers |
|---|---|---|
| `research` | 14 | experimental design, statistics, grants, peer review, academic writing |
| `scientific` | 116 | structure prediction, genomics, 30+ databases, single-cell, chem, clinical, lab platforms |
| `references` | 20 | paper search, BibTeX, citation formats, patents, document extraction |
| `dev` | 6 | frontend, UI/UX systems, cloud, GPU, agent harness |
| `data-ml` | 21 | polars/dask, time series, stats, deep learning, graphs |
| `docs-figures` | 11 | publication figures, slides, infographics, Mermaid |
| `team` | 33 roles | expert personas (SRE, PM, Architect, QA, Security, …) |

Plus 14 directly-usable top-level skills: `pdf`, `docx`, `xlsx`, `pptx`,
`find-skills`, `skill-creator`, `workflow-skill-creator`, `credentials`, `uv`,
`generate-image`, `grounded-build`, `omc-reference`, `autoskill`,
`product-self-knowledge`.

## Install

One command (installs to `~/.agents/skills`, asks which hosts to link, checks keys):

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash
```

Interactive selection (pick which hubs/skills to install):

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- --select
```

Skip host linking (library only, for DSH-style hosts that read `~/.agents/skills`):

```bash
curl -fsSL … | bash -s -- --skip-hosts
```

Alternative — npm ecosystem (`npx skills`):

```bash
npx skills add jmche/skills-hub -s scientific -a claude
```

### Hosts

The installer detects installed coding agents and offers to link the library
into their skill directories (purely additive symlinks, idempotent, never
deletes your local skills):

| Host | Skills dir | Roles dir |
|---|---|---|
| Claude Code | `~/.claude/skills` | `~/.claude/agents` |
| Codex | `~/.codex/skills` | — |
| OpenCode | `~/.config/opencode/skills` | — |
| Cursor | `~/.cursor/skills` | `~/.cursor/agents` |
| Gemini CLI | `~/.gemini/skills` | `~/.gemini/agents` |
| GitHub Copilot | `~/.copilot/skills` | `~/.copilot/agents` |
| Hermes | `~/.hermes/skills` | — |

## API keys

Many skills benefit from API keys (OpenAlex, NCBI, Exa, OpenRouter, …).
The required keys and where to get them: [`env.example`](env.example).

Put your real values in `~/.shell_env` (or `.env` in the repo root) and source
it from `~/.bashrc` **and** `~/.profile`:

```sh
[ -f "$HOME/.shell_env" ] && . "$HOME/.shell_env"
```

The installer offers to set this up (`install_env.py`) and verifies with
`bash -lc` that the keys are visible to non-interactive shells.

## Update / uninstall

```bash
bash ~/.agents/skills/install.sh update      # git pull
bash ~/.agents/skills/install.sh hidden      # list moved-away (non-published) skills
bash ~/.agents/skills/install.sh enable <name>
bash ~/.agents/skills/install.sh status
# uninstall
rm -rf ~/.agents/skills
```

## Versioning

`0.x.y` while the library is not yet product-grade (current: **v0.1.0**):

- **patch** (0.1.x) — wording/description fixes, gate & script bugfixes
- **minor** (0.y.0) — skills added/removed, hub structure changes, installer behavior
- **1.0.0** — reserved; will be tagged only on an explicit product-grade declaration

## License

MIT for the library (routing hubs, curation, installer, tooling).
Sub-skills curate upstream content; full attribution in
[`LICENSE-NOTES.md`](LICENSE-NOTES.md) and machine-readable
[`LICENSE-AUDIT.csv`](LICENSE-AUDIT.csv). Some sub-skills document how to
call third-party tools (e.g. ProteinMPNN → MIT, OpenMS → BSD-3-Clause) —
the documents stay MIT; the tools keep their own permissive licenses (see
notes).

## Maintainer tools (not needed by users)

- `sync.sh` — regenerate hub indexes, run gates, refresh host links
- `check.py` — C1–C9 consistency gates (no stray SKILL.md, links, depth, catalog size…)
- `gen_routers.py` — collect skills into hubs, render hub `SKILL.md` indexes
- `_assignments.json` / `routes_meta.yaml` — the two human-maintained inputs
