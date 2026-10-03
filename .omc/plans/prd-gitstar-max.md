# PRD: build-your-own-ai-agent

> GitHub Star 극대화를 위한 오픈소스 프로젝트 기획

---

## 1. 조사 결과 요약 (2025.01 ~ 2026.03)

### 1.1 Star 상위 카테고리 분석

| 순위 | 카테고리 | 대표 사례 | Star 범위 |
|------|----------|-----------|-----------|
| 1 | 학습 리소스/로드맵 | build-your-own-x (467K), freeCodeCamp (420K), developer-roadmap (310K) | 100K~467K |
| 2 | Curated 리스트 | awesome-python (285K), awesome-selfhosted (276K) | 100K~350K |
| 3 | AI 에이전트/도구 | n8n (160K), Ollama (160K), Langflow (140K), Dify (120K) | 50K~216K |
| 4 | AI 코딩 어시스턴트 | Gemini CLI (87K), Claude Code (72K), Cline (57K) | 50K~87K |
| 5 | 개발자 도구 | uv (80K), Hoppscotch (71K), superpowers (66K) | 40K~80K |

### 1.2 2025~2026 바이럴 사례

| 프로젝트 | Star 수 | 성장 속도 | 핵심 요인 |
|----------|---------|-----------|-----------|
| OpenClaw | 216K | 14일에 190K | 멀티플랫폼 AI 에이전트 (WhatsApp/Telegram/Discord) |
| system-prompts-and-models | 122K | 1주에 +7,784 | AI 도구 시스템 프롬프트 공개 (투명성) |
| DeepSeek-R1 | 77K | 1일에 +10,000 | GPT-4급 오픈소스 LLM |
| superpowers | 66K | 1주에 +6,964 | Claude Code 스킬 프레임워크 |
| browser-use | 74K | 51명 기여자로 21K | AI 브라우저 자동화 |
| OpenCut | 44K | 수일 내 수만 | CapCut 오픈소스 대안 |

### 1.3 Star-to-Effort 비율 (높은 순)

1. **Curated 리스트** - 코드 없음, 커뮤니티가 PR로 기여, SEO 우수
2. **학습 리소스/로드맵** - 에버그린 콘텐츠, 교육기관이 공유
3. **"build-your-own-X" 형태** - 실습 코드 + 학습 = 최강 조합 (467K star 실증)
4. **CLI 개발자 도구** - 즉시 유용, 블로그/SNS 공유
5. **셀프호스팅 대안** - "데이터 주권" 내러티브

### 1.4 2026년 3월 현재 트렌드

- **Skill Engineering**: 구조화된 SKILL.md로 AI 에이전트에 방법론 주입
- **Context Engineering**: LLM 컨텍스트 윈도우 관리가 독립 엔지니어링 분야로 부상
- **MCP 생태계 폭발**: Linux Foundation 기부, 9,700만 월간 SDK 다운로드
- **Multi-Agent Orchestration**: 복수 AI 에이전트 조율 인프라
- **On-Device AI**: 엣지 디바이스에서 LLM 실행
- **Vibe Coding 반발**: 구조화된 개발 방법론 수요 급증

---

## 2. 선정 주제: `build-your-own-ai-agent`

### 2.1 왜 이 주제인가

**"build-your-own-X" 포맷 + "AI Agent" 주제 = 검증된 최고 조합**

| 근거 | 데이터 |
|------|--------|
| 포맷 실증 | build-your-own-x가 GitHub 전체 1위 (467K star) |
| 주제 실증 | AI Agent가 2025-2026 GitHub에서 가장 빠르게 성장하는 카테고리 |
| 경쟁 공백 | "build-your-own-x"에 AI Agent 전용 버전이 아직 없음 |
| 타겟 크기 | GitHub에 AI 관련 repo 430만개, 개발자 1.8억명 |
| 에버그린 | AI Agent 기술은 최소 3-5년간 메인스트림 |
| 다국어 잠재력 | 한/영/중/일 README로 글로벌 Star 확보 |

### 2.2 프로젝트 컨셉

**"Build Your Own AI Agent"** - 처음부터 직접 만들며 배우는 AI 에이전트 개발 가이드

- 각 챕터마다 **실행 가능한 코드**로 하나의 AI 에이전트를 처음부터 구축
- 이론 설명 최소화, **실습 중심** (Learn by Building)
- 초급(챗봇) → 중급(RAG) → 고급(멀티에이전트) 점진적 난이도
- Python 기반 (GitHub 2위 언어, AI 생태계 표준)
- 각 프로젝트는 **독립적**으로 실행 가능 (의존성 최소화)

