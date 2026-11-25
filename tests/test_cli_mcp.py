"""`specir mcp`: sldb's MCP server with specIR's extension already loaded (no stdio is started)."""

from __future__ import annotations

from click.testing import CliRunner
from sldb.mcp import extension, server
from sldb.mcp.mutability import READ

from specir.cli import main

DOMAIN = {"specir_types", "specir_nodes", "specir_rules", "specir_impact"}
EXTENSION = "specir.mcp_extension:register"


def test_the_server_with_the_extension_has_the_four_specir_tools(tmp_path) -> None:
    import asyncio

    built = server.build_server(tmp_path, extensions=[extension.load_extension(EXTENSION)])
    tools = built.list_tools() if hasattr(built, "list_tools") else built._tool_manager.list_tools()
    if asyncio.iscoroutine(tools):
        tools = asyncio.run(tools)
    assert DOMAIN <= {t.name for t in tools}


def test_help_names_store() -> None:
    result = CliRunner().invoke(main, ["mcp", "--help"])
    assert result.exit_code == 0 and "--store" in result.output


def test_arguments_reaching_serve(monkeypatch, tmp_path) -> None:
    seen: dict = {}
    monkeypatch.setattr(server, "serve", lambda store, **kw: seen.update(store=store, **kw))
    result = CliRunner().invoke(main, ["mcp", "--store", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert seen["extensions"] == (EXTENSION,) and seen["level"] == READ and seen["actor"] is None
    seen.clear()
    CliRunner().invoke(main, ["mcp", "--store", str(tmp_path), "--level", "1", "--actor", "me"])
    assert seen["level"] == 1 and seen["actor"] == "me"
