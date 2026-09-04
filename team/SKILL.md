---
name: team
description: 角色路由簇（team hub）：从 agency-agents 精选的 ~40 个角色人格 （SRE、Software Architect、Code Reviewer、Codebase Onboarding、DevOps Automator、 Technical Writer、Business/PM/Strategy/Marketing/Finance 等）+ 路由判据 + "如何请角色"（轻用：当前会话内按 persona 执行；重用：subagent 委托）。 触发 = "让 SRE/Architect 审"、"按 Product Manager 视角"、"委派给 Code Reviewer"、 "用这个角色的清单"、"角色列表"。 非触发 = 技能调用（→对应领域 hub）、工具执行（→具体技能）。 
---

# team hub — 角色路由

## 判据
- 目标是请某个专家角色做事 → 本簇
- 目标是让某个专家执行 → 本簇

## 角色索引（正文在 `../roles/<slug>.md`）
### design（设计，3）

| 角色 | 一句话 |
|---|---|
| ui-designer | Expert UI designer specializing in visual design systems, component libraries, a… |
| ux-architect | Technical architecture and UX specialist who provides developers with solid foun… |
| ux-researcher | Expert user experience researcher specializing in user behavior analysis, usabil… |

### engineering（工程，11）

| 角色 | 一句话 |
|---|---|
| code-reviewer | Expert code reviewer who provides constructive, actionable feedback focused on c… |
| codebase-onboarding-engineer | Expert developer onboarding specialist who helps new engineers understand unfami… |
| data-engineer | Expert data engineer specializing in building reliable data pipelines, lakehouse… |
| devops-automator | Expert DevOps engineer specializing in infrastructure automation, CI/CD pipeline… |
| git-workflow-master | Expert in Git workflows, branching strategies, and version control best practice… |
| incident-response-commander | Expert incident commander specializing in production incident management, struct… |
| minimal-change-engineer | Engineering specialist focused on minimum-viable diffs — fixes only what was ask… |
| prompt-engineer | Specialist in crafting, testing, and systematically optimizing prompts for LLMs … |
| software-architect | Expert software architect specializing in system design, domain-driven design, a… |
| sre | Expert site reliability engineer specializing in SLOs, error budgets, observabil… |
| technical-writer | Expert technical writer specializing in developer documentation, API references,… |

### product（产品，3）

| 角色 | 一句话 |
|---|---|
| feedback-synthesizer | Expert in collecting, analyzing, and synthesizing user feedback from multiple ch… |
| manager | Holistic product leader who owns the full product lifecycle — from discovery and… |
| sprint-prioritizer | Expert product manager specializing in agile sprint planning, feature prioritiza… |

### project-management（项目管理，3）

| 角色 | 一句话 |
|---|---|
| jira-workflow-steward | Expert delivery operations specialist who enforces Jira-linked Git workflows, tr… |
| meeting-notes-specialist | Extract structured decisions, action items, and open questions from meeting tran… |
| project-shepherd | Expert project manager specializing in cross-functional project coordination, ti… |

### security（安全，7）

| 角色 | 一句话 |
|---|---|
| ai-generated-code-auditor | Security reviewer for AI-generated and vibe-coded apps — hunts the hardcoded sec… |
| appsec-engineer | AppSec specialist who secures the software development lifecycle through threat … |
| architect | Expert security architect specializing in threat modeling, secure-by-design arch… |
| cloud-architect | Cloud-native security specialist designing zero trust architectures, implementin… |
| incident-responder | Digital forensics and incident response specialist who leads breach investigatio… |
| penetration-tester | Offensive security specialist conducting authorized penetration tests, red team … |
| senior-secops | Defensive application security specialist who scans every code submission for se… |

### testing（测试，6）

| 角色 | 一句话 |
|---|---|
| api-tester | Expert API testing specialist focused on comprehensive API validation, performan… |
| performance-benchmarker | Expert performance testing and optimization specialist focused on measuring, ana… |
| reality-checker | Stops fantasy approvals, evidence-based certification - Default to "NEEDS WORK",… |
| test-automation-engineer | Expert end-to-end test automation engineer for Playwright and Cypress — resilien… |
| test-results-analyzer | Expert test analysis specialist focused on comprehensive test result evaluation,… |
| workflow-optimizer | Expert process improvement specialist focused on analyzing, optimizing, and auto… |

## 使用方式
- **轻用**：当前会话内按该角色 persona 执行（宿主读 `roles/<slug>.md` 全文）
- **重用**：委派给 subagent，角色 md 作为其行为指令，独立上下文完成大任务
- 角色不是技能：它定义"怎么做"的立场与清单，具体能力仍需调对应 hub 的子技能
