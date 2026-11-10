# Build Your Own AI Agent — Learning Notes

This repository contains a hands-on learning path for understanding AI-agent design through practical Python projects. The upstream project focuses on implementing agent patterns and orchestration concepts rather than hiding the workflow behind a single abstraction.

## Learning themes
- LLM request and response loops
- Tool calling and structured outputs
- Planning and task decomposition
- Memory and state management
- Multi-agent coordination
- Error handling and evaluation

## How to use this repository
Start with the introductory examples and progress through the projects in sequence. Follow the upstream setup instructions and check each project's own dependency requirements before running it.

## Engineering principles
- Give agents narrowly scoped tools and explicit permissions.
- Validate tool inputs and outputs.
- Add iteration limits and clear stopping conditions.
- Keep API keys outside source control.
- Test failure paths, not only successful demonstrations.
- Require human confirmation before consequential external actions.

## Attribution
This repository is based on the upstream learning project. Preserve its original licence, author credits and source links when modifying or redistributing the material.

## Maintainer's profile
**Ravi Kumar Rao** · [GitHub](https://github.com/Ravi506051)

## Engineering Review Checklist

- Define the agent's goal, available tools, and stopping conditions before execution.
- Validate tool inputs and outputs, and handle timeouts or tool failures explicitly.
- Keep tool permissions narrow and require confirmation before consequential external actions.
- Evaluate task completion, tool-call correctness, latency, and failure recovery using repeatable test cases.
