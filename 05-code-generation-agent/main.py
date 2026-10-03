"""Interactive code-generation agent with execution and self-correction."""

import os
import re
from typing import Optional

import requests
from colorama import Fore, Style, init
from openai import OpenAI

from sandbox import execute_code

init(autoreset=True)

SYSTEM_PROMPT = (
    "You write Python code only. Return only runnable Python code in a single "
    "markdown code block. Do not add explanations."
)


def extract_python(text: str) -> str:
    """Extract Python from a markdown code block, or return raw text."""
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text.strip()


def call_openai(prompt: str) -> str:
    """Generate text from OpenAI chat completions."""
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""


def call_ollama(prompt: str) -> str:
    """Generate text from an Ollama local server."""
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    payload = {
        "model": model,
        "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
        "stream": False,
    }
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json().get("response", "")


def generate_code(task: str, previous_code: Optional[str] = None, error: str = "") -> str:
    """Generate or repair Python code for a user task."""
    if previous_code and error:
        prompt = (
            "Fix this Python code based on the error. Return corrected code only.\n\n"
            f"Task:\n{task}\n\n"
            f"Previous code:\n```python\n{previous_code}\n```\n\n"
            f"Error:\n{error}\n"
        )
    else:
        prompt = f"Write Python code for this task:\n{task}\n"

    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    raw = call_openai(prompt) if provider == "openai" else call_ollama(prompt)
    return extract_python(raw)


def print_code(code: str) -> None:
    """Print generated code in cyan."""
    print(Fore.CYAN + "\nGenerated code:\n")
    for i, line in enumerate(code.splitlines(), start=1):
        print(Fore.CYAN + f"{i:>3}: {line}")
    print(Style.RESET_ALL)


def run_task(task: str) -> None:
    """Generate, execute, and iteratively repair Python code."""
    code = ""
    error = ""

    for attempt in range(1, 4):
        print(f"\nAttempt {attempt}/3")
        try:
            code = generate_code(task, previous_code=code if code else None, error=error)
        except Exception as exc:
            print(Fore.RED + f"LLM error: {exc}")
            return

        print_code(code)
        result = execute_code(code)

        if result["success"]:
            output = result["output"].strip() or "(no output)"
            print(Fore.GREEN + "Execution output:")
            print(Fore.GREEN + output)
            return

        error = result["error"].strip() or "Unknown error"
        print(Fore.RED + "Execution error:")
        print(Fore.RED + error)

    print(Fore.RED + "\nFailed after 3 attempts.")


def repl() -> None:
    """Run the interactive prompt loop."""
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    print(f"Code generation agent ready (provider={provider}). Type /quit to exit.")

    while True:
        try:
            task = input("\nTask> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return

        if not task:
            continue
        if task == "/quit":
            print("Goodbye.")
            return

        run_task(task)


if __name__ == "__main__":
    """Entrypoint for running the agent as a script."""
    repl()
