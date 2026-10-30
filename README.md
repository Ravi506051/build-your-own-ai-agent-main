<div align="center">

# Build Your Own AI Agent
### 12 practical projects to master AI agents from scratch

[![GitHub stars](https://img.shields.io/github/stars/lay4/build-your-own-ai-agent?style=for-the-badge&color=ffd700)](https://github.com/lay4/build-your-own-ai-agent/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Projects: 12](https://img.shields.io/badge/Projects-12-success.svg?style=for-the-badge)](./)

**Learn to build AI agents by actually building them. No frameworks, no magic — just Python and an LLM.**

[English](./README.md) | [한국어](./README.ko.md) | [中文](./README.zh.md) | [日本語](./README.ja.md)

---
</div>

## 🚀 Why This Exists

In 2025-2026, the AI landscape is dominated by heavy frameworks that promise "one-line agents" but often hide the underlying mechanics behind layers of abstraction. While these tools are great for production, they can be a "black box" for developers who want to truly understand how agents reason, plan, and execute tasks.

This repository is designed to strip away the magic. We use **pure Python** to implement the core patterns of modern AI agents—from simple tool-calling loops to complex multi-agent orchestrations. By building these from scratch, you gain the intuition needed to debug, optimize, and eventually scale AI systems effectively.

Whether you're a seasoned engineer or just starting with LLMs, this series provides a hands-on path to mastering the architectural patterns that power the next generation of autonomous software.

## 🛠️ The Roadmap

| # | Project | Level | Time | What You'll Build |
| :--- | :--- | :--- | :--- | :--- |
| 01 | **Simple Chatbot** | Beginner | 15min | A robust terminal chatbot with streaming responses and basic state. |
| 02 | **Tool-Calling Agent** | Beginner | 20min | An agent that can interact with the real world via external function calls. |
| 03 | **RAG Agent** | Intermediate | 30min | Implementation of Retrieval-Augmented Generation for document-based Q&A. |
| 04 | **Web Browsing Agent** | Intermediate | 30min | An agent that can navigate, search, and extract information from the live web. |
| 05 | **Code Gen Agent** | Intermediate | 25min | An agent that writes, executes, and self-corrects Python code in a sandbox. |
| 06 | **Memory Agent** | Intermediate | 25min | Implementing long-term persistence and conversational memory architectures. |
| 07 | **MCP Agent** | Advanced | 30min | Integration with the Model Context Protocol for standardized tool access. |
| 08 | **Multi-Agent System** | Advanced | 30min | A collaborative team of specialized agents working toward a common goal. |
| 09 | **Voice Agent** | Advanced | 30min | A low-latency speech-to-speech agent for natural vocal interaction. |
| 10 | **Autonomous Agent** | Expert | 30min | A self-planning agent that decomposes complex goals into executable steps. |
| 11 | **Skill-Based Agent** | Expert | 30min | An extensible agent that can dynamically load and learn new capabilities. |
| 12 | **Local LLM Agent** | Bonus | 20min | A fully private agent running entirely offline using Ollama and local models. |

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-username/build-your-own-ai-agent.git
cd build-your-own-ai-agent

# 2. Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the first project
cd 01-simple-chatbot
python main.py
```

## 📋 Prerequisites

- **Python 3.10+**: The codebase uses modern typing and async features.
- **API Key or Local LLM**:
  - An [OpenAI API Key](https://platform.openai.com/) (recommended for starters)
  - **OR** [Ollama](https://ollama.com/) installed for local model execution.
- **Basic Python Knowledge**: Comfort with `async/await` and basic object-oriented programming.

## 🧠 How Each Project Works

Every project in this series is designed to be **self-contained**. 
- **`main.py`**: The entry point for the agent.
- **`core.py`**: The logic and "brain" of the agent, written without external agent frameworks.
- **`README.md`**: Each folder contains its own detailed explanation of the concepts introduced.

The progression is linear: we start with simple text loops and gradually introduce concepts like tool schemas, vector embeddings, state machines, and multi-agent coordination.

## 🤝 Contributing

Contributions are welcome! If you have a better way to implement a pattern or want to add a new project, feel free to open a Pull Request. Please see `CONTRIBUTING.md` for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### If you found this helpful, please give it a ⭐!
Your support helps keep this tutorial series updated with the latest AI patterns.

[Back to top](#build-your-own-ai-agent)
</div>

## Local Repository Note

This repository is maintained as a learning reference for studying AI-agent patterns. Before running an example, review its individual instructions and required environment variables. Keep API credentials in local environment files that are excluded from version control, and inspect tool permissions before allowing an agent to modify files or execute commands.

When adapting an example, document your own changes separately from the upstream material and retain the original project's license and attribution requirements.

## Project Development Notes

Treat this repository as an agent-learning reference: inspect each example before running it, scope tool permissions, and keep API credentials outside version control.

For reproducible updates, record the dataset or upstream version, environment and dependency versions, configuration, and actual outputs from each run. Keep illustrative examples clearly labelled and never commit credentials or private data.
