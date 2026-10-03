# 02 - Tool-Calling Agent

Build an AI agent that uses external tools via the ReAct pattern.

## What You'll Learn

- Defining tools with JSON schemas
- The ReAct (Reason + Act) agent loop
- Parsing LLM output to extract tool calls
- Feeding tool results back into the conversation

## Architecture

```mermaid
flowchart LR
    U[User Query] --> A[Agent Loop]
    A --> L[LLM (Think)]
    L --> P[Parse Action]
    P --> T[Tool Registry]
    T --> E[Execute Tool]
    E --> O[Observe Result]
    O --> A
    A --> F[Final Answer]
```

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## How It Works

The agent follows a ReAct loop: it reasons about the user input, decides whether to call a tool, executes the action, and observes the result before continuing. Tool definitions live in `tools.py` and use structured schemas so the model can produce valid tool arguments. Each tool output is fed back into the conversation as an observation, allowing the agent to iterate until it can produce a final answer.

## Key Concepts

- ReAct pattern
- Function calling
- Tool schemas
- Agent loops

## Available Tools

- `calculator`
- `get_weather`
- `search_web`
- `get_current_time`
