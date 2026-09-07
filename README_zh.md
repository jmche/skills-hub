# skills-hub

带**路由 Hub**的精选 Agent 技能库：200+ 子技能归入 7 个大 Hub，让宿主（Claude Code、Codex、OpenCode、Cursor、Gemini、Copilot、Hermes、DSH）只加载很小的 catalog，按需再拉取完整说明。

> **v0.1.0** —— 1.0 之前的预发布版本；版本策略见下方。
>语言：[English](README.md) · [中文](README_zh.md) · [한국어](README_ko.md)

## 包含内容

| Hub | 子技能数 | 覆盖 |
|---|---|---|
| `research` | 14 | 实验设计、统计、标书、同行评审、学术写作 |
| `scientific` | 116 | 结构预测、基因组学、30+ 数据库、单细胞、化学、临床、实验平台 |
| `references` | 20 | 文献检索、BibTeX、引文格式、专利、文档抽取 |
| `dev` | 6 | 前端、UI/UX、云、GPU、Agent harness |
| `data-ml` | 21 | polars/dask、时序、统计、深度学习、图 |
| `docs-figures` | 11 | 发表级图、幻灯片、infographic、Mermaid |
| `team` | 33 角色 | 专家人格（SRE、PM、架构师、QA、安全…） |

另有 14 个顶层可用技能：`pdf`、`docx`、`xlsx`、`pptx`、`find-skills`、`skill-creator`、`workflow-skill-creator`、`credentials`、`uv`、`generate-image`、`grounded-build`、`omc-reference`、`autoskill`、`product-self-knowledge`。

## 安装

一条命令（安装到 `~/.agents/skills`，询问要链接哪些宿主，检查 API key）：

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash
```

交互式选择（挑选要装的 Hub/技能）：

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- --select
```

跳过宿主链接（只装库，供直接读 `~/.agents/skills` 的宿主，如 DSH）：

```bash
curl -fsSL … | bash -s -- --skip-hosts
```

另一种方式 —— npm 生态（`npx skills`）：

```bash
npx skills add jmche/skills-hub -s scientific -a claude
```

## API 密钥

许多技能需要 API key（OpenAlex、NCBI、Exa、OpenRouter 等）。密钥清单与申请地址见 [`env.example`](env.example)。

真实值放 `~/.shell_env`（或仓库根 `.env`），并在 `~/.bashrc` **与** `~/.profile` 中 source：

```sh
[ -f "$HOME/.shell_env" ] && . "$HOME/.shell_env"
```

安装器会引导配置（`install_env.py`），并用 `bash -lc` 验证非交互 shell 可见性。

## 更新 / 卸载

```bash
bash ~/.agents/skills/install.sh update       # git pull
bash ~/.agents/skills/install.sh hidden       # 列出被移走的（未发布）技能
bash ~/.agents/skills/install.sh enable <name>
bash ~/.agents/skills/install.sh status
# 卸载
rm -rf ~/.agents/skills
```

## 版本策略

`0.x.y`，产品级完成前停留在 1.0 之下（当前 **v0.1.0**）：

- **patch**（0.1.x）——文案/描述修正、门禁与脚本 bug 修复
- **minor**（0.y.0）——新增/移除技能、Hub 结构变化、安装器行为变化
- **1.0.0**——保留版本号，仅在明确宣布产品级完成时打上

## 许可

库本体（路由 Hub、策展、安装器、工具）为 MIT。子技能来自上游内容，完整归属见
[`LICENSE-NOTES.md`](LICENSE-NOTES.md) 与机器可读的
[`LICENSE-AUDIT.csv`](LICENSE-AUDIT.csv)。部分子技能说明调用第三方工具
（如 ProteinMPNN → MIT，OpenMS → BSD-3-Clause）——文档本身仍是 MIT，工具保持
各自的宽松许可（见说明）。

## 维护者工具（使用者不需要）

- `sync.sh` —— 重新生成 Hub 索引、跑门禁、刷新宿主链接
- `check.py` —— C1–C9 一致性门禁
- `gen_routers.py` —— 收集技能入 Hub、渲染 Hub 的 `SKILL.md` 索引
- `_assignments.json` / `routes_meta.yaml` —— 两个人工维护的输入
