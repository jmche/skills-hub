# skills-hub

**에이전트 컨텍스트 창에 200개 스킬을 다시는 넣지 마세요.**

skills-hub은 코딩 에이전트를 위한 큐레이션된 스킬 라이브러리입니다. **서브스킬 188개와
전문가 역할 33개**를 7개의 라우팅 허브로 묶어, 에이전트가 아주 작은 카탈로그(221개 대신
23개)만 보고 실제 과제에 필요할 때 전체 설명을 가져오게 합니다 — 라이브러리 수준의
점진적 공개(progressive disclosure).

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/jmche/skills-hub/actions/workflows/ci.yml/badge.svg)](https://github.com/jmche/skills-hub/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](VERSION)
[![Sub-skills](https://img.shields.io/badge/sub--skills-188-8A2BE2)](#포함된-내용)
[![Roles](https://img.shields.io/badge/roles-33-FF69B4)](#포함된-내용)
[![Hosts](https://img.shields.io/badge/hosts-7-4A90D9)](#호스트)
[![Repo size](https://img.shields.io/github/repo-size/jmche/skills-hub)](https://github.com/jmche/skills-hub)

[English](README.md) · [中文](README_zh.md) · [한국어](README_ko.md)

## 해결하는 문제

원시 스킬 200개를 `~/.claude/skills`에 넣으면 매 턴 약 2만 토큰의 카탈로그가 소모되고,
에이전트는 여전히 어떤 스킬을 쓸지 추측합니다. 7개 호스트 디렉터리를 일일이 연결하는 것도
오류가 나기 쉽습니다. skills-hub은 hub-and-spoke 구조로 이를 해결합니다:

```text
~/.agents/skills/
├── research/      ┐
├── scientific/     │  7개 허브 — SKILL.md는 작은 인덱스(서브스킬당 한 줄)
├── references/     │  전체 설명은 <hub>/<name>/INSTRUCTIONS.md에 있으며,
├── dev/            │  필요할 때만 읽고 절대 미리 로드하지 않습니다
├── data-ml/        │
├── docs-figures/   │
└── team/          ┘  33개 전문가 페르소나, 이름으로 호출 또는 subagent 위임
```

- **카탈로그 비용**: 호스트에 보이는 description이 82,939자 → 11,898자(−86%)
- **온디맨드**: 허브 인덱스를 먼저 읽고, 선택된 서브스킬 본문만 로드
- **단일 진실 공급원**: 모든 호스트가 `~/.agents/skills`로 심링크 — 한 곳만 고치면
  전체 에이전트에 반영, 사본 드리프트 없음

![skills-hub 전후 비교](docs/img/catalog.svg)

## 실제 동작

**라우팅 — 단백질 조회가 건드리는 서브스킬은 정확히 하나:**

![라우팅 데모: catalog → scientific hub → uniprot-database → 실제 UniProt API 결과](docs/img/demo-routing.gif)

**grounded-build(submodule로 통합) — 고정 SHA 기반의 증거 중심 계획:**

![grounded-build 데모: 고정 스냅샷 → 병렬 조사 → 교차 리뷰 → 계획 → 격리 구현](docs/img/demo-grounded-build.gif)

*(라우팅 GIF은 전부 실제 콘텐츠 — 실제 허브 규칙, 인덱스 행, frontmatter, API 응답을 이 머신에서 캡처; 실행 순서만 스크립트로 지정. grounded-build GIF은 문서화된 흐름의 예시 데모.)*

## 하이라이트

188개 중 일부, 구체적으로:

| 스킬 | 에이전트에게 주는 능력 |
|---|---|
| `scientific/alphafold2` | 서열 기반 단백질 구조 예측 |
| `scientific/scanpy` | 단일세포 RNA-seq 전체 분석 워크플로 |
| `scientific/gnomad-database` | 인구 변이 빈도 조회(API 처리 포함) |
| `scientific/rdkit` | 화학정보학: 기술자, 부분구조 검색, 반응 |
| `scientific/diffdock` | 확산 모델 분자 도킹 |
| `scientific/opentrons-integration` | 자동 피펫팅 실험 프로토콜 |
| `references/pubmed-database` | PubMed 문헌 검색(속도 제한 처리 포함) |
| `dev/ui-ux-pro-max` | 84가지 UI 스타일 × 22 스택 |
| `team/engineering-sre` | SRE 관점의 장애 리뷰 |

## 다른 방식과의 차이

| | 원시 덤프(200 디렉터리) | Awesome-list | skills-hub |
|---|---|---|---|
| 카탈로그 비용 | 매 턴 ~2만 토큰 | —(링크만) | **~5K 토큰, 온디맨드** |
| 큐레이션 | 수동 | 좋은 읽기 목록 | **설치됨 + 라우팅** |
| 라우팅 | 에이전트가 추측 | — | **허브 규칙 + 허브 간 인계** |
| 멀티 호스트 | 수동 복사 ×7 | 수동 | **호스트당 심링크 1개, 멱등** |
| 업데이트 | 재다운로드 | 수동 | **한 줄** |

## 설치

한 줄 설치(`~/.agents/skills`에 클론, 링크할 호스트 질문, API 키 확인):

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash
```

대화형 선택(허브/스킬 하나씩 고르기):

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- --select
```

라이브러리만 설치(`~/.agents/skills`을 직접 읽는 DSH 등 호스트용):

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- --skip-hosts
```

npm 생태계 이용:

```bash
npx skills add jmche/skills-hub -s scientific -a claude
```

### 호스트

설치기는 설치된 코딩 에이전트를 감지해 스킬 디렉터리에 라이브러리를 심링크합니다 —
순수 추가 방식, 멱등, 기존 로컬 스킬은 절대 삭제하지 않습니다:

| 호스트 | 스킬 디렉터리 | 역할 디렉터리 |
|---|---|---|
| Claude Code | `~/.claude/skills` | `~/.claude/agents` |
| Codex | `~/.codex/skills` | — |
| OpenCode | `~/.config/opencode/skills` | — |
| Cursor | `~/.cursor/skills` | `~/.cursor/agents` |
| Gemini CLI | `~/.gemini/skills` | `~/.gemini/agents` |
| GitHub Copilot | `~/.copilot/skills` | `~/.copilot/agents` |
| Hermes | `~/.hermes/skills` | — |

## 포함된 내용

| Hub | 서브스킬 수 | 범위 |
|---|---|---|
| `research` | 14 | 실험 설계, 통계, 연구제안, 동료 심사, 학술 글쓰기 |
| `scientific` | 116 | 구조 예측, 유전체학, 30+ 데이터베이스, 단일세포, 화학정보학, 임상, 실험 플랫폼 |
| `references` | 20 | 논문 검색, BibTeX, 인용 형식, 특허, 문서 추출 |
| `dev` | 6 | 프론트엔드, UI/UX, 클라우드, GPU, 에이전트 하니스 |
| `data-ml` | 21 | polars/dask, 시계열, 통계, 딥러닝, 그래프 |
| `docs-figures` | 11 | 논문급 도표, 슬라이드, 인포그래픽, Mermaid |
| `team` | 33 역할 | SRE, PM, 아키텍트, QA, 보안 등 |

그 외 16개 최상위 스킬: `pdf`, `docx`, `xlsx`, `pptx`, `grill-me`,
`grill-with-docs`, `find-skills`, `skill-creator`, `workflow-skill-creator`,
`credentials`, `uv`, `generate-image`, `grounded-build`(git submodule),
`omc-reference`, `autoskill`, `product-self-knowledge`.

각 허브의 `SKILL.md`에는 한 줄 설명과 인접 허브와의 라우팅 규칙이 담긴 전체
서브스킬 인덱스가 들어 있습니다.

## 업데이트

어느 디렉터리에서든 한 줄:

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- update
```

또는 리포 안에서 `bash install.sh update`(git pull; grounded-build와 archify 등 vendored 스킬은 최신 안정판으로 자동 갱신).
기타: `hidden`(미공개 스킬 목록) · `enable <name>`(복원) · `status`(설치 상태).

## API 키

많은 스킬이 API 키를 사용합니다(OpenAlex, NCBI, Exa, OpenRouter 등). 전체 목록과
발급처는 [`env.example`](env.example) 참조. 실제 값은 `~/.shell_env`(또는 이
README 옆의 `.env`)에 넣고 `~/.bashrc` **와** `~/.profile` 양쪽에서 source:

```sh
[ -f "$HOME/.shell_env" ] && . "$HOME/.shell_env"
```

설치기가 설정을 도우며 `bash -lc`로 비대화 셸에서도 키가 보이는지 검증합니다.

## 설계 노트

- **C1 게이트**: 서브스킬 디렉터리에는 `INSTRUCTIONS.md`만 있고 `SKILL.md`는 없음 —
  깊이 탐색기(예: `npx skills`)가 188개 서브스킬을 최상위로 이중 등록하는 것을 차단.
- **추가 전용 호스트 링크**: 설치기는 호스트에 이미 있는 스킬을 절대 덮어쓰지 않고
  없는 것만 링크를 추가.
- **비공개 콘텐츠는 비공개로**: 개인 스킬은 라이브러리 옆에 두고 버전 관리에서
  제외할 수 있음(우리의 `gov-*` 사례) — 새 클론에는 절대 포함되지 않음.

## 라이선스

라이브러리(라우팅 허브, 큐레이션, 설치기, 도구)는 MIT. 서브스킬은 업스트림
콘텐츠를 큐레이션한 것으로, 출처 표기는 [`LICENSE-NOTES.md`](LICENSE-NOTES.md)와
머신리더블 [`LICENSE-AUDIT.csv`](LICENSE-AUDIT.csv) 참조. 일부 서브스킬은
서드파티 도구 호출법을 설명합니다(예: ProteinMPNN → MIT, OpenMS → BSD-3-Clause) —
문서는 MIT이며 도구는 각자의 permissive 라이선스를 유지.

## 관련 프로젝트

- [grounded-build](https://github.com/jmche/grounded-build) — 코딩 에이전트용
  리포지토리 기반 구현 계획(본 라이브러리에 git submodule로 통합)
- [agency-agents](https://github.com/msitarzewski/agency-agents) — `team/`의 33개
  역할 페르소나 출처(MIT)
