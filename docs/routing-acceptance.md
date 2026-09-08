# Routing acceptance (miss log)

## 18/20 pass · 2 miss · 2026-09-04

| # | Task | Expected route | Result | Action |
|---|---|---|---|---|
| 19 | "Have the SRE investigate this incident" | team/sre | pending | closes automatically once roles are in place |
| 20 | K8s deployment plan | dev | no sub-skill | known gap; install a K8s skill later via find-skills |

## Judging standard
- Route is correct when the hub description, rules, or cross-hub handoff
  uniquely points to the right cluster for the described task.
- 100% is not required: routing is a soft mechanism bounded by both lexical
  and LLM-based dispatch.
