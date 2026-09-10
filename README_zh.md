# skills-hub

**别再把 200 个技能塞进 agent 的上下文窗口了。**

skills-hub 是面向编程 agent 的精选技能库：**188 个子技能 + 33 个专家角色**，归入 7 个路由
Hub。agent 看到的是极小的目录（23 个条目而非 221 个），只在任务真正需要时才拉取完整说明
——库级别的渐进式披露。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/jmche/skills-hub/actions/workflows/ci.yml/badge.svg)](https://github.com/jmche/skills-hub/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](VERSION)
[![Sub-skills](https://img.shields.io/badge/sub--skills-188-8A2BE2)](#包含内容)
[![Roles](https://img.shields.io/badge/roles-33-FF69B4)](#包含内容)
[![Hosts](https://img.shields.io/badge/hosts-7-4A90D9)](#宿主)
[![Repo size](https://img.shields.io/github/repo-size/jmche/skills-hub)](https://github.com/jmche/skills-hub)

[English](README.md) · [中文](README_zh.md) · [한국어](README_ko.md)

## 解决什么问题

把 200 个原始技能丢进 `~/.claude/skills`，每轮对话要烧掉约 2 万 token 的目录，agent 依然
在猜该用哪个技能；手动给 7 个宿主目录逐个接线更是容易出错。skills-hub 用 hub-and-spoke
布局解决：

```text
~/.agents/skills/
├── research/      ┐
├── scientific/     │  7 个 Hub — SKILL.md 只是小索引（每个子技能一行）
├── references/     │  完整说明在 <hub>/<name>/INSTRUCTIONS.md，
├── dev/            │  按需读取，绝不预载
├── data-ml/        │
├── docs-figures/   │
└── team/          ┘  33 个专家人格，按名调用或委托给 subagent
```

- **目录开销**：宿主可见 description 从 82,939 字符降到 11,898 字符（−86%）
- **按需加载**：先读 Hub 索引，只有选中的子技能才读全文
- **单一事实源**：所有宿主软链到 `~/.agents/skills` —— 改一处，全部生效，无副本漂移

![skills-hub 前后对比](docs/img/catalog.svg)

## 实际效果

**路由 —— 一次蛋白查询只触碰一个子技能：**

![路由演示：catalog → scientific hub → uniprot-database → 真实 UniProt API 结果](docs/img/demo-routing.gif)

**grounded-build（以 submodule 集成）—— 冻结 SHA 上的证据驱动规划：**

![grounded-build 演示：冻结快照 → 并行调查 → 交叉评审 → 计划 → 隔离实现](docs/img/demo-grounded-build.gif)

*（路由 GIF 全部为真实内容——真实的 hub 规则、索引行、frontmatter、API 响应，均取自本机；仅执行顺序为脚本编排。grounded-build GIF 为其文档流程的示意演示。）*

## 精选亮点

188 个中的一小部分，先看具体的：

| 技能 | 给 agent 的能力 |
|---|---|
| `scientific/alphafold2` | 从序列预测蛋白质结构 |
| `scientific/scanpy` | 完整的单细胞 RNA-seq 分析流程 |
| `scientific/gnomad-database` | 人群变异频率查询（含 API 限流处理） |
| `scientific/rdkit` | 化学信息学：描述符、子结构搜索、反应 |
| `scientific/diffdock` | 扩散模型分子对接 |
| `scientific/opentrons-integration` | 移液工作站实验协议 |
| `references/pubmed-database` | PubMed 文献检索（含限速处理） |
| `dev/ui-ux-pro-max` | 84 种 UI 风格 × 22 技术栈 |
| `team/engineering-sre` | 以 SRE 视角复盘线上故障 |

## 和其他方案的区别

| | 原始堆放（200 个目录） | Awesome-list | skills-hub |
|---|---|---|---|
| 目录开销 | 每轮 ~2 万 token | —（只是链接） | **~5K token，按需加载** |
| 策展 | 手动 | 好书单 | **已安装、可路由** |
| 路由 | agent 猜 | — | **hub 判据 + 跳簇规则** |
| 多宿主 | 手工复制 ×7 | 手动 | **每家一条软链，幂等** |
| 更新 | 重新下载 | 手动 | **一行命令** |

## 安装

一条命令（克隆到 `~/.agents/skills`，询问链接哪些宿主，检查 API key）：

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash
```

交互式挑选（逐个勾选 Hub/技能）：

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- --select
```

只装库（给 DSH 这类直接读 `~/.agents/skills` 的宿主）：

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- --skip-hosts
```

或走 npm 生态：

```bash
npx skills add jmche/skills-hub -s scientific -a claude
```

### 宿主

安装器探测已装的编程 agent，把库软链进它们的技能目录——纯增量、幂等、绝不删除你本地
已有的技能：

| 宿主 | 技能目录 | 角色目录 |
|---|---|---|
| Claude Code | `~/.claude/skills` | `~/.claude/agents` |
| Codex | `~/.codex/skills` | — |
| OpenCode | `~/.config/opencode/skills` | — |
| Cursor | `~/.cursor/skills` | `~/.cursor/agents` |
| Gemini CLI | `~/.gemini/skills` | `~/.gemini/agents` |
| GitHub Copilot | `~/.copilot/skills` | `~/.copilot/agents` |
| Hermes | `~/.hermes/skills` | — |

## 包含内容

| Hub | 子技能数 | 覆盖 |
|---|---|---|
| `research` | 14 | 实验设计、统计、标书、同行评审、学术写作 |
| `scientific` | 116 | 结构预测、基因组学、30+ 数据库、单细胞、化学信息学、临床、实验平台 |
| `references` | 20 | 文献检索、BibTeX、引文格式、专利、文档抽取 |
| `dev` | 6 | 前端、UI/UX、云、GPU、agent harness |
| `data-ml` | 21 | polars/dask、时序、统计、深度学习、图 |
| `docs-figures` | 11 | 发表级图、幻灯片、infographic、Mermaid |
| `team` | 33 角色 | SRE、PM、架构师、QA、安全… |

另有 16 个其他顶层技能：`pdf`、`docx`、`xlsx`、`pptx`、`grill-me`、`grill-with-docs`、
`find-skills`、`skill-creator`、`workflow-skill-creator`、`credentials`、`uv`、
`generate-image`、`grounded-build`（git submodule）、`omc-reference`、`autoskill`、
`product-self-knowledge`。

每个 Hub 的 `SKILL.md` 都带完整子技能索引（一行简介 + 与相邻 Hub 的路由规则）。

## 更新

任意目录一行命令：

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- update
```

或仓库内 `bash install.sh update`（git pull；grounded-build 与 archify 等 vendored 技能会自动刷新到其最新正式版）。
另有：`hidden`（列出未发布技能）· `enable <name>`（恢复启用）· `status`（安装状态）。

## API key

许多技能受益于 API key（OpenAlex、NCBI、Exa、OpenRouter…）。完整清单与申请链接见
[`env.example`](env.example)。真实值放 `~/.shell_env`（或本 README 旁的 `.env`），
并在 `~/.bashrc` 与 `~/.profile` 中 source：

```sh
[ -f "$HOME/.shell_env" ] && . "$HOME/.shell_env"
```

安装器可代为配置，并用 `bash -lc` 验证 key 对非交互 shell 可见。

## 设计要点

- **C1 门禁**：子技能目录内只有 `INSTRUCTIONS.md`、绝无多余 `SKILL.md`——防止深度
  扫描器（如 `npx skills`）把 188 个子技能重复注册成顶层技能。
- **增量宿主软链**：安装器绝不覆盖宿主已有技能，只为缺失的补链。
- **私有内容保持私有**：个人技能可与库同目录共存且不进版本控制（我们的 `gov-*`）——
  新克隆永远不会带上它们。

## 许可

库本体（路由 Hub、策展、安装器、工具）为 MIT。子技能源自上游内容，归属明细见
[`LICENSE-NOTES.md`](LICENSE-NOTES.md) 与机器可读的
[`LICENSE-AUDIT.csv`](LICENSE-AUDIT.csv)。部分子技能说明第三方工具的调用
（如 ProteinMPNN → MIT，OpenMS → BSD-3-Clause）——文档本身为 MIT，工具保持
各自宽松许可。

## 相关项目

- [grounded-build](https://github.com/jmche/grounded-build) —— 面向编程 agent 的
  仓库级落地实现规划（本库以 git submodule 集成）
- [agency-agents](https://github.com/msitarzewski/agency-agents) —— `team/` 中 33 个
  角色人格的来源（MIT）
