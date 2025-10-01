#!/usr/bin/env python3

import asyncio
import sys
import json
import msgpack
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from reinvent_2025_mcp.tools.session_tools import create_session_tools

# Load data synchronously at module level
data_path = Path(__file__).parent / "data" / "sessions.msgpack"
with open(data_path, 'rb') as f:
    sessions = msgpack.unpack(f, raw=False, strict_map_key=False)

# Initialize server and tools
server = Server("reinvent-2025-mcp")
tools = create_session_tools(sessions)

print(f"Initialized {len(tools)} tools with {len(sessions)} sessions", file=sys.stderr)

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools."""
    return [
        Tool(
            name=tool_data["name"],
            description=tool_data["description"],
            inputSchema=tool_data["inputSchema"]
        )
        for tool_data in tools.values()
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[dict]:
    """Execute a tool with given arguments."""
    if name not in tools:
        raise ValueError(f"Tool {name} not found")
    
    result = tools[name]["handler"](arguments)
    return [{"type": "text", "text": json.dumps(result, indent=2)}]

def main():
    """Main entry point."""
    async def run_server():
        # Run server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(run_server())

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    asyncio.run(main())
