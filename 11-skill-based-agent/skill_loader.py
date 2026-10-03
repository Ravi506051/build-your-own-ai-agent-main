"""Skill loading and matching utilities for the skill-based agent."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Skill:
    """Represents a single skill definition loaded from YAML."""

    name: str
    description: str
    prompt_template: str
    output_format: str


class SkillLoader:
    """Loads skill definitions and performs basic query-to-skill matching."""

    def load_skills(self, skills_dir: str = "skills") -> dict[str, Skill]:
        """Load all YAML skill files from a directory into a name->Skill dict."""
        skills: dict[str, Skill] = {}
        base = Path(skills_dir)
        if not base.exists() or not base.is_dir():
            return skills

        for path in sorted(base.glob("*.yaml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                skill = Skill(
                    name=str(data["name"]),
                    description=str(data["description"]),
                    prompt_template=str(data["prompt_template"]),
                    output_format=str(data["output_format"]),
                )
                skills[skill.name] = skill
            except Exception:
                continue
        return skills

    def match_skill(self, query: str, skills: dict[str, Skill]) -> Skill:
        """Select a skill using simple keyword overlap with name/description."""
        if not skills:
            raise ValueError("No skills loaded")

        q_words = {w.lower() for w in query.replace("_", " ").split() if w.strip()}
        best_skill: Skill | None = None
        best_score = -1

        for skill in skills.values():
            haystack = f"{skill.name} {skill.description}".lower().replace("_", " ")
            keywords = {w for w in haystack.split() if len(w) > 2}
            score = len(q_words & keywords)
            if skill.name.lower() in query.lower():
                score += 2
            if score > best_score:
                best_score = score
                best_skill = skill

        return best_skill or next(iter(skills.values()))
