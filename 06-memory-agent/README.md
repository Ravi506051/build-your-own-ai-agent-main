# 06 - Memory Agent

Build an AI chatbot with persistent long-term memory.

## What You'll Learn

- Short-term vs long-term memory architectures
- Storing and retrieving facts with SQLite
- Extracting key information from conversations
- Memory-augmented LLM prompting

## Architecture

```mermaid
flowchart LR
    U[User Message] --> STM[Short-term Memory\n(conversation)]
    U --> LTM[Long-term Memory\n(SQLite)]
    STM --> S[Memory Search]
    LTM --> S
    S --> RF[Relevant Facts]
    RF --> LC[LLM + Context]
    STM --> LC
    LC --> R[Response]
    R --> EF[Extract Facts]
    EF --> STORE[Store in Long-term Memory]
    STORE --> LTM
```

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## How It Works

`memory.py` defines a `MemoryStore` class that manages persistent memory in SQLite.

- The chatbot keeps short-term memory in the active conversation history.
- It extracts durable user facts from messages (preferences, profile details, recurring goals).
- Before generating a reply, it retrieves relevant stored facts and injects them into the prompt.
- After each response, newly extracted facts are written back to long-term memory for future chats.

## Key Concepts

- Conversational memory
- Fact extraction
- SQLite storage
- Memory-augmented generation

## Commands

- `/memory` - View stored memory
- `/forget` - Remove memory entries
- `/quit` - Exit the chatbot
