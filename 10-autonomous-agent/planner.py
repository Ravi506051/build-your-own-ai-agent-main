"""Planning module for the autonomous agent."""

import json
import os

import requests
from openai import OpenAI


class Planner:
    """Creates step-by-step plans from a high-level goal."""

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

    def create_plan(self, goal: str, feedback: str = None) -> list[dict]:
        """Break a goal into 3-5 executable steps, optionally revised by feedback."""
        revise = f"Evaluator feedback to address: {feedback}\n" if feedback else ""
        prompt = (
            "Return ONLY valid JSON as an array of 3-5 step objects. "
            "Each object must have keys: step_number, description, expected_output.\n"
            f"Goal: {goal}\n{revise}"
            "Keep steps concrete and ordered."
        )
        raw = self._ask(prompt)
        try:
            start, end = raw.find("["), raw.rfind("]") + 1
            steps = json.loads(raw[start:end])
            return [
                {
                    "step_number": int(s.get("step_number", i + 1)),
                    "description": str(s.get("description", "")).strip(),
                    "expected_output": str(s.get("expected_output", "")).strip(),
                }
                for i, s in enumerate(steps)
            ]
        except Exception:
            return [
                {
                    "step_number": 1,
                    "description": f"Analyze and complete the goal: {goal}",
                    "expected_output": "A clear final response that satisfies the goal.",
                }
            ]
