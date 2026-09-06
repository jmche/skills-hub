---
name: team
description: 角色路由簇（team hub）：从 agency-agents 精选的 ~40 个角色人格 （SRE、Software Architect、Code Reviewer、Codebase Onboarding、DevOps Automator、 Technical Writer、Business/PM/Strategy/Marketing/Finance 等）+ 路由判据 + "如何请角色"（轻用：当前会话内按 persona 执行；重用：subagent 委托）。 触发 = "让 SRE/Architect 审"、"按 Product Manager 视角"、"委派给 Code Reviewer"、 "用这个角色的清单"、"角色列表"。 非触发 = 技能调用（→对应领域 hub）、工具执行（→具体技能）。 
---

# team hub

## 判据
- 目标是请某个专家角色做事 → 本簇
- 目标是让某个专家执行 → 本簇

## 子技能索引

| 子技能 | 说明 |
|---|---|

## 跳簇规则
- 角色 persona 在 roles/*.md；执行走 subagent 或当前会话内按 persona

## 使用方式

1. 按上表选中子技能；2. 读 `skills/team/<name>/INSTRUCTIONS.md`；3. 其内部脚本/资源相对该文件所在目录解析。
