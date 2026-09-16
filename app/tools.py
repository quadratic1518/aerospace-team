"""Safe wrappers for the repository's deterministic engineering calculators."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "shared" / "tools"
ALLOWED_TOOLS = {"trajectory", "staging", "geometry", "cost_estimator", "timeline"}

TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "engineering_calculator",
        "description": "Run a verified local aerospace calculator. Choose a listed script and pass its CLI tokens exactly as documented.",
        "parameters": {
            "type": "object",
            "properties": {
                "script": {"type": "string", "enum": sorted(ALLOWED_TOOLS)},
                "arguments": {"type": "array", "items": {"type": "string"}, "description": "CLI tokens after the script name, for example ['hohmann', 'Earth', 'Mars']."},
            },
            "required": ["script", "arguments"],
            "additionalProperties": False,
        },
    },
}


def run_calculator(script: str, arguments: list[str]) -> dict:
    if script not in ALLOWED_TOOLS:
        return {"error": "Calculator is not allow-listed."}
    if not all(isinstance(argument, str) and len(argument) <= 160 for argument in arguments):
        return {"error": "Arguments must be short strings."}
    command = [sys.executable, str(TOOLS_DIR / f"{script}.py"), *arguments]
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
    except subprocess.TimeoutExpired:
        return {"error": "Calculator timed out."}
    if result.returncode:
        return {"error": "Calculator failed.", "details": result.stderr[-1000:]}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw_output": result.stdout[-4000:]}
