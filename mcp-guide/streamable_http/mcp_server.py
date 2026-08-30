""" Stdio simple MCP server example using FastMCP."""

from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
def fetch_http(path : str | None):
    """Fetches a file from the given path."""
    return {"data": "Fetching from" + (path if path else "") + "..."}

@mcp.tool()
def process_http():
    """Processes a greeting message."""
    return {"data": "Processing http request complete!"}

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)