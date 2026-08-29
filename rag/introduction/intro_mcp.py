""" Stdio simple MCP server example using FastMCP."""

from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
def fetch():
    """Fetches a greeting message."""
    return {"data": "Hello, MCP!"}

@mcp.tool()
def process():
    """Processes a greeting message."""
    return {"data": "Processing complete."}

if __name__ == "__main__":
    mcp.run(transport="stdio")