---

## 3. 목표 (Goals)

### 3.1 Star 목표

| 마일스톤 | 기간 | 전략 |
|----------|------|------|
| 100 stars | 1주 | 개인 네트워크 + Reddit/HN 런칭 |
| 1,000 stars | 1개월 | Hacker News Show HN + Dev.to 포스트 |
| 5,000 stars | 3개월 | GitHub Trending 진입 + 뉴스레터 |
| 10,000 stars | 6개월 | 지속적 콘텐츠 추가 + 커뮤니티 기여 |
| 50,000+ stars | 12개월+ | awesome list 등재 + 다국어 + 컨퍼런스 |

### 3.2 기능 목표

1. 최소 10개의 독립적인 AI 에이전트 빌드 프로젝트 제공
2. 각 프로젝트는 `pip install -r requirements.txt && python main.py`로 즉시 실행 가능
3. 한국어 + 영어 동시 지원 (README, 문서)
4. 시각적 아키텍처 다이어그램 포함
5. 각 프로젝트 30분 이내 완료 가능

### 3.3 비목표 (Non-Goals)

- 프레임워크나 라이브러리 개발이 아님 (교육 리소스)
- 프로덕션 코드 품질을 목표로 하지 않음 (학습 목적)
- 특정 LLM 벤더 종속 없음 (Ollama/OpenAI/Anthropic 모두 지원)
- 모바일/웹 프론트엔드 개발 없음 (CLI/터미널 중심)

---

## 4. 프로젝트 구조

```
build-your-own-ai-agent/
├── README.md                          # 영어 (메인)
├── README.ko.md                       # 한국어
├── README.zh.md                       # 중국어 (추후)
├── README.ja.md                       # 일본어 (추후)
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # 기여 가이드
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/                     # CI: 각 프로젝트 실행 테스트
├── assets/
│   ├── banner.png                     # 히어로 배너 이미지
│   ├── architecture/                  # 아키텍처 다이어그램
│   └── demos/                         # GIF 데모
├── 01-simple-chatbot/                 # 레벨 1: 기초
│   ├── README.md
│   ├── main.py
│   ├── requirements.txt
│   └── architecture.png
├── 02-tool-calling-agent/             # 레벨 1: Tool Use
│   ├── README.md
│   ├── main.py
│   ├── tools.py
│   └── requirements.txt
├── 03-rag-agent/                      # 레벨 2: RAG
│   ├── README.md
│   ├── main.py
│   ├── retriever.py
│   ├── vector_store.py
│   └── requirements.txt
├── 04-web-browsing-agent/             # 레벨 2: 브라우저 자동화
│   ├── README.md
│   ├── main.py
│   ├── browser.py
│   └── requirements.txt
├── 05-code-generation-agent/          # 레벨 2: 코드 생성
│   ├── README.md
│   ├── main.py
│   ├── sandbox.py
│   └── requirements.txt
├── 06-memory-agent/                   # 레벨 2: 장기 메모리
│   ├── README.md
│   ├── main.py
│   ├── memory.py
│   └── requirements.txt
├── 07-mcp-agent/                      # 레벨 3: MCP 프로토콜
│   ├── README.md
│   ├── main.py
│   ├── mcp_server.py
│   ├── mcp_client.py
│   └── requirements.txt
├── 08-multi-agent-system/             # 레벨 3: 멀티에이전트
│   ├── README.md
│   ├── main.py
│   ├── orchestrator.py
│   ├── agents/
│   └── requirements.txt
├── 09-voice-agent/                    # 레벨 3: 음성 에이전트
│   ├── README.md
│   ├── main.py
│   ├── stt.py
│   ├── tts.py
│   └── requirements.txt
├── 10-autonomous-agent/               # 레벨 4: 자율 에이전트
│   ├── README.md
│   ├── main.py
│   ├── planner.py
│   ├── executor.py
│   ├── evaluator.py
│   └── requirements.txt
├── 11-skill-based-agent/              # 레벨 4: 스킬 엔지니어링 (2026 트렌드)
│   ├── README.md
│   ├── main.py
│   ├── skill_loader.py
│   ├── skills/
│   └── requirements.txt
└── 12-local-llm-agent/               # 보너스: Ollama 로컬 에이전트
    ├── README.md
    ├── main.py
    └── requirements.txt
```

---

## 5. 각 프로젝트 상세

