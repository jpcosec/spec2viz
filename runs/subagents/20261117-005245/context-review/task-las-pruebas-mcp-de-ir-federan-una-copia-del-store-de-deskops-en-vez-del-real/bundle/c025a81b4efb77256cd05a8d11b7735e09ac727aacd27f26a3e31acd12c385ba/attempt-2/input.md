FILE:desk/tasks/task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real.md
---
sldb:
  by: agent
  at: '2026-11-17T00:08:00Z'
  authority: generated
  via: save_document_payload
id: task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- tests/conftest.py
- tests/test_mcp_extension.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Las pruebas MCP de IR federan una copia del store de deskops en vez del real

## Rationale

_Explain why this task exists or the business driver behind it._

tests/test_mcp_extension.py::test_reading_through_every_tool_leaves_every_store_untouched digiere el store real de deskops (FEDERATED en tests/conftest.py). Cualquier agente que escriba en deskops mientras corre la suite completa de IR la hace fallar sin relación con la tarea que se prueba. Le pasó tres veces seguidas al tester de IR13g (runs/subagents/deskops-t-e9062210030f, corridas 1 a 3), y antes al de la federación. Así, la suite de IR no da verde mientras deskops trabaja.

## Goal

_Describe the concrete result this task must produce._

La suite completa de IR es reproducible con independencia de lo que hagan otros desks: las pruebas MCP enlazan y digieren una copia del store de deskops tomada al inicio de la sesión, no el store real.

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/conftest.py y tests/test_mcp_extension.py. El fixture que enlaza deskops copia su store (y lo que haga falta para que sus enlaces resuelvan) a un directorio temporal de sesión, y la prueba de untouched digiere esa copia. Se conserva la cobertura de leer a través de un store federado. Fuera: cambiar deskops o sldb; la tarea de federación de spec2viz, que ya cambia esos archivos y va primero.

## Implementation Path

_Outline the expected implementation route or affected surface._

Empezar con task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a integrada (closeout 4f1e108 en main de IR). Seguir su patrón: build_spec_store construye un store temporal y el digest cubre ese store temporal. Si copiar el store de deskops rompe la resolución de sus enlaces a sldb, pron o scion, detenerse y anotarlo como bloqueo en result-summary.md. Precisiones (preflight-1): (a) Una función auxiliar build_deskops_copy(tmp_path_factory) -> Path, llamada desde un fixture de pytest con scope="session", hace la copia una vez, al montarse el fixture y antes de cualquier prueba que lo use. Crea <tmp>/deskops con el .sldb de deskops (sin la caché) y los archivos que lista git -C <deskops> ls-files, y devuelve <tmp>/deskops/.sldb. (b) Enlaces (corregida en el ciclo de corrección 1, tras el FAIL D2 del tester deskops-t-af2c27434a91): la copia no debe permitir que la sesión salga de <tmp>. Los symlinks a los repos reales quedan prohibidos, porque los stores de sldb y scion federan de vuelta ../deskops/.sldb, y así la sesión MCP leía el store real. Primera opción: quitar de la copia los enlaces a sldb, pron y scion con la CLI pública (sldb stores remove, con --store sobre la copia). Si sldb rechaza quitar un enlace porque un modelo de deskops depende de él, la segunda opción es copiar ese store enlazado igual que el de deskops (su .sldb sin caché más los archivos de su git ls-files) a <tmp>/<nombre>. Así sus enlaces relativos de vuelta a ../deskops resuelven a la copia. Un enlace de esas copias que apunte fuera de <tmp> se quita con sldb stores remove. Si sldb también rechaza eso, se detiene y se reporta. Esos stores copiados solo se leen y no se digieren. (c) FEDERATED pasa a recibir esa copia, por fixture y no como constante con la ruta real. federated_digest digiere la copia, con el mismo criterio de hoy: el árbol .sldb más los .md listados por git ls-files del proyecto real, leídos en la copia. mount_copy enlaza la copia con sldb stores add <copia> --name deskops. (d) La prueba de untouched es tests/test_mcp_extension.py::test_reading_through_every_tool_leaves_every_store_untouched; sus aserciones no se relajan.

