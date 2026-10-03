<div align="center">

# 나만의 AI 에이전트 만들기
### AI 에이전트를 처음부터 직접 만드는 12개의 실전 프로젝트

[![GitHub stars](https://img.shields.io/github/stars/lay4/build-your-own-ai-agent?style=for-the-badge&color=ffd700)](https://github.com/lay4/build-your-own-ai-agent/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Projects: 12](https://img.shields.io/badge/Projects-12-success.svg?style=for-the-badge)](./)

**직접 만들어보며 AI 에이전트 구축 방법을 배우세요. 프레임워크나 마법 같은 도구 없이, 오직 Python과 LLM만 사용합니다.**

[English](./README.md) | [한국어](./README.ko.md) | [中文](./README.zh.md) | [日本語](./README.ja.md)

---
</div>

## 🚀 프로젝트의 취지

2025-2026년의 AI 생태계는 "코드 한 줄로 만드는 에이전트"를 약속하는 무거운 프레임워크들이 주도하고 있습니다. 이러한 도구들은 실제 서비스 구축에는 훌륭할지 몰라도, 에이전트가 어떻게 추론하고 계획하며 작업을 수행하는지에 대한 핵심 메커니즘을 추상화 계층 뒤에 숨겨버리는 "블랙박스"가 되기도 합니다.

이 저장소는 그런 마법 같은 포장지를 걷어내기 위해 만들어졌습니다. 단순한 도구 호출 루프부터 복잡한 멀티 에이전트 오케스트레이션에 이르기까지, 현대적인 AI 에이전트의 핵심 패턴을 **순수 Python**으로 구현합니다. 이를 처음부터 직접 구축함으로써, AI 시스템을 효과적으로 디버깅하고 최적화하며 나아가 확장하는 데 필요한 통찰력을 얻을 수 있습니다.

숙련된 엔지니어이든 LLM을 막 시작한 입문자이든, 이 시리즈는 차세대 자율 소프트웨어를 구동하는 아키텍처 패턴을 마스터할 수 있는 실전적인 길을 제시합니다.

## 🛠️ 로드맵

| # | 프로젝트 | 난이도 | 소요 시간 | 구현 내용 |
| :--- | :--- | :--- | :--- | :--- |
| 01 | **Simple Chatbot** | 초급 | 15분 | 스트리밍 응답과 기본적인 상태 관리가 가능한 터미널 챗봇 구축 |
| 02 | **Tool-Calling Agent** | 초급 | 20분 | 외부 함수 호출을 통해 실제 세상과 상호작용하는 에이전트 구현 |
| 03 | **RAG Agent** | 중급 | 30분 | 문서 기반 질의응답을 위한 검색 증강 생성(Retrieval-Augmented Generation) 구현 |
| 04 | **Web Browsing Agent** | 중급 | 30분 | 웹을 탐색, 검색하고 정보를 추출하는 에이전트 구축 |
| 05 | **Code Gen Agent** | 중급 | 25분 | 샌드박스 환경에서 Python 코드를 작성, 실행하고 스스로 수정하는 에이전트 |
| 06 | **Memory Agent** | 중급 | 25분 | 장기 기억 저장소와 대화형 메모리 아키텍처 구현 |
| 07 | **MCP Agent** | 고급 | 30분 | 표준화된 도구 접근을 위한 Model Context Protocol 연동 |
| 08 | **Multi-Agent System** | 고급 | 30분 | 공통의 목표를 위해 협업하는 특화된 에이전트 팀 구축 |
| 09 | **Voice Agent** | 고급 | 30분 | 자연스러운 음성 상호작용을 위한 저지연 Speech-to-Speech 에이전트 |
| 10 | **Autonomous Agent** | 전문가 | 30분 | 복잡한 목표를 실행 가능한 단계로 스스로 분해하는 자율 계획 에이전트 |
| 11 | **Skill-Based Agent** | 전문가 | 30분 | 새로운 능력을 동적으로 로드하고 학습하는 확장 가능한 에이전트 |
| 12 | **Local LLM Agent** | 보너스 | 20분 | Ollama와 로컬 모델을 사용하여 완전히 오프라인으로 작동하는 개인용 에이전트 |

## ⚡ 퀵 스타트

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/build-your-own-ai-agent.git
cd build-your-own-ai-agent

# 2. 가상 환경 설정
python -m venv venv
source venv/bin/activate  # Windows의 경우: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 첫 번째 프로젝트 실행
cd 01-simple-chatbot
python main.py
```

## 📋 사전 준비 사항

- **Python 3.10+**: 코드베이스는 현대적인 타입 힌트와 비동기(async) 기능을 사용합니다.
- **API 키 또는 로컬 LLM**:
  - [OpenAI API Key](https://platform.openai.com/) (입문자에게 권장)
  - **또는** 로컬 모델 실행을 위한 [Ollama](https://ollama.com/) 설치
- **기본적인 Python 지식**: `async/await` 및 기본적인 객체 지향 프로그래밍에 대한 이해

## 🧠 각 프로젝트의 작동 방식

이 시리즈의 모든 프로젝트는 **독립적**으로 설계되었습니다.
- **`main.py`**: 에이전트의 진입점(Entry point).
- **`core.py`**: 외부 에이전트 프레임워크 없이 작성된 에이전트의 로직과 "두뇌".
- **`README.md`**: 각 폴더에는 도입된 개념에 대한 자세한 설명이 포함되어 있습니다.

진행 과정은 선형적입니다. 단순한 텍스트 루프로 시작하여 도구 스키마, 벡터 임베딩, 상태 머신(State machines), 멀티 에이전트 코디네이션과 같은 개념을 점진적으로 소개합니다.

## 🤝 기여하기

기여는 언제나 환영합니다! 패턴을 구현하는 더 나은 방법이 있거나 새로운 프로젝트를 추가하고 싶다면 자유롭게 Pull Request를 열어주세요. 자세한 내용은 `CONTRIBUTING.md`를 참고해 주세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

---

<div align="center">

### 이 프로젝트가 도움이 되었다면 ⭐를 눌러주세요!
여러분의 응원은 이 튜토리얼 시리즈가 최신 AI 패턴을 유지하도록 하는 데 큰 힘이 됩니다.

[맨 위로 이동](#나만의-ai-에이전트-만들기)
</div>