### 01. Simple Chatbot (초급, 15분)
- **배우는 것**: LLM API 호출, 대화 기록 관리, 스트리밍 응답
- **기술**: OpenAI API or Ollama
- **결과물**: 터미널 챗봇

### 02. Tool-Calling Agent (초급, 20분)
- **배우는 것**: Function calling, 도구 정의, 에이전트 루프
- **기술**: Tool use pattern, JSON Schema
- **결과물**: 날씨/계산/검색이 가능한 에이전트

### 03. RAG Agent (중급, 30분)
- **배우는 것**: 문서 임베딩, 벡터 검색, 컨텍스트 주입
- **기술**: ChromaDB, sentence-transformers
- **결과물**: PDF 문서 질의응답 에이전트

### 04. Web Browsing Agent (중급, 30분)
- **배우는 것**: 브라우저 자동화, HTML 파싱, 에이전트 의사결정
- **기술**: Playwright, BeautifulSoup
- **결과물**: 웹 검색 및 정보 추출 에이전트

### 05. Code Generation Agent (중급, 25분)
- **배우는 것**: 코드 생성, 샌드박스 실행, 오류 자가 수정
- **기술**: subprocess, AST parsing
- **결과물**: 코드 작성 + 실행 + 디버깅 에이전트

### 06. Memory Agent (중급, 25분)
- **배우는 것**: 단기/장기 메모리, 메모리 검색, 개인화
- **기술**: SQLite, embedding similarity
- **결과물**: 이전 대화를 기억하는 에이전트

### 07. MCP Agent (고급, 30분)
- **배우는 것**: Model Context Protocol, 서버/클라이언트 구현
- **기술**: MCP SDK, stdio transport
- **결과물**: MCP 서버 + 이를 사용하는 에이전트

### 08. Multi-Agent System (고급, 30분)
- **배우는 것**: 에이전트 오케스트레이션, 역할 분담, 협업 패턴
- **기술**: 메시지 패싱, 공유 상태
- **결과물**: Researcher + Writer + Reviewer 3인 팀 에이전트

### 09. Voice Agent (고급, 30분)
- **배우는 것**: STT, TTS, 실시간 음성 파이프라인
- **기술**: Whisper, edge-tts
- **결과물**: 음성으로 대화하는 AI 에이전트

### 10. Autonomous Agent (최고급, 30분)
- **배우는 것**: 계획-실행-평가 루프, 자기 반성, 목표 분해
- **기술**: ReAct pattern, self-reflection
- **결과물**: 복잡한 작업을 자율적으로 완료하는 에이전트

### 11. Skill-Based Agent (최고급, 30분) - 2026 트렌드
- **배우는 것**: 스킬 정의/로딩, 동적 능력 확장, 컨텍스트 엔지니어링
- **기술**: YAML skill definitions, dynamic loading
- **결과물**: 플러그인처럼 스킬을 추가할 수 있는 에이전트

### 12. Local LLM Agent (보너스, 20분)
- **배우는 것**: Ollama 설정, 로컬 추론, 프라이버시 보존
- **기술**: Ollama API, quantized models
- **결과물**: 인터넷 없이 동작하는 완전 로컬 에이전트

---

## 6. README 전략 (Star 극대화)

### 6.1 Above-the-fold (첫 화면)

```markdown
<!-- 히어로 배너: 깔끔한 타이포그래피 + 에이전트 아이콘 -->
<p align="center">
  <img src="assets/banner.png" width="800" />
</p>

<h1 align="center">Build Your Own AI Agent</h1>
<p align="center">
  <b>12 practical projects to master AI agents from scratch</b>
</p>

<!-- 배지 -->
<p align="center">
  <img src="https://img.shields.io/github/stars/..." />
  <img src="https://img.shields.io/github/license/..." />
  <img src="https://img.shields.io/badge/projects-12-blue" />
  <img src="https://img.shields.io/badge/python-3.10+-green" />
</p>

<!-- 30초 데모 GIF -->
<p align="center">
  <img src="assets/demos/hero-demo.gif" width="600" />
</p>

<!-- 한 줄 요약 -->
> Learn to build AI agents by actually building them.
> No frameworks, no magic — just Python and an LLM.

<!-- 다국어 링크 -->
🌍 [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md)
```

### 6.2 프로젝트 테이블 (스크롤 유도)

시각적 프로그레스 트래커 + 난이도별 이모지 + 소요시간

### 6.3 Star CTA

```markdown
---
If this helped you understand AI agents better, please ⭐ star this repo —
it helps others discover it too!
---
```

---

## 7. 런칭 전략

