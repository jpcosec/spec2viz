"""Fixtures of the specIR tests: an isolated copy of this repo's real store, mounted with
SLDB's public CLI, and the real MCP server of sldb (`sldb mcp`) with specIR's extension
(`specir.mcp_extension:register`) over stdio, driven by the real MCP client.

Nothing is fabricated: the copy holds this repo's `.sldb/`, `sldb/` and `desk/` as they
are, plus every `runs/subagents/*/run.md` at its own relative path. The store linked as `deskops`
is not the real one: it is a copy of deskops's `.sldb/` and git-tracked files, taken once per
session (`deskops_copy`), with its links to other stores removed (or, where sldb refuses, pointed
at copies of those stores), so other desks writing to deskops during the run neither move the
digest nor are read by the server; it is only read. The store linked as `spec2viz` is not spec2viz's: it is a new sldb store
in a temporary directory, built with `sldb.api` from a spec fixture of this repo
(`spec_store`), and also only read."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
WORKSPACE = REPO.parent
COPIED = (".sldb", "sldb", "desk")
#: The store registers RunDocs, which live outside `.sldb/` and `desk/`.
RUN_DOCS = "runs/subagents/*/run.md"
#: The git-tracked files of each store copy, listed once when the copy was made.
TRACKED: dict[Path, list[str]] = {}
#: The spec synced into the temporary specs store (`spec_store`), at the same relative path
#: under that store's project as under the fixture root.
SPEC_FIXTURES = REPO / "tests" / "visual" / "fixtures" / "spec2viz"
SPEC_FIXTURE = "docs/architecture/spec2viz/class-sldb-models.yml"
CACHE = ".sldb_cache"
TOOL_TIMEOUT = 300
#: specIR's tools on the server of sldb (`sldb mcp --extension`).
EXTENSION = "specir.mcp_extension:register"


def tree_digest(*roots: Path) -> dict[str, str]:
    """sha256 of every file under `roots` (caches left out: they are regenerable)."""
    digest: dict[str, str] = {}
    for root in roots:
        for path in sorted(root.rglob("*")):
            if path.is_file() and CACHE not in path.parts:
                digest[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def copy_store_project(source: Path, root: Path) -> Path:
    """Copy a store's project: `<source>/.sldb/` (cache left out) and the files `git ls-files`
    lists in `source`, into `root`; its `.sldb` path. The list is taken once, here."""
    listed = subprocess.run(["git", "-C", str(source), "ls-files", "-z"], check=True, capture_output=True).stdout.decode()
    tracked = [rel for rel in listed.split("\0") if rel]
    shutil.copytree(source / ".sldb", root / ".sldb", ignore=shutil.ignore_patterns(CACHE), symlinks=True)
    for rel in tracked:
        origin = source / rel
        target = root / rel
        if rel.startswith(".sldb/") or CACHE in Path(rel).parts or not (origin.is_file() or origin.is_symlink()):
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, target, follow_symlinks=False)
    store = root / ".sldb"
    TRACKED[store] = tracked
    return store


def linked_stores(root: Path) -> dict[str, Path]:
    """The stores the store_index of the project at `root` links, by name, resolved from `root`."""
    index = yaml.safe_load((root / ".sldb" / "core" / "store_index.yaml").read_text(encoding="utf-8"))
    return {link["name"]: (root / link["path"]).resolve() for link in index.get("stores") or []}


def remove_link(root: Path, name: str) -> subprocess.CompletedProcess:
    """`sldb stores remove <name>` on the store of the project at `root` (sldb refuses it while
    a model there is inherited from that store), then `sldb stores declare --write` so the
    store's declaration (`.sldb/store.yaml`) drops the link too and no rebuild brings it back."""
    sldb_cli = str(Path(sys.executable).with_name("sldb"))
    removed = subprocess.run([sldb_cli, "stores", "remove", name, "--store", ".sldb"], cwd=root, capture_output=True, text=True)
    if removed.returncode != 0:
        return removed
    return subprocess.run([sldb_cli, "stores", "declare", "--write", "--store", ".sldb"], cwd=root, capture_output=True, text=True)


