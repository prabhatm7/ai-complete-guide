import asyncio
import os
import sys
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters


# path to mcp server script
mcp_server_path = os.path.join(os.path.dirname(__file__), "mcp_server.py")
print(mcp_server_path)

# create server parameters
server_params = StdioServerParameters(
    command = sys.executable,
    args = [str(mcp_server_path)],
    env = {}
)

# create client session
async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # You can now use the session to communicate with the server

            # list tools 
            list_tool_response = await session.list_tools()
            for tool in list_tool_response.tools:
                print(tool.name)
                print(tool.inputSchema)

            fetch_result = await session.call_tool("fetch", arguments={"path": "/opt/mcp"})
            print("\n" + "Fetch result:", fetch_result.structuredContent["data"] , "\n")

            process_result = await session.call_tool("process", arguments={})
            print("\n" + "Process result:", process_result.structuredContent["data"] , "\n")


if __name__ == "__main__":
    asyncio.run(main())

