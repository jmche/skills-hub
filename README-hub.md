# ~/.agents/skills — canonical 技能 Hub

**单一事实源**：本目录即全部技能与角色的 canonical 位置。
宿主（Claude/Codex/Hermes/OpenCode/Cursor/Gemini/Copilot）通过**软链**共享这里的内容——改这里，全宿主同步；不需要逐宿主复制。

## 布局

```
~/.agents/skills/
├── <name>/SKILL.md        顶层技能（~37 个：常用工具 pdf/docx/xlsx/… + gov-* 14 个 + hub 入口 7 个）
│   ├── research/          ┐
│   ├── scientific/         │ 路由 hub：SKILL.md = 导航 + 子技能索引表
│   ├── references/         │   子技能 = <name>/INSTRUCTIONS.md（原名 SKILL.md 改名而来）
│   ├── dev/                │   子技能的 scripts/references 保持原相对路径
│   ├── data-ml/            │
│   ├── docs-figures/       │
│   └── team/               ┘ 角色路由（索引见 roles/）
├── roles/                 33 个角色人格（agency-agents MIT 精选；~/.{claude,cursor,gemini,copilot}/agents → 这里）
│   └── _source/           上游原始备份（更新 diff 用）
├── _scripts/              生成器 + 门禁 + 分发
├── _assignments.json      人工维护：218 → 顶层/7 hub 的归簇清单
├── routes_meta.yaml       人工维护：hub 的 description/判据/跳簇/scientific 分节
├── registry.json          生成物：机器索引
├── INDEX.md               生成物：人读总索引
├── env.example            模板：所有技能用到的 API key 清单（只列 key 名，含放置规则）
├── .env                   真密钥（gitignore 排除；放这里，全宿主共用）
├── _miss_log.md           路由验收记录
└── _backups/              tar.gz 归档（20260904-1640 基线）
```

## 日常三个动作

```bash
# 1. 改了 INSTRUCTIONS/frontmatter/routes_meta 之后 → 一键重新生成索引+门禁+全宿主刷新
bash _scripts/sync.sh

# 2. 路由 miss（任务没被分发到正确 hub/子技能）→
#    a) 改对应 INSTRUCTIONS.md 的 frontmatter description（加触发词 + 反向排除词）
#    b) bash _scripts/sync.sh
#    c) 记一笔 _miss_log.md

# 3. 装新技能（skills.sh 生态）→ 落到本目录后：
#    a) 加进 _assignments.json 的 top 或某 hub 列表
#    b) 若进 hub：git mv <name> <hub>/<name> && 改名 SKILL.md→INSTRUCTIONS.md
#    c) bash _scripts/sync.sh
```

## 关键规则（别破坏）

1. **子技能目录内只准出现 `INSTRUCTIONS.md`，不准有 `SKILL.md`**
   —— `npx skills`（深度扫描 3 层）等工具会把它们当独立技能重新注册，catalog 立刻打回 200+ 条目。
   check.py C1 硬门禁。
2. **深度红线**：`skills/<hub>/<name>/` 内 `INSTRUCTIONS.md` 必须正好 2 层深；`scripts/`、
   `references/` 放 `<name>/` 内部即可（它们不是技能容器）。
3. **宿主软链是增量语义**：宿主已有的同名本地技能一律保留不动（如 hermes 的 86 个本地技能）。
   断链/指向已迁移子技能的旧链接：由本 README 的清理逻辑处理，发现即删（hub 已覆盖）。
4. **roles 的宿主形态**：
   - Claude/Cursor/Gemini/Copilot：`<host>/agents → roles/`（目录软链，一角色一 md，✅）
   - Codex：需要渲染成 `~/.codex/agents/*.toml`（契约差异，见后续增强清单）
   - Hermes：建议走其 router-plugin（`delegate_task` 工具），未做
5. **备份**：`_backups/agents-backup-20260904-1640.tar.gz` 是重构前基线；
   任何大规模操作前先 `_backups/` 加一份新归档；git 是第二道兜底。

## 数字对比（重构前 → 重构后）

| 指标 | 前 | 后 |
|---|---|---|
| 宿主 catalog 顶层条目 | 218 | **37**（-83%） |
| description 常驻 token | ≈ 20.2K | ≈ 4–5K（待复测） |
| OpenCode 119 上限 | **必超限** | ✅ 3 倍余量 |
| 角色 | 散落各宿主 | `roles/` 33 个单一源 + 4 宿主软链 |

## 已知缺口（known gaps）

- **dev hub 无 K8s/部署运维技能**（路由验收 #20 miss）→ `find-skills` 装后归 dev
- **roles 无 marketing/finance**（本期只挑了工程/测试/安全/设计/产品/PM 6 类）
- **Codex roles toml 渲染**、**Hermes router-plugin** 未做
- **uniprot-database** 自带文档中 2 条上游断链（`references/id_mapping_documentation.md` 缺文件）——上游自带问题，已降级为 WARN 不阻塞

## 风险红字

**不要**直接 `rm -rf ~/.claude/skills` 之类的宿主目录——它里面混着真实目录与软链，
删宿主目录本身没问题，**但如果哪天你 `rm -rf` canonical（本目录）而宿主的软链还在**，
会留下满屏断链；恢复：解压 `_backups/` 或 `git reset --hard`。
