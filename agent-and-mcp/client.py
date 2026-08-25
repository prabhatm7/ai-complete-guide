from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
load_dotenv()

async def main():
    mcp_client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8000/mcp",
            },
            "math": {
                "transport": "stdio",
                "command": ".venv/bin/python",
                "args": ["math-server.py"],
                "cwd": ".",
            },
        }
    )
    tools = await mcp_client.get_tools()

    agent = create_react_agent(
        ChatGroq(model="qwen/qwen3.6-27b"),
        tools=tools,
        prompt="You are a helpful assistant. Use the MCP tools when needed.",
    )

    response = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the weather in New York and what is 5 multiplied by 3?"
                )
            ]
        }
    )
    print(response["messages"][-1].content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
