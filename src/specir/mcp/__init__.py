"""The read-only MCP server of specIR (IR03): thin MCP adapters over `sldb.api`.

`read_tools.ReadTools` holds the operations as plain functions that return JSON-ready
dicts; `server.build_server` exposes them as MCP tools over stdio. Nothing here writes to a
store, keeps an edge index, traverses the graph or parses predicates: SLDB does all of it."""

from specir.mcp.read_tools import ReadTools

__all__ = ["ReadTools"]
