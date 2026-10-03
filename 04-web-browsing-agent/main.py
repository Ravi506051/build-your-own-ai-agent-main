"""Simple web-browsing ReAct agent with OpenAI/Ollama backends."""

import json
import os
import re
from typing import Dict, List
from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from openai import OpenAI

MAX_CHARS = 2000
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
}


def truncate(text: str, limit: int = MAX_CHARS) -> str:
    """Return text truncated to the given limit."""
    text = (text or "").strip()
    return text[:limit] + ("..." if len(text) > limit else "")


def fetch_html(url: str) -> str:
    """Fetch raw HTML from a URL with timeout and browser-like headers."""
    r = requests.get(url, headers=HEADERS, timeout=12)
    r.raise_for_status()
    return r.text


def fetch_page(url: str) -> str:
    """Fetch page title + text content from URL."""
    try:
        soup = BeautifulSoup(fetch_html(url), "html.parser")
        for t in soup(["script", "style", "noscript"]):
            t.extract()
        title = (soup.title.string or "").strip() if soup.title else ""
        text = truncate(soup.get_text(" ", strip=True))
        return f"TITLE: {title}\nURL: {url}\nTEXT: {text}"
    except Exception as e:
        return f"Error fetching page: {e}"


def extract_links(url: str) -> str:
    """Extract absolute links from a page."""
    try:
        soup = BeautifulSoup(fetch_html(url), "html.parser")
        out = []
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"])
            label = a.get_text(" ", strip=True)
            if href.startswith("http"):
                out.append(f"- {label[:80]} | {href}")
            if len(out) >= 15:
                break
        return "\n".join(out) if out else "No links found."
    except Exception as e:
        return f"Error extracting links: {e}"


def extract_text(url: str) -> str:
    """Extract plain text from a page, limited for model context."""
    try:
        soup = BeautifulSoup(fetch_html(url), "html.parser")
        for t in soup(["script", "style", "noscript"]):
            t.extract()
        return truncate(soup.get_text(" ", strip=True))
    except Exception as e:
        return f"Error extracting text: {e}"


def search_google(query: str) -> str:
    """Search Google and return top organic results parsed from HTML."""
    try:
        url = f"https://www.google.com/search?q={quote_plus(query)}&num=5"
        soup = BeautifulSoup(fetch_html(url), "html.parser")
        results = []
        for a in soup.select("a"):
            href = a.get("href", "")
            title = a.get_text(" ", strip=True)
            m = re.match(r"/url\?q=([^&]+)", href)
            if m and title:
                results.append(f"- {title[:90]} | {m.group(1)}")
            if len(results) >= 5:
                break
        return "\n".join(results) if results else "No search results parsed."
    except Exception as e:
        return f"Error in search_google: {e}"


class LLM:
    """Provider wrapper for OpenAI and Ollama chat APIs."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.model = os.getenv(
            "LLM_MODEL", "gpt-4o-mini" if self.provider == "openai" else "llama3.1"
        )
        self.client = OpenAI() if self.provider == "openai" else None

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Return assistant text from selected provider."""
        if self.provider == "openai":
            r = self.client.chat.completions.create(model=self.model, messages=messages, temperature=0.2)
            return r.choices[0].message.content or ""
        payload = {"model": self.model, "messages": messages, "stream": False}
        r = requests.post("http://localhost:11434/api/chat", json=payload, timeout=60)
        r.raise_for_status()
        return (r.json().get("message") or {}).get("content", "")


def run_agent(question: str, llm: LLM) -> str:
    """Run a short ReAct loop where the model chooses tools until final answer."""
    system = (
        "You are a web research agent. Use tools to gather evidence and answer accurately. "
        "Respond ONLY JSON: {\"thought\":str,\"action\":str,\"input\":str}. "
        "Actions: search_google, fetch_page, extract_links, extract_text, final. "
        "When done, set action=final and put final answer in input."
    )
    history: List[Dict[str, str]] = [{"role": "system", "content": system}]
    tools = {
        "search_google": search_google,
        "fetch_page": fetch_page,
        "extract_links": extract_links,
        "extract_text": extract_text,
    }

    for _ in range(6):
        prompt = (
            f"Question: {question}\n"
            "Previous observations:\n"
            + "\n".join([m["content"] for m in history if m["role"] == "tool"])
        )
        history.append({"role": "user", "content": prompt})
        raw = llm.chat(history)
        try:
            data = json.loads(raw.strip().strip("`").replace("json\n", "", 1))
        except Exception:
            m = re.search(r"\{.*\}", raw, re.S)
            if not m:
                return f"Model parse error: {raw[:300]}"
            data = json.loads(m.group(0))

        thought = data.get("thought", "")
        action = data.get("action", "")
        tool_input = data.get("input", "")
        print(Fore.YELLOW + f"[thinking] {thought}" + Style.RESET_ALL)

        if action == "final":
            return tool_input
        if action not in tools:
            return f"Unknown action: {action}"

        print(Fore.CYAN + f"[browsing] {action}({tool_input})" + Style.RESET_ALL)
        obs = truncate(tools[action](tool_input))
        history.append({"role": "tool", "content": f"{action}({tool_input}) => {obs}"})

    return "I could not complete in the step limit."


def repl() -> None:
    """Interactive shell for asking web questions."""
    init(autoreset=True)
    llm = LLM()
    print(f"Provider={llm.provider} Model={llm.model}. Type /quit to exit.")
    while True:
        q = input("\nAsk> ").strip()
        if not q:
            continue
        if q == "/quit":
            break
        ans = run_agent(q, llm)
        print(Fore.GREEN + f"[answer] {ans}" + Style.RESET_ALL)


if __name__ == "__main__":
    repl()
