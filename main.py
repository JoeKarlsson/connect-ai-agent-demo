#!/usr/bin/env python3
"""
Enterprise Data AI Agent — CData Connect AI Demo

A natural-language interface to your enterprise data sources via CData Connect AI's
managed MCP server. Built as part of a first-session developer experience audit.
See docs/dx-audit.md for findings.

Usage:
    python main.py                  # interactive mode
    python main.py "your question"  # single query mode
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def _get_required_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        print(f"Error: {key} is not set.")
        print("Copy .env.example to .env and add your credentials.")
        sys.exit(1)
    return value


def main():
    email = _get_required_env("CDATA_EMAIL")
    token = _get_required_env("CDATA_ACCESS_TOKEN")

    # Delay import so credential check happens before any SDK initialization
    from mcp_client import ConnectAIMCPClient
    from agent import run_query

    mcp = ConnectAIMCPClient(email, token)

    try:
        tools = mcp.list_tools()
    except Exception as e:
        print(f"Failed to connect to CData Connect AI: {e}")
        print("Check your credentials and ensure you have at least one data source connected.")
        sys.exit(1)

    print(f"Connected — {len(tools)} tools available from CData Connect AI")

    # Single query mode: python main.py "what are my top accounts?"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print("Thinking...", flush=True)
        answer = run_query(query, mcp)
        print(answer)
        return

    # Interactive mode
    print("Ask anything about your connected data. Type 'quit' to exit.\n")
    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if query.lower() in ("quit", "exit", "q"):
            break

        if not query:
            continue

        try:
            print("Thinking...", flush=True)
            answer = run_query(query, mcp)
        except Exception as e:
            answer = f"Error: {e}"

        print(f"\nAgent: {answer}\n")


if __name__ == "__main__":
    main()
