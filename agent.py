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

Available connections and schemas:

GoogleSheets1 (Google Sheets), schema: GoogleSheets
  Table: [GoogleSheets1].[GoogleSheets].[Connect AI Demo — Sales Pipeline_pipeline]
  Columns: id, opportunity_name, account_name, industry, stage, arr_value (INTEGER),
           close_date (DATE), account_owner, region, source
  Stage values: Discovery, Proposal, Negotiation, Closed Won, Closed Lost

SampleConnection1 (PostgreSQL), schema: public
  Customers: customerid, companyname, address, country, city, sector, industry,
             city_id, iso3_country_code, modified_date
  Orders: orderid, customerid, orderdate, cost, subtotal, taxes, total,
          uuid_group, segment, is_10k, is_100k, is_1m, is_10m, is_100m, is_1b, modified_date
  OrderLines: orderlineid, orderid, stockitemid, stockitemname, quantity,
              unitcost, saleprice, taxrate, totalcost, subtotal, tax, totalorderlineprice,
              uuid_group, modified_date

SampleConnection2 (MySQL), schema: dv_demo_data — same tables as SampleConnection1

GitHub1 (GitHub), schema: GitHub — tables: Repositories, Commits, Issues, PullRequests

All queries must use fully qualified [Catalog].[Schema].[Table] names.
Use queryData to run SQL SELECT statements. Go directly to querying. Do not call getInstructions.

For multi-step questions that span sources: query each source independently, then synthesize."""


def run_query(user_query: str, mcp: ConnectAIMCPClient, on_tool_call=None) -> str:
    """
    Execute a natural-language query against connected data sources.
    Returns the final text response from the agent.
    on_tool_call: optional callback(tool_names: list[str]) called before each tool round.
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
            if on_tool_call:
                on_tool_call(tool_names)
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
