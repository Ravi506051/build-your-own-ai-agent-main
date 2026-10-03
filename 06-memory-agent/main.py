"""CLI memory chatbot with short-term context and SQLite long-term memory."""

from __future__ import annotations

import os
import re
from typing import Any

import requests
from colorama import Fore, Style, init
from openai import OpenAI

from memory import MemoryStore


def extract_facts(text: str) -> list[str]:
    """Extract simple user facts from text using lightweight heuristics."""
    fact_patterns = [
        r"\bmy name is\b.*",
        r"\bi am\b.*",
        r"\bi'm\b.*",
        r"\bi live\b.*",
        r"\bi work\b.*",
        r"\bi like\b.*",
        r"\bi prefer\b.*",
        r"\bmy favorite\b.*",
        r"\bI have\b.*",
    ]
    facts: list[str] = []
    for sentence in re.split(r"[.!?]\s+", text.strip()):
        s = sentence.strip()
        if not s:
            continue
        for pattern in fact_patterns:
            if re.search(pattern, s, re.IGNORECASE):
                facts.append(s)
                break
    return list(dict.fromkeys(facts))


def chat_openai(messages: list[dict[str, str]]) -> str:
    """Call OpenAI Chat Completions API."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(model=model, messages=messages)
    return (response.choices[0].message.content or "").strip()


def chat_ollama(messages: list[dict[str, str]]) -> str:
    """Call Ollama local API."""
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    response = requests.post(
        f"{base_url}/api/chat",
        json={"model": model, "messages": messages, "stream": False},
        timeout=120,
    )
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    return str(data.get("message", {}).get("content", "")).strip()


def build_messages(
    short_term: list[dict[str, str]], user_input: str, memories: list[str]
) -> list[dict[str, str]]:
    """Compose model input with system prompt, long-term memory, and chat history."""
    memory_block = "\n".join(f"- {m}" for m in memories) if memories else "- (none)"
    system_prompt = (
        "You are a helpful assistant. Use the user's long-term memory facts when relevant. "
        "If memory conflicts with current user input, trust current input.\n\n"
        f"Long-term memory facts:\n{memory_block}"
    )
    return [{"role": "system", "content": system_prompt}, *short_term, {"role": "user", "content": user_input}]


def print_system(text: str) -> None:
    """Print system messages in yellow."""
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")


def print_memory(text: str) -> None:
    """Print memory messages in dim text."""
    print(f"{Style.DIM}{text}{Style.RESET_ALL}")


def print_answer(text: str) -> None:
    """Print assistant answers in green."""
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")


def main() -> None:
    """Run the interactive memory chatbot."""
    init(autoreset=True)
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    store = MemoryStore("memory.db")
    short_term: list[dict[str, str]] = []

    print_system("Memory Agent started. Commands: /memory, /forget, /quit")
    print_system(f"Provider: {provider}")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print_system("\nExiting.")
            break

        if not user_input:
            continue
        if user_input == "/quit":
            print_system("Bye.")
            break
        if user_input == "/memory":
            all_mem = store.get_all()
            print_memory("Stored facts:")
            if not all_mem:
                print_memory("  (empty)")
            for fact in all_mem:
                print_memory(f"  {fact}")
            continue
        if user_input == "/forget":
            store.clear()
            print_system("Long-term memory cleared.")
            continue

        memories = store.search(user_input, limit=5)
        if memories:
            print_memory("Retrieved memory:")
            for fact in memories:
                print_memory(f"  - {fact}")

        messages = build_messages(short_term, user_input, memories)
        try:
            if provider == "openai":
                answer = chat_openai(messages)
            elif provider == "ollama":
                answer = chat_ollama(messages)
            else:
                print_system("Invalid LLM_PROVIDER. Use 'openai' or 'ollama'.")
                continue
        except Exception as exc:  # noqa: BLE001
            print_system(f"Model call failed: {exc}")
            continue

        print_answer(answer)
        short_term.extend(
            [{"role": "user", "content": user_input}, {"role": "assistant", "content": answer}]
        )
        if len(short_term) > 20:
            short_term = short_term[-20:]

        for fact in extract_facts(user_input):
            store.add(fact=fact, category="user_fact")


if __name__ == "__main__":
    main()
