"""Tool definitions and schemas for the ReAct agent."""

from __future__ import annotations

import ast
from datetime import datetime


CALCULATOR_TOOL_SCHEMA = {
    "name": "calculator",
    "description": "Safely evaluate a math expression, e.g. '2 + 3 * (4 - 1)'.",
    "parameters": {
        "type": "object",
        "properties": {"expression": {"type": "string", "description": "Math expression"}},
        "required": ["expression"],
    },
}

GET_WEATHER_TOOL_SCHEMA = {
    "name": "get_weather",
    "description": "Get mock weather data for a city.",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "City name"}},
        "required": ["city"],
    },
}

SEARCH_WEB_TOOL_SCHEMA = {
    "name": "search_web",
    "description": "Return 3 mock web search results for a query.",
    "parameters": {
        "type": "object",
        "properties": {"query": {"type": "string", "description": "Search query"}},
        "required": ["query"],
    },
}

GET_CURRENT_TIME_TOOL_SCHEMA = {
    "name": "get_current_time",
    "description": "Get the current local date and time.",
    "parameters": {"type": "object", "properties": {}, "required": []},
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        val = _safe_eval(node.operand)
        return val if isinstance(node.op, ast.UAdd) else -val
    if isinstance(node, ast.BinOp) and isinstance(
        node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow)
    ):
        left, right = _safe_eval(node.left), _safe_eval(node.right)
        ops = {
            ast.Add: left + right,
            ast.Sub: left - right,
            ast.Mult: left * right,
            ast.Div: left / right,
            ast.Mod: left % right,
            ast.Pow: left**right,
        }
        return float(ops[type(node.op)])
    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _safe_eval(parsed)
        return str(int(result) if result.is_integer() else result)
    except Exception as exc:
        return f"Calculator error: {exc}"


def get_weather(city: str) -> str:
    samples = [
        ("sunny", 25),
        ("cloudy", 19),
        ("rainy", 16),
        ("windy", 21),
    ]
    cond, temp = samples[abs(hash(city.lower())) % len(samples)]
    return f"{city}: {cond}, {temp}°C"


def search_web(query: str) -> str:
    results = [
        {"title": f"{query} guide", "url": "https://example.com/guide"},
        {"title": f"Latest on {query}", "url": "https://example.com/latest"},
        {"title": f"{query} explained", "url": "https://example.com/explained"},
    ]
    return "\n".join(f"{i}. {r['title']} - {r['url']}" for i, r in enumerate(results, 1))


def get_current_time() -> str:
    return datetime.now().isoformat(timespec="seconds")


TOOLS = {
    "calculator": calculator,
    "get_weather": get_weather,
    "search_web": search_web,
    "get_current_time": get_current_time,
}


def get_all_tool_schemas() -> list[dict]:
    return [
        CALCULATOR_TOOL_SCHEMA,
        GET_WEATHER_TOOL_SCHEMA,
        SEARCH_WEB_TOOL_SCHEMA,
        GET_CURRENT_TIME_TOOL_SCHEMA,
    ]
