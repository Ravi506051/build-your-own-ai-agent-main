"""Execution module for the autonomous agent."""

import os

import requests
from openai import OpenAI


class Executor:
    """Executes planned steps while preserving step context."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.client = OpenAI() if self.provider == "openai" else None
        self.history = []

    def _ask(self, prompt: str) -> str:
        if self.provider == "openai":
            resp = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return resp.choices[0].message.content or ""
        payload = {"model": self.ollama_model, "prompt": prompt, "stream": False}
        resp = requests.post("http://localhost:11434/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "")

    def execute_step(self, step: dict, context: str = "") -> str:
        """Execute a single step and append output to internal history."""
        prior = "\n".join(f"Step {i+1}: {r}" for i, r in enumerate(self.history[-5:]))
        prompt = (
            "Execute the requested step thoroughly and return the result text only.\n"
            f"Step #{step.get('step_number')}: {step.get('description')}\n"
            f"Expected output: {step.get('expected_output')}\n"
            f"Global context: {context}\n"
            f"Previous outputs:\n{prior}"
        )
        result = self._ask(prompt).strip()
        self.history.append(result)
        return result
