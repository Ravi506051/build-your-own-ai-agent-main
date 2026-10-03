"""Simple terminal chatbot supporting OpenAI and Ollama providers."""

from __future__ import annotations

import os
import sys
from typing import Dict, List

import requests
from colorama import Fore, Style, init
from openai import OpenAI


OPENAI_MODEL = "gpt-4o-mini"
OLLAMA_MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/chat"


class ChatBot:
    """Interactive chatbot with conversation history and streaming output."""

    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
        if self.provider not in {"openai", "ollama"}:
            print(
                Fore.YELLOW
                + "Invalid LLM_PROVIDER. Falling back to 'ollama'."
                + Style.RESET_ALL
            )
            self.provider = "ollama"

        # Keep conversation context as role/content messages.
        self.history: List[Dict[str, str]] = []
        self.openai_client = OpenAI() if self.provider == "openai" else None

    def clear_history(self) -> None:
        """Reset conversation history."""
        self.history.clear()

    def stream_openai(self) -> str:
        """Send chat history to OpenAI and stream assistant output."""
        assert self.openai_client is not None
        stream = self.openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=self.history,
            stream=True,
        )

        full_text = ""
        for chunk in stream:
            delta = chunk.choices[0].delta
            token = delta.content or ""
            if token:
                print(token, end="", flush=True)
                full_text += token
        return full_text

    def stream_ollama(self) -> str:
        """Send chat history to Ollama and stream assistant output."""
        payload = {
            "model": OLLAMA_MODEL,
            "messages": self.history,
            "stream": True,
        }
        response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60)
        response.raise_for_status()

        full_text = ""
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                data = requests.models.complexjson.loads(line)
            except ValueError:
                continue

            token = data.get("message", {}).get("content", "")
            if token:
                print(token, end="", flush=True)
                full_text += token

            if data.get("done"):
                break
        return full_text

    def reply(self, user_text: str) -> None:
        """Append user message, stream assistant response, then save it."""
        self.history.append({"role": "user", "content": user_text})
        print(Fore.CYAN + "Assistant: " + Style.RESET_ALL, end="")

        try:
            if self.provider == "openai":
                assistant_text = self.stream_openai()
            else:
                assistant_text = self.stream_ollama()
        except requests.exceptions.ConnectionError:
            print(
                Fore.RED
                + "\nConnection failed. Is Ollama running on http://localhost:11434?"
                + Style.RESET_ALL
            )
            self.history.pop()
            return
        except requests.exceptions.RequestException as exc:
            print(Fore.RED + f"\nOllama request error: {exc}" + Style.RESET_ALL)
            self.history.pop()
            return
        except Exception as exc:  # Handles OpenAI and unexpected failures cleanly.
            print(Fore.RED + f"\nLLM error: {exc}" + Style.RESET_ALL)
            self.history.pop()
            return

        print()
        self.history.append({"role": "assistant", "content": assistant_text})

    def run(self) -> None:
        """Start interactive chat loop."""
        print(Fore.GREEN + f"Provider: {self.provider}" + Style.RESET_ALL)
        print("Commands: /clear to reset history, /quit to exit")

        while True:
            try:
                user_text = input(Fore.YELLOW + "You: " + Style.RESET_ALL).strip()
            except (KeyboardInterrupt, EOFError):
                print("\nBye!")
                break

            if not user_text:
                continue

            if user_text == "/quit":
                print("Bye!")
                break
            if user_text == "/clear":
                self.clear_history()
                print(Fore.MAGENTA + "History cleared." + Style.RESET_ALL)
                continue

            self.reply(user_text)


def main() -> int:
    """Program entry point."""
    init(autoreset=True)
    bot = ChatBot()
    bot.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
