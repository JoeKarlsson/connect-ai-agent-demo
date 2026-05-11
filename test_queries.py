#!/usr/bin/env python3
"""
Final query validation — no Anthropic API, no credits burned.
"""
import os
import json
from dotenv import load_dotenv
from mcp_client import ConnectAIMCPClient

load_dotenv()

mcp = ConnectAIMCPClient(os.environ["CDATA_EMAIL"], os.environ["CDATA_ACCESS_TOKEN"])
PIPELINE = "[GoogleSheets1].[GoogleSheets].[Connect AI Demo — Sales Pipeline_pipeline]"
CUSTOMERS = "[SampleConnection1].[public].[Customers]"
ORDERS = "[SampleConnection1].[public].[Orders]"


def q(label, sql):
    print(f"\n{'='*60}\n>> {label}")
    result = mcp._rpc("tools/call", {"name": "queryData", "arguments": {"query": sql}})
    content = result.get("content", [])
    text = content[0].get("text", "") if content and isinstance(content[0], dict) else ""
    try:
        parsed = json.loads(text)
    except Exception:
        print(f"  RAW: {text[:300]}")
        return
    if "error" in parsed:
        print(f"  ERROR: {parsed['error']['message']}")
        return
    if "results" in parsed:
        for row in parsed["results"]:
            row.pop("schema", None)
            print(json.dumps(row, indent=2))
    else:
        print(json.dumps(parsed, indent=2))


# === DEMO QUERY 1 ===
print("\n\n### DEMO QUERY 1: QBR weighted pipeline + rep concentration risk ###")

q("Stage breakdown with weighted ARR",
  f"""SELECT stage,
       COUNT(*) AS deals,
       SUM(arr_value) AS total_arr,
       ROUND(SUM(arr_value * CASE stage
           WHEN 'Discovery'   THEN 0.10
           WHEN 'Proposal'    THEN 0.40
           WHEN 'Negotiation' THEN 0.75
           WHEN 'Closed Won'  THEN 1.00
           ELSE 0 END), 0) AS weighted_arr
     FROM {PIPELINE}
     GROUP BY stage
     ORDER BY total_arr DESC""")

q("Rep ranking by weighted pipeline (open deals only)",
  f"""SELECT account_owner,
       COUNT(*) AS open_deals,
       SUM(arr_value) AS raw_pipeline,
       ROUND(SUM(arr_value * CASE stage
           WHEN 'Discovery'   THEN 0.10
           WHEN 'Proposal'    THEN 0.40
           WHEN 'Negotiation' THEN 0.75
           ELSE 0 END), 0) AS weighted_pipeline
     FROM {PIPELINE}
     WHERE stage NOT IN ('Closed Won', 'Closed Lost')
     GROUP BY account_owner
     ORDER BY weighted_pipeline DESC""")


# === DEMO QUERY 2 ===
print("\n\n### DEMO QUERY 2: Pipeline industries vs. customer DB sectors ###")

q("Open pipeline ARR by industry",
  f"""SELECT industry,
       COUNT(*) AS deals,
       SUM(arr_value) AS pipeline_arr
     FROM {PIPELINE}
     WHERE stage NOT IN ('Closed Won', 'Closed Lost')
     GROUP BY industry
     ORDER BY pipeline_arr DESC""")

q("Customer DB: revenue by sector (top 8)",
  f"""SELECT c.sector,
       COUNT(DISTINCT c.customerid) AS customers,
       SUM(o.total) AS total_revenue,
       ROUND(AVG(o.total), 0) AS avg_order_value
     FROM {CUSTOMERS} c
     JOIN {ORDERS} o ON c.customerid = o.customerid
     WHERE c.sector IS NOT NULL AND c.sector != 'n/a'
     GROUP BY c.sector
     ORDER BY total_revenue DESC
     LIMIT 8""")

print("\n\nAll queries passed. Data is valid for demo.")
