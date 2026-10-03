# 11 - Skill-Based Agent

Build an AI agent that dynamically loads skills from YAML definitions.

## What You'll Learn
- Skill/plugin architecture for agent capabilities
- YAML-based skill configuration
- Dynamic capability loading at runtime
- Context engineering with prompt templates for AI agents

## Architecture
```mermaid
flowchart LR
    A[Startup] --> B[Scan skills/ dir]
    B --> C[Load YAML definitions]
    C --> D[User Query]
    D --> E[Skill Matcher]
    E --> F[Select Best Skill]
    F --> G[Fill Prompt Template]
    G --> H[LLM]
    H --> I[Formatted Output]
```

## Quick Start
```bash
cd 11-skill-based-agent
pip install -r requirements.txt
python main.py
```

Inside the REPL:
- `/skills` to list loaded skills
- `/reload` to rescan YAML files
- `/quit` to exit

## How It Works
`skill_loader.py` handles two core jobs:
- Load all `*.yaml` files in `skills/` into `Skill` objects
- Match a user query to the best skill using keyword overlap between query words and each skill's `name` + `description`

Each YAML file defines one skill using:
- `name`
- `description`
- `prompt_template`
- `output_format`

`main.py` runs the REPL, selects a skill, fills template variables (like `{input}` and `{target_language}`), sends the prompt to the configured LLM provider, and prints formatted results.

## Key Concepts
- Skill engineering: designing focused, reusable capabilities
- Plugin architecture: adding behavior by dropping new files into `skills/`
- YAML configs: declarative capability definitions
- Prompt templates: structured context injection for LLM calls

## Built-in Skills
- `summarize`: concise bullet-point summaries
- `translate`: translation with target-language variable support
- `code_review`: markdown-style review suggestions for code

## Adding Custom Skills
Create a new file in `skills/` (for example, `skills/explain.yaml`):

```yaml
name: explain
description: Explain technical concepts clearly for beginners
prompt_template: "Explain this concept with an example: {input}"
output_format: markdown
```

Then run `/reload` in the CLI to load it.
