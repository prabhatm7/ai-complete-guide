""" Stdio simple MCP server example using FastMCP."""

from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
def fetch(path : str | None):
    """Fetches a file from the given path."""
    return {"data": "Fetching from" + (path if path else "") + "..."}

@mcp.tool()
def process():
    """Processes a greeting message."""
    return {"data": "Processing complete!"}

if __name__ == "__main__":
    mcp.run(transport="stdio")