### Phase 1: Pre-launch (1주)
- [ ] 프로젝트 01-04 완성 (MVP)
- [ ] README 영문/한국어 완성
- [ ] 히어로 배너 + 데모 GIF 제작
- [ ] GitHub Topics 설정: `ai-agent`, `llm`, `tutorial`, `python`, `learn-by-doing`
- [ ] 관련 Discord/Reddit 커뮤니티 가입 및 활동 시작

### Phase 2: Launch Day (화~목 중 택1)
- [ ] Hacker News "Show HN" 포스트 (미국 동부 오전 9시)
- [ ] Reddit r/MachineLearning, r/Python, r/artificial 포스트
- [ ] Twitter/X 스레드 + Demo GIF
- [ ] 개인 네트워크 DM (초기 Star 씨딩)

### Phase 3: Amplification (1-4주)
- [ ] Dev.to "How I Built This" 블로그 포스트
- [ ] awesome-python, awesome-machine-learning PR 제출
- [ ] 프로젝트 05-08 추가 (주 1개씩)
- [ ] GitHub Trending 진입 모니터링

### Phase 4: Sustain (2-6개월)
- [ ] 프로젝트 09-12 추가
- [ ] 중국어/일본어 README
- [ ] Python Weekly, TLDR AI 뉴스레터 피칭
- [ ] 기여자 유치 (Good First Issue 라벨)

---

## 8. 수용 기준 (Acceptance Criteria)

### 8.1 필수 (MVP)
- [ ] 최소 4개 프로젝트 (01-04) 완성
- [ ] 각 프로젝트는 `pip install -r requirements.txt && python main.py`로 실행 가능
- [ ] 영문 README 완성 (배너, 데모 GIF, 프로젝트 목록, Star CTA)
- [ ] 한국어 README 완성
- [ ] MIT 라이센스
- [ ] CONTRIBUTING.md
- [ ] GitHub Actions CI (각 프로젝트 실행 테스트)
- [ ] 각 프로젝트별 아키텍처 다이어그램

### 8.2 확장 (Post-MVP)
- [ ] 12개 전체 프로젝트 완성
- [ ] 중국어/일본어 README
- [ ] 각 프로젝트별 데모 GIF
- [ ] GitHub Pages 문서 사이트
- [ ] awesome 리스트 3개 이상 등재

---

## 9. 기술 제약

- **Python 3.10+** (가장 넓은 호환성)
- **외부 서비스 최소화**: Ollama로 로컬 실행 가능한 옵션 항상 제공
- **프레임워크 최소**: LangChain/LlamaIndex 등 사용하지 않음 (학습 목적상 직접 구현)
- **각 프로젝트 독립**: 공유 라이브러리 없음, 각각 self-contained
- **파일 수 최소**: 프로젝트당 최대 5개 파일

---

## 10. 리스크 및 대응

| 리스크 | 영향 | 대응 |
|--------|------|------|
| 유사 프로젝트 선점 | Star 분산 | 차별화: "프레임워크 없이 순수 Python" 강조 |
| LLM API 비용 | 실행 장벽 | Ollama 로컬 실행 옵션 항상 제공 |
| API 변경 | 코드 깨짐 | CI 자동 테스트 + 버전 핀닝 |
| 콘텐츠 부실 | Star 정체 | 주 1개 프로젝트 추가 (지속적 활동 신호) |
| 다국어 번역 품질 | 신뢰도 | 네이티브 리뷰어 확보 |

---

## 11. 구현 순서 (Phases)

### Phase 1: Foundation (1-2일)
1. 리포지토리 초기화 (README, LICENSE, CONTRIBUTING, .github)
2. 히어로 배너 및 에셋 디렉토리 구성
3. 프로젝트 01: Simple Chatbot 구현
4. 프로젝트 02: Tool-Calling Agent 구현

### Phase 2: Core Projects (3-5일)
5. 프로젝트 03: RAG Agent 구현
6. 프로젝트 04: Web Browsing Agent 구현
7. GitHub Actions CI 설정
8. 데모 GIF 제작
9. 영문/한국어 README 완성

### Phase 3: Advanced Projects (1-2주)
10. 프로젝트 05-08 구현
11. 아키텍처 다이어그램 제작
12. 런칭 실행

### Phase 4: Expert Projects (2-4주)
13. 프로젝트 09-12 구현
14. 다국어 README 확장
15. 커뮤니티 성장 활동

---

*PRD 생성일: 2026-03-01*
*경로: .omc/plans/prd-gitstar-max.md*
