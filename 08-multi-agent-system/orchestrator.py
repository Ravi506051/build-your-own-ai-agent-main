"""Orchestration layer for a simple multi-agent research workflow."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class Agent:
    """Represents a specialized agent backed by the same LLM."""

    role: str
    system_prompt: str
    color: str


class Orchestrator:
    """Coordinates Researcher -> Writer -> Reviewer with revision rounds."""

    def __init__(
        self,
        llm_call: Callable[[str, str], str],
        colors: Dict[str, str],
        max_revisions: int = 2,
    ) -> None:
        self.llm_call = llm_call
        self.colors = colors
        self.max_revisions = max_revisions
        self.agents = {
            "researcher": Agent(
                "Researcher",
                (
                    "You are a focused researcher. Provide key facts, trends, and source leads "
                    "for the topic. Keep it concise, factual, and structured in bullet points."
                ),
                colors["researcher"],
            ),
            "writer": Agent(
                "Writer",
                (
                    "You are a strong technical writer. Draft clear, coherent content from given "
                    "research and reviewer feedback. Keep it readable and actionable."
                ),
                colors["writer"],
            ),
            "reviewer": Agent(
                "Reviewer",
                (
                    "You are a strict reviewer. Evaluate clarity, completeness, and accuracy. "
                    "Return only valid JSON with keys: approved (bool), feedback (string), "
                    "score (0-10)."
                ),
                colors["reviewer"],
            ),
        }

    def _log(self, who: str, text: str) -> None:
        print(f"{self.colors[who]}[{who.upper()}] {text}{self.colors['reset']}")

    def _run_agent(self, agent_key: str, message: Dict[str, Any]) -> str:
        agent = self.agents[agent_key]
        prompt = (
            "Use the following structured input JSON.\n"
            f"{json.dumps(message, ensure_ascii=True, indent=2)}"
        )
        output = self.llm_call(agent.system_prompt, prompt).strip()
        self._log(agent_key, output)
        return output

    @staticmethod
    def _parse_review(text: str) -> Dict[str, Any]:
        try:
            parsed = json.loads(text)
            approved = bool(parsed.get("approved", False))
            feedback = str(parsed.get("feedback", "")).strip()
            score = parsed.get("score", 0)
            return {"approved": approved, "feedback": feedback, "score": score}
        except json.JSONDecodeError:
            return {"approved": False, "feedback": f"Reviewer output was not JSON: {text}", "score": 0}

    def run_pipeline(self, topic: str) -> Dict[str, Any]:
        """Execute the full multi-agent workflow for a topic."""
        self._log("orchestrator", f"Starting workflow for topic: {topic}")

        research_payload = {"topic": topic, "task": "Gather reliable research notes."}
        research_notes = self._run_agent("researcher", research_payload)

        draft_payload = {
            "topic": topic,
            "research_notes": research_notes,
            "task": "Create the first draft.",
        }
        draft = self._run_agent("writer", draft_payload)

        revision_round = 0
        review_result: Dict[str, Any] = {"approved": False, "feedback": "", "score": 0}

        while revision_round <= self.max_revisions:
            self._log("orchestrator", f"Review cycle {revision_round + 1}")
            review_payload = {
                "topic": topic,
                "draft": draft,
                "task": "Review and return strict JSON only.",
            }
            review_text = self._run_agent("reviewer", review_payload)
            review_result = self._parse_review(review_text)

            approved = review_result["approved"]
            feedback = review_result["feedback"]
            score = review_result["score"]
            self._log("orchestrator", f"Reviewer score={score}, approved={approved}")

            if approved or not feedback or revision_round == self.max_revisions:
                break

            revision_round += 1
            revise_payload = {
                "topic": topic,
                "research_notes": research_notes,
                "current_draft": draft,
                "reviewer_feedback": feedback,
                "task": "Revise the draft to address all feedback.",
            }
            draft = self._run_agent("writer", revise_payload)

        self._log("orchestrator", "Workflow complete.")
        return {
            "topic": topic,
            "research": research_notes,
            "final_draft": draft,
            "review": review_result,
            "revisions_used": revision_round,
        }
