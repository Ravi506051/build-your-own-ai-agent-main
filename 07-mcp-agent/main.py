"""Interactive MCP agent with OpenAI/Ollama LLM backends."""

from __future__ import annotations

import json
import os
from typing import Any

import requests
from colorama import Fore, Style, init

from mcp_client import MCPClient

SYSTEM_PROMPT = (
    "You are a tool-using assistant. Respond only as JSON with fields: "
    "action ('tool' or 'final'), tool_name, tool_args, final_answer. "
    "Choose action='tool' when a tool is needed."
)


def ask_openai(messages: list[dict[str, str]], model: str) -> str:
    """Return raw assistant text from OpenAI chat completion."""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return resp.choices[0].message.content or "{}"


def ask_ollama(messages: list[dict[str, str]], model: str) -> str:
    """Return raw assistant text from Ollama /api/chat."""
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
    r = requests.post(url, json={"model": model, "messages": messages, "stream": False}, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data.get("message", {}).get("content", "{}")


def llm_json(messages: list[dict[str, str]]) -> dict[str, Any]:
    """Ask selected LLM provider and parse JSON response."""
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    model = os.getenv("LLM_MODEL", "llama3.1") if provider == "ollama" else os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    raw = ask_openai(messages, model) if provider == "openai" else ask_ollama(messages, model)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"action": "final", "final_answer": raw.strip()}


def format_tools(tools: list[dict]) -> str:
    """Serialize tool metadata for prompt injection."""
    return json.dumps(
        [
            {
                "name": t["name"],
                "description": t["description"],
                "inputSchema": t.get("inputSchema", {}),
            }
            for t in tools
        ]
    )


def run_agent(client: MCPClient, tools: list[dict], query: str) -> str:
    """Loop LLM/tool execution until final answer is produced."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Tools: {format_tools(tools)}"},
        {"role": "user", "content": query},
    ]
    for _ in range(4):
        print(Fore.YELLOW + "thinking..." + Style.RESET_ALL)
        decision = llm_json(messages)
        if decision.get("action") == "tool":
            name = decision.get("tool_name", "")
            args = decision.get("tool_args", {}) or {}
            print(Fore.CYAN + f"tool -> {name} {args}" + Style.RESET_ALL)
            result = client.call_tool(name, args)
            print(Fore.GREEN + f"result -> {result}" + Style.RESET_ALL)
            messages.append({"role": "assistant", "content": json.dumps(decision)})
            messages.append({"role": "user", "content": f"Tool result: {json.dumps(result)}"})
            continue
        return decision.get("final_answer", "No answer generated.")
    return "Reached tool loop limit."


def main() -> None:
    """Start MCP client, show tools, and run interactive agent REPL."""
    init(autoreset=True)
    client = MCPClient("mcp_server.py")
    client.connect()
    tools = client.list_tools()
    print(Fore.CYAN + "Available tools:" + Style.RESET_ALL)
    for t in tools:
        print(Fore.CYAN + f"- {t['name']}: {t['description']}" + Style.RESET_ALL)

    try:
        while True:
            user = input("\nYou> ").strip()
            if not user:
                continue
            if user == "/quit":
                break
            if user == "/tools":
                tools = client.list_tools()
                for t in tools:
                    print(Fore.CYAN + f"- {t['name']}" + Style.RESET_ALL)
                continue
            answer = run_agent(client, tools, user)
            print(f"Assistant> {answer}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
