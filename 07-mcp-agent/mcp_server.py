"""Minimal JSON-RPC 2.0 MCP-like server over stdio."""

from __future__ import annotations

import ast
import json
import math
import operator
import sys
from datetime import datetime

TOOLS = [
    {"name": "get_weather", "description": "Get mock weather for a city.", "inputSchema": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}},
    {"name": "calculate", "description": "Evaluate a math expression safely.", "inputSchema": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}},
    {"name": "get_time", "description": "Get current local server time.", "inputSchema": {"type": "object", "properties": {}}},
]
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod, ast.USub: operator.neg}


def safe_eval(expr: str) -> float:
    """Evaluate arithmetic/math-function expressions without builtins access."""

    def walk(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](walk(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            fn = getattr(math, node.func.id, None)
            vals = [walk(arg) for arg in node.args]
            if fn and all(isinstance(v, (int, float)) for v in vals):
                return fn(*vals)
        raise ValueError("Unsafe expression")

    return float(walk(ast.parse(expr, mode="eval").body))


def call_tool(name: str, args: dict) -> dict:
    """Run one of the server tools and return structured output."""
    if name == "get_weather":
        city = args.get("city", "Unknown")
        return {"city": city, "forecast": "Sunny", "temp_c": 23}
    if name == "calculate":
        expr = args.get("expression", "0")
        return {"expression": expr, "result": safe_eval(expr)}
    if name == "get_time":
        return {"time": datetime.now().isoformat(timespec="seconds")}
    raise ValueError(f"Unknown tool: {name}")


def send(msg_id, result=None, error=None) -> None:
    """Write a JSON-RPC response on stdout as one line."""
    payload = {"jsonrpc": "2.0", "id": msg_id, "result": result} if not error else {"jsonrpc": "2.0", "id": msg_id, "error": error}
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


def main() -> None:
    """Serve initialize, tools/list, and tools/call methods via stdio."""
    for line in sys.stdin:
        req = None
        try:
            req = json.loads(line)
            method, params, msg_id = req.get("method"), req.get("params", {}), req.get("id")
            if method == "initialize":
                send(msg_id, {"server": "mini-mcp", "version": "1.0"})
            elif method == "tools/list":
                send(msg_id, {"tools": TOOLS})
            elif method == "tools/call":
                send(msg_id, {"content": call_tool(params.get("name", ""), params.get("arguments", {}))})
            else:
                send(msg_id, error={"code": -32601, "message": "Method not found"})
        except Exception as e:  # noqa: BLE001
            send(req.get("id") if isinstance(req, dict) else None, error={"code": -32000, "message": str(e)})


if __name__ == "__main__":
    main()
