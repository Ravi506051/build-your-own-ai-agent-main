"""Minimal ReAct tool-calling agent supporting OpenAI and Ollama."""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any

import requests
try:
    from colorama import Fore, Style, init
except ImportError:  # Optional runtime fallback before dependencies are installed
    class _NoColor:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""

    class _NoStyle:
        RESET_ALL = ""

    def init(*_args: Any, **_kwargs: Any) -> None:
        return None

    Fore = _NoColor()
    Style = _NoStyle()

from tools import TOOLS, get_all_tool_schemas


SYSTEM_PROMPT = """You are a ReAct agent with tools.
Rules:
1) Think step-by-step and output using this exact format:
Thought: <reasoning>
Action: <tool_name or NONE>
Action Input: <json object>
2) If you can answer fully, use:
Thought: <reasoning>
Final Answer: <answer>
3) Tool names must be one of the provided tools.
4) Action Input must be valid JSON.
"""


def extract_action(text: str) -> tuple[str | None, dict[str, Any] | None, str | None]:
    final = re.search(r"Final Answer:\s*(.*)", text, flags=re.IGNORECASE | re.DOTALL)
    if final:
        return None, None, final.group(1).strip()

    action_match = re.search(r"Action:\s*([\w_]+)", text, flags=re.IGNORECASE)
    input_match = re.search(r"Action Input:\s*(\{.*\})", text, flags=re.IGNORECASE | re.DOTALL)
    if not action_match:
        return None, None, None

    action = action_match.group(1).strip()
    payload: dict[str, Any] = {}
    if input_match:
        try:
            payload = json.loads(input_match.group(1).strip())
        except json.JSONDecodeError:
            payload = {}
    return action, payload, None


def call_openai(messages: list[dict[str, str]]) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    resp = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    return resp.choices[0].message.content or ""


def call_ollama(messages: list[dict[str, str]]) -> str:
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
    payload = {"model": model, "messages": messages, "stream": False}
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json().get("message", {}).get("content", "")


def llm_chat(messages: list[dict[str, str]]) -> str:
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    if provider == "openai":
        return call_openai(messages)
    if provider == "ollama":
        return call_ollama(messages)
    raise ValueError("LLM_PROVIDER must be 'openai' or 'ollama'")


def run_agent(user_query: str, max_steps: int = 10) -> None:
    init(autoreset=True)
    schema_text = json.dumps(get_all_tool_schemas(), indent=2)
    messages: list[dict[str, str]] = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\nAvailable tools:\n{schema_text}"},
        {"role": "user", "content": user_query},
    ]

    for step in range(1, max_steps + 1):
        try:
            reply = llm_chat(messages).strip()
        except Exception as exc:
            print(f"{Fore.RED}LLM error: {exc}{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}[Step {step} Thinking]\n{reply}\n{Style.RESET_ALL}")
        action, action_input, final = extract_action(reply)
        messages.append({"role": "assistant", "content": reply})

        if final is not None:
            print(f"{Fore.GREEN}[Final]\n{final}{Style.RESET_ALL}")
            return

        if not action:
            print(f"{Fore.RED}Could not parse action. Stopping.{Style.RESET_ALL}")
            return

        if action.upper() == "NONE":
            print(f"{Fore.RED}Action is NONE but no final answer found. Stopping.{Style.RESET_ALL}")
            return

        tool = TOOLS.get(action)
        if not tool:
            observation = f"Unknown tool: {action}"
        else:
            try:
                observation = tool(**(action_input or {}))
            except Exception as exc:
                observation = f"Tool execution error: {exc}"

        print(f"{Fore.CYAN}[Action] {action}({action_input or {}}){Style.RESET_ALL}")
        print(f"{Fore.GREEN}[Result] {observation}{Style.RESET_ALL}\n")
        messages.append(
            {
                "role": "user",
                "content": f"Observation: {observation}\nContinue with the required format.",
            }
        )

    print(f"{Fore.RED}Reached max steps without final answer.{Style.RESET_ALL}")


def main() -> None:
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:]).strip()
    else:
        query = input("Ask the agent: ").strip()

    if not query:
        print("Please provide a question.")
        return

    run_agent(query)


if __name__ == "__main__":
    main()
