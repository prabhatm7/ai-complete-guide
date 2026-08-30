import asyncio
import os
import sys

from langchain_mcp_adapters.client import MultiServerMCPClient


MCP_SERVER_PATH = os.path.join(
    os.path.dirname(__file__), "..", "stdio_mcp", "mcp_server.py"
)

async def main():
    client = MultiServerMCPClient(

    {
        "mcp_server_stdio_details" :{
            "transport" : "stdio",
            "command": sys.executable,
            "args" : [os.path.abspath(MCP_SERVER_PATH)]
        }
    }
    )

    # list tools
    list_tool_response = await client.get_tools()
    print("Available tools:", list_tool_response)

if __name__ == "__main__":
    asyncio.run(main()) 