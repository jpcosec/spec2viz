"""Fixtures of the specIR tests: an isolated copy of this repo's real store, mounted with
SLDB's public CLI, and the real MCP server over stdio with the real MCP client.

Nothing is fabricated: the copy holds this repo's `.sldb/`, `sldb/` and `desk/` as they
are; the deskops and spec2viz stores are linked in place and only read."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterator

import pytest

REPO = Path(__file__).resolve().parents[1]
WORKSPACE = REPO.parent
COPIED = (".sldb", "sldb", "desk")
FEDERATED = {"deskops": WORKSPACE / "deskops" / ".sldb", "spec2viz": WORKSPACE / "spec2viz" / ".sldb"}
CACHE = ".sldb_cache"
TOOL_TIMEOUT = 300


def tree_digest(*roots: Path) -> dict[str, str]:
    """sha256 of every file under `roots` (caches left out: they are regenerable)."""
    digest: dict[str, str] = {}
    for root in roots:
        for path in sorted(root.rglob("*")):
            if path.is_file() and CACHE not in path.parts:
                digest[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def federated_digest() -> dict[str, str]:
    """The linked stores' `.sldb/` trees and the documents they track (git-tracked files of
    each store's project, outside the cache)."""
    digest = tree_digest(*FEDERATED.values())
    for store in FEDERATED.values():
        root = store.parent
        listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], check=True, capture_output=True).stdout.decode()
        for rel in filter(None, listed.split("\0")):
            path = root / rel
            if path.is_file() and path.suffix == ".md":
                digest[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def sldb(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    """Run the public `sldb` CLI of this environment; fail the test with its output on error."""
    command = [str(Path(sys.executable).with_name("sldb")), *args]
    done = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if done.returncode != 0:
        pytest.fail(f"{' '.join(args)} failed ({done.returncode}):\n{done.stdout}\n{done.stderr}")
    return done


@pytest.fixture(scope="session")
def original_digest() -> dict[str, str]:
    """This repo's `.sldb/` and `desk/` before any test ran."""
    return tree_digest(REPO / ".sldb", REPO / "desk")


@pytest.fixture(scope="session")
def store_copy(tmp_path_factory: pytest.TempPathFactory, original_digest: dict[str, str]) -> Path:
    """The project root of an isolated copy of this repo's store, mounted and checked."""
    for name, store in FEDERATED.items():
        if not (store / "core").is_dir():
            pytest.fail(f"the {name} store is missing: {store}")
    root = tmp_path_factory.mktemp("specir-store") / "IR"
    root.mkdir()
    for name in COPIED:
        shutil.copytree(REPO / name, root / name, ignore=shutil.ignore_patterns(CACHE), symlinks=True)
    sldb("stores", "add", str(FEDERATED["deskops"]), "--name", "deskops", "--replace", "--store", ".sldb", cwd=root)
    sldb("stores", "add", str(FEDERATED["spec2viz"]), "--name", "spec2viz", "--store", ".sldb", cwd=root)
    sldb("stores", "update", "--store", ".sldb", cwd=root)
    sldb("edges", "rebuild", "--store", ".sldb", cwd=root)
    sldb("stores", "check", "--store", ".sldb", cwd=root)
    return root


class McpSession:
    """The real MCP client, connected over stdio to the real specIR server, driven from sync tests."""

    def __init__(self, portal: Any, client: Any) -> None:
        self.portal = portal
        self.client = client

    def list_tools(self) -> list[Any]:
        return self.portal.call(self.client.list_tools).tools

    def call(self, tool: str, **arguments: Any) -> dict[str, Any]:
        """The tool's structured JSON answer; a tool error fails the test with its message."""
        result = self.portal.call(lambda: self.client.call_tool(tool, arguments))
        if result.is_error:
            pytest.fail(f"{tool}({arguments}) failed: {result.content}")
        return result.structured_content

    def error_of(self, tool: str, **arguments: Any) -> str:
        """The error text of a call that must fail."""
        result = self.portal.call(lambda: self.client.call_tool(tool, arguments))
        assert result.is_error, f"{tool}({arguments}) did not fail: {result.structured_content}"
        return " ".join(getattr(c, "text", "") for c in result.content)


@pytest.fixture(scope="session")
def copy_digest_before(store_copy: Path) -> dict[str, str]:
    """The mounted copy and the linked stores before the server reads them."""
    return {**tree_digest(*(store_copy / name for name in COPIED)), **federated_digest()}


@pytest.fixture(scope="session")
def mcp(store_copy: Path, copy_digest_before: dict[str, str]) -> Iterator[McpSession]:
    """A session with `python -m specir.mcp.server --store <copy>/.sldb`, launched by stdio."""
    from anyio.from_thread import start_blocking_portal
    from mcp import Client, StdioServerParameters

    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "specir.mcp.server", "--store", str(store_copy / ".sldb")],
        cwd=str(store_copy),
        env={**os.environ},
    )
    with start_blocking_portal() as portal:
        with portal.wrap_async_context_manager(Client(params, read_timeout_seconds=TOOL_TIMEOUT)) as client:
            yield McpSession(portal, client)