## Validation

_List the checks required before this task can close._

- grep -nE 'WORKSPACE / "deskops"|\.\./deskops' tests/conftest.py tests/test_mcp_extension.py solo encuentra, si encuentra algo, el origen de la copia dentro de build_deskops_copy; ninguna prueba ni digest usa la ruta real.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -rs -p no:cacheprovider tests/test_mcp_extension.py sale con rc 0 y sin skipped.
- En la copia montada, sldb stores list (o el store_index de la copia) muestra el alias deskops apuntando a un directorio temporal, no a ../deskops del workspace.
- strace -f sobre la corrida de tests/test_mcp_extension.py: pasada la ventana de la copia, ningún proceso (pytest, sldb mcp, sldb stores) abre archivos bajo SLDB_1/deskops/ del workspace.
- Suite completa una vez bajo flock /dev/shm/sldb1-tests.lock con rc 0.
- deskops graph missing --root . (desde la raíz de IR) sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas MCP de IR no leen ni digieren el store real de deskops y la suite completa da verde aunque deskops escriba durante la corrida.

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:49Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo
status: active
summary: Mandato anti-mock para toda tarea de código de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: sin mocks ni datos fabricados; detenerse ante un bloqueo

## What

_Define the context or guardrail this pill carries._

El entregable no contiene mocks, stubs, constantes falsas, no-ops, datos fabricados ni atajos TODO. Las pruebas validan la salida real contra un store, fixture o golden real, no contra literales que duplican la respuesta esperada.

## Why

_Explain why this context matters for safe execution._

Un cierre verde con datos falsos oculta que la capacidad no existe; el valor de specIR es que el grafo refleje el sistema real.

## When

_Describe when an agent should apply this pill._

En toda tarea de código, durante la implementación y la validación.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/, tests/ y tests/fixtures/.

## How

_Describe the correct way to apply this guidance._

Las pruebas corren contra un store SLDB de prueba real y contra fixtures que son aplicaciones o specs reales. Si una dependencia real no está disponible, el ejecutor se detiene y reporta el bloqueo.

## How Not

_Describe the shortcut or failure mode to avoid._

No simular SLDB, el SDK de MCP ni una aplicación de fixture; no escribir pruebas que solo comparan con un literal inline; no marcar como hecho algo que solo está esbozado.

FILE:tests/conftest.py
"""Fixtures of the specIR tests: an isolated copy of this repo's real store, mounted with
SLDB's public CLI, and the real MCP server of sldb (`sldb mcp`) with specIR's extension
(`specir.mcp_extension:register`) over stdio, driven by the real MCP client.

Nothing is fabricated: the copy holds this repo's `.sldb/`, `sldb/` and `desk/` as they
are, plus every `runs/subagents/*/run.md` at its own relative path. The store linked as `deskops`
is not the real one: it is a copy of deskops's `.sldb/` and git-tracked files, taken once per
session (`deskops_copy`), so other desks writing to deskops during the run do not move the digest;
it is only read. The store linked as `spec2viz` is not spec2viz's: it is a new sldb store
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

REPO = Path(__file__).resolve().parents[1]
WORKSPACE = REPO.parent
COPIED = (".sldb", "sldb", "desk")
#: The store registers RunDocs, which live outside `.sldb/` and `desk/`.
RUN_DOCS = "runs/subagents/*/run.md"
#: The workspace repos the deskops store links by relative path (`../<name>/.sldb` in its
#: store_index); next to the copy they are symlinks to the real repos, only read, not digested.
DESKOPS_LINKED = ("sldb", "pron", "scion")
#: The git-tracked files of each deskops copy, listed once when the copy was made.
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


def build_deskops_copy(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A copy of the deskops store, made once: `<tmp>/deskops` with deskops's `.sldb/` (cache
    left out) and the files `git ls-files` lists in deskops, plus `<tmp>/{sldb,pron,scion}`
    symlinked to the real workspace repos so the store's relative links resolve; its `.sldb` path."""
    source = WORKSPACE / "deskops"
    if not (source / ".sldb" / "core").is_dir():
        pytest.fail(f"the deskops store is missing: {source / '.sldb'}")
    base = tmp_path_factory.mktemp("deskops-copy")
    for name in DESKOPS_LINKED:
        linked = WORKSPACE / name
        if not (linked / ".sldb" / "core").is_dir():
            pytest.fail(f"the {name} store linked by deskops is missing: {linked / '.sldb'}")
        (base / name).symlink_to(linked, target_is_directory=True)
    root = base / "deskops"
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

