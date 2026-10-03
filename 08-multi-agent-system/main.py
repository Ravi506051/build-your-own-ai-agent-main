"""CLI entrypoint for a colorized multi-agent research assistant."""

from __future__ import annotations

import os
import sys
from typing import Callable

import requests
from colorama import Fore, Style, init
from openai import OpenAI

from orchestrator import Orchestrator


def build_llm_call() -> Callable[[str, str], str]:
    """Build a provider-backed LLM function based on LLM_PROVIDER."""
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()

    if provider == "openai":
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        def call(system_prompt: str, user_prompt: str) -> str:
            response = client.chat.completions.create(
                model=model,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return (response.choices[0].message.content or "").strip()

        return call

    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "llama3.1")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        def call(system_prompt: str, user_prompt: str) -> str:
            payload = {
                "model": model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            }
            resp = requests.post(f"{base_url}/api/chat", json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "").strip()

        return call

    raise ValueError("LLM_PROVIDER must be 'openai' or 'ollama'.")


def run_repl() -> None:
    """Run an interactive prompt for research topics."""
    init(autoreset=True)
    colors = {
        "researcher": Fore.CYAN,
        "writer": Fore.GREEN,
        "reviewer": Fore.YELLOW,
        "orchestrator": Fore.MAGENTA,
        "reset": Style.RESET_ALL,
    }

    try:
        llm_call = build_llm_call()
    except Exception as exc:
        print(f"{Fore.RED}Initialization error: {exc}{Style.RESET_ALL}")
        sys.exit(1)

    orchestrator = Orchestrator(llm_call=llm_call, colors=colors, max_revisions=2)
    print(f"{colors['orchestrator']}Multi-Agent Research REPL (/quit to exit){colors['reset']}")

    while True:
        topic = input("\nTopic> ").strip()
        if topic == "/quit":
            print(f"{colors['orchestrator']}Goodbye.{colors['reset']}")
            break
        if not topic:
            continue

        try:
            result = orchestrator.run_pipeline(topic)
            print(f"\n{colors['orchestrator']}[FINAL OUTPUT]{colors['reset']}")
            print(f"{colors['writer']}{result['final_draft']}{colors['reset']}")
        except Exception as exc:
            print(f"{Fore.RED}Runtime error: {exc}{Style.RESET_ALL}")


if __name__ == "__main__":
    run_repl()
