from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Server")

@mcp.tool()
def get_weather(location: str) -> str:
    """Returns the current weather for a given location."""
    # In a real implementation, you would call a weather API here.
    return f"The current weather in {location} is sunny with a temperature of 25°C."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")