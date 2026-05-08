"""
HTTP client for CData Connect AI MCP server.

The server speaks JSON-RPC 2.0 over HTTP with Server-Sent Events (SSE) responses.
Auth is Basic with base64(email:personal_access_token).
"""
import base64
import json
import requests


MCP_SERVER_URL = "https://mcp.cloud.cdata.com/mcp/"


class ConnectAIMCPClient:
    def __init__(self, email: str, access_token: str):
        credentials = base64.b64encode(f"{email}:{access_token}".encode()).decode()
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        })
        self._tools_cache: list[dict] | None = None

    def _rpc(self, method: str, params: dict) -> dict:
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        response = self.session.post(MCP_SERVER_URL, json=payload, stream=True)
        response.raise_for_status()

        for line in response.iter_lines():
            if line and line.startswith(b"data: "):
                data = json.loads(line[6:])
                if "result" in data:
                    return data["result"]
                if "error" in data:
                    raise RuntimeError(f"MCP error: {data['error']['message']}")

        raise RuntimeError("No result received from MCP server")

    def list_tools(self) -> list[dict]:
        if self._tools_cache is None:
            result = self._rpc("tools/list", {})
            self._tools_cache = result.get("tools", [])
        return self._tools_cache

    def list_tools_for_anthropic(self) -> list[dict]:
        """Format tool definitions for the Anthropic messages API."""
        return [
            {
                "name": t["name"],
                "description": t.get("description", ""),
                "input_schema": t.get("inputSchema", {"type": "object", "properties": {}}),
            }
            for t in self.list_tools()
        ]

    def call_tool(self, tool_name: str, arguments: dict) -> str:
        result = self._rpc("tools/call", {"name": tool_name, "arguments": arguments})
        content = result.get("content", [])
        if content and isinstance(content[0], dict):
            return content[0].get("text", json.dumps(content))
        return json.dumps(result)

    def get_sources(self) -> list[str]:
        """List connected data sources (convenience wrapper over list_tools)."""
        tools = self.list_tools()
        seen = set()
        sources = []
        for t in tools:
            # Tool names follow pattern like "query_salesforce_contacts" — extract source
            parts = t["name"].split("_")
            if len(parts) >= 2:
                source = parts[1].capitalize()
                if source not in seen:
                    seen.add(source)
                    sources.append(source)
        return sources
