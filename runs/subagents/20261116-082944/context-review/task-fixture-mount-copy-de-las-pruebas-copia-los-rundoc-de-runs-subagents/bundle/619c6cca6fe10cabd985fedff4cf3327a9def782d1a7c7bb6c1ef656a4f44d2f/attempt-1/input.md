FILE:desk/tasks/task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents.md
---
sldb:
  by: agent
  at: '2026-11-16T08:29:18Z'
  authority: generated
  via: save_document_payload
id: task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:pruebas
- host:robocop2
current_node: ritual-execution
history: []
references:
- runs/subagents/deskops-t-5a39cc2dfbf8/result-summary.md
depends_on: []
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- tests/conftest.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Fixture mount_copy de las pruebas copia los RunDoc de runs/subagents

## Rationale

_Explain why this task exists or the business driver behind it._

El store de IR registra RunDocs, que el rol deskops-supervisor exige escribir como intención antes de cada despacho, y esos RunDocs viven en runs/subagents/<run>/run.md. El fixture mount_copy de tests/conftest.py copia solo .sldb, sldb y desk (COPIED), así que en la copia aislada 'sldb stores update' falla con 'Skipped missing documents: run-…' y las 5 pruebas de tests/test_mcp_extension.py dan error de setup. Con eso la suite completa de IR no puede salir con rc 0 mientras exista un RunDoc. Evidencia: runs/subagents/deskops-t-5a39cc2dfbf8/result-summary.md, sección «Suite completa».

## Goal

_Describe the concrete result this task must produce._

La copia aislada del store que arma mount_copy contiene también cada runs/subagents/*/run.md del repo, en la misma ruta relativa, y tests/test_mcp_extension.py pasa con RunDocs registrados en el store.

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/conftest.py, solo mount_copy y sus constantes: además de COPIED, copiar cada archivo que coincida con runs/subagents/*/run.md (y solo esos, no el resto de runs/ ni session.jsonl) a la misma ruta relativa bajo la raíz de la copia; actualizar el docstring del módulo, que hoy dice que la copia tiene .sldb, sldb y desk. Fuera: tocar .sldb, desk o runs del repo; cambiar original_digest o copy_digest (siguen midiendo .sldb y desk); cambiar FEDERATED; cualquier otro archivo de tests o de src.

## Implementation Path

_Outline the expected implementation route or affected surface._

En tests/conftest.py, mount_copy (línea 70): después del bucle sobre COPIED, recorrer sorted(REPO.glob('runs/subagents/*/run.md')) y copiar cada uno con shutil.copy2 a root / path.relative_to(REPO), creando el directorio padre. Declarar el patrón como constante de módulo junto a COPIED (por ejemplo RUN_DOCS = 'runs/subagents/*/run.md'), con un comentario de una línea que diga por qué: el store registra RunDocs que viven fuera de .sldb y desk. Comandos desde la raíz de IR con TMPDIR=/dev/shm y el .venv del repo.

## Validation

_List the checks required before this task can close._

- Con RunDocs registrados en el store (hoy existen runs/subagents/deskops-e-31500ac1cfa1/run.md y runs/subagents/deskops-t-5a39cc2dfbf8/run.md): TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mcp_extension.py sale con rc 0 y 5 passed.
- git diff --stat muestra solo tests/conftest.py fuera de desk/, .sldb/ y runs/.
- Suite completa una vez bajo el lock: SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/ sale con rc 0.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

mount_copy copia los runs/subagents/*/run.md, tests/test_mcp_extension.py pasa con RunDocs en el store y la suite completa de IR sale con rc 0.

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
are; the deskops and spec2viz stores are linked in place and only read."""

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
FEDERATED = {"deskops": WORKSPACE / "deskops" / ".sldb", "spec2viz": WORKSPACE / "spec2viz" / ".sldb"}
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


def mount_copy(tmp_path_factory: pytest.TempPathFactory, name: str) -> Path:
    """The project root of a new isolated copy of this repo's store, mounted and checked."""
    for alias, store in FEDERATED.items():
        if not (store / "core").is_dir():
            pytest.fail(f"the {alias} store is missing: {store}")
    root = tmp_path_factory.mktemp(name) / "IR"
    root.mkdir()
    for name in COPIED:
        shutil.copytree(REPO / name, root / name, ignore=shutil.ignore_patterns(CACHE), symlinks=True)
    sldb("stores", "add", str(FEDERATED["deskops"]), "--name", "deskops", "--replace", "--store", ".sldb", cwd=root)
    sldb("stores", "add", str(FEDERATED["spec2viz"]), "--name", "spec2viz", "--store", ".sldb", cwd=root)
    sldb("stores", "update", "--store", ".sldb", cwd=root)
    sldb("edges", "rebuild", "--store", ".sldb", cwd=root)
    sldb("stores", "check", "--store", ".sldb", cwd=root)
    return root


def copy_digest(root: Path) -> dict[str, str]:
    """A mounted copy and the linked stores, file by file."""
    return {**tree_digest(*(root / name for name in COPIED)), **federated_digest()}


@pytest.fixture(scope="session")
def store_copy(tmp_path_factory: pytest.TempPathFactory, original_digest: dict[str, str]) -> Path:
    """The copy the read tools are served from; nothing writes to it."""
    return mount_copy(tmp_path_factory, "specir-store")


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
def copy_digest_before(store_copy: Path) -> dict[str, str]:
    """The mounted copy and the linked stores before the server reads them."""
    return copy_digest(store_copy)


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

FILE:instruccion
Cold-bundle de la tarea task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Con RunDocs registrados en el store (hoy existen runs/subagents/deskops-e-31500ac1cfa1/run.md y runs/subagents/deskops-t-5a39cc2dfbf8/run.md): TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mcp_extension.py sale con rc 0 y 5 passed.
- git diff --stat muestra solo tests/conftest.py fuera de desk/, .sldb/ y runs/.
- Suite completa una vez bajo el lock: SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/ sale con rc 0.
- deskops graph missing --root . sale con rc 0.

