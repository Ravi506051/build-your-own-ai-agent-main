"""Sandboxed execution utility for generated Python code."""

import os
import subprocess
import tempfile
from typing import Dict


BLOCKED_PATTERNS = [
    "os.system",
    "subprocess.",
    "import subprocess",
    "from subprocess",
]


def execute_code(code: str) -> Dict[str, str]:
    """Run Python code in a temporary file and return execution results."""
    lowered = code.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lowered:
            return {
                "success": False,
                "output": "",
                "error": f"Blocked unsafe pattern: {pattern}",
            }

    temp_path = ""
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(code)
            temp_path = f.name

        proc = subprocess.run(
            ["python3", temp_path],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return {
            "success": proc.returncode == 0,
            "output": proc.stdout,
            "error": proc.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "", "error": "Execution timed out (10s)."}
    except Exception as exc:
        return {"success": False, "output": "", "error": str(exc)}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
