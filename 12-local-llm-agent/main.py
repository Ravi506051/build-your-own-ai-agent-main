"""Offline Ollama agent with chat, tools, and simple in-memory RAG."""

import json
import math
import os
import re
from collections import Counter

import requests
from colorama import Fore, Style, init

OLLAMA_URL = "http://localhost:11434"


class MiniVectorStore:
    """Very small in-memory vector store using token-frequency cosine similarity."""

    def __init__(self):
        self.docs = []

    @staticmethod
    def _tok(text):
        return re.findall(r"[a-zA-Z0-9_]+", text.lower())

    def _vec(self, text):
        return Counter(self._tok(text))

    def add(self, text, meta=""):
        if text.strip():
            self.docs.append({"text": text, "meta": meta, "vec": self._vec(text)})

    @staticmethod
    def _cos(a, b):
        dot = sum(v * b.get(k, 0) for k, v in a.items())
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        return dot / (na * nb) if na and nb else 0.0

    def search(self, query, k=3):
        qv = self._vec(query)
        scored = sorted(
            ((self._cos(qv, d["vec"]), d) for d in self.docs), key=lambda x: x[0], reverse=True
        )
        return [d for s, d in scored[:k] if s > 0]


def ollama_request(model, prompt):
    """Call local Ollama generate API and return text response."""
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=90,
    )
    r.raise_for_status()
    return r.json().get("response", "")


def list_models():
    """Fetch installed Ollama model names from local daemon."""
    r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
    r.raise_for_status()
    return [m["name"] for m in r.json().get("models", [])]


def run_tool(name, arg, store):
    """Run one built-in local tool and return tool output."""
    if name == "calculator":
        try:
            expr = re.sub(r"[^0-9+\-*/().% ]", "", arg)
            return str(eval(expr, {"__builtins__": {}}, {}))
        except Exception as e:
            return f"calculator error: {e}"
    if name == "file_reader":
        path = os.path.abspath(arg.strip())
        if not os.path.isfile(path):
            return f"file not found: {path}"
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(4000)
            store.add(content, meta=f"file:{path}")
            return content if content else "empty file"
        except Exception as e:
            return f"file read error: {e}"
    if name == "web_search_mock":
        data = {
            "ollama": "Ollama runs local LLMs via a local HTTP API.",
            "rag": "RAG retrieves relevant context before generation.",
            "react": "ReAct alternates reasoning and tool actions.",
        }
        key = max(data, key=lambda k: len(set(k.split()) & set(arg.lower().split())))
        return f"mock result for '{arg}': {data.get(key, 'No mock results found.')}"
    return "unknown tool"


def build_prompt(user_msg, context, scratchpad):
    """Compose strict ReAct prompt for local tool-using agent."""
    return f"""
You are a local AI agent. Zero cloud dependency - everything runs locally.
Use ReAct format strictly.
Available tools: calculator, file_reader, web_search_mock.
When done, use: Action: finish

Context snippets:\n{context or 'None'}

User question: {user_msg}

Previous steps:\n{scratchpad or 'None'}

Respond exactly with:
Thought: <brief reasoning>
Action: <calculator|file_reader|web_search_mock|finish>
Action Input: <single line>
""".strip()


def parse_action(text):
    """Extract Action and Action Input from model output."""
    action = re.search(r"Action:\s*([a-zA-Z_]+)", text)
    arg = re.search(r"Action Input:\s*(.*)", text)
    return (action.group(1).strip().lower() if action else "finish", arg.group(1).strip() if arg else "")


def agent_reply(model, user_msg, store):
    """Run a short ReAct loop with local tools and retrieved context."""
    retrieved = store.search(user_msg, k=3)
    context = "\n".join([f"[{d['meta']}] {d['text'][:300]}" for d in retrieved])
    scratchpad = ""
    final = ""
    for _ in range(4):
        out = ollama_request(model, build_prompt(user_msg, context, scratchpad))
        action, arg = parse_action(out)
        thought = re.search(r"Thought:\s*(.*)", out)
        if thought:
            scratchpad += f"Thought: {thought.group(1)}\n"
        if action == "finish":
            final = arg or out
            break
        tool_result = run_tool(action, arg, store)
        print(Fore.CYAN + f"[tool:{action}] {arg}" + Style.RESET_ALL)
        print(Fore.GREEN + f"[result] {tool_result[:500]}" + Style.RESET_ALL)
        scratchpad += f"Action: {action}\nAction Input: {arg}\nObservation: {tool_result}\n"
    return final or "I could not complete that reliably."


def choose_model(models):
    """Prompt user to select a model from local Ollama list."""
    print("Available models:")
    for i, m in enumerate(models, 1):
        print(f"  {i}. {m}")
    while True:
        pick = input("Pick model number: ").strip()
        if pick.isdigit() and 1 <= int(pick) <= len(models):
            return models[int(pick) - 1]
        print("Invalid choice.")


def main():
    """Interactive local-agent CLI powered only by Ollama."""
    init(autoreset=True)
    print("Zero cloud dependency - everything runs locally")
    try:
        models = list_models()
    except Exception as e:
        print(f"Cannot connect to Ollama at {OLLAMA_URL}: {e}")
        return
    if not models:
        print("No local models found. Run: ollama pull <model>")
        return
    model = choose_model(models)
    store = MiniVectorStore()
    print("Commands: /models, /switch <model>, /quit")
    while True:
        user = input("you> ").strip()
        if not user:
            continue
        if user == "/quit":
            break
        if user == "/models":
            print("\n".join(list_models()))
            continue
        if user.startswith("/switch "):
            target = user.split(" ", 1)[1].strip()
            if target in list_models():
                model = target
                print(Fore.MAGENTA + f"[model] switched to {model}" + Style.RESET_ALL)
            else:
                print("Model not found.")
            continue
        print(Fore.MAGENTA + f"[model] {model}" + Style.RESET_ALL)
        ans = agent_reply(model, user, store)
        print(ans)
        store.add(f"Q: {user}\nA: {ans}", meta="chat")


if __name__ == "__main__":
    main()
