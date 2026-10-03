# 01 - Simple Chatbot

Build a terminal chatbot with streaming LLM responses.

## What You'll Learn

- How to call LLM APIs (OpenAI and Ollama)
- Managing conversation history
- Implementing streaming token-by-token output
- Building a simple REPL interface

## Architecture

```mermaid
flowchart LR
    A[User Input] --> B[Chat Loop]
    B --> C[LLM API (OpenAI/Ollama)]
    C --> D[Streaming Response]
    D --> E[Terminal Output]
```

## Quick Start

```bash
pip install -r requirements.txt
# For Ollama (default):
python main.py
# For OpenAI:
LLM_PROVIDER=openai OPENAI_API_KEY=your-key python main.py
```

## How It Works

The chatbot runs a REPL loop that reads user input, appends it to conversation history, sends the full context to the configured LLM provider, and streams the model response back to the terminal token by token. After streaming completes, the assistant reply is saved in history so follow-up messages stay contextual.

## Key Concepts

- LLM API calls
- Conversation context
- Streaming responses

## Commands

- `/clear` to reset conversation history
- `/quit` to exit the chatbot
