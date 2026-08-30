# MCP Guide

## Stdio MCP Example

From the `mcp-guide` folder, install the project dependencies:

```bash
uv sync
```

Run the stdio client:

```bash
uv run python stdio_mcp/mcp_client.py
```

The client starts the stdio server for you, initializes the MCP session, and prints the available tools.

If you want to start the stdio server directly:

```bash
uv run python stdio_mcp/mcp_server.py
```

The server uses stdio transport, so it is mainly meant to be launched by an MCP client rather than interacted with manually in the terminal.
