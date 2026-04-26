#!/usr/bin/env python3
"""
Test script for the Local Agent MCP Server.
This demonstrates calling the tools directly (for testing purposes).
"""

import json

from mcp_server import call_local_model, read_file, run_command, web_search, write_file


def pretty(raw: str) -> str:
    try:
        return json.dumps(json.loads(raw), indent=2)
    except json.JSONDecodeError:
        return raw

def test_tools():
    """Test the tools directly."""

    print("Testing write_file...")
    result = write_file("test_output.txt", "Hello from MCP test!\nThis file was created by the local agent.")
    print("Result:\n", pretty(result))

    print("\nTesting read_file...")
    result = read_file("test_output.txt")
    print("Result:\n", pretty(result))

    print("\nTesting run_command...")
    result = run_command("ls -la")
    print("Result:\n", pretty(result))

    print("\nTesting web_search...")
    result = web_search("what is AI")
    print("Result:\n", pretty(result))

    print("\nTesting call_local_model...")
    result = call_local_model("Give 3 short tips to build a safe MCP server.")
    print("Result:\n", pretty(result))

    print("\nTest complete. Check for test_output.txt file.")

if __name__ == "__main__":
    test_tools()