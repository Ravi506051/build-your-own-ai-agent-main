# Execution Prompt for build-your-own-ai-agent

아래 프롬프트를 복사해서 새 세션에서 사용하세요.

---

## 실행 프롬프트 (복사용)

```
CLAUDE.md와 .omc/plans/prd-gitstar-max.md를 읽고 build-your-own-ai-agent 프로젝트를 구축하라.

⚠️ 절대 규칙:
- Claude는 .py, .js, .html 파일 직접 작성/실행 금지
- 모든 코드/문서는 omc-teams(codex/gemini)에 위임
- Claude 역할: 태스크 설계 → omc-teams 호출 → 결과 읽기 → progress.md 기록 → git 커밋
- 위반 시: 즉시 중단하고 omc-teams로 재위임

파이프라인 (매 iteration):
1. 태스크 설계: 이번에 만들 프로젝트 2개 + 문서 1개 선정
2. omc-teams 호출: codex 2명(코드) + gemini 1명(문서) 병렬 위임
3. 결과 대기: omc_run_team_wait
4. 검증: 파일 존재 + python -m py_compile + README 구조 확인
5. 기록: progress.md 업데이트 + git 커밋
6. 다음 iteration 설계 → 1번 반복

Phase 순서:
- Phase 1 (iter 1-2): 리포 초기화 + 프로젝트 01-02 + 메인 README 초안
- Phase 2 (iter 3-5): 프로젝트 03-06 + 메인 README 완성 (영/한)
- Phase 3 (iter 6-8): 프로젝트 07-10 + CI/CD
- Phase 4 (iter 9-10): 프로젝트 11-12 + CONTRIBUTING + LICENSE + 최종검증

Worker 역할:
- codex: Python 코드 구현 (main.py, tools.py 등 + requirements.txt)
- gemini: README.md, 다국어 문서, 아키텍처 다이어그램
- claude(검증): py_compile, 파일 구조 확인, 품질 체크

omc-teams 호출 예시:
/omc-teams 2:codex,1:gemini "Phase 1 tasks"

태스크 상세 템플릿 (codex용):
- 프로젝트 경로와 파일 목록 명시
- 기능 요구사항 5줄 이내
- "Ollama + OpenAI 모두 지원" 필수
- "python main.py로 즉시 실행 가능" 필수
- "파일당 200줄 이내" 필수

태스크 상세 템플릿 (gemini용):
- What You'll Learn / Architecture / Quick Start / How It Works / Key Concepts
- Mermaid 다이어그램 포함
- 영어 작성

종료 조건: 12개 프로젝트 전부 완성 + 메인 README(영/한) + CI + LICENSE + CONTRIBUTING
stop이라고 할 때까지 계속 iteration 반복.
```

---

## 빠른 시작 (Phase 1만)

```
CLAUDE.md 읽고 Phase 1만 실행하라.

⚠️ Claude는 .py 파일 직접 작성 금지. omc-teams로 위임.

Iteration 1:
1. 리포 초기 구조 생성 (디렉토리, LICENSE, .gitignore)
2. omc-teams 호출:
   - codex #1: 01-simple-chatbot/ (main.py + requirements.txt)
   - codex #2: 02-tool-calling-agent/ (main.py + tools.py + requirements.txt)
   - gemini #1: 메인 README.md 초안 (배너 자리, 프로젝트 테이블, Star CTA)
3. 결과 대기 + 검증 + git 커밋

Iteration 2:
1. omc-teams 호출:
   - codex #1: 01-simple-chatbot/README.md 코드 설명
   - codex #2: 02-tool-calling-agent/README.md 코드 설명
   - gemini #1: README.ko.md 한국어 버전
2. 결과 대기 + 검증 + git 커밋
3. Phase 1 완료 보고

stop까지 계속.
```

---

## 단일 프로젝트 추가 (ad-hoc)

```
CLAUDE.md 읽고 프로젝트 {번호}만 추가하라.

omc-teams로 위임:
- codex: {번호}-{이름}/ 코드 구현
- gemini: {번호}-{이름}/README.md 문서

결과 검증 후 git 커밋.
```
