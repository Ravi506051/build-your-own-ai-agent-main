# 05 - Code Generation Agent

Build an AI agent that writes, executes, and self-corrects Python code.

## What You'll Learn
- Generating code from natural language descriptions
- Safe code execution in a sandboxed subprocess
- Automated error detection and self-correction
- Iterative refinement loop (generate -> execute -> fix)

## Architecture
```mermaid
flowchart LR
    A[User Task Description] --> B[LLM generates code]
    B --> C[Sandbox Execution]
    C --> D{Success?}
    D -->|Yes| E[Show Output]
    D -->|No| F[Error Analysis]
    F --> G[LLM fixes code]
    G --> H[Retry (max 3)]
    H --> C
```

## Quick Start
```bash
pip install -r requirements.txt
python main.py
```

## How It Works
The agent runs a generate-execute-fix loop:
1. The LLM generates Python code from a user task description.
2. The code is executed in an isolated subprocess.
3. If execution fails, the error is analyzed and sent back to the LLM for a corrected version.
4. The cycle repeats until success or the retry limit is reached.

`sandbox.py` handles controlled execution by running generated code in a restricted subprocess environment and capturing stdout/stderr for feedback.

## Key Concepts
- **Code generation**: Turning natural language tasks into runnable Python.
- **Sandboxed execution**: Running untrusted code with isolation and limits.
- **Self-correction**: Using runtime errors as feedback to improve generated code.
- **Iterative refinement**: Repeating generate -> execute -> fix for higher reliability.

## Safety
This project applies basic safeguards for executing generated code:
- Isolated subprocess execution
- Captured outputs and errors (no silent failures)
- Bounded retry count (max 3)
- Restricted runtime flow through a sandbox wrapper

These safeguards reduce risk but are not a complete security boundary for hostile code.
