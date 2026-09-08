# skills-hub

**라우팅 허브**가 있는 큐레이션된 에이전트 스킬 라이브러리입니다. 200개 이상의
서브스킬을 7개의 큰 허브로 묶어, 호스트(Claude Code, Codex, OpenCode, Cursor,
Gemini, Copilot, Hermes, DSH)가 매우 작은 catalog만 로드하고 필요 시 전체
설명을 가져오게 합니다.

> **v0.1.0** — 1.0 이전의 프리릴리스. 버전 정책은 아래 참조.
>Language: [English](README.md) · [中文](README_zh.md) · [한국어](README_ko.md)

## 포함된 내용

| Hub | 서브스킬 수 | 범위 |
|---|---|---|
| `research` | 14 | 실험 설계, 통계, 연구 제안(그랜트), 동료 심사, 학술 글쓰기 |
| `scientific` | 116 | 구조 예측, 유전체학, 30+ 데이터베이스, 단일세포, 화학, 임상, 실험 플랫폼 |
| `references` | 20 | 논문 검색, BibTeX, 인용 형식, 특허, 문서 추출 |
| `dev` | 6 | 프론트엔드, UI/UX, 클라우드, GPU, 에이전트 하니스 |
| `data-ml` | 21 | polars/dask, 시계열, 통계, 딥러닝, 그래프 |
| `docs-figures` | 11 | 논문급 도표, 슬라이드, 인포그래픽, Mermaid |
| `team` | 33 역할 | 전문가 페르소나(SRE, PM, 아키텍트, QA, 보안 등) |

그 외 16개의 최상위 스킬: `pdf`, `docx`, `xlsx`, `pptx`, `grill-me`, `grill-with-docs`,
`find-skills`, `skill-creator`, `workflow-skill-creator`, `credentials`, `uv`, `generate-image`,
`grounded-build`, `omc-reference`, `autoskill`, `product-self-knowledge`.

## 설치

한 줄 설치(`~/.agents/skills`에 설치, 링크할 호스트 선택, API 키 확인):

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash
```

대화형 선택(装할 허브/스킬 골라짐):

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- --select
```

호스트 링크 없이 라이브러리만 (`~/.agents/skills`을 직접 읽는 DSH 등 호스트용):

```bash
curl -fsSL … | bash -s -- --skip-hosts
```

대안 — npm 생태계 (`npx skills`):

```bash
npx skills add jmche/skills-hub -s scientific -a claude
```

## API 키

많은 스킬이 API 키를 사용합니다(OpenAlex, NCBI, Exa, OpenRouter 등).
필요 키 목록과 발급처는 [`env.example`](env.example) 참조.

실제 값은 `~/.shell_env`(또는 리포 루트의 `.env`)에 넣고,
`~/.bashrc` **와** `~/.profile` 두 곳에서 source해야 합니다:

```sh
[ -f "$HOME/.shell_env" ] && . "$HOME/.shell_env"
```

설치기는 키 설정을 도와주며(`install_env.py`), `bash -lc`로 비대화(shell)
환경에서 잘 보이는지 검증합니다.

## 업데이트 / 제거

한 줄 업데이트, 어느 디렉터리에서든 실행 가능(리포 진입 불필요):

```bash
curl -fsSL https://raw.githubusercontent.com/jmche/skills-hub/main/install.sh | bash -s -- update
```

또는 리포 안에서:

```bash
bash ~/.agents/skills/install.sh update       # git pull + submodule 동기화
bash ~/.agents/skills/install.sh hidden       # 옮기진(未공개) 스킬 목록
bash ~/.agents/skills/install.sh enable <name>
bash ~/.agents/skills/install.sh status
# 제거
rm -rf ~/.agents/skills
```

## 버전 정책

제품 수준(v1.0)에 도달하기 전까지 `0.x.y` 유지(현재 **v0.1.0**):

- **patch**(0.1.x) — 문구/설명 수정, 게이트·스크립트 버그 수정
- **minor**(0.y.0) — 스킬 추가/삭제, 허브 구조 변화, 설치기 동작 변화
- **1.0.0** — 예약. 명시적으로 제품 수준을 선언했을 때만 태깅

## 라이선스

라이브러리(라우팅 허브, 큐레이션, 설치기, 도구)는 MIT.
서브스킬은 업스트림 콘텐츠를 큐레이션한 것이며, 전체 출처 표기는
[`LICENSE-NOTES.md`](LICENSE-NOTES.md) 및 머신리더블
[`LICENSE-AUDIT.csv`](LICENSE-AUDIT.csv) 참조. 일부 서브스킬은
서드파티 도구 호출 방법을 설명합니다(예: ProteinMPNN → MIT, OpenMS →
BSD-3-Clause) — 문서는 MIT이며 도구는 각자의 permissive 라이선스를 유지합니다
(상세 참조).

## 유지보수자 도구(사용자 불필요)

- `sync.sh` — 허브 인덱스 재생성, 게이트 실행, 호스트 링크 갱신
- `check.py` — C1–C9 일관성 게이트
- `gen_routers.py` — 스킬을 허브로 수집, 허브 `SKILL.md` 인덱스 렌더링
- `_assignments.json` / `routes_meta.yaml` — 사람이 유지하는 두 입력 파일
