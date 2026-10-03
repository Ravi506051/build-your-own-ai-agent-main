"""Tiny MCP client over stdio JSON-RPC 2.0."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


class MCPClient:
    """Spawns and communicates with mcp_server.py using stdio pipes."""

    def __init__(self, server_path: str = "mcp_server.py"):
        self.server_path = Path(server_path)
        self.proc: subprocess.Popen[str] | None = None
        self.req_id = 0

    def connect(self) -> dict:
        self.proc = subprocess.Popen(
            [sys.executable, str(self.server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        return self._request("initialize", {})

    def list_tools(self) -> list[dict]:
        return self._request("tools/list", {}).get("tools", [])

    def call_tool(self, name: str, args: dict) -> dict:
        return self._request("tools/call", {"name": name, "arguments": args}).get("content", {})

    def disconnect(self) -> None:
        if not self.proc:
            return
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = None

    def _request(self, method: str, params: dict) -> dict:
        if not self.proc or not self.proc.stdin or not self.proc.stdout:
            raise RuntimeError("MCP client is not connected")
        self.req_id += 1
        req = {"jsonrpc": "2.0", "id": self.req_id, "method": method, "params": params}
        self.proc.stdin.write(json.dumps(req) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            err = self.proc.stderr.read() if self.proc.stderr else "server closed"
            raise RuntimeError(f"No response from MCP server: {err}")
        resp = json.loads(line)
        if "error" in resp:
            raise RuntimeError(resp["error"].get("message", "Unknown error"))
        return resp.get("result", {})