FILE:tests/test_mcp_extension.py
"""specIR on the MCP server of sldb: the real `sldb mcp --extension specir.mcp_extension:register`,
reached by the real MCP client over stdio, over an isolated copy of this repo's store (with a
session copy of the deskops store linked, and a temporary specs store built from this repo's spec fixture
linked as `spec2viz`). At level 0 there is no write tool, and reading through every tool, sldb's
and specIR's, changes no file of any store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from sldb.api import extract_document_payload

from conftest import REPO, WORKSPACE, copy_digest, tree_digest

#: sldb's read surface (sldb.mcp.registry.READ_TOOLS) and its signal log.
SLDB_READ = {
    "list_models", "describe_model", "list_relation_types", "describe_relation_type",
    "read_document", "select_documents", "neighbors", "neighborhood",
    "list_views", "resolve_view", "check_integrity", "list_signals",
}
SLDB_WRITE = {"propose_changes", "apply_changes"}
#: specIR's own tools (specir.mcp_extension).
DOMAIN = {"specir_types", "specir_nodes"}
SPEC_STORE = "spec2viz"
SPEC = "class.sldb-models"


def every_page(mcp, tool: str, limit: int = 50, **arguments: Any) -> list[Any]:
    """Every item of a paged answer, following `next_offset`."""
    items: list[Any] = []
    offset: int | None = 0
    while offset is not None:
        answer = mcp.call(tool, offset=offset, limit=limit, **arguments)
        items += answer["items"]
        offset = answer["next_offset"]
    return items


def test_the_server_of_sldb_serves_its_tools_and_specirs(mcp) -> None:
    tools = {t.name: t for t in mcp.list_tools()}
    assert set(tools) == SLDB_READ | DOMAIN
    for name in DOMAIN:
        assert tools[name].description and tools[name].output_schema is not None, name
        assert tools[name].annotations.read_only_hint is True, name


def test_at_level_0_no_write_tool_exists(mcp) -> None:
    assert not SLDB_WRITE & {t.name for t in mcp.list_tools()}
    answer = mcp.portal.call(lambda: mcp.client.call_tool("propose_changes", {"changes": []}))
    assert answer.is_error is False and answer.structured_content["signal"] == "unknown_tool", answer


def test_specir_types_over_a_store_without_them(mcp) -> None:
    from specir.models import DOMAIN_MODELS

    answer = mcp.call("specir_types")
    assert [r["type"] for r in answer["items"]] == [m.__name__ for m in DOMAIN_MODELS]
    assert not any(r["registered"] for r in answer["items"]) and "specir.install" in answer["explanation"]
    nodes = mcp.call("specir_nodes")
    assert nodes["total"] == 0 and nodes["explanation"]


def test_a_spec_of_the_linked_spec2viz_store_is_read_through_the_server(mcp, spec_store: Path) -> None:
    store = spec_store
    indexed = store / "core" / "documents" / "SpecDoc" / f"{SPEC}.yaml"
    assert indexed.is_file(), f"the {SPEC_STORE} store has no SpecDoc {SPEC}: {indexed}"
    export_id = f"{SPEC_STORE}:SpecDoc:{SPEC}"
    assert export_id in {v["view"] for v in every_page(mcp, "list_views") if v["kind"] == "spec"}
    entry = yaml.safe_load(indexed.read_text(encoding="utf-8").split("\n---", 1)[0])
    document = mcp.call("read_document", ref=export_id)
    assert document["found"] and document["store"] == SPEC_STORE and document["address"] == f"sldb://document/{export_id}"
    assert document["path"] == entry["path"] and document["version"] == entry["content_hash"]
    assert (store.parent / entry["path"]).is_file()
    #: The payload sldb extracts from the temporary store itself (the document's front matter also
    #: carries sldb's provenance block `sldb:`, which is not a field of the payload).
    expected = extract_document_payload(store, None, SPEC)
    assert expected["id"] == SPEC
    for key, value in expected.items():
        assert document["payload"][key] == value, key


def test_the_deskops_store_linked_is_the_session_copy(store_copy: Path, federated: dict[str, Path]) -> None:
    index = yaml.safe_load((store_copy / ".sldb" / "core" / "store_index.yaml").read_text(encoding="utf-8"))
    linked = {store["name"]: (store_copy / store["path"]).resolve() for store in index["stores"]}
    assert linked["deskops"] == federated["deskops"].resolve()
    assert not linked["deskops"].is_relative_to(WORKSPACE.resolve()), linked["deskops"]


def test_reading_through_every_tool_leaves_every_store_untouched(mcp, store_copy: Path, spec_store: Path, federated: dict[str, Path], copy_digest_before: dict[str, str], original_digest: dict[str, str]) -> None:
    task = mcp.call("select_documents", model="TaskDoc", limit=1)["items"][0]["export_id"]
    calls = [
        ("list_models", {}),
        ("describe_model", {"model": "TaskDoc"}),
        ("list_relation_types", {}),
        ("describe_relation_type", {"name": "references"}),
        ("read_document", {"ref": task}),
        ("read_document", {"ref": task, "field": "status"}),
        ("select_documents", {"model": "AtomDoc", "include_linked": True}),
        ("neighbors", {"node": task, "direction": "outgoing"}),
        ("neighbors", {"node": task, "direction": "incoming"}),
        ("neighborhood", {"node": task, "direction": "both", "depth": 2}),
        ("list_views", {}),
        ("resolve_view", {"view": f"{SPEC_STORE}:SpecDoc:{SPEC}"}),
        ("resolve_view", {"view": "board"}),
        ("check_integrity", {}),
        ("list_signals", {}),
        ("specir_types", {}),
        ("specir_nodes", {"layer": "api"}),
    ]
    for tool, arguments in calls:
        mcp.call(tool, **arguments)
    assert {tool for tool, _ in calls} == {t.name for t in mcp.list_tools()}
    after = copy_digest(store_copy, spec_store, federated)
    changed = sorted(path for path in set(copy_digest_before) | set(after) if copy_digest_before.get(path) != after.get(path))
    assert not changed, f"reading wrote to: {changed}"
    now = tree_digest(REPO / ".sldb", REPO / "desk")
    moved = sorted(path for path in set(original_digest) | set(now) if original_digest.get(path) != now.get(path))
    assert not moved, f"the repo's own store changed during the tests: {moved}"

FILE:instruccion
Cold-bundle de la tarea task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -nE 'WORKSPACE / "deskops"|\.\./deskops' tests/conftest.py tests/test_mcp_extension.py solo encuentra, si encuentra algo, el origen de la copia dentro de build_deskops_copy; ninguna prueba ni digest usa la ruta real.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -rs -p no:cacheprovider tests/test_mcp_extension.py sale con rc 0 y sin skipped.
- En la copia montada, sldb stores list (o el store_index de la copia) muestra el alias deskops apuntando a un directorio temporal, no a ../deskops del workspace.
- strace -f sobre la corrida de tests/test_mcp_extension.py: pasada la ventana de la copia, ningún proceso (pytest, sldb mcp, sldb stores) abre archivos bajo SLDB_1/deskops/ del workspace.
- Suite completa una vez bajo flock /dev/shm/sldb1-tests.lock con rc 0.
- deskops graph missing --root . (desde la raíz de IR) sale con rc 0.