def build_deskops_copy(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A copy of the deskops store, made once, that does not lead out of `<tmp>`: `<tmp>/deskops`
    (`copy_store_project`) with its links removed by `sldb stores remove`. A link sldb refuses to
    remove is served by a copy of that store at `<tmp>/<name>`, so its links back to `../deskops`
    resolve to the copy, and that copy's links leading out of `<tmp>` are removed; if sldb refuses
    that too, the test fails. Its `.sldb` path."""
    source = WORKSPACE / "deskops"
    if not (source / ".sldb" / "core").is_dir():
        pytest.fail(f"the deskops store is missing: {source / '.sldb'}")
    base = tmp_path_factory.mktemp("deskops-copy").resolve()
    root = base / "deskops"
    store = copy_store_project(source, root)
    pending = [root]
    while pending:
        project = pending.pop()
        for name, linked in linked_stores(project).items():
            if linked.is_relative_to(base) and (linked / "core").is_dir():
                continue
            removed = remove_link(project, name)
            if removed.returncode == 0:
                continue
            if project != root:
                pytest.fail(f"sldb refused to remove the link {name} -> {linked} of the copy {project}, which leads out of {base} ({removed.returncode}):\n{removed.stdout}\n{removed.stderr}")
            copied = base / name
            if copied.exists() or not (linked / "core").is_dir():
                pytest.fail(f"sldb refused to remove the link {name} -> {linked} of the deskops copy and it cannot be copied to {copied} ({removed.returncode}):\n{removed.stdout}\n{removed.stderr}")
            copy_store_project(linked.parent, copied)
            if linked_stores(root)[name] != (copied / ".sldb").resolve():
                pytest.fail(f"the link {name} of the deskops copy does not resolve to its copy {copied}")
            pending.append(copied)
    return store


@pytest.fixture(scope="session")
def deskops_copy(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The `.sldb` of the session's copy of the deskops store (`build_deskops_copy`)."""
    return build_deskops_copy(tmp_path_factory)


@pytest.fixture(scope="session")
def federated(deskops_copy: Path) -> dict[str, Path]:
    """The stores linked by alias in every mounted copy, besides the specs store: the deskops copy."""
    return {"deskops": deskops_copy}


def federated_digest(federated: dict[str, Path]) -> dict[str, str]:
    """The linked stores' `.sldb/` trees and the documents they track (the files of each store's
    project that git listed when the copy was made, read in the copy, outside the cache)."""
    digest = tree_digest(*federated.values())
    for store in federated.values():
        root = store.parent
        for rel in TRACKED[store]:
            path = root / rel
            if path.is_file() and path.suffix == ".md" and CACHE not in path.parts:
                digest[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def sldb(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    """Run the public `sldb` CLI of this environment; fail the test with its output on error."""
    command = [str(Path(sys.executable).with_name("sldb")), *args]
    done = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if done.returncode != 0:
        pytest.fail(f"{' '.join(args)} failed ({done.returncode}):\n{done.stdout}\n{done.stderr}")
    return done


def spec_store_digest(spec_store: Path) -> dict[str, str]:
    """The specs store's `.sldb/` tree and the documents of its project (not a git repo, so
    every `.md` under it, outside the cache)."""
    digest = tree_digest(spec_store)
    for path in sorted(spec_store.parent.rglob("*.md")):
        if path.is_file() and CACHE not in path.parts:
            digest[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def build_spec_store(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A new sldb store, outside any mounted copy, with the SpecDoc of this repo's spec fixture
    synced by `sldb.api` (as tests/visual/test_notations_parity.py does); its `.sldb` path."""
    from sldb.api import init_store
    from sldb.api.notations import SpecSync

    project = tmp_path_factory.mktemp("spec-store")
    spec = project / SPEC_FIXTURE
    spec.parent.mkdir(parents=True)
    shutil.copy2(SPEC_FIXTURES / SPEC_FIXTURE, spec)
    init_store(project)
    store = project / ".sldb"
    SpecSync(store).sync(spec)
    return store


@pytest.fixture(scope="session")
def spec_store(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The `.sldb` of the temporary specs store linked as `spec2viz` in every mounted copy."""
    return build_spec_store(tmp_path_factory)


@pytest.fixture(scope="session")
def original_digest() -> dict[str, str]:
    """This repo's `.sldb/` and `desk/` before any test ran."""
    return tree_digest(REPO / ".sldb", REPO / "desk")


def mount_copy(tmp_path_factory: pytest.TempPathFactory, name: str, spec_store: Path, federated: dict[str, Path]) -> Path:
    """The project root of a new isolated copy of this repo's store, mounted and checked, with
    the `federated` stores (the deskops copy) and the specs store `spec_store` (as `spec2viz`) linked."""
    for alias, store in federated.items():
        if not (store / "core").is_dir():
            pytest.fail(f"the {alias} store is missing: {store}")
    root = tmp_path_factory.mktemp(name) / "IR"
    root.mkdir()
    for name in COPIED:
        shutil.copytree(REPO / name, root / name, ignore=shutil.ignore_patterns(CACHE), symlinks=True)
    for run_doc in sorted(REPO.glob(RUN_DOCS)):
        target = root / run_doc.relative_to(REPO)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(run_doc, target)
    sldb("stores", "add", str(federated["deskops"]), "--name", "deskops", "--replace", "--store", ".sldb", cwd=root)
    sldb("stores", "add", str(spec_store), "--name", "spec2viz", "--store", ".sldb", cwd=root)
    sldb("stores", "update", "--store", ".sldb", cwd=root)
    sldb("edges", "rebuild", "--store", ".sldb", cwd=root)
    sldb("stores", "check", "--store", ".sldb", cwd=root)
    return root


def copy_digest(root: Path, spec_store: Path, federated: dict[str, Path]) -> dict[str, str]:
    """A mounted copy and the linked stores (the `federated` copies and the specs store), file by file."""
    return {**tree_digest(*(root / name for name in COPIED)), **federated_digest(federated), **spec_store_digest(spec_store)}


@pytest.fixture(scope="session")
def store_copy(tmp_path_factory: pytest.TempPathFactory, original_digest: dict[str, str], spec_store: Path, federated: dict[str, Path]) -> Path:
    """The copy the read tools are served from; nothing writes to it."""
    return mount_copy(tmp_path_factory, "specir-store", spec_store, federated)


class McpSession:
    """The real MCP client, connected over stdio to the real `sldb mcp` server, driven from sync tests."""

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
def copy_digest_before(store_copy: Path, spec_store: Path, federated: dict[str, Path]) -> dict[str, str]:
    """The mounted copy and the linked stores before the server reads them."""
    return copy_digest(store_copy, spec_store, federated)


@contextmanager
def served(root: Path, *options: str) -> Iterator[McpSession]:
    """A session with `python -m sldb mcp --store <root>/.sldb --extension specir.mcp_extension:register
    <options>`, launched by stdio."""
    from anyio.from_thread import start_blocking_portal
    from mcp import Client, StdioServerParameters

    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "sldb", "mcp", "--store", str(root / ".sldb"), "--extension", EXTENSION, *options],
        cwd=str(root),
        env={**os.environ},
    )
    with start_blocking_portal() as portal:
        with portal.wrap_async_context_manager(Client(params, read_timeout_seconds=TOOL_TIMEOUT)) as client:
            yield McpSession(portal, client)


@pytest.fixture(scope="session")
def mcp(store_copy: Path, copy_digest_before: dict[str, str]) -> Iterator[McpSession]:
    """The read-only server (level 0, the default) over the read copy."""
    with served(store_copy) as session:
        yield session


#: Who writes the blog chain (IR06); every node and edge of it must carry it.
BLOG_WRITER = "agent:specir-ir06-blog"


@pytest.fixture(scope="session")
def blog_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A new project with an SLDB store and specIR installed (tests/models/blog.py), empty."""
    from blog import new_blog_project

    return new_blog_project(tmp_path_factory.mktemp("specir-blog") / "blog")


@pytest.fixture(scope="session")
def blog(blog_root: Path) -> Iterator[McpSession]:
    """The server at write level 1 over the blog store, after it wrote the chain of
    tests/fixtures/blog_chain.yaml (its answers in `blog.populated`)."""
    from blog import populate

    with served(blog_root, "--level", "1", "--actor", BLOG_WRITER) as session:
        session.populated = populate(session)
        yield session
