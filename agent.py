"""
Agent loop using the Anthropic Python SDK with CData Connect AI MCP tools.

Each call to run_query() is stateless — it gets a fresh message history.
The MCP client caches tool discovery, so repeated calls don't re-fetch the tool list.
"""
import anthropic
from mcp_client import ConnectAIMCPClient

_client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096
MAX_TOOL_ROUNDS = 10

SYSTEM_PROMPT = """You are a data analyst with access to CData Connect AI, which provides SQL access to connected data sources.

Available connections:
- SampleConnection1 (PostgreSQL): tables include Customers, Orders, OrderLines, StockItems in schema 'public'
- SampleConnection2 (MySQL): tables include Customers, Orders, OrderLines, StockItems in schema 'dv_demo_data'
- SalesPipeline (Google Sheets): a sales pipeline spreadsheet with columns: opportunity_name, account_name, industry, stage, arr_value, close_date, account_owner, region, source
- GitHub1 (GitHub): repositories, commits, issues, pull requests for the connected GitHub account

Query tables using fully qualified names like: SampleConnection1.public.Customers
For Google Sheets use: SalesPipeline.[Connect AI Demo — Sales Pipeline].[Sheet1]
For GitHub use: GitHub1.GitHub.Repositories

Use queryData to run SQL SELECT statements. Go directly to querying — do not call getCatalogs, getSchemas, or getTables unless the user asks about available data sources. Do not call getInstructions."""


def run_query(user_query: str, mcp: ConnectAIMCPClient) -> str:
    """
    Execute a natural-language query against connected data sources.
    Returns the final text response from the agent.
    """
    tools = mcp.list_tools_for_anthropic()
    messages: list[dict] = [{"role": "user", "content": user_query}]

    for _ in range(MAX_TOOL_ROUNDS):
        response = _client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return _extract_text(response.content)

        if response.stop_reason == "tool_use":
            tool_names = [b.name for b in response.content if b.type == "tool_use"]
            print(f"  → {', '.join(tool_names)}...", flush=True)
            tool_results = _execute_tool_calls(response.content, mcp)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            return _extract_text(response.content)

    return "Reached maximum tool call limit without a final answer."


def _execute_tool_calls(content_blocks, mcp: ConnectAIMCPClient) -> list[dict]:
    results = []
    for block in content_blocks:
        if block.type == "tool_use":
            try:
                result = mcp.call_tool(block.name, block.input)
            except Exception as e:
                result = f"Tool call failed: {e}"
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })
    return results


def _extract_text(content_blocks) -> str:
    parts = [block.text for block in content_blocks if hasattr(block, "text")]
    return "\n".join(parts)
