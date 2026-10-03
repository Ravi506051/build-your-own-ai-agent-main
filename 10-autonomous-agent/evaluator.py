"""Evaluation module for the autonomous agent."""

import json
import os

import requests
from openai import OpenAI


class Evaluator:
    """Evaluates whether step outputs satisfy the user goal."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.client = OpenAI() if self.provider == "openai" else None

    def _ask(self, prompt: str) -> str:
        if self.provider == "openai":
            resp = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content or ""
        payload = {"model": self.ollama_model, "prompt": prompt, "stream": False}
        resp = requests.post("http://localhost:11434/api/generate", json=payload, timeout=90)
        resp.raise_for_status()
        return resp.json().get("response", "")

    def evaluate(self, goal: str, results: list[str]) -> dict:
        """Judge success and produce summary plus targeted replanning feedback."""
        prompt = (
            "Return ONLY valid JSON with keys: success (bool), feedback (str), summary (str).\n"
            f"Goal: {goal}\n"
            f"Step Results:\n" + "\n".join(f"- {r}" for r in results)
        )
        raw = self._ask(prompt)
        try:
            start, end = raw.find("{"), raw.rfind("}") + 1
            data = json.loads(raw[start:end])
            return {
                "success": bool(data.get("success", False)),
                "feedback": str(data.get("feedback", "")).strip(),
                "summary": str(data.get("summary", "")).strip(),
            }
        except Exception:
            return {
                "success": False,
                "feedback": "Evaluation parsing failed; provide clearer and more complete outputs.",
                "summary": raw.strip() or "No summary generated.",
            }
