# miss log（路由验收记录）

## 18/20 pass  ·  2 miss  ·  2026-09-04

| # | 任务 | 期望 | 结果 | 处置 |
|---|---|---|---|---|
| 19 | 让 SRE 查线上故障 | team/sre | ⏳ 未验证 | Step 4 roles 落地后自动关闭 |
| 20 | K8s 部署方案 | dev | ❌ 无子技能 | known_gaps，后续 `find-skills` 装 |

## 判定口径
- 任务描述 → 宿主自动触发 hub 或人工判读 hub description + 判据文本
- 路由正确：hub description/判据/跳簇规则任一能唯一指向正确簇
- 不要求 100%（路由是软机制，词面/LLM 路由的共同天花板）
