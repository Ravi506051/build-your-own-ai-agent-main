"""CLI skill-based agent that loads YAML-defined skills and runs them via LLM."""

from __future__ import annotations

import os
import re
from pathlib import Path

import requests
from colorama import Fore, Style, init

from skill_loader import Skill, SkillLoader


class SkillAgent:
    """Interactive agent that selects and executes skills with OpenAI or Ollama."""

    def __init__(self, skills_dir: str = "skills") -> None:
        self.skills_dir = skills_dir
        self.loader = SkillLoader()
        self.skills: dict[str, Skill] = {}
        self.provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower() or "ollama"
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        init(autoreset=True)

    def reload_skills(self) -> None:
        """Rescan the skills directory and reload all YAML skill definitions."""
        self.skills = self.loader.load_skills(self.skills_dir)
        print(f"{Fore.YELLOW}[system]{Style.RESET_ALL} Loaded {len(self.skills)} skills from {self.skills_dir}")

    def list_skills(self) -> None:
        """Print the currently loaded skills."""
        if not self.skills:
            print(f"{Fore.YELLOW}[system]{Style.RESET_ALL} No skills loaded.")
            return
        print(f"{Fore.YELLOW}[system]{Style.RESET_ALL} Loaded skills:")
        for skill in self.skills.values():
            print(f"  {Fore.CYAN}{skill.name}{Style.RESET_ALL} - {skill.description}")

    def _extract_target_language(self, query: str) -> str:
        """Extract target language from user query for translate skill."""
        match = re.search(r"\bto\s+([A-Za-z][A-Za-z\s-]{1,30})\b", query, re.IGNORECASE)
        return (match.group(1).strip() if match else "English")

    def _build_prompt(self, skill: Skill, user_input: str) -> str:
        """Fill the selected skill prompt template with query variables."""
        values = {"input": user_input, "target_language": self._extract_target_language(user_input)}
        try:
            return skill.prompt_template.format(**values)
        except KeyError:
            return f"{skill.prompt_template}\n\nInput:\n{user_input}"

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI chat completions API and return model output."""
        from openai import OpenAI

        client = OpenAI()
        rsp = client.chat.completions.create(
            model=self.openai_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return rsp.choices[0].message.content or ""

    def _call_ollama(self, prompt: str) -> str:
        """Call local Ollama generate API and return model output."""
        url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        rsp = requests.post(url, json={"model": self.ollama_model, "prompt": prompt, "stream": False}, timeout=90)
        rsp.raise_for_status()
        data = rsp.json()
        return str(data.get("response", ""))

    def run_skill(self, query: str) -> None:
        """Match a skill for a query, execute it via configured provider, and print result."""
        if not self.skills:
            print(f"{Fore.YELLOW}[system]{Style.RESET_ALL} No skills available. Try /reload.")
            return

        skill = self.loader.match_skill(query, self.skills)
        prompt = self._build_prompt(skill, query)
        print(f"{Fore.CYAN}[skill]{Style.RESET_ALL} {skill.name} ({skill.output_format})")

        try:
            if self.provider == "openai":
                output = self._call_openai(prompt)
            elif self.provider == "ollama":
                output = self._call_ollama(prompt)
            else:
                print(f"{Fore.YELLOW}[system]{Style.RESET_ALL} Unknown LLM_PROVIDER '{self.provider}'.")
                return
            print(f"{Fore.GREEN}[result]{Style.RESET_ALL}\n{output.strip() or '(empty response)'}")
        except Exception as exc:
            print(f"{Fore.YELLOW}[system]{Style.RESET_ALL} LLM error: {exc}")

    def repl(self) -> None:
        """Start interactive command loop."""
        print(f"{Fore.YELLOW}[system]{Style.RESET_ALL} Provider: {self.provider}")
        print(f"{Fore.YELLOW}[system]{Style.RESET_ALL} Commands: /skills, /reload, /quit")
        self.reload_skills()
        while True:
            try:
                query = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                break

            if not query:
                continue
            if query == "/quit":
                print("Bye.")
                break
            if query == "/skills":
                self.list_skills()
                continue
            if query == "/reload":
                self.reload_skills()
                continue

            self.run_skill(query)


def main() -> None:
    """Entrypoint for running the skill-based agent."""
    base_dir = Path(__file__).resolve().parent
    os.chdir(base_dir)
    SkillAgent(skills_dir="skills").repl()


if __name__ == "__main__":
    main()
