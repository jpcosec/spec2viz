"""The specIR read-only MCP server over stdio.

`specir-mcp --store <project>/.sldb` (or `python -m specir.mcp.server --store ...`) serves the
tools of `read_tools.ReadTools`. Every tool is annotated read-only and idempotent and returns
structured JSON; none writes to the store or to its linked stores."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Callable

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

from specir.mcp.paging import DEFAULT_LIMIT
from specir.mcp.read_tools import ReadTools

READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)

INSTRUCTIONS = (
    "Read-only access to one SLDB store and the stores it links. Documents are named "
    "`Model:name` (`alias:Model:name` in a linked store); every document carries its stable "
    "address `sldb://document/<export id>`. Sets come as pages {items, total, offset, limit, "
    "truncated, next_offset}; an empty set carries an `explanation`."
)


def run(method: Callable[..., dict[str, Any]], *args: Any) -> dict[str, Any]:
    """`method(*args)`, with any failure (a bad argument, a predicate SLDB cannot parse, a view
    SLDB cannot resolve) answered as a tool error that names its cause, not an opaque crash."""
    try:
        return method(*args)
    except Exception as error:  # every failure reaches the agent with its cause
        raise ToolError(f"{type(error).__name__}: {error}") from error


def build_server(store: str | Path) -> MCPServer:
    """An MCP server whose tools read `store` through `sldb.api`."""
    tools = ReadTools(store)
    server = MCPServer("specir", instructions=INSTRUCTIONS)

    @server.tool(annotations=READ_ONLY)
    def list_models(offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """List the models the store registers (its own and the inherited ones)."""
        return run(tools.list_models, offset, limit)

    @server.tool(annotations=READ_ONLY)
    def describe_model(model: str, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Describe a model: its fields with their types, and a page of its documents."""
        return run(tools.describe_model, model, offset, limit)

    @server.tool(annotations=READ_ONLY)
    def list_relation_types(offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """List the relation types of the edge index with their endpoint types."""
        return run(tools.list_relation_types, offset, limit)

    @server.tool(annotations=READ_ONLY)
    def describe_relation_type(name: str) -> dict[str, Any]:
        """Describe one relation type: endpoints, direction, cardinality, description."""
        return run(tools.describe_relation_type, name)

    @server.tool(annotations=READ_ONLY)
    def read_document(ref: str, field: str | None = None) -> dict[str, Any]:
        """Read a document (`Model:name` or `alias:Model:name`): its payload, or one dotted field path."""
        return run(tools.read_document, ref, field)

    @server.tool(annotations=READ_ONLY)
    def select_documents(
        model: str | None = None,
        where: str | None = None,
        ref: str | None = None,
        prefix: str | None = None,
        path_glob: str | None = None,
        include_linked: bool = False,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        """Select documents by model, rules-language predicate (`where`), ref, name prefix or path glob."""
        return run(tools.select_documents, model, where, ref, prefix, path_glob, include_linked, offset, limit)

    @server.tool(annotations=READ_ONLY)
    def neighbors(node: str, direction: str = "outgoing", relation: str | None = None, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Edges leaving (`outgoing`) or reaching (`incoming`) a document or node, optionally of one relation type."""
        return run(tools.neighbors, node, direction, relation, offset, limit)

    @server.tool(annotations=READ_ONLY)
    def neighborhood(node: str, direction: str = "outgoing", depth: int = 1, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Node ids within `depth` hops in one direction (`outgoing`, `incoming`, `both`), over every relation type."""
        return run(tools.neighborhood, node, direction, depth, offset, limit)

    @server.tool(annotations=READ_ONLY)
    def list_views(offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """List the views the store resolves: composed ViewDocs, projection ViewDocs and SpecDocs."""
        return run(tools.list_views, offset, limit)

    @server.tool(annotations=READ_ONLY)
    def resolve_view(view: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        """Resolve a view to JSON: a composed ViewDoc by name, or a ViewDoc/SpecDoc by export id."""
        return run(tools.resolve_view, view, params)

    @server.tool(annotations=READ_ONLY)
    def check_integrity(offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """Check the store's integrity and its edge index; findings come as one page."""
        return run(tools.check_integrity, offset, limit)

    return server


def main(argv: list[str] | None = None) -> None:
    """Serve the read tools of one store over stdio."""
    parser = argparse.ArgumentParser(prog="specir-mcp", description=__doc__.splitlines()[0])
    parser.add_argument("--store", required=True, help="The store directory (`<project>/.sldb`).")
    args = parser.parse_args(argv)
    build_server(args.store).run("stdio")


if __name__ == "__main__":
    main()
