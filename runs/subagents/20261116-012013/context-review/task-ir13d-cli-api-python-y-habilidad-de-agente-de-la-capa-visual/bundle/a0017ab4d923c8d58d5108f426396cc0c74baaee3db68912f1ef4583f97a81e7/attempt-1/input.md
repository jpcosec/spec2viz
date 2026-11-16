FILE:desk/tasks/task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual.md
---
sldb:
  by: agent
  at: '2026-11-16T01:20:02Z'
  authority: generated
  via: save_document_payload
id: task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs
- task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos
- task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/cli.py
- src/specir/visual/__init__.py
- src/specir/visual/commands.py
- pyproject.toml
- skills/use-specir/SKILL.md
- docs/spec2viz/correspondencia-cli.md
- docs/spec2viz/matriz-de-cobertura.md
- tests/visual/test_cli.py
- tests/visual/test_api.py
- tests/visual/test_packaging.py
- tests/visual/test_render_commands.py
- tests/visual/test_schema.py
- tests/visual/test_lint_mermaid.py
- tests/visual/test_render_cases.py
- tests/visual/test_bpmn.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13d CLI, API Python y habilidad de agente de la capa visual

## Rationale

_Explain why this task exists or the business driver behind it._

Parte de la migración final de spec2viz, separada de IR13 para que cada tarea tenga un solo entregable. Los consumidores de spec2viz lo usan por su comando, por su API Python y por una habilidad de agente; sin equivalentes en specIR no tienen a dónde migrar.

## Goal

_Describe the concrete result this task must produce._

specIR ofrece un comando, una API Python pública y una habilidad de agente que cubren cada entrada pública de spec2viz.

## Scope

_State what is in scope and what is out of scope._

Dentro: comando de specIR con equivalentes de todos los comandos y subgrupos de spec2viz (diagram, notation, palette, catalog, y los alias de primer nivel render, validate, lint, schema y build, y about); API Python pública equivalente a la que exporta el paquete spec2viz; habilidad de agente que reemplaza a la de uso de spec2viz; tabla de correspondencia comando por comando.
Fuera: implementar las capacidades, que vienen de las tareas de compiladores, renderers, IR13a, IR13b e IR13c; instalar la habilidad en otros repos; migrar consumidores.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo src/specir/cli.py y exportaciones públicas en src/specir/visual/__init__.py que conectan las capacidades ya implementadas; habilidad en skills/use-specir/SKILL.md; correspondencia en docs/spec2viz/correspondencia-cli.md. Paridad medida portando a tests/visual/ las pruebas de spec2viz de CLI, API y empaquetado. Propiedad de archivos compartidos: src/specir/visual/__init__.py ya existe cuando esta tarea empieza: lo crea la tarea de compiladores y proyecciones (IR11), de la que esta depende por la cadena IR13a e IR12. Aquí solo se extiende con las exportaciones públicas que faltan; no se recrea ni se quitan las exportaciones existentes.

Precisiones (preflight-2, resueltas por el worker de IR13d):
1. API pública: la lista sale de los nombres públicos del `__init__` del paquete spec2viz en la revisión 2de1056 (load, validate, compile_ir, render, json_schema, write_json_schema, render_to_file, with_provenance, provenance_header, provenance_text, EXT_MAP, DEFAULT_RENDERER, BaseDiagram). load y validate son de sldb (SV-J01, D3): se usan como `sldb.api.notations.load_spec` y `validate_spec`, sin reexportarlos en specIR. El resto lo exporta `specir.visual`, junto con el linter de mermaid y el catálogo (build_catalog, render_catalog, AnnotationsTarget). tests/visual/test_api.py porta el test_api de spec2viz y comprueba que cada nombre público de spec2viz tiene su equivalente (en specir.visual o en sldb).
2. Habilidad: mismo formato que las habilidades de agente existentes (frontmatter con name y description, orientación, ruta de lectura, taxonomía, contrato de renderers, flujo y validación). Nombra solo comandos que existen; lo que es de sldb lo enseña con el comando de sldb (regla de JP: nada de envoltorios sobre la CLI o la API de sldb).
3. Inventario de comandos: el árbol de comandos de la CLI de spec2viz (el mismo que comprueba tests/test_matriz_cobertura_spec2viz.py), filas SV-K01 a SV-K30 de la matriz. Los subgrupos notation y palette y los comandos sync, from-graph, generate, catalog sync, catalog validate y catalog serve no tienen equivalente en specIR: la correspondencia remite al comando de sldb y specIR no lo duplica.
4. Matriz: docs/spec2viz/matriz-de-cobertura.md (filas SV-J02, SV-J03, SV-J07 a SV-J09 y SV-K*). IR13d cita sus pruebas sin marcar filas cumplidas; marcarlas es de IR13.
5. Entorno limpio: un venv nuevo en /dev/shm con sldb y la wheel de specIR (sin spec2viz), donde `specir --help` y `specir about` arrancan y `import spec2viz` falla.
6. SV-K16 (validar un spec por CLI): sldb aún no tiene el comando (pedido en su inbox). Mientras tanto `specir diagram validate` y el alias `validate` llaman a `load_spec` y `validate_spec` de sldb sin redefinir nada; cuando sldb publique su comando, el de specIR se retira y la cabecera de procedencia pasa a nombrar el de sldb. Registrado en la matriz.
7. El script `specir` pasa a `specir.cli:main`; el módulo de comandos de IR12 conserva los grupos diagram y catalog, que cli.py monta y extiende con catalog build, los alias y about.

## Validation

_List the checks required before this task can close._

- Cada comando y subgrupo que lista la ayuda de spec2viz tiene una fila en la tabla de correspondencia con su equivalente en specIR, y una prueba invoca cada equivalente.
- Las pruebas de API de spec2viz portadas pasan contra la API pública de specIR.
- La habilidad de agente nombra solo comandos que existen en el comando de specIR (comprobado por una prueba que los extrae y los invoca con ayuda).
- El paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y las filas de CLI, API Python y habilidad de la matriz de cobertura tienen su condición de retiro cumplida.

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

FILE:desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:48Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-specir-solo-usa-la-api-pública-de-sldb
status: active
summary: Dependencias permitidas del paquete specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: specIR solo usa la API pública de SLDB

## What

_Define the context or guardrail this pill carries._

El código de specIR importa de SLDB únicamente sldb.api. No importa sldb.store, sldb.core ni otros módulos internos, y no importa pron ni spec2viz.

## Why

_Explain why this context matters for safe execution._

specIR es un repo periférico sobre SLDB; pron quedó descartado como base y spec2viz va a retirarse. Acoplarse a módulos internos de SLDB es lo que desfasó a pron.

## When

_Describe when an agent should apply this pill._

En toda tarea que escriba o modifique código bajo src/specir/ o tests/.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/ y tests/; lo comprueba tests/test_imports.py.

## How

_Describe the correct way to apply this guidance._

Si falta una operación general, se documenta la carencia y se pide en el desk de SLDB con deskops message send --to sldb; la tarea se detiene en ese punto si la carencia la bloquea.

## How Not

_Describe the shortcut or failure mode to avoid._

No reimplementar en specIR lo que es general de SLDB; no copiar código de pron ni de spec2viz como dependencia; no alcanzar módulos internos de SLDB aunque funcione.

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

FILE:desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas
status: active
summary: Cómo se acredita la cobertura de una capacidad de spec2viz.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: la paridad con spec2viz se demuestra con sus pruebas

## What

_Define the context or guardrail this pill carries._

Una capacidad de spec2viz se considera cubierta solo cuando la prueba o golden correspondiente de spec2viz pasa contra specIR, o cuando su fila de la matriz de cobertura declara un reemplazo con una prueba equivalente que pasa.

## Why

_Explain why this context matters for safe execution._

El objetivo es retirar spec2viz; declarar paridad sin prueba dejaría funcionalidades perdidas al retirarlo.

## When

_Describe when an agent should apply this pill._

En toda tarea que migre o reemplace una capacidad de spec2viz, y al evaluar el gate de retiro.

## Where

_Name the files, surfaces, or scope this pill applies to._

tests/visual/ en specIR; como referencia de solo lectura, spec2viz/tests/ y la matriz docs/spec2viz/matriz-de-cobertura.md.

## How

_Describe the correct way to apply this guidance._

Portar los fixtures y golden de spec2viz a tests/ de specIR y ejecutarlos; registrar en la matriz, por fila, la prueba que acredita la cobertura.

## How Not

_Describe the shortcut or failure mode to avoid._

No declarar una fila como cubierta porque otra herramienta la sustituya de hecho; no descartar una capacidad por falta de uso; no modificar un golden para que la prueba pase.

FILE:desk/atoms/atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:35Z'
  authority: generated
  via: create_document
id: atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
title: specIR reemplaza a spec2viz y cubre todas sus funciones
five_wh_one_plus: when
tags:
- system:specir
- system:spec2viz
- topic:migracion
---

# specIR reemplaza a spec2viz y cubre todas sus funciones

## Answer

spec2viz nació aparte porque SLDB no tenía grafos; ahora los tiene. specIR incorporará la capa visual y debe cubrir todas las funcionalidades de spec2viz; cuando las cubra, spec2viz se retira. Ninguna funcionalidad se da por descartada porque otra herramienta la sustituya de hecho: cada una se cubre migrándola tal cual, reemplazándola por otra arquitectura o experiencia con resultado equivalente, o exponiendo desde specIR lo que ya vive en SLDB. En los tres casos specIR responde por el camino de retiro. No es un consumidor permanente de spec2viz. Decisión del dueño del proyecto, 2026-11-11.

FILE:desk/atoms/atom-specir-depende-solo-de-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:34Z'
  authority: generated
  via: create_document
id: atom-specir-depende-solo-de-la-api-pública-de-sldb
title: specIR depende solo de la API pública de SLDB
five_wh_one_plus: how
tags:
- system:specir
- system:sldb
- topic:dependencias
- layer:arquitectura
---

# specIR depende solo de la API pública de SLDB

## Answer

specIR se construye directamente sobre la API pública de SLDB (sldb.api), como hace deskops. Una capacidad general que falte (por ejemplo una operación de grafo o de store) se pide o se agrega en SLDB; no se reimplementa dentro de specIR ni se alcanza por módulos internos de SLDB. En specIR vive lo específico: el servidor MCP, los tipos y reglas del modelado de sistemas de software, y más adelante la capa visual.

FILE:src/specir/cli.py
"""The `specir` command: the visual layer's CLI, with the taxonomy of spec2viz's (IR13d).

- `diagram` (render, validate, lint, schema) and `catalog` (schema) are IR12's groups
  (`specir.visual.commands`); this module mounts them and adds `catalog build` (IR13b's page, with
  the option to save its annotations through `sldb serve`), the top-level aliases `render`,
  `validate`, `lint`, `schema` and `build`, and `about`.
- What spec2viz's CLI did that is sldb's has no command here, by design (JP: no wrapper over sldb's
  CLI or API): syncing a spec, a notation, a palette or a catalog (`sldb notations sync --spec`,
  `--notation`, `--palette`, `--catalog [--check]`), generating a spec from a graph or from Python
  (`sldb notations from-graph`), listing notations and palettes (`sldb notations list`), resolving a
  view (`sldb notations view`) and serving the catalog's annotations (`sldb serve`). The table is
  `docs/spec2viz/correspondencia-cli.md`.
- `diagram validate` (and `validate`) runs sldb's `load_spec`/`validate_spec` and redefines
  nothing: sldb has no command that validates a spec yet (SV-K16); when it has one, it goes."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from specir.visual.commands import (
    DIAGRAM_RENDERERS,
    _lint_paths,
    _render_paths,
    _validate_paths,
    _write_schema,
    catalog,
    diagram,
)

#: The top-level aliases, each with the group command it stands for (spec2viz's legacy commands).
ALIASES = {"render": "diagram render", "validate": "diagram validate", "lint": "diagram lint", "schema": "diagram schema",
           "build": "catalog build"}


@click.group(
    help=(
        "specIR CLI: semantic diagram specs -> diagrams -> catalog HTML.\n\n"
        "\b\nTaxonomy:\n"
        "- diagram: semantic diagram specs (render, validate, lint, schema)\n"
        "- catalog: HTML bundles and hierarchical diagram stores (build, schema)\n\n"
        "Top-level aliases (render, validate, lint, schema, build) remain available for compatibility.\n\n"
        "Syncing specs, notations, palettes and catalogs into a store, generating specs from a graph "
        "or from Python, resolving views and serving annotations are sldb's: use `sldb notations ...` "
        "and `sldb serve` directly."
    )
)
@click.version_option(package_name="specir", prog_name="specir")
def main():
    pass


main.add_command(diagram)
main.add_command(catalog)


@main.command("about", short_help="Where diagrams live and how the flow reaches HTML.")
def about():
    """Point to where the diagrams live and the full spec -> HTML flow, with sldb's commands for the store."""
    from sldb.api.notations import find_store

    cwd = Path.cwd()
    store = find_store(cwd)
    click.echo("specir — semantic specs -> diagrams -> catalog HTML (specIR's visual layer over sldb)\n")

    click.echo("Where the diagrams live:")
    click.echo("  spec files       : YAML specs (`type:` one of the eight diagram types) next to their vistas.yml")
    click.echo(f"  store            : {store if store else f'no .sldb store above {cwd}'}")
    click.echo("  specs in a store : SpecDoc documents (`sldb notations list --store <.sldb>`)")
    click.echo("  catalog config   : a vistas.yml registry or a project.yml / diagram-store config\n")

    click.echo("Flow to HTML:")
    click.echo("  1. specir diagram validate <spec.yml>")
    click.echo("  2. specir diagram render   <spec.yml> --out <dir>")
    click.echo("  3. specir diagram lint     <rendered.mmd>")
    click.echo("  4. specir catalog build    --config <vistas.yml> --out <out.html>")
    click.echo("     (build alias = catalog build; --atoms-dir injects window.ATOMS_DB)\n")

    click.echo("Into the store (sldb, used directly):")
    click.echo("  sldb notations sync --spec <spec.yml> --store <.sldb>")
    click.echo("  sldb notations sync --catalog <vistas.yml> [--check] --store <.sldb>")
    click.echo("  sldb notations from-graph --python <src_dir> | --store <.sldb> | --snapshot <graph.json>")
    click.echo("  sldb notations view <SpecDoc id> --store <.sldb>\n")

    click.echo("Save a built catalog's annotations (replaces spec2viz's `catalog serve`):")
    click.echo("  sldb models add specir.visual.catalog.annotations:CatalogAnnotationsDoc --store <.sldb>")
    click.echo("  sldb serve --store <.sldb> --cors --port 8765")
    click.echo("  specir catalog build --config <vistas.yml> --out <out.html> --sldb-url http://127.0.0.1:8765")


# ── catalog build and its alias ─────────────────────────────────────────────────────────────────


def _build_catalog(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...],
                   strict_atoms: bool, annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    from specir.visual.catalog import AnnotationsTarget, build_catalog

    target = AnnotationsTarget(server=sldb_url or "", doc=annotations_doc or "") if (annotations or sldb_url or annotations_doc) else None
    try:
        build_catalog(config, out, base_dir, atoms_dir, list(atoms_tags) or None, strict_atoms, target)
        click.echo(f"Rendered catalog -> {out}")
    except Exception as exc:
        click.echo(f"Error building catalog: {exc}", err=True)
        sys.exit(1)


def _catalog_build_options(function):
    options = [
        click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="Path to a legacy vistas.yml registry or a hierarchical diagram store config."),
        click.option("--out", required=True, type=click.Path(path_type=Path), help="HTML file to write."),
        click.option("--base-dir", type=click.Path(exists=True, path_type=Path), help="Base directory for template and vista source paths. Defaults to the config file directory."),
        click.option("--atoms-dir", type=click.Path(exists=True, path_type=Path), help="Directory with W5H1 atom markdown files to inject as window.ATOMS_DB."),
        click.option("--atoms-tag", "atoms_tags", multiple=True, help="Embed only atoms carrying this tag (full `ns:value` or just `value`); repeatable. Default: all atoms."),
        click.option("--strict-atoms", is_flag=True, help="Fail the build if a spec `atoms:` id does not exist among the loaded atoms (default: warning)."),
        click.option("--annotations", is_flag=True, help="Save the page's annotations in an sldb store through `sldb serve`; the server and the document can also come from the page URL (`?sldb=<url>&annotations=<id>`)."),
        click.option("--sldb-url", default=None, help="Base URL of `sldb serve --cors` that keeps the annotations (implies --annotations)."),
        click.option("--annotations-doc", default=None, help="Id of the CatalogAnnotationsDoc that holds them (implies --annotations). Default: derived from the catalog's name."),
    ]
    for option in reversed(options):
        function = option(function)
    return function


@catalog.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@_catalog_build_options
def catalog_build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool,
                  annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    """Build a diagram catalog HTML bundle from a vistas registry or diagram store."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations, sldb_url, annotations_doc)


@main.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@_catalog_build_options
def build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool,
          annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    """Legacy alias for `catalog build`."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations, sldb_url, annotations_doc)


# ── the other top-level aliases ─────────────────────────────────────────────────────────────────


@main.command("render", short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option("--renderer", "--backend", type=click.Choice(DIAGRAM_RENDERERS), default=None, help="Force a renderer instead of using the spec type default.")
def render(paths: list[Path], out: Path, renderer: str | None):
    """Legacy alias for `diagram render`."""
    _render_paths(paths, out, renderer)


@main.command("validate", short_help="Validate semantic diagram spec files (sldb's load_spec and validate_spec).")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
def validate_cmd(paths: list[Path]):
    """Legacy alias for `diagram validate`."""
    _validate_paths(paths)


@main.command("lint", short_help="Lint rendered mermaid for browser-breaking syntax.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC_OR_MMD ...")
def lint_cmd(paths: list[Path]):
    """Legacy alias for `diagram lint`."""
    _lint_paths(paths)


@main.command("schema", short_help="Export JSON Schema for semantic specs.")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Limit the schema to one type: class, sequence, state, component, activity, deployment, component_view_matrix, or diagram-store.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def schema(diagram_type: str | None, out: Path | None):
    """Legacy schema entrypoint for diagram specs and diagram stores."""
    _write_schema(diagram_type, out)


__all__ = ["ALIASES", "main"]


if __name__ == "__main__":
    main()

FILE:src/specir/visual/__init__.py
"""specIR's visual layer: the intermediate representation, its compilers and the projections of
the graph to it (IR11); its renderers, mermaid linter, JSON Schema export, packaged resources and the
render, lint and schema commands are in `specir.visual.renderers`, `lint_mermaid`, `schema`,
`templates/`, `render_file` and `commands` (IR12); the HTML catalog of diagrams, its atoms and its
annotations saved with `sldb serve` are in `specir.visual.catalog` (IR13b). IR13d extends this module
with the full public API of the layer.

The spec models of the eight diagram types are sldb's (D3) and are only re-exported here for the
visual layer's callers; nothing of them is defined in specIR. `load_spec` and `validate_spec` are
used from `sldb.api.notations` directly, without a wrapper. So are syncing a spec to the store
(`SpecSync`, `sync_spec`; `sldb notations sync --spec`, D1) and generating a component spec from a
graph, a snapshot or the Python AST (`component_spec_from_graph`, `component_spec_from_python`,
`write_component_spec`; `sldb notations from-graph`, D2): specIR defines none of them (IR13a). So are
the matching of atoms with diagram elements and the coverage per view (`sldb.api.matching`, D4) and
the catalog's path rule, validation and sync (`sldb.api.notations`, `sldb notations sync --catalog`,
D1).

The public API of the layer (IR13d) covers what the `spec2viz` package exported: `compile_ir`,
`render` (with `RENDERER_MAP`, `EXT_MAP` and `DEFAULT_RENDERER`), `render_to_file` and its provenance
header (`with_provenance`, `provenance_header`, `provenance_text`), `json_schema` and
`write_json_schema`, plus the mermaid linter (`lint_mermaid`, `assert_mermaid_ok`) and the catalog page
(`render_catalog`, `build_catalog`, `AnnotationsTarget`). spec2viz's `load` and `validate` are sldb's
`load_spec` and `validate_spec` (`sldb.api.notations`), used directly and not re-exported here. The
`specir` command is `specir.cli`."""

from specir.visual.catalog import AnnotationsTarget, build_catalog, render_catalog
from specir.visual.compilers import compile_ir
from specir.visual.compilers.activity import ActivityCompiler
from specir.visual.compilers.class_diagram import ClassCompiler
from specir.visual.compilers.component import ComponentCompiler
from specir.visual.compilers.deployment import DeploymentCompiler
from specir.visual.compilers.matrix import MatrixCompiler
from specir.visual.compilers.reflection import ReflectionCompiler
from specir.visual.compilers.sequence import SequenceCompiler
from specir.visual.compilers.state import StateCompiler
from specir.visual.exceptions import CompileError, RenderError, Spec2VizError
from specir.visual.ir import *  # noqa: F401,F403 (the IR dataclasses, see specir.visual.ir.__all__)
from specir.visual.ir import __all__ as _IR
from specir.visual.lint_mermaid import MermaidLintError, assert_mermaid_ok, lint_mermaid
from specir.visual.normalize import differences, equivalent, normalize
from specir.visual.projections import component_from_view, from_spec_doc, state_from_view, view_graph
from specir.visual.render_file import provenance_header, provenance_text, render_to_file, with_provenance
from specir.visual.renderers import DEFAULT_RENDERER, EXT_MAP, RENDERER_MAP, render
from specir.visual.schema import json_schema, write_json_schema
from specir.visual.spec_models import (
    SPEC_MODELS,
    ActivityDiagram,
    BaseDiagram,
    ClassDiagram,
    ComponentDiagram,
    DeploymentDiagram,
    EnforcementArtifact,
    EnforcementFact,
    MatrixDiagram,
    ReflectionDiagram,
    SequenceDiagram,
    StateDiagram,
)

__all__ = [
    *_IR,
    "ActivityCompiler", "ClassCompiler", "ComponentCompiler", "DeploymentCompiler", "MatrixCompiler",
    "ReflectionCompiler", "SequenceCompiler", "StateCompiler", "compile_ir",
    "CompileError", "RenderError", "Spec2VizError",
    "differences", "equivalent", "normalize",
    "component_from_view", "from_spec_doc", "state_from_view", "view_graph",
    "SPEC_MODELS", "ActivityDiagram", "BaseDiagram", "ClassDiagram", "ComponentDiagram", "DeploymentDiagram",
    "EnforcementArtifact", "EnforcementFact", "MatrixDiagram", "ReflectionDiagram", "SequenceDiagram",
    "StateDiagram",
    # IR13d: the rest of what the spec2viz package exported, the linter and the catalog page.
    "DEFAULT_RENDERER", "EXT_MAP", "RENDERER_MAP", "render",
    "provenance_header", "provenance_text", "render_to_file", "with_provenance",
    "json_schema", "write_json_schema",
    "MermaidLintError", "assert_mermaid_ok", "lint_mermaid",
    "AnnotationsTarget", "build_catalog", "render_catalog",
]

FILE:src/specir/visual/commands.py
"""The render, lint and schema commands of the visual layer, migrated from `spec2viz.cli`.

`diagram render|lint|schema` and `catalog schema` keep spec2viz's arguments, options (`--renderer`
with its alias `--backend` and its nine values) and output. `diagram validate` runs sldb's
`load_spec`/`validate_spec` (D3) and is the command the provenance header of a projection names
(SV-K16: sldb has no command that validates a spec yet; when it has one, this one goes).
The `specir` command is `specir.cli` (IR13d): it mounts these two groups, adds `catalog build`, the
top-level aliases and `about`. The helpers `_render_paths`, `_validate_paths`, `_lint_paths` and
`_write_schema` are what a group command and its top-level alias share."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from sldb.api.notations import load_spec, validate_spec

from specir.visual.exceptions import Spec2VizError
from specir.visual.notation_style import NotationError
from specir.visual.render_file import render_to_file
from specir.visual.renderers import RENDERER_MAP
from specir.visual.schema import json_schema, write_json_schema

#: The values of `--renderer`, in spec2viz's order (the keys of the render dispatch).
DIAGRAM_RENDERERS = ["plantuml", "mermaid", "vega", "d2", "antonia-html", "tree", "graph", "bpmn", "json"]
assert set(DIAGRAM_RENDERERS) == set(RENDERER_MAP)

#: What a spec, a render or a lint can fail with: specIR's visual errors and sldb's notation errors.
ERRORS = (Spec2VizError, NotationError)


def _render_paths(paths: list[Path], out: Path, renderer: str | None):
    for path in paths:
        try:
            output = render_to_file(path, out=out, renderer=renderer)
            click.echo(f"Rendered {path.name} -> {output}")
            if renderer == "bpmn":
                click.echo(f"Rendered {path.name} -> {output.with_name(output.name + '.html')}")
        except ERRORS as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)


def _validate_paths(paths: list[Path]):
    for path in paths:
        try:
            validate_spec(load_spec(path))
            click.echo(f"{path.name}: OK")
        except ERRORS as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            sys.exit(1)


def _lint_paths(paths: list[Path]):
    """Lint mermaid text files (.mmd) or render specs to mermaid then lint."""
    from specir.visual.compilers import compile_ir
    from specir.visual.lint_mermaid import lint_mermaid
    from specir.visual.renderers import render

    had_issue = False
    for path in paths:
        try:
            if path.suffix == ".mmd":
                text = path.read_text(encoding="utf-8")
            else:
                text = render(compile_ir(load_spec(path)), "mermaid")
            problems = lint_mermaid(text)
        except ERRORS as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            had_issue = True
            continue
        if problems:
            had_issue = True
            click.echo(f"{path.name}: {len(problems)} issue(s)", err=True)
            for p in problems:
                click.echo(f"  - {p}", err=True)
        else:
            click.echo(f"{path.name}: OK")
    if had_issue:
        sys.exit(1)


def _write_schema(diagram_type: str | None, out: Path | None):
    if out:
        write_json_schema(out, diagram_type=diagram_type)
        click.echo(f"Wrote schema to {out}")
    else:
        click.echo(json.dumps(json_schema(diagram_type), indent=2))


@click.group(help="Work with semantic diagram specs.")
def diagram():
    pass


@click.group(help="Work with diagram catalogs, vistas registries, and hierarchical stores.")
def catalog():
    pass


@diagram.command("render", short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option(
    "--renderer",
    "--backend",
    type=click.Choice(DIAGRAM_RENDERERS),
    default=None,
    help="Force a renderer instead of using the spec type default.",
)
def diagram_render(paths: list[Path], out: Path, renderer: str | None):
    """Render one or more semantic diagram spec files."""
    _render_paths(paths, out, renderer)


@diagram.command("validate", short_help="Validate semantic diagram spec files (sldb's load_spec and validate_spec).")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
def diagram_validate(paths: list[Path]):
    """Validate one or more semantic diagram spec files."""
    _validate_paths(paths)


@diagram.command("lint", short_help="Lint rendered mermaid for browser-breaking syntax.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC_OR_MMD ...")
def diagram_lint(paths: list[Path]):
    """Lint .mmd files, or render specs to mermaid and lint the result."""
    _lint_paths(paths)


@diagram.command("schema", short_help="Export JSON Schema for semantic diagram specs.")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Limit the schema to one type: class, sequence, state, component, activity, deployment, component_view_matrix, or diagram-store.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def diagram_schema(diagram_type: str | None, out: Path | None):
    """Export JSON Schema for all diagram spec types or one diagram type."""
    _write_schema(diagram_type, out)


@catalog.command("schema", short_help="Export JSON Schema for hierarchical diagram stores.")
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def catalog_schema(out: Path | None):
    """Export JSON Schema for diagram-store / project.yml configs."""
    _write_schema("diagram-store", out)


__all__ = ["DIAGRAM_RENDERERS", "ERRORS", "catalog", "diagram"]

FILE:pyproject.toml
[project]
name = "specir"
version = "0.1.0"
description = "specIR: cross-layer domain types over an SLDB store, built on sldb.api, and its tools on the MCP server of sldb (sldb mcp --extension specir.mcp_extension:register)"
requires-python = ">=3.12"
dependencies = [
    "structuredLanguageDB",
    "pyyaml>=6.0",
    "click>=8.1",
]

[project.optional-dependencies]
# The extension (specir.mcp_extension) runs on the MCP server of sldb.
mcp = [
    "structuredLanguageDB[mcp]",
]
test = [
    # `code` brings tree-sitter, which sldb's Python AST spec generator (D2) needs (IR13a's tests).
    "structuredLanguageDB[mcp,code]",
    "pytest>=8",
    "pyyaml>=6.0",
]

[project.scripts]
specir-install = "specir.install:main"
# The visual layer's command (IR13d): diagram, catalog, the top-level aliases and about.
specir = "specir.cli:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
specir = ["data/*.yaml", "visual/templates/*.html", "visual/templates/*.js", "visual/templates/vendor/bpmn-js/*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "parity: compares specIR with spec2viz as the oracle; skipped when spec2viz is not installed",
]

FILE:skills/use-specir/SKILL.md
---
name: use-specir
description: Use when rendering, validating, linting or exporting the schema of semantic diagram specs, building the HTML catalog of diagrams (vistas.yml or diagram-store), or choosing a renderer, with specIR's `specir` command and its Python API (`specir.visual`). Replaces use-spec2viz. What is generic (syncing specs, notations, palettes and catalogs into a store, generating specs from a graph or from Python, resolving views, serving annotations) is sldb's and is used with the `sldb` command directly.
---

# Use specIR (visual layer)

specIR is the visual layer and domain mapping over SLDB stores. It replaces spec2viz: same diagram
types, same renderers, same catalog page. sldb owns everything generic; specIR never wraps it.

Use this skill when the task touches:

- rendering a diagram spec (plantuml, mermaid, vega, d2, antonia-html, tree, graph, bpmn, json)
- validating a spec, linting rendered mermaid, or exporting the JSON Schema of specs or diagram stores
- building the catalog HTML from a `vistas.yml` registry or a `project.yml` / diagram-store config
- saving the catalog's annotations in an sldb store
- the Python API `specir.visual` (compile, render, render to file, schema, lint, catalog)

## Fast orientation

Run `about` first: it shows the store above the current directory and the whole flow to HTML,
including the sldb commands for the store.

```bash
specir about
specir --help
specir diagram --help
specir catalog --help
```

`python -m specir.cli` is the same command when the script is not on `PATH`.

## Who owns what

| Need | Use | Not |
|---|---|---|
| Render, lint, schema of a spec | `specir diagram render`, `specir diagram lint`, `specir diagram schema` | |
| Validate a spec | `specir diagram validate` (calls sldb's `load_spec` and `validate_spec`; provisional until sldb has its own command) | |
| Catalog HTML | `specir catalog build` | |
| Catalog schema | `specir catalog schema` | |
| Sync a spec into a store | `sldb notations sync --spec` | a specIR command |
| Sync a notation or a palette | `sldb notations sync --notation`, `sldb notations sync --palette` | a specIR command |
| Sync or check a catalog | `sldb notations sync --catalog`, `sldb notations sync --catalog --check` | a specIR command |
| Spec from a graph, a store or Python | `sldb notations from-graph` (`--snapshot`, `--store`, `--python`) | a specIR command |
| List notations, palettes, views | `sldb notations list` | a specIR command |
| Resolve a spec's view | `sldb notations view` | a specIR command |
| Serve the catalog's annotations | `sldb serve` | spec2viz's catalog serve |
| Load and validate a spec in Python | `sldb.api.notations.load_spec`, `validate_spec` | a specIR re-export |

If sldb lacks something generic, write it to sldb's inbox (`deskops message send --to sldb`); do not
add it to specIR.

## Mandatory read route

1. `docs/spec2viz/correspondencia-cli.md`: every spec2viz command and its equivalent.
2. `src/specir/cli.py`: the command, the aliases and `about`.
3. `src/specir/visual/__init__.py`: the public Python API.
4. `src/specir/visual/renderers/__init__.py`: `RENDERER_MAP`, `EXT_MAP`, `DEFAULT_RENDERER`.
5. `src/specir/visual/catalog/build.py` when the task involves the catalog.

## CLI taxonomy

- `diagram`: `render`, `validate`, `lint`, `schema`
- `catalog`: `build`, `schema`
- top level: `about`, and the aliases `render`, `validate`, `lint`, `schema`, `build`

Core commands (canonical form):

```bash
specir diagram validate <spec.yml>
specir diagram render <spec.yml> --out <dir>
specir diagram render <spec.yml> --out <dir> --renderer mermaid
specir diagram lint <rendered.mmd>
specir diagram schema --type sequence --out <schema.json>
specir catalog schema --out <store.schema.json>
specir catalog build --config <vistas.yml> --out <out.html>
specir catalog build --config <vistas.yml> --out <out.html> --atoms-dir <atoms> --atoms-tag <tag> --strict-atoms
```

`--backend` is an alias of `--renderer`. A rendered text projection starts with a provenance header
that names its spec and `specir diagram validate`: never edit it by hand, re-render it.

## Renderer contract

The nine renderer names (`RENDERER_MAP` in `src/specir/visual/renderers/__init__.py`):

- `plantuml`, `mermaid`, `vega`, `d2`, `antonia-html`, `tree`, `graph`, `bpmn`, `json`

The default per type: class `mermaid`; sequence, state, activity and deployment `plantuml`; component
`graph`; matrix `vega`; reflection `json`. `bpmn` writes `<stem>.bpmn` and `<stem>.bpmn.html` (offline
viewer). Do not document a renderer list that disagrees with `RENDERER_MAP`.

## Full flow to HTML

```
specir diagram validate -> specir diagram render -> specir diagram lint -> specir catalog build -> HTML
```

And into a store, with sldb:

```bash
sldb notations sync --spec <spec.yml> --store <.sldb>
sldb notations sync --catalog <vistas.yml> --check --store <.sldb>
sldb notations sync --catalog <vistas.yml> --store <.sldb>
sldb notations from-graph --python <src_dir> --output <spec.yml>
sldb notations view <spec_id> --store <.sldb>
```

`specir catalog build` (and the alias `specir build`):

- input: a `vistas.yml` registry or a hierarchical diagram-store config (`project.yml`)
- output: one self-contained HTML file
- sources: template and view files resolved against `--base-dir` or the config directory
- `--atoms-dir`: W5H1 atom markdown files injected as `window.ATOMS_DB`; atoms are matched to diagram
  elements by sldb (`sldb.api.matching`)

## Catalog annotations (replaces spec2viz's catalog serve)

The page saves its annotations in a `CatalogAnnotationsDoc` of an sldb store, through `sldb serve`:

```bash
sldb models add specir.visual.catalog.annotations:CatalogAnnotationsDoc --store <.sldb>
sldb serve --store <.sldb> --cors --port 8765
specir catalog build --config <vistas.yml> --out <out.html> --sldb-url http://127.0.0.1:8765
```

`--annotations-doc <id>` fixes the document id; `--annotations` alone embeds the saver and the page
takes the server from its URL (`?sldb=<url>&annotations=<id>`).

## Python API

```python
from sldb.api.notations import load_spec, validate_spec
from specir.visual import compile_ir, render, render_to_file, json_schema, lint_mermaid, build_catalog

diagram = load_spec("spec.yml")
validate_spec(diagram)
text = render(compile_ir(diagram), "mermaid")
path = render_to_file("spec.yml", out="build", renderer="plantuml")
```

`specir.visual` also exports the IR dataclasses, the compilers, `RENDERER_MAP`, `EXT_MAP`,
`DEFAULT_RENDERER`, `with_provenance`, `provenance_header`, `provenance_text`, `write_json_schema`,
`assert_mermaid_ok`, `render_catalog`, `AnnotationsTarget` and the errors `Spec2VizError`,
`CompileError` and `RenderError`.

## Validation

For CLI, help or skill changes, run:

```bash
specir --help
specir about
specir diagram render --help
specir catalog build --help
```

and the tests of the files you touched, one file at a time, for example
`tests/visual/test_cli.py`, `tests/visual/test_api.py` and `tests/visual/test_packaging.py`.

## Anti-drift rule

Keep these aligned:

- `docs/spec2viz/correspondencia-cli.md`
- command help in `src/specir/cli.py` and `src/specir/visual/commands.py`
- renderers in `src/specir/visual/renderers/__init__.py`
- this skill: every command it names must exist (checked by `tests/visual/test_cli.py`)

FILE:docs/spec2viz/correspondencia-cli.md
# Correspondencia de la CLI de spec2viz con specIR y sldb

Tabla comando por comando de la CLI de spec2viz (revisión `2de1056`, filas SV-K de
`docs/spec2viz/matriz-de-cobertura.md`) con su equivalente. La escribe IR13d.

Regla (JP, 2026-11-15): lo genérico es de sldb y specIR es la capa visual y el mapeo de dominio. Si un
comando de spec2viz lo cubre un comando de sldb, specIR **no** lo duplica: el equivalente es el comando de
sldb y se usa directamente. specIR no envuelve la CLI ni la API de sldb.

- Comando de specIR: `specir` (script del paquete, `specir.cli:main`; también `python -m specir.cli`).
- Comando de sldb: `sldb` (paquete `structuredLanguageDB`, dependencia de specIR).
- La columna «Equivalente» se lee como código: `tests/visual/test_cli.py` extrae cada comando de esa columna
  y lo invoca con `--help` (los de sldb, como proceso aparte), y comprueba que cada opción nombrada aparece
  en la ayuda. Las funciones de la API de sldb (sin comando en sldb todavía) se invocan sobre una builtin.
- La prueba también comprueba que la primera columna cubre exactamente el árbol de comandos de spec2viz.

| ID | Comando de spec2viz | Modo | Equivalente | Prueba que lo invoca |
|---|---|---|---|---|
| SV-K30 | `spec2viz --help` | migrar tal cual | `specir --help` | test_help_mentions_taxonomy_groups_and_renderers |
| SV-K01 | `spec2viz about` | migrar tal cual | `specir about` | test_about_names_the_commands_of_specir_and_sldb |
| SV-K02 | `spec2viz build` | migrar tal cual | `specir build` | test_catalog_build_alias_matches_legacy_build, test_build_command* |
| SV-K03 | `spec2viz catalog` | migrar tal cual | `specir catalog` | test_help_mentions_taxonomy_groups_and_renderers |
| SV-K04 | `spec2viz catalog build` | migrar tal cual | `specir catalog build` | test_catalog_build_alias_matches_legacy_build, test_catalog_build_embeds_the_annotations_saver_of_ir13b |
| SV-K05 | `spec2viz catalog schema` | migrar tal cual | `specir catalog schema` | test_catalog_schema_stdout |
| SV-K06 | `spec2viz catalog serve` | reemplazar | `sldb serve --store --cors` | test_every_equivalent_of_the_table_answers_its_help; flujo completo en test_catalog_annotations.py (IR13b) |
| SV-K07 | `spec2viz catalog sync` | migrado a sldb | `sldb notations sync --catalog` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_catalog_parity.py (IR13b) |
| SV-K08 | `spec2viz catalog validate` | migrado a sldb | `sldb notations sync --catalog --check` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_catalog_parity.py (IR13b) |
| SV-K09 | `spec2viz diagram` | migrar tal cual | `specir diagram` | test_help_mentions_taxonomy_groups_and_renderers |
| SV-K10 | `spec2viz diagram from-graph` | migrado a sldb | `sldb notations from-graph --snapshot --store` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_sync_generation_parity.py (IR13a) |
| SV-K11 | `spec2viz diagram generate` | migrado a sldb | `sldb notations from-graph --python --output` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_sync_generation_parity.py (IR13a) |
| SV-K12 | `spec2viz diagram lint` | migrar tal cual | `specir diagram lint` | test_lint_alias_matches_diagram_lint; casos en test_lint_mermaid.py (IR12) |
| SV-K13 | `spec2viz diagram render` | migrar tal cual | `specir diagram render --renderer --backend --out` | test_render_* de test_render_commands.py (IR12) |
| SV-K14 | `spec2viz diagram schema` | migrar tal cual | `specir diagram schema --type --out` | test_schema.py (IR12) |
| SV-K15 | `spec2viz diagram sync` | migrado a sldb | `sldb notations sync --spec --notation --strict` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_sync_generation_parity.py (IR13a) |
| SV-K16 | `spec2viz diagram validate` | migrado a sldb (provisional en specIR) | `specir diagram validate` | test_diagram_validate_valid, test_diagram_validate_invalid (ver la decisión de abajo) |
| SV-K17 | `spec2viz lint` | migrar tal cual | `specir lint` | test_lint_alias_matches_diagram_lint |
| SV-K18 | `spec2viz notation` | usar sldb directamente | `sldb notations` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K19 | `spec2viz notation list` | usar sldb directamente | `sldb notations list` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K20 | `spec2viz notation sync` | usar sldb directamente | `sldb notations sync --notation` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K21 | `spec2viz notation validate` | usar sldb directamente | `sldb.notations.load_notation` (API; sldb aún no tiene comando) | test_every_equivalent_of_the_table_answers_its_help |
| SV-K22 | `spec2viz notation view` | usar sldb directamente | `sldb notations view --store` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K23 | `spec2viz palette` | usar sldb directamente | `sldb notations` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K24 | `spec2viz palette list` | usar sldb directamente | `sldb notations list` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K25 | `spec2viz palette sync` | usar sldb directamente | `sldb notations sync --palette` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K26 | `spec2viz palette validate` | usar sldb directamente | `sldb.notations.load_palette` (API; sldb aún no tiene comando) | test_every_equivalent_of_the_table_answers_its_help |
| SV-K27 | `spec2viz render` | migrar tal cual | `specir render --renderer --backend --out` | test_render_* (alias) de test_cli.py |
| SV-K28 | `spec2viz schema` | migrar tal cual | `specir schema --type --out` | test_schema_stdout, test_schema_outfile, test_schema_diagram_store_stdout, test_schema_invalid_type_fails |
| SV-K29 | `spec2viz validate` | migrado a sldb (provisional en specIR) | `specir validate` | test_validate_valid, test_validate_invalid, test_validate_all_types |

## Opciones de `catalog build` que cambian

- `--config`, `--out`, `--base-dir`, `--atoms-dir`, `--atoms-tag` y `--strict-atoms`: iguales que en spec2viz.
- Nuevas (IR13b e IR13d): `--annotations`, `--sldb-url <url>` y `--annotations-doc <id>`. La página guarda
  sus anotaciones en un `CatalogAnnotationsDoc` del store a través de `sldb serve --cors`. El modelo se
  registra en el store con sldb: `sldb models add specir.visual.catalog.annotations:CatalogAnnotationsDoc`.
  Esto sustituye a `catalog serve`, que las escribía en un JSON junto al HTML.

## Decisión sobre SV-K16 y SV-K29 (validar un spec por CLI)

- La lógica es de sldb (`load_spec` y `validate_spec` de `sldb.api.notations`, D3). sldb no tiene todavía
  un comando que valide un spec por ruta: está pedido en su inbox (nota
  `20261115-192054-suggestion-sldb-notations-validar-una-notaci-n-una-paleta-o-un-spec-por-nombre-o-ruta-desde-la-cli`,
  que también pide validar notaciones y paletas, SV-K21 y SV-K26).
- `sldb validate` no lo cubre: valida un documento o unos datos contra un modelo, sin elegir el tipo de
  diagrama ni hacer la validación semántica de `validate_spec`.
- Decisión (IR13d): mientras sldb no tenga el comando, `specir diagram validate` y su alias `validate`
  siguen en specIR. Solo llaman a `load_spec` y `validate_spec` de sldb y no redefinen nada. La cabecera de
  procedencia de las proyecciones nombra `specir diagram validate`.
- Cuando sldb publique su comando, `specir diagram validate` y `specir validate` se retiran, la cabecera
  pasa a nombrar el comando de sldb y esta fila pasa a «usar sldb directamente».

FILE:docs/spec2viz/matriz-de-cobertura.md
# Matriz de cobertura de spec2viz

Plan de cobertura para retirar spec2viz (tarea IR07). Cada capacidad de spec2viz tiene una fila con su
**modo** y su **condición de retiro**. Esta matriz **no acredita nada**: no hay columna de evidencia y
ninguna fila se da por cumplida. La tarea final IR13 añade por fila la prueba que acredita la cobertura
(después de IR13a, IR13b, IR13c e IR13d) y es la única que puede marcar una fila como cumplida.

- Revisión inventariada de spec2viz: commit `2de1056` del repo `spec2viz` (versión 0.2.0 en su
  `pyproject.toml`). La ayuda del CLI instalado (`spec2viz --help` y la de cada subgrupo) coincide con
  `spec2viz/spec2viz/cli.py` de esa revisión.
- Revisión de sldb consultada: rama main de `sldb` en `641ecdfa`. Plan de sldb que absorbe lo genérico:
  `sldb/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/` (`alcance.md`, `brief.md`, `decisiones.md`).
- Decisión vigente (JP, 2026-11-15): lo genérico va a sldb; specIR es adaptador y mapeo de dominio y
  conserva la capa visual (compiladores en IR11, renderers en IR12).
- La decisión sobre el papel del YAML de spec frente al grafo está en
  `docs/decisiones/fuente-de-verdad-del-diagrama.md` y en el atom
  `atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`. Es una **propuesta pendiente de JP**;
  ninguna fila de esta matriz depende de que se acepte en un sentido u otro salvo las marcadas con †.
- El procedimiento del gate está en `docs/spec2viz/gate-de-retiro.md`; la lista comprobable está al final
  de este documento.

## Modos

| Modo | Qué significa | Qué debe citar la fila |
|---|---|---|
| migrar tal cual | El código pasa a specIR (capa visual) con sus pruebas de spec2viz portadas. | Tarea de specIR que lo migra y pruebas de spec2viz que se portan. |
| reemplazar | Otra arquitectura o experiencia con resultado equivalente. | Sustituto y prueba que demostrará la equivalencia. |
| usar sldb directamente | Ya vive en SLDB; se consume por su API, su CLI o `sldb serve`, sin envoltorio ni reexportación en specIR. | Operación pública de SLDB que la respalda. |
| migrado a sldb | Pieza no visual ni de dominio; su código pasa a sldb con sus pruebas portadas y specIR la consume desde allí. | Tarea de sldb que la migra y pruebas de spec2viz que se portan a sldb. |

Tareas citadas (ids completos):

| Abreviatura | Tarea | Desk |
|---|---|---|
| D1 | `task-migrar-specsync-de-spec2viz-a-sldb-api-notations-junto-a-notationsync-y-palettesync-d1-b1-cierra-lo` (espejo en IR: `task-espejo-sldb-specsync-en-sldb-api-notations-d1`) | sldb |
| D2 | `task-migrar-a-sldb-el-generador-de-spec-de-componentes-desde-un-grafo-y-desde-el-ast-de-python-d2-b4` (espejo: `task-espejo-sldb-generador-de-spec-desde-grafo-y-ast-d2`) | sldb |
| D3 | `task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp` (espejo: `task-espejo-sldb-modelos-de-spec-por-tipo-de-diagrama-d3`) | sldb |
| D4 | `task-emparejamiento-de-átomos-con-elementos-de-diagrama-explícito-y-difuso-en-sldb-api-matching-d4` (espejo: `task-espejo-sldb-emparejamiento-de-átomos-en-sldb-api-matching-d4`) | sldb |
| IR11 | `task-ir11-compiladores-y-proyecciones-de-spec2viz` | IR |
| IR12 | `task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz` | IR |
| IR13a | `task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs` | IR |
| IR13b | `task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos` | IR |
| IR13d | `task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual` | IR |
| IR13 | `task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz` | IR |

IR13c (notaciones y paletas) se retiró porque era un envoltorio de `sldb notations`: sus filas están en
modo «usar sldb directamente» y la prueba de paridad de esas filas la aporta IR13 (ver «Pendientes de
derivación»).

Rutas: las de spec2viz son relativas a la raíz del repo `spec2viz` (`spec2viz/<módulo>.py` es el paquete;
`tests/` sus pruebas). Las pruebas citadas son las de `spec2viz/tests/` en la revisión inventariada.

## Matriz

### A. Modelos de spec, carga, validación y JSON Schema

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-A01 | Modelo de spec de diagrama de clases (paquetes, herencia, sobrecargas) | `spec2viz/models/class_diagram.py` | migrado a sldb | D3: subpaquete de modelos de diagrama junto a SpecDoc en sldb | Pasan en sldb, portadas por D3: de `tests/test_class_diagram.py` test_semantic_errors_are_rejected, test_inheritance_cycle_is_rejected_but_dependency_cycles_are_allowed, test_overloads_with_distinct_parameter_types_are_allowed y test_invalid_schema_fails_at_load; de `tests/test_class_packages.py` test_typed_validation y test_package_id_cannot_be_a_class_id. specIR no define el modelo (prueba de imports y nombres de IR11). |
| SV-A02 | Modelo de spec de secuencia | `spec2viz/models/sequence.py` | migrado a sldb | D3 | `tests/test_models_sequence.py` (3) portado a sldb y en verde; specIR importa el modelo de sldb (IR11). |
| SV-A03 | Modelo de spec de estado | `spec2viz/models/state.py` | migrado a sldb | D3 | `tests/test_models_state.py` (3) portado a sldb y en verde; ídem IR11. |
| SV-A04 | Modelo de spec de componentes | `spec2viz/models/component.py` | migrado a sldb | D3 | `tests/test_models_component.py` (3) portado a sldb y en verde; ídem IR11. |
| SV-A05 | Modelo de spec de actividad (particiones, merge, notas) | `spec2viz/models/activity.py` | migrado a sldb | D3 | `tests/test_models_activity.py` (3) portado a sldb y en verde; ídem IR11. |
| SV-A06 | Modelo de spec de despliegue (nodos anidados, communication paths) | `spec2viz/models/deployment.py` | migrado a sldb | D3 | `tests/test_models_deployment.py` (4) portado a sldb y en verde; ídem IR11. |
| SV-A07 | Modelo de spec de matriz (component_view_matrix) | `spec2viz/models/matrix.py` | migrado a sldb | D3 | `tests/test_models_matrix.py` (4) portado a sldb y en verde; ídem IR11. |
| SV-A08 | Modelo de spec de reflexión (enforcement) | `spec2viz/models/reflection.py` | migrado a sldb | D3 | spec2viz no tiene prueba de modelo propia de reflexión: la condición es la comparación de errores de D3 (misma clase y mismo texto de error) sobre todos los ejemplos y fixtures de spec2viz, que incluye `examples/reflection/`; specIR importa el modelo de sldb (IR11). |
| SV-A09 | Modelo base común (`BaseDiagram`, metadata, `DiagramType`) | `spec2viz/models/base.py` | migrado a sldb | D3 (DiagramType se reutiliza de `sldb.notations.diagram_type`, no se migra) | `tests/test_base_model.py` (3) portado a sldb y en verde. |
| SV-A10 | Modelo de catálogo (`vistas.yml` y stores jerárquicos de diagramas) | `spec2viz/models/catalog.py` | migrado a sldb | D3 | El modelo valida en sldb los fixtures de catálogo de spec2viz (`examples/catalog/`, `docs/architecture/spec2viz/vistas.yml`) con los mismos errores (comparación de errores de D3). |
| SV-A11 | Carga de un spec desde YAML (`load`) | `spec2viz/loader.py` | migrado a sldb | D3: `sldb.api.notations.load_spec` | `tests/test_loader.py` (16) portado a sldb y en verde. |
| SV-A12 | Validación semántica de un spec (`validate`) | `spec2viz/validator.py` | migrado a sldb | D3: `sldb.api.notations.validate_spec` | `tests/test_validator.py` (19) portado a sldb y en verde. |
| SV-A13 | Errores de carga y validación (`ParseError`, `ValidationError` y su jerarquía) | `spec2viz/exceptions.py` | migrado a sldb | D3: `ParseError` nueva bajo `NotationError`; el resto se reutiliza de `sldb.notations.exceptions` | `tests/test_exceptions.py` (2), solo los asertos de ParseError y ValidationError, portado a sldb y en verde. |
| SV-A14 | Errores de la capa visual (`Spec2VizError`, `CompileError`, `RenderError`) | `spec2viz/exceptions.py` | migrar tal cual | IR11 (CompileError) e IR12 (RenderError, raíz visual) | Los asertos de `tests/test_exceptions.py` sobre esas tres clases pasan en specIR con sus nombres; las pruebas de compiladores y renderers portadas levantan las mismas clases. |
| SV-A15 | Export de JSON Schema de specs (por tipo o todos) | `spec2viz/schema.py` | migrar tal cual | IR12 (`src/specir/visual/schema.py`) | El schema que exporta specIR es igual al de spec2viz para cada tipo (prueba de schema de IR12); pasan portadas test_json_schema_for_all_types, test_json_schema_for_specific_type y test_write_json_schema de `tests/test_api.py`, test_schema_stdout, test_schema_outfile y test_schema_invalid_type_fails de `tests/test_cli.py`, y test_schema_examples_match_generated_output y test_every_model_field_has_a_description de `tests/test_packaging.py`. |
| SV-A16 | Export de JSON Schema de catálogos y stores jerárquicos | `spec2viz/schema.py`, `spec2viz/cli.py` (`catalog schema`) | migrar tal cual | IR12 | Igual a spec2viz; pasan portadas test_schema_diagram_store_stdout y test_catalog_schema_stdout de `tests/test_cli.py`. |
| SV-A17 | Modelos de store de spec2viz (`SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `ViewDoc`) | `spec2viz/sldb_models.py` | usar sldb directamente | Modelos públicos de sldb: `sldb.models.notation.spec_doc.SpecDoc`, `spec_node_doc.SpecNodeDoc`, `notation_doc.NotationDoc`, `glyph_doc.GlyphDoc`, `link_doc.LinkDoc`, `palette_doc.PaletteDoc`, `view_doc.ViewDoc` | Los casos de `tests/test_view_doc.py` (3) pasan importando `ViewDoc` de sldb; specIR no define ninguna clase con esos nombres (IR11); ningún store registra `spec2viz.sldb_models` (gate G5). |

### B. Representación intermedia y compiladores (IR11)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-B01 | Representación intermedia visual (una dataclass por tipo de diagrama, `EnforcementArtifact`) | `spec2viz/ir.py` | migrar tal cual | IR11 | `tests/test_ir.py` (3) portado a specIR y en verde. |
| SV-B02 | Despacho de compilación por tipo (`compile_ir`) | `spec2viz/compilers/__init__.py` | migrar tal cual | IR11 | test_compile_* de `tests/test_api.py` (6) y `tests/test_compilers.py` (17) portados y en verde con la normalización de IR11. |
| SV-B03 | Compilador de clases | `spec2viz/compilers/class_diagram.py` | migrar tal cual | IR11 | Pasan en specIR las pruebas de compilación y render de `tests/test_class_diagram.py` y `tests/test_class_packages.py` que no porta D3 (las que invocan compile_ir o render). |
| SV-B04 | Compilador de secuencia | `spec2viz/compilers/sequence.py` | migrar tal cual | IR11 | Casos de secuencia de `tests/test_compilers.py` portados; IR equivalente según la normalización de IR11. |
| SV-B05 | Compilador de estado | `spec2viz/compilers/state.py` | migrar tal cual | IR11 | Casos de estado de `tests/test_compilers.py` portados; IR equivalente. |
| SV-B06 | Compilador de componentes | `spec2viz/compilers/component.py` | migrar tal cual | IR11 | Casos de componentes de `tests/test_compilers.py` portados; IR equivalente. |
| SV-B07 | Compilador de actividad (particiones, merge, notas) | `spec2viz/compilers/activity.py` | migrar tal cual | IR11 | Casos de actividad de `tests/test_compilers.py` y `tests/test_activity_lanes.py` (10) portados; IR equivalente. |
| SV-B08 | Compilador de despliegue (anidado, communication paths, deploy/manifest) | `spec2viz/compilers/deployment.py` | migrar tal cual | IR11 | Casos de despliegue de `tests/test_compilers.py` y `tests/test_deployment_nested.py` (6) portados; IR equivalente. |
| SV-B09 | Compilador de matriz | `spec2viz/compilers/matrix.py` | migrar tal cual | IR11 | Casos de matriz de `tests/test_compilers.py` portados; IR equivalente. |
| SV-B10 | Compilador de reflexión (artefacto de enforcement) | `spec2viz/compilers/reflection.py` | migrar tal cual | IR11 | `tests/test_reflection_compiler.py` (1) portado y en verde. |

### C. Renderizadores (IR12)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-C01 | Despacho de render, selector `--renderer`/`--backend` (9 valores), extensiones y renderer por defecto por tipo | `spec2viz/renderers/__init__.py` | migrar tal cual | IR12 (`src/specir/visual/renderers/__init__.py`) | Los 9 valores (plantuml, mermaid, vega, d2, antonia-html, tree, graph, bpmn, json) existen en specIR; test_render_str, test_render_dict y test_render_mermaid_override de `tests/test_api.py` y test_render_override y test_render_backend_alias de `tests/test_cli.py` portados y en verde. |
| SV-C02 | Mermaid | `spec2viz/renderers/mermaid.py` | migrar tal cual | IR12 | Casos mermaid de `tests/test_renderers.py` (golden idéntico o diferencia declarada aquí con su prueba), más los de `tests/test_activity_lanes.py` y `tests/test_deployment_nested.py`. |
| SV-C03 | PlantUML | `spec2viz/renderers/plantuml.py` | migrar tal cual | IR12 | Casos plantuml de `tests/test_renderers.py`, `tests/test_activity_lanes.py` y `tests/test_deployment_nested.py`. |
| SV-C04 | D2 | `spec2viz/renderers/d2.py` | migrar tal cual | IR12 | Casos d2 de `tests/test_renderers.py`, `tests/test_activity_lanes.py`, `tests/test_deployment_nested.py` y test_render_d2 de `tests/test_cli.py`. |
| SV-C05 | Vega (matriz) | `spec2viz/renderers/vega.py` | migrar tal cual | IR12 | Casos vega de `tests/test_renderers.py` y test_render_to_file_vega de `tests/test_api.py`. Diferencia declarada (IR12): spec2viz listaba el dominio de la escala `kindColor` en el orden de un set, que cambia con `PYTHONHASHSEED`; specIR lo lista en orden de primera aparición y el color de cada kind es el mismo. Prueba: test_vega_lists_the_kinds_in_order_of_first_appearance y la paridad de `tests/visual/test_render_parity.py`, que compara esa escala como correspondencia kind → color. |
| SV-C06 | BPMN (XML con DI) | `spec2viz/renderers/bpmn.py` | migrar tal cual | IR12 | `tests/test_bpmn.py` (26), parte XML y DI, portado y en verde. |
| SV-C07 | Visor BPMN offline (bpmn-js embebido, leyenda, metadata, panel) | `spec2viz/renderers/bpmn_viewer.py` | migrar tal cual | IR12 | Casos del visor de `tests/test_bpmn.py`; la prueba de recursos de IR12 abre el HTML sin recursos externos faltantes. |
| SV-C08 | Paleta BPMN in Color compartida por renderer y visor | `spec2viz/renderers/bpmn_palette.py` | migrar tal cual | IR12 | Mismos colores en XML y visor sobre los fixtures de `tests/test_bpmn.py`. |
| SV-C09 | Árbol (HTML colapsable) | `spec2viz/renderers/tree.py` | migrar tal cual | IR12 | Casos tree de `tests/test_renderers.py` portados. |
| SV-C10 | HTML de grafo (DOM puro, sin CDN) | `spec2viz/renderers/graph_html.py` | migrar tal cual | IR12 | Casos graph de `tests/test_renderers.py` y test_render_to_file_component de `tests/test_api.py`; abre desde file:// sin recursos externos (prueba de recursos de IR12). |
| SV-C11 | antonia-html | `spec2viz/renderers/antonia.py` | migrar tal cual | IR12 | Casos antonia de `tests/test_renderers.py` y test_render_antonia_html de `tests/test_cli.py`. |
| SV-C12 | Salida JSON (`JsonRenderer`, artefacto `.artifact.json`) | `spec2viz/renderers/__init__.py` | migrar tal cual | IR12 (`json_out`) | test_render_json_reflection_artifact de `tests/test_cli.py` portado y en verde. |
| SV-C13 | Backends UML de sintaxis para el ClassIR (mermaid y plantuml de clases) | `spec2viz/renderers/class_diagram.py` | migrar tal cual | IR12 (`src/specir/visual/renderers/class_diagram.py`) | Casos de clases de `tests/test_renderers.py`, `tests/test_class_diagram.py` y `tests/test_class_packages.py` con render. |
| SV-C14 | Mermaid desde una vista resuelta (glifo, forma, keyword, compartimentos, estilo) | `spec2viz/renderers/view_mermaid.py` | migrar tal cual | IR12 (`src/specir/visual/renderers/view_mermaid.py`), consumiendo `sldb.api.notations.resolve_view` | `tests/test_catalog_resolved_views.py` (8) portado y en verde contra la vista resuelta de sldb. |
| SV-C15 | Prueba de regresión de render a archivo | `spec2viz/__init__.py` (`render_to_file`) | migrar tal cual | IR12 e IR13d | `tests/test_rendering_bug.py` (1) portado y en verde. |

### D. Linter

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-D01 | Linter de Mermaid (heurísticas y pasada real con mmdc si está) | `spec2viz/linters/mermaid.py` | migrar tal cual | IR12 (`src/specir/visual/lint_mermaid.py`; la variable `SPECIR_MMDC` sustituye a `SPEC2VIZ_MMDC`, que sigue valiendo) | `tests/test_mermaid_mmdc.py` (4) portado y en verde; los mismos hallazgos que spec2viz sobre los fixtures de lint (prueba de lint de IR12). |

### E. Sincronización al store (SpecSync)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-E01 | SpecSync: materializar un spec como SpecDoc, SpecNodeDoc y RelationDoc, crear el RelationTypeDoc que falte y borrar lo que salió del spec; informe (`format_report`) | `spec2viz/sldb_sync.py` | migrado a sldb | D1: `SpecSync`, `sync_spec` en `sldb.api.notations`; `sldb notations sync --spec`. Reutiliza `StoreWriter` y `SyncReport` de sldb | `tests/test_sldb_sync.py` (16) portado a sldb, contra store real y sin mocks, en verde; informe igual campo a campo al de spec2viz sobre los mismos specs (D1); specIR llama a la API de sldb sin envoltorio (IR13a): `tests/visual/test_sync_generation_parity.py` sincroniza con sldb y con spec2viz los 14 specs válidos de `tests/fixtures/` y los ARQ/FLOW de `tests/test_sldb_sync.py` (con un resync que quita un nodo) y compara informes y SpecDoc, SpecNodeDoc, RelationDoc, RelationTypeDoc y documentos de notación; borrado al resincronizar y RelationTypeDoc de relación no builtin con `check_edges` limpio, contra store real. Diferencia declarada: la descripción del RelationTypeDoc que crea la sincronización ya no termina en «de spec2viz». |
| SV-E02 | Sincronización de notaciones y paletas al store (`NotationSync`, `PaletteSync`, `format_notation_report`) | `spec2viz/sldb_sync.py` | usar sldb directamente | `sldb.api.notations.NotationSync`, `PaletteSync`, `sync_notation`, `sync_palette`; CLI `sldb notations sync --notation/--palette` | Los casos de notación y paleta de `tests/test_sldb_sync.py` y `tests/test_style_palette.py` que sincronizan pasan llamando a la API de sldb, sin envoltorio en specIR. |

### F. Generación de specs

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-F01 | from-graph: compilar el grafo de un store (edge index) o un snapshot node-link en un spec de componentes | `spec2viz/graph_import.py` | migrado a sldb | D2: `component_spec_from_graph` en `sldb.api.notations`; `sldb notations from-graph --snapshot/--store` | `tests/test_graph_import.py` (21) portado a sldb y en verde; todo spec generado valida con el modelo de componentes de D3. IR13a (`tests/visual/test_sync_generation_parity.py`): sobre los snapshots node-link de `tests/test_graph_import.py` (el de documentos y `PY_GRAPH`) y sobre el edge index de un store sincronizado, `load_node_link`, `load_node_link_graph`, `index_graph` y `component_spec_from_graph` dan lo mismo que spec2viz, y cada spec valida con `load_spec`/`validate_spec`; sin diferencias. |
| SV-F02 | Generar un spec de componentes desde el AST de Python | `spec2viz/generators/python_ast.py` | migrado a sldb | D2: `component_spec_from_python` sobre `sldb.code.scan_tree`, `write_component_spec`; `sldb notations from-graph --python` | spec2viz no tiene pruebas de este generador: la condición es la prueba nueva de D2 que compara con `generate_python_ast_spec` de spec2viz sobre un árbol pequeño (mismos módulos, clases y relaciones defines) y valida con el modelo de D3. IR13a (`tests/visual/test_sync_generation_parity.py`) compara sobre un paquete real (`src/specir`): módulos, clases y aristas defines idénticos y en el mismo orden; el spec valida. Diferencias declaradas en las aristas imports, porque sldb las lee de `sldb.code.scan_tree`: cuenta los `import x` (spec2viz solo los `from x import y`), resuelve los imports relativos contra el paquete del módulo (spec2viz emite el nombre sin resolver), no repite una arista por sentencia y no lee los `from x import y` anidados bajo el nivel superior del módulo (en funciones, `if` o `try`; spec2viz recorre todo el árbol). Lo último es una pérdida pedida al desk de sldb (`code/scan-tree-nested-imports`); los nodos external siguen a las aristas. |

### G. Catálogos

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-G01 | Construcción del catálogo HTML autocontenido desde un `vistas.yml` o un store de stores (marca, subtítulo, plantilla local, `project.yml`, secciones HTML, anchors únicos) | `spec2viz/orchestrator.py` | migrar tal cual | IR13b con los renderers de IR12 | test_build_command* (7), test_catalog_build_alias_matches_legacy_build y test_build_command_reports_errors de `tests/test_cli.py` portados y en verde; mismas vistas, categorías y navegación que spec2viz sobre el fixture (IR13b). IR13b (`tests/visual/test_catalog.py`, sección de `tests/test_cli.py`): los 9 casos de build portados sobre la API (`specir.visual.catalog.build_catalog`/`render_catalog`; el comando, el alias `build` y sus mensajes «Rendered catalog» y «Error building catalog» son de IR13d; el error de construcción es la excepción). `tests/visual/test_catalog_parity.py`: la página es la de spec2viz byte a byte sobre `docs/architecture/vistas.yml` y `examples/catalog/` de spec2viz, sobre un proyecto sincronizado, stores de stores con overrides, `project.yml`, fragmentos y fuentes de todo tipo; diferencia declarada: los avisos de átomos y cobertura son findings de sldb (`level`, `code`, `subject`, `what`, `fix`) donde spec2viz escribía `{scope, message}`, y se comparan por su texto. `test_the_built_catalog_opens_without_missing_resources`: ninguna referencia local ni anchor roto (mermaid, vega y fuentes por CDN, igual que spec2viz). IR13d: `specir catalog build` y el alias `specir build` con sus mensajes; test_catalog_build_alias_matches_legacy_build, los test_build_command* (7) y test_build_command_reports_errors de `tests/test_cli.py` portados sobre el comando en `tests/visual/test_cli.py`. |
| SV-G02 | Registro `vistas.yml` y stores jerárquicos de diagramas: regla de rutas de `src`, `mmd`, `specs` y `notation` | `spec2viz/catalog_paths.py` | migrar tal cual | IR13b | `tests/test_catalog_paths.py` (9) portado y en verde. IR13b: la regla de rutas ya vive en sldb (`sldb.api.notations.catalog_paths`, D1) y specIR la usa sin copiarla; el cargador del registro y de los stores jerárquicos es `specir.visual.catalog.loader`. `tests/test_catalog_paths.py` (9) portado en `tests/visual/test_catalog.py` contra `catalog_paths` de sldb y `sldb notations sync --catalog [--check]`. |
| SV-G03 | Vistas del catálogo desde la vista resuelta (misma fuente que graph_ui) | `spec2viz/catalog_views.py` | migrar tal cual | IR13b, consumiendo `sldb.api.notations.resolve_view` | `tests/test_catalog_resolved_views.py` (8) portado y en verde (compartido con SV-C14). IR13b: `specir.visual.catalog.views` sobre `resolve_view` y `SpecSync` de sldb y `view_to_mermaid` de IR12; los 4 casos de `catalog build` portados en `tests/visual/test_catalog.py` (los dos que usaban monkeypatch se rehacen con una notación que solo vive en el store y con un spec que no es grafo) y los mismos tableros que spec2viz en `tests/visual/test_catalog_parity.py` (`test_resolved_views_are_spec2viz_s`, `test_the_catalog_of_a_synced_project_is_spec2viz_s`). |
| SV-G04 | Sincronización del catálogo al store (`catalog sync`: cada spec del `vistas.yml` con su notación y metadata) | `spec2viz/sldb_sync.py` (`sync_catalog`) | migrado a sldb | D1: `sync_catalog`; `sldb notations sync --catalog` (con `--prune` para borrar los SpecDoc que salieron) | `tests/test_catalog_notation.py` (6) portado a sldb y en verde; no escribe nada si una vista falla (IR13b). IR13b: `tests/test_catalog_notation.py` (6) portado en `tests/visual/test_catalog.py` sobre `sldb notations sync --catalog`; `tests/visual/test_catalog_parity.py` `test_catalog_sync_leaves_what_spec2viz_leaves` (mismos documentos que spec2viz sobre su `docs/architecture/vistas.yml`, comparación de IR13a) y `test_a_failing_view_makes_both_write_nothing`; `tests/visual/test_catalog.py` `test_a_failing_view_writes_nothing_even_after_valid_ones`. |
| SV-G05 | Validación del catálogo (`catalog validate`: specs existen y validan, notaciones del tipo correcto) | `spec2viz/sldb_sync.py` (`check_catalog`) | migrado a sldb | D1: `check_catalog`; `sldb notations sync --catalog --check` | Casos de validación de `tests/test_catalog_notation.py` portados a sldb; mismos errores tipados que spec2viz (IR13b). IR13b: `tests/visual/test_catalog_parity.py` compara `check_catalog` de sldb con el de spec2viz entrada por entrada (vista, spec, clase y mensaje del error) sobre los registros de `test_catalog_paths` y `test_catalog_notation` (rutas faltantes y ambiguas, notación inexistente, de otro tipo o solo del store) y sobre `docs/architecture/vistas.yml` de spec2viz; sin diferencias. |
| SV-G06 | Servir el catálogo en local con autoguardado de anotaciones (`catalog serve`) | `spec2viz/cli.py` (`catalog_serve`) | reemplazar | Sustituto: `sldb serve` (lectura de documento por id y escritura con guarda de hash, comprobado por D4 paso 7) más el JS del catálogo de specIR (IR13b) | Prueba de equivalencia: IR13b demuestra que una anotación hecha con el catálogo servido por `sldb serve` queda guardada y reaparece al recargar. Si D4 concluye que `sldb serve` no alcanza, la fila no se cumple hasta que sldb resuelva la nota `serve/annotation-autosave-gap`. IR13b: `sldb serve` alcanza, sin nota. specIR guarda las anotaciones de un catálogo en un documento `CatalogAnnotationsDoc` (modelo de specIR registrado con `add_model`) y la página las lee con `GET /document?id=` y las guarda con `POST /save` y `expected` (script `templates/annotations-sldb.js`, embebido con `render_catalog(..., annotations=AnnotationsTarget(...))` o por la URL `?sldb=&annotations=`). `tests/visual/test_catalog_annotations.py`: con un `sldb serve --cors` real, el código de la página corrido en node guarda una anotación, que reaparece al recargar (proceso nuevo, `localStorage` vacío) y queda en el store; una página con la guarda vieja (409) mezcla y reintenta. Diferencia declarada: spec2viz escribía `comentarios-arquitectura.json` junto al HTML. |
| SV-G07 | Inyección de átomos en el HTML del catálogo (`render_deskops`, `build_deskops`, `split_shared_atoms`, adaptador `CatalogItem`) | `spec2viz/deskops.py` | migrar tal cual | IR13b (capa visual; D4 lo deja fuera de sldb) | `tests/test_deskops.py` (7) y, de `tests/test_atoms_matching.py`, test_split_shared_atoms_emits_repeated_payload_once y test_catalog_build_embeds_atoms_once_and_honors_atoms_tag, portados y en verde. IR13b: `specir.visual.catalog.atoms` (adaptador de la vista del catálogo a `SpecView`, descubrimiento del store de la vista, `split_shared_atoms`, inyección) sobre `sldb.api.matching`. Portados en `tests/visual/test_catalog.py`: `tests/test_deskops.py` (7; los dos de `parse_atoms` contra sldb, el de cobertura a través del catálogo, el del store con un store real en `tests/visual/test_catalog_parity.py`) y los dos casos de `tests/test_atoms_matching.py`. `tests/visual/test_catalog_parity.py`: los mismos `ATOMS_DB`, `ATOMS_BY_VIEW`, `ATOMS_EXPLICIT`, `ATOMS_LINKED`, `REFS_EXPLICIT` y `COVERAGE_BY_VIEW` que spec2viz (carpeta de átomos, filtro por tags, explícitos, desconocidos, átomos y refs del store de la vista). |
| SV-G08 | Plantilla HTML del catálogo, incluido el emparejamiento difuso en el navegador (`findAtomData`, `normKey`) y las pestañas por átomo | `spec2viz/templates/default.html` | migrar tal cual | IR12 (`src/specir/visual/templates/default.html`) e IR13b | Los casos de `tests/test_atoms_matching.py` que ejecutan la plantilla con node y test_tabs_follow_the_target_atom portados y en verde; `label_key` de D4 sigue coincidiendo con `normKey`. IR13b (`tests/visual/test_catalog.py`): los 7 casos de emparejamiento en el navegador, los 6 de markdown de átomos y `test_tabs_follow_the_target_atom` portados sobre la plantilla de specIR. `label_key` de D4 coincide con `normKey` salvo en `_`: `label_key` lo conserva y `normKey` lo separa (un elemento sin label con `_` en su id no encuentra su átomo explícito; spec2viz tenía el mismo defecto). Queda como xfail estricto (`test_label_key_of_sldb_splits_underscores_like_norm_key`) y pedido al desk de sldb (`matching/label-key-underscore`). |

### H. Notaciones, paletas y estilo (usar sldb directamente)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-H01 | Modelo, carga y validación de notaciones (NotationDoc, GlyphDoc, LinkDoc en YAML; `where` en la gramática de `sldb find --where`) | `spec2viz/notation.py` | usar sldb directamente | `sldb.notations.load_notation`, `sldb.notations.NotationSpec` | Los casos de `tests/test_notation.py` (14) pasan contra `sldb.notations` sin envoltorio en specIR. |
| SV-H02 | Notaciones builtin (8) y notación por defecto por tipo | `spec2viz/notations/*.yml`, `DEFAULT_NOTATIONS` | usar sldb directamente | `sldb.notations.builtin_notations`, `sldb.notations.DEFAULT_NOTATIONS` | Las 8 notaciones de spec2viz (activity, component, component-view-matrix, deployment, reflection, statechart, uml-class, uml-sequence) aparecen en `sldb notations list` y su contenido valida igual. |
| SV-H03 | Vista resuelta de un spec (glifo por nodo, link por relación, leyenda) y de documentos sin SpecDoc | `spec2viz/notation_view.py` (`resolve_view`, `resolve_documents`) | usar sldb directamente | `sldb.api.notations.resolve_view`, `sldb.api.notations.resolve_documents`; CLI `sldb notations view` y `sldb notations resolve` | `tests/test_notation_view.py` (11) y `tests/test_view_contract_resolved.py` (2) pasan contra la API de sldb; graph_ui ya no importa `spec2viz.notation_view` (gate G4). |
| SV-H04 | Modelo, carga y validación de paletas, con contraste WCAG (trazo ≥ 3:1, texto ≥ 4.5:1, forma+icono distintos por kind) | `spec2viz/palette.py` | usar sldb directamente | `sldb.notations.load_palette`, `sldb.notations.PaletteSpec`, `sldb.notations.contrast` | Los casos de paleta y contraste de `tests/test_style_palette.py` pasan contra `sldb.notations`. |
| SV-H05 | Paleta builtin `default` | `spec2viz/palettes/default.yml` | usar sldb directamente | `sldb.notations.builtin_palettes` (`src/sldb/notations/palettes/default.yml`) | `sldb notations list` la lista y su contenido valida igual. |
| SV-H06 | Estilo con una sola precedencia (glifo > `style.kinds` del spec > paleta) | `spec2viz/styling.py` | usar sldb directamente | `sldb.notations.resolve_style`, `sldb.notations.resolve_line_color` | Los casos de precedencia de `tests/test_style_palette.py` pasan contra `sldb.notations`. |

### I. Emparejamiento de átomos con elementos de diagrama

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-I01 | Emparejamiento explícito (`atoms:` en el elemento), alias por título y etiquetas, filtro por tags, avisos y modo estricto (`UnknownAtomError`) | `spec2viz/deskops.py` | migrado a sldb | D4: `sldb.api.matching` (módulos de claves y alias, resolución explícita) | Portados a sldb y en verde: de `tests/test_atoms_matching.py` test_filter_atoms_payload_by_full_tag_or_value; de `tests/test_explicit_atoms.py` test_build_exposes_explicit_map_by_label_and_id, test_unknown_atom_is_warning_unless_strict, test_fully_explicit_view_embeds_no_fuzzy_payload, test_partially_explicit_view_keeps_fuzzy_payload y test_atoms_linked_from_explicit_are_embedded_one_level. IR13b: el catálogo lo usa sin envoltorio (`tests/test_imports.py::test_specir_defines_no_atom_matching_and_no_catalog_path_rule`); los casos de build de `tests/test_explicit_atoms.py` portados en `tests/visual/test_catalog.py` (el desconocido es aviso `matching/unknown-atom`, o `UnknownAtomError` de sldb con `strict_atoms`) y los mismos átomos por elemento que spec2viz en `tests/visual/test_catalog_parity.py` (`test_explicit_atoms_are_spec2viz_s`, `test_strict_atoms_fail_both`). |
| SV-I02 | Emparejamiento difuso de átomos con elementos | `spec2viz/templates/default.html` (en el navegador) | migrado a sldb | D4: `DocumentIndex.rank` sobre `Matcher`/`DifflibMatcher` con alias (sin matcher nuevo); el JS del navegador sigue en SV-G08 | Prueba nueva de D4 de emparejamiento difuso con alias en verde, y SV-G08 cumplida. IR13b: el difuso del navegador es el de la plantilla (SV-G08); el catálogo embebe el mismo payload que spec2viz (`tests/visual/test_catalog_parity.py`). |
| SV-I03 | Referencias `refs: [Model:name]` por elemento hacia documentos sldb y aristas de átomos (`collect_explicit_refs`, `build_explicit_refs`, `attach_atom_edges`) | `spec2viz/deskops.py` | migrado a sldb | D4 (resolución de refs) | `tests/test_refs.py` (14) en verde: los casos de resolución contra sldb (D4) y los de schema y CLI contra specIR (IR12, IR13d). D4 no lista hoy `tests/test_refs.py` entre sus pruebas portadas: ver pendientes. IR13b: las refs de un elemento contra el store de la vista, con sus aristas, iguales a spec2viz en `tests/visual/test_catalog_parity.py` (`test_atoms_of_the_view_s_store_and_its_refs_are_spec2viz_s`, con un store sldb real y una ref desconocida). |
| SV-I04 | Cobertura de átomos por vista | `spec2viz/deskops.py` (`build_coverage_by_view`) | migrado a sldb | D4 (módulo de cobertura) | Prueba de cobertura de D4 en verde y los casos de cobertura de `tests/test_deskops.py` portados. IR13b: la misma `COVERAGE_BY_VIEW` que spec2viz en `tests/visual/test_catalog_parity.py`; el caso de cobertura de `tests/test_deskops.py` portado a través del catálogo en `tests/visual/test_catalog.py`. |
| SV-I05 | Descubrimiento y carga del store de átomos (`SldbAtomResolver`) | `spec2viz/deskops.py` | usar sldb directamente | `sldb.api.stores.open_store` y lectura de documentos y del edge index de `sldb.api` | Las pruebas de SV-I01 a SV-I04 pasan sin `SldbAtomResolver`. IR13b: el catálogo descubre el store de cada vista con `sldb.api.notations.find_store` (con el límite de proyecto de spec2viz) y lee con `StoreReader`; mismo resultado que `SldbAtomResolver` en `tests/visual/test_catalog_parity.py`. |

### J. API Python pública, recursos empaquetados, about y habilidad

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-J01 | `spec2viz.load` y `spec2viz.validate` | `spec2viz/__init__.py` | migrado a sldb | D3: `sldb.api.notations.load_spec`, `validate_spec` | test_load_* (6), test_validate_passes y test_validate_fails de `tests/test_api.py` pasan contra la API de sldb. |
| SV-J02 | `compile_ir`, `render`, `json_schema`, `write_json_schema` | `spec2viz/__init__.py` | migrar tal cual | IR13d (API pública de la capa visual de specIR) | El resto de `tests/test_api.py` (27 en total) portado contra la API de specIR y en verde. IR13d: `specir.visual` exporta `compile_ir`, `render`, `RENDERER_MAP`, `EXT_MAP`, `DEFAULT_RENDERER`, `json_schema` y `write_json_schema` (además, `lint_mermaid`, `assert_mermaid_ok`, `render_catalog`, `build_catalog` y `AnnotationsTarget`); `tests/test_api.py` portado entero en `tests/visual/test_api.py` (27, con `load`/`validate` de sldb, SV-J01) y test_every_public_name_of_spec2viz_has_its_equivalent comprueba cada nombre público del `__init__` de spec2viz. |
| SV-J03 | `render_to_file` con cabecera de procedencia (`with_provenance`, `provenance_header`, `provenance_text`) y salida BPMN doble (`.bpmn` y `.bpmn.html`) | `spec2viz/__init__.py` | migrar tal cual | IR12 lo migra (`src/specir/visual/render_file.py`, lo necesita `diagram render`); IR13d lo expone en la API pública | test_render_to_file_* (7) de `tests/test_api.py` y test_rendered_text_projections_carry_a_provenance_header de `tests/test_cli.py` portados; la cabecera nombra el comando de specIR que valida. IR13d: `render_to_file`, `with_provenance`, `provenance_header` y `provenance_text` en `specir.visual` (`tests/visual/test_api.py`: test_render_to_file_* y test_the_provenance_helpers_name_specir). |
| SV-J04 | Recurso empaquetado: bpmn-js vendorizado | `spec2viz/templates/vendor/bpmn-js/` | migrar tal cual | IR12 (prueba de recursos) | El visor BPMN abre offline (SV-C07) y `tests/test_packaging.py` portado (incluido test_examples_render_successfully) en verde. |
| SV-J05 | Recurso empaquetado: plantilla HTML del catálogo | `spec2viz/templates/default.html` | migrar tal cual | IR12 | Ver SV-G08; la plantilla viaja en el paquete instalado de specIR (prueba de recursos de IR12). |
| SV-J06 | Recursos empaquetados: notaciones y paleta builtin | `spec2viz/notations/`, `spec2viz/palettes/` | usar sldb directamente | Builtins de sldb (`src/sldb/notations/builtin/`, `src/sldb/notations/palettes/`) vía `sldb.notations.builtin_notations` y `builtin_palettes` | specIR no empaqueta notaciones ni paletas; SV-H02 y SV-H05 cumplidas. |
| SV-J07 | Punto de entrada `spec2viz` y empaquetado (instala y arranca) | `pyproject.toml` (`[project.scripts]`), `spec2viz/cli.py` (`main`) | reemplazar | Sustituto: el comando de specIR (IR13d) | Prueba de IR13d: el paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado; test_primary_cli_still_exposes_commands de `tests/test_packaging.py` portado. IR13d: el script `specir` apunta a `specir.cli:main`; `tests/visual/test_packaging.py`: test_primary_cli_still_exposes_commands portado, test_the_script_is_the_command_of_specir_cli y test_the_package_installs_in_a_clean_environment_and_starts_without_spec2viz (venv nuevo con sldb y la wheel de specIR, sin spec2viz: `specir --help`, `about`, `render` y `validate` arrancan e `import spec2viz` falla). |
| SV-J08 | Comando about (dónde viven los diagramas y cómo llega el flujo al HTML) | `spec2viz/cli.py` (`about`) | migrar tal cual | IR13d | El comando equivalente de specIR existe y lo invoca la prueba de CLI de IR13d; su texto nombra los comandos de specIR y de sldb que sustituyen a los de spec2viz. IR13d: `specir about` (store sobre el directorio actual, flujo a HTML con los comandos de specIR y los de sldb para el store y las anotaciones); test_about_names_the_commands_of_specir_and_sldb (invoca con `--help` cada comando que nombra) y test_about_shows_the_store_above_the_current_directory de `tests/visual/test_cli.py`. |
| SV-J09 | Habilidad de agente use-spec2viz | `.pi/skills/use-spec2viz/SKILL.md` (copia distinta en `deskops/.opencode/skills/use-spec2viz/SKILL.md`) | reemplazar | Sustituto: `skills/use-specir/SKILL.md` (IR13d) | Prueba de IR13d que extrae los comandos que nombra la habilidad y los invoca con ayuda; la habilidad no nombra comandos de spec2viz. IR13d: `skills/use-specir/SKILL.md`; test_the_skill_names_only_commands_that_exist (extrae los `specir …` y `sldb …` de la habilidad y los invoca con `--help`, con sus opciones) y test_the_skill_names_no_spec2viz_command de `tests/visual/test_cli.py`. |

### K. Comandos y subgrupos del CLI

Una fila por cada entrada que lista la ayuda (`spec2viz --help` y la de cada subgrupo). La correspondencia
detallada la escribe IR13d en `docs/spec2viz/correspondencia-cli.md`. Cuando la capacidad vive en sldb, el
equivalente es el comando de sldb y specIR no define subcomando propio.

| ID | Comando | Modo | Equivalente | Condición de retiro |
|---|---|---|---|---|
| SV-K01 | `spec2viz about` | migrar tal cual | Comando about de specIR (IR13d) | SV-J08. IR13d: `specir about`; test_about_names_the_commands_of_specir_and_sldb. |
| SV-K02 | `spec2viz build` (alias de `catalog build`) | migrar tal cual | Alias en el comando de specIR (IR13d) | SV-G01; test_catalog_build_alias_matches_legacy_build portado. IR13d: `specir build`; test_catalog_build_alias_matches_legacy_build y test_build_command* de `tests/visual/test_cli.py`. |
| SV-K03 | `spec2viz catalog` (subgrupo) | migrar tal cual | Subgrupo catalog de specIR con build y schema; sync, validate y serve remiten a sldb | SV-K04 a SV-K08 cumplidas. IR13d: `specir catalog` (build, schema); test_help_mentions_taxonomy_groups_and_renderers y test_specir_defines_no_command_the_table_gives_to_sldb de `tests/visual/test_cli.py`. |
| SV-K04 | `spec2viz catalog build` | migrar tal cual | specIR (IR13b, IR13d) | SV-G01. IR13d: `specir catalog build` (con `--annotations`, `--sldb-url` y `--annotations-doc`); test_build_command_extracts_* y test_catalog_build_embeds_the_annotations_saver_of_ir13b de `tests/visual/test_cli.py`. |
| SV-K05 | `spec2viz catalog schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A16. IR13d: `specir catalog schema`; test_catalog_schema_stdout de `tests/visual/test_cli.py`. |
| SV-K06 | `spec2viz catalog serve` | reemplazar | `sldb serve` sobre el store del catálogo (IR13b) | SV-G06. IR13d: `sldb serve --store --cors`; test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K07 | `spec2viz catalog sync` | migrado a sldb | `sldb notations sync --catalog` (D1) | SV-G04. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K08 | `spec2viz catalog validate` | migrado a sldb | `sldb notations sync --catalog --check` (D1) | SV-G05. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K09 | `spec2viz diagram` (subgrupo) | migrar tal cual | Subgrupo diagram de specIR con render, lint y schema (y validate, ver SV-K16); sync, from-graph y generate remiten a sldb | SV-K10 a SV-K16 cumplidas. IR13d: `specir diagram` (render, validate, lint, schema); test_help_mentions_taxonomy_groups_and_renderers de `tests/visual/test_cli.py`. |
| SV-K10 | `spec2viz diagram from-graph` | migrado a sldb | `sldb notations from-graph --snapshot/--store` (D2) | SV-F01; test_cli_from_graph_* (5) y test_cli_from_graph_module_prefix reescritos contra el comando de sldb (D2). IR13d: `sldb notations from-graph --snapshot/--store`; test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K11 | `spec2viz diagram generate` | migrado a sldb | `sldb notations from-graph --python` (D2) | SV-F02. IR13d: `sldb notations from-graph --python`; test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K12 | `spec2viz diagram lint` | migrar tal cual | specIR (IR12, IR13d) | SV-D01. IR13d: `specir diagram lint`; test_lint_alias_matches_diagram_lint de `tests/visual/test_cli.py`. |
| SV-K13 | `spec2viz diagram render` | migrar tal cual | specIR (IR12, IR13d) | test_render_* de `tests/test_cli.py` portados; SV-C01 a SV-C12. IR13d: `specir diagram render`; test_render_* de `tests/visual/test_render_commands.py` (IR12) y test_the_render_alias_writes_what_diagram_render_writes de `tests/visual/test_cli.py`. |
| SV-K14 | `spec2viz diagram schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A15. IR13d: `specir diagram schema`; `tests/visual/test_schema.py` (IR12) y test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K15 | `spec2viz diagram sync` | migrado a sldb | `sldb notations sync --spec` (D1) | SV-E01. IR13d: `sldb notations sync --spec`; test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K16 | `spec2viz diagram validate` | migrado a sldb | Lógica en sldb (`load_spec`, `validate_spec`, D3). Decisión de IR13d: sldb aún no tiene comando que valide un spec (pedido en su inbox; `sldb validate` valida contra un modelo, sin despacho por tipo ni validación semántica), así que `specir diagram validate` y el alias `specir validate` quedan en specIR de forma provisional: solo llaman a `load_spec` y `validate_spec` de sldb, sin redefinir nada. Cuando sldb publique su comando, los de specIR se retiran, la cabecera de procedencia lo nombra y la fila pasa a «usar sldb directamente» (`docs/spec2viz/correspondencia-cli.md`) | test_validate_valid, test_validate_invalid y test_validate_all_types de `tests/test_cli.py` portados contra el comando elegido; SV-A11 y SV-A12. IR13d: test_validate_valid, test_validate_invalid y test_validate_all_types portados sobre `specir validate`, y test_diagram_validate_valid y test_diagram_validate_invalid sobre `specir diagram validate`, en `tests/visual/test_cli.py`. |
| SV-K17 | `spec2viz lint` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K12. IR13d: `specir lint`; test_lint_alias_matches_diagram_lint y test_every_alias_stands_for_a_group_command_with_the_same_parameters de `tests/visual/test_cli.py`. |
| SV-K18 | `spec2viz notation` (subgrupo) | usar sldb directamente | `sldb notations` | SV-K19 a SV-K22 cumplidas. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`); specIR no define el subgrupo (test_specir_defines_no_command_the_table_gives_to_sldb). |
| SV-K19 | `spec2viz notation list` | usar sldb directamente | `sldb notations list` | SV-H02. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K20 | `spec2viz notation sync` | usar sldb directamente | `sldb notations sync --notation` | SV-E02. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K21 | `spec2viz notation validate` | usar sldb directamente | `sldb.notations.load_notation`; sldb no tiene hoy comando de validación de notaciones (ver pendientes) | SV-H01 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. IR13d: la tabla remite a `sldb.notations.load_notation`, que test_every_equivalent_of_the_table_answers_its_help invoca sobre cada builtin; el comando de sldb sigue pedido. |
| SV-K22 | `spec2viz notation view` | usar sldb directamente | `sldb notations view` | SV-H03. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K23 | `spec2viz palette` (subgrupo) | usar sldb directamente | `sldb notations` (`list`, `sync --palette`) | SV-K24 a SV-K26 cumplidas. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`); specIR no define el subgrupo. |
| SV-K24 | `spec2viz palette list` | usar sldb directamente | `sldb notations list` (incluye `builtin_palettes`) | SV-H05. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K25 | `spec2viz palette sync` | usar sldb directamente | `sldb notations sync --palette` | SV-E02. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K26 | `spec2viz palette validate` | usar sldb directamente | `sldb.notations.load_palette` (con contraste WCAG); sldb no tiene hoy comando de validación de paletas (ver pendientes) | SV-H04 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. IR13d: la tabla remite a `sldb.notations.load_palette`, que test_every_equivalent_of_the_table_answers_its_help invoca sobre cada builtin; el comando de sldb sigue pedido. |
| SV-K27 | `spec2viz render` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K13. IR13d: `specir render`; test_render_each_type (6), test_render_override, test_render_backend_alias, test_render_multiple, test_render_invalid_fails, test_render_d2, test_render_antonia_html y test_render_json_reflection_artifact portados sobre el alias en `tests/visual/test_cli.py`. |
| SV-K28 | `spec2viz schema` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K14. IR13d: `specir schema`; test_schema_stdout, test_schema_outfile, test_schema_diagram_store_stdout y test_schema_invalid_type_fails de `tests/visual/test_cli.py`. |
| SV-K29 | `spec2viz validate` (alias) | migrado a sldb | Igual que SV-K16 | SV-K16. IR13d: `specir validate`; ver SV-K16. |
| SV-K30 | Ayuda raíz con taxonomía (diagram, catalog) y lista de renderers | migrar tal cual | Ayuda del comando de specIR (IR13d) | test_help_mentions_taxonomy_groups_and_renderers de `tests/test_cli.py` portado. IR13d: test_help_mentions_taxonomy_groups_and_renderers portado en `tests/visual/test_cli.py`; la ayuda dice «Top-level aliases (render, validate, lint, schema, build) remain available» donde spec2viz decía «Legacy top-level commands remain available». |

### Pruebas de spec2viz por fila

Cada archivo de `spec2viz/tests/` y las filas que lo portan o reemplazan. El gate G2 exige que cada
archivo tenga todos sus casos cubiertos por alguna fila.

| Archivo | Filas |
|---|---|
| `tests/test_activity_lanes.py` | SV-A05, SV-B07, SV-C02, SV-C03, SV-C04 |
| `tests/test_api.py` | SV-A15, SV-B02, SV-C01, SV-C05, SV-C10, SV-J01, SV-J02, SV-J03 |
| `tests/test_atoms_matching.py` | SV-G07, SV-G08, SV-I01, SV-I02 |
| `tests/test_base_model.py` | SV-A09 |
| `tests/test_bpmn.py` | SV-C06, SV-C07, SV-C08, SV-J03 |
| `tests/test_catalog_notation.py` | SV-G04, SV-G05 |
| `tests/test_catalog_paths.py` | SV-G02 |
| `tests/test_catalog_resolved_views.py` | SV-C14, SV-G03 |
| `tests/test_class_diagram.py` | SV-A01, SV-B03, SV-C13 |
| `tests/test_class_packages.py` | SV-A01, SV-B03, SV-C13 |
| `tests/test_cli.py` | SV-A15, SV-A16, SV-C01, SV-C04, SV-C11, SV-C12, SV-G01, SV-J03, SV-K01 a SV-K30 |
| `tests/test_compilers.py` | SV-B02 a SV-B09 |
| `tests/test_deployment_nested.py` | SV-A06, SV-B08, SV-C02, SV-C03, SV-C04 |
| `tests/test_deskops.py` | SV-G07, SV-I04 |
| `tests/test_exceptions.py` | SV-A13, SV-A14 |
| `tests/test_explicit_atoms.py` | SV-I01 |
| `tests/test_graph_import.py` | SV-F01, SV-K10 |
| `tests/test_ir.py` | SV-B01 |
| `tests/test_loader.py` | SV-A11 |
| `tests/test_mermaid_mmdc.py` | SV-D01 |
| `tests/test_models_activity.py` | SV-A05 |
| `tests/test_models_component.py` | SV-A04 |
| `tests/test_models_deployment.py` | SV-A06 |
| `tests/test_models_matrix.py` | SV-A07 |
| `tests/test_models_sequence.py` | SV-A02 |
| `tests/test_models_state.py` | SV-A03 |
| `tests/test_notation.py` | SV-H01, SV-H02 |
| `tests/test_notation_view.py` | SV-H03 |
| `tests/test_packaging.py` | SV-A15, SV-J04, SV-J07 |
| `tests/test_reflection_compiler.py` | SV-B10 |
| `tests/test_refs.py` | SV-I03 |
| `tests/test_renderers.py` | SV-C02 a SV-C11, SV-C13 |
| `tests/test_rendering_bug.py` | SV-C15 |
| `tests/test_sldb_sync.py` | SV-E01, SV-E02 |
| `tests/test_style_palette.py` | SV-E02, SV-H04, SV-H06 |
| `tests/test_validator.py` | SV-A12 |
| `tests/test_view_contract_resolved.py` | SV-H03 |
| `tests/test_view_doc.py` | SV-A17 |

## Inventario de consumidores

Universo auditado por IR13 (y solo este; añadir uno exige actualizar primero esta sección). Búsqueda hecha
el 2026-11-15 sobre los repos con `.git` bajo `SLDB_1/` (`IR`, `deskops`, `pron`, `scion`, `sldb`,
`spec2viz`, `UIs/graph_ui`; `sldb-runtime` y `deskops-runtime` son checkouts de despliegue de `sldb` y
`deskops` y se auditan por su repo de origen) y sobre todo `store.yaml` y `store_index.yaml` bajo
`SLDB_1/`. `scion` no tiene dependencias de spec2viz. Clases de dependencia como las define IR13
(importación, dependencia declarada, invocación del comando, modelo registrado en un store).

| Consumidor | Archivo y línea | Clase | Sustituto previsto |
|---|---|---|---|
| graph_ui | `UIs/graph_ui/frontends/mindmap/sldb_adapter.py:245` (`from spec2viz.notation_view import ViewError, resolve_view`) | importación | `sldb.api.notations.resolve_view` y `ViewError` (SV-H03) |
| graph_ui | `UIs/graph_ui/frontends/mindmap/sldb_adapter.py:437` (`from spec2viz.notation_view import ViewError, resolve_documents`) | importación | `sldb.api.notations.resolve_documents` (SV-H03) |
| graph_ui | `UIs/graph_ui/pyproject.toml:19` (extra `notation = ["spec2viz>=0.1.0"]`) y `:24` (extra `test`) | dependencia declarada | quitar; sldb ya es dependencia |
| graph_ui | `UIs/graph_ui/.github/requirements-suite.txt:10` (`-e git+https://github.com/jpcosec/spec2viz@master#egg=spec2viz`, lo usa el CI para leer los specs piloto) | dependencia declarada (CI) | specs piloto copiados como fixtures o leídos desde specIR |
| graph_ui | `UIs/graph_ui/tests/test_projection_views.py:18` (importorskip), `:33` y `:82` (`spec2viz diagram sync`), `:167` (`spec2viz.sldb_models` ViewDoc) | importación e invocación | `sldb notations sync --spec` (SV-E01), `ViewDoc` de sldb (SV-A17) |
| graph_ui | `UIs/graph_ui/tests/test_mindmap_notation.py:20-21` (`from spec2viz.notation_view import resolve_view`) y `:45` (`spec2viz diagram sync`) | importación e invocación | SV-H03, SV-E01 |
| graph_ui | `UIs/graph_ui/tests/e2e_notation_class.py:58`, `e2e_notation_sequence.py:108`, `e2e_notation_deployment.py:92`, `e2e_notation_activity.py:128`, `e2e_notation_style.py:147`, `e2e_notation_legibility.py:38` y `:175`, `e2e_mindmap_notation.py:27` y `:48`, `e2e_review_workbench_views.py:40`, `:76` y `:96` (`spec2viz diagram sync` e importorskip) | importación e invocación | SV-E01 |
| deskops | `deskops/deskops/graph/desk_graph.py:75` (regla de rutas `FileRule(kind="spec", path_prefixes=("spec", "docs/architecture/spec2viz"))`) | regla de rutas del grafo del desk | decidir la ruta de specs según la decisión del YAML (†); pedido al desk de deskops |
| deskops | `deskops/desk/drawer/plans/workspace-documental/render_diagram.py:7` y `:9` (`spec2viz diagram validate` y `diagram render`) | invocación | comandos de specIR (SV-K13, SV-K16) |
| deskops | `deskops/docs/diagrams/README.md` y los `.md`/`.mmd` de `deskops/docs/diagrams/` que nombran a spec2viz | documentación de diagramas (no cuenta como dependencia para IR13; se regenera con specIR) | renderers de specIR |
| deskops | `deskops/.opencode/skills/use-spec2viz/SKILL.md`; `deskops/.claude/skills/deskops-workflow/SKILL.md` y `references/spec2viz-cli.md` (instruyen a agentes a invocar `spec2viz`) | habilidad de agente | `skills/use-specir/SKILL.md` (SV-J09) |
| pron | `pron/docs/spec2viz/build.py:22-24` (`spec2viz diagram validate`, `diagram render --backend mermaid`, `catalog build`) | invocación | comandos de specIR (SV-K13, SV-K16, SV-K04) |
| sldb | `sldb/docs/architecture/spec2viz/vistas.yml` y sus specs (`current-*.yml`, `python-ast.yml`) | registro de catálogo que construye `spec2viz catalog build` | catálogo de specIR (SV-G01) |
| sldb | `sldb/contracts/identity.toml:299` (`consumers = [..., "spec2viz", ...]`) | configuración de contrato | quitar spec2viz de la lista al retirarlo |
| IR (specIR) | `IR/tests/conftest.py:24` y `:80` (federa el store `spec2viz/.sldb`), `IR/tests/test_mcp_extension.py:24` (`SPEC_STORE = "spec2viz"`) | lectura del store de spec2viz en pruebas | store con modelos de sldb (G5) o fixture propio |
| store `spec2viz/.sldb` | `spec2viz/.sldb/store.yaml:44-57`, `spec2viz/.sldb/core/store_index.yaml:141-194`, `spec2viz/.sldb/core/models/{SpecDoc,SpecNodeDoc,NotationDoc,GlyphDoc,LinkDoc,PaletteDoc,ViewDoc}.yaml` | modelos `spec2viz.sldb_models` registrados | `sldb.models.notation.*` (SV-A17) |

Es el único store bajo `SLDB_1/` cuyo índice registra `spec2viz.sldb_models`.

Specs YAML existentes que afecta la decisión del YAML (†): `spec2viz` (44: `tests/fixtures/`,
`docs/architecture/spec2viz/`, `examples/`), `sldb` (46: `tests/fixtures/`, `docs/architecture/`),
`UIs/graph_ui` (24: `tests/fixtures/`, `docs/representacion/`), `pron` (4: `docs/spec2viz/specs/`),
`deskops` (1: `desk/drawer/plans/workspace-documental/`). Conteo de archivos con `type:` de uno de los
ocho tipos en la raíz, sin `.sldb/`, `build/` ni entornos.

## Pendientes de derivación

Lo que esta matriz deja abierto y debe convertirse en tarea o pedido (no lo resuelve IR07):

1. Filas «usar sldb directamente» (SV-A17, SV-E02, SV-H01 a SV-H06, SV-I05, SV-J06, SV-K18 a SV-K26):
   con IR13c retirada, ninguna tarea porta hoy `tests/test_notation.py`, `tests/test_notation_view.py`,
   `tests/test_view_contract_resolved.py`, `tests/test_style_palette.py` ni `tests/test_view_doc.py`
   contra sldb. La prueba de paridad la aporta IR13 (prueba en specIR que llama a sldb sin envoltorio) o
   una tarea nueva derivada de estas filas.
2. SV-K21 y SV-K26: sldb no tiene comando para validar una notación o una paleta por nombre o ruta.
   Pedido al desk de sldb (`deskops message send --to sldb`) pendiente.
3. SV-K16 y SV-K29: decidido en IR13d. Mientras sldb no tenga el comando (pedido a su desk), lo da
   `specir diagram validate` (y `specir validate`) sobre `load_spec`/`validate_spec` de sldb, sin redefinir
   nada; se retira cuando sldb lo publique.
4. SV-I03: D4 no lista `tests/test_refs.py` entre sus pruebas portadas; pedir a sldb que lo incluya o
   asignar la parte de resolución a IR13b.
5. SV-C13 y SV-C14: resuelto por IR12, que incluyó en su lista de archivos los backends UML de clases y el
   mermaid desde vista resuelta.
6. Consumidores: pedidos de migración a los desks de graph_ui, deskops, pron y sldb (los emite IR13).

## Gate de retiro

Lista comprobable. spec2viz solo se retira cuando **todos** los ítems se cumplen; el procedimiento está en
`docs/spec2viz/gate-de-retiro.md` y lo evalúa IR13.

- [ ] **G1. Filas cumplidas.** Toda fila SV-* de esta matriz tiene su condición de retiro cumplida y la
  prueba que lo acredita citada por IR13 en la fila (ninguna fila sin prueba; ninguna dice descartado ni
  fuera de alcance).
- [ ] **G2. Suite de spec2viz.** Cada caso de cada archivo de `spec2viz/tests/` pasa contra specIR o
  contra sldb (portado), o pertenece a una fila en modo reemplazar cuya prueba equivalente está declarada y
  pasa. La tabla «Pruebas de spec2viz por fila» no deja archivo sin fila.
- [ ] **G3. CLI.** Cada comando y subgrupo de la ayuda de spec2viz (filas SV-K*) tiene equivalente que
  existe y una prueba lo invoca (`docs/spec2viz/correspondencia-cli.md` de IR13d).
- [ ] **G4. Consumidores.** Ningún consumidor del inventario importa ni invoca spec2viz: cero
  `import spec2viz`/`from spec2viz`, cero dependencias declaradas (pyproject, requirements, CI), cero
  invocaciones del comando `spec2viz` en código, scripts o configuración ejecutable, y ninguna habilidad de
  agente que instruya a invocarlo. El comprobador de IR13 sale con código distinto de cero si encuentra una.
- [ ] **G5. Stores.** Ningún store del universo registra modelos `spec2viz.sldb_models` en su
  `store.yaml`, su `store_index.yaml` ni sus `core/models/*.yaml`.
- [ ] **G6. specIR limpio.** Ningún módulo bajo `src/specir/` importa spec2viz (prueba de imports) y specIR
  no define envoltorios de lo que se usa de sldb directamente.
- [ ] **G7. Decisión del YAML.** La decisión sobre el YAML de spec frente al grafo
  (`docs/decisiones/fuente-de-verdad-del-diagrama.md`) está aceptada por JP y las filas marcadas con †
  están alineadas con ella.

FILE:tests/visual/test_cli.py
"""The `specir` command (IR13d): spec2viz's `tests/test_cli.py` ported, the correspondence table and the
agent skill.

- Ported from spec2viz (revision 2de1056), over the same fixtures (`fixtures/spec2viz/`) and on the same
  top-level aliases spec2viz's tests call: `test_validate_*`, `test_render_*`, `test_schema_*`,
  `test_help_mentions_taxonomy_groups_and_renderers`, `test_catalog_schema_stdout`,
  `test_catalog_build_alias_matches_legacy_build` and every `test_build_command*`. The help says
  "Top-level aliases ... remain available" where spec2viz said "Legacy top-level commands remain
  available". The render cases on `diagram render`, the provenance header and the API ones are IR12's
  (`test_render_commands.py`).
- `docs/spec2viz/correspondencia-cli.md` covers exactly the command tree of spec2viz's CLI, and every
  equivalent it names answers `--help` with the options it names (sldb's commands run as a separate
  process; sldb's API functions are called on a builtin).
- `skills/use-specir/SKILL.md` names only commands that exist (each is invoked with `--help`) and no
  spec2viz command."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from specir.cli import ALIASES, main
from specir.visual.catalog import AnnotationsTarget, render_catalog

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CORPUS = HERE / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLES = CORPUS / "examples"
CORRESPONDENCE = REPO / "docs" / "spec2viz" / "correspondencia-cli.md"
SKILL = REPO / "skills" / "use-specir" / "SKILL.md"
SLDB = str(Path(sys.executable).with_name("sldb"))
runner = CliRunner()

sys.path.insert(0, str(REPO / "tests"))
import test_matriz_cobertura_spec2viz as matrix  # noqa: E402


# ── validate ──────────────────────────────────────────────────────────────────


def test_validate_valid():
    r = runner.invoke(main, ["validate", str(FIXTURES / "sequence.create-quotation.yml")])
    assert r.exit_code == 0
    assert "OK" in r.output


def test_validate_invalid():
    r = runner.invoke(main, ["validate", str(FIXTURES / "invalid" / "unknown_node.yml")])
    assert r.exit_code != 0


def test_validate_all_types():
    for name in [
        "sequence.create-quotation.yml",
        "state.quotation.yml",
        "activity.validation.yml",
        "deployment.runtime.yml",
        "component.quotation.yml",
        "matrix.quotation-view.yml",
    ]:
        r = runner.invoke(main, ["validate", str(FIXTURES / name)])
        assert r.exit_code == 0, f"{name}: {r.output}"


def test_diagram_validate_valid():
    r = runner.invoke(main, ["diagram", "validate", str(FIXTURES / "state.quotation.yml")])
    assert r.exit_code == 0 and r.output == "state.quotation.yml: OK\n"


def test_diagram_validate_invalid():
    r = runner.invoke(main, ["diagram", "validate", str(FIXTURES / "invalid" / "unknown_node.yml")])
    assert r.exit_code == 1 and "unknown_node.yml: ERROR: " in r.output


# ── render (top-level alias) ──────────────────────────────────────────────────


def _render(*args: str):
    return runner.invoke(main, ["render", *args])


@pytest.mark.parametrize(
    ("name", "output"),
    [
        ("sequence.create-quotation.yml", "sequence.create-quotation.puml"),
        ("matrix.quotation-view.yml", "matrix.quotation-view.vega.json"),
        ("state.quotation.yml", "state.quotation.puml"),
        ("activity.validation.yml", "activity.validation.puml"),
        ("deployment.runtime.yml", "deployment.runtime.puml"),
        ("component.quotation.yml", "component.quotation.graph.html"),
    ],
)
def test_render_each_type(tmp_path, name, output):
    """spec2viz's test_render_sequence, _matrix, _state, _activity, _deployment and _component."""
    r = _render(str(FIXTURES / name), "--out", str(tmp_path))
    assert r.exit_code == 0, r.output
    assert (tmp_path / output).exists()


def test_render_override(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.mmd").exists()


def test_render_backend_alias(tmp_path):
    r = _render(str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path), "--backend", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.mmd").exists()


def test_render_multiple(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_invalid_fails(tmp_path):
    r = _render(str(FIXTURES / "invalid" / "unknown_node.yml"), "--out", str(tmp_path))
    assert r.exit_code != 0


def test_render_d2(tmp_path):
    r = _render(str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path), "--renderer", "d2")
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.d2").exists()


def test_render_antonia_html(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "antonia-html")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.html").exists()


def test_render_json_reflection_artifact(tmp_path):
    r = _render(str(EXAMPLES / "reflection" / "canonical.yml"), "--out", str(tmp_path), "--renderer", "json")
    assert r.exit_code == 0
    assert (tmp_path / "canonical.artifact.json").exists()


def test_the_render_alias_writes_what_diagram_render_writes(tmp_path):
    for renderer in ("plantuml", "mermaid", "d2", "graph"):
        a, b = tmp_path / f"alias-{renderer}", tmp_path / f"group-{renderer}"
        spec = str(FIXTURES / "component.quotation.yml")
        assert runner.invoke(main, ["render", spec, "--out", str(a), "--renderer", renderer]).exit_code == 0
        assert runner.invoke(main, ["diagram", "render", spec, "--out", str(b), "--renderer", renderer]).exit_code == 0
        [fa], [fb] = sorted(a.iterdir()), sorted(b.iterdir())
        assert fa.name == fb.name and fa.read_bytes() == fb.read_bytes()


# ── lint (top-level alias) ────────────────────────────────────────────────────


def test_lint_alias_matches_diagram_lint(tmp_path):
    good = tmp_path / "good.mmd"
    good.write_text("graph TD\nA-->B\n", encoding="utf-8")
    bad = tmp_path / "bad.mmd"
    bad.write_text("graph TD\nA[<b>x</b>]-->B\n", encoding="utf-8")
    spec = str(FIXTURES / "state.quotation.yml")
    for args in ([str(good)], [str(bad)], [spec], [str(good), str(bad)]):
        alias, group = runner.invoke(main, ["lint", *args]), runner.invoke(main, ["diagram", "lint", *args])
        assert (alias.exit_code, alias.output) == (group.exit_code, group.output), args
    assert runner.invoke(main, ["lint", str(good)]).exit_code == 0
    assert runner.invoke(main, ["lint", spec]).exit_code == 0


# ── schema ────────────────────────────────────────────────────────────────────


def test_schema_stdout():
    r = runner.invoke(main, ["schema", "--type", "sequence"])
    assert r.exit_code == 0
    assert '"title": "SequenceDiagram"' in r.output


def test_schema_outfile(tmp_path):
    out = tmp_path / "schema.json"
    r = runner.invoke(main, ["schema", "--type", "state", "--out", str(out)])
    assert r.exit_code == 0
    assert out.exists()


def test_schema_diagram_store_stdout():
    r = runner.invoke(main, ["schema", "--type", "diagram-store"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output
    assert '"diagram_store"' in r.output


def test_schema_invalid_type_fails():
    r = runner.invoke(main, ["schema", "--type", "unknown"])
    assert r.exit_code != 0


def test_catalog_schema_stdout():
    r = runner.invoke(main, ["catalog", "schema"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output


# ── help and about ────────────────────────────────────────────────────────────


def test_help_mentions_taxonomy_groups_and_renderers():
    r = runner.invoke(main, ["--help"])
    assert r.exit_code == 0
    assert "diagram" in r.output
    assert "catalog" in r.output
    assert "Top-level aliases (render, validate, lint, schema, build) remain available" in r.output

    r = runner.invoke(main, ["render", "--help"])
    assert r.exit_code == 0
    for name in ["plantuml", "mermaid", "vega", "d2", "antonia-html", "json"]:
        assert name in r.output

    r = runner.invoke(main, ["diagram", "--help"])
    assert r.exit_code == 0
    assert "render" in r.output
    assert "validate" in r.output
    assert "schema" in r.output

    r = runner.invoke(main, ["catalog", "--help"])
    assert r.exit_code == 0
    assert "build" in r.output
    assert "schema" in r.output


def test_every_alias_stands_for_a_group_command_with_the_same_parameters():
    for alias, target in ALIASES.items():
        group, name = target.split()
        a, g = main.commands[alias], main.commands[group].commands[name]
        assert [p.opts for p in a.params] == [p.opts for p in g.params], alias


def test_about_names_the_commands_of_specir_and_sldb(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    r = runner.invoke(main, ["about"])
    assert r.exit_code == 0, r.output
    assert f"no .sldb store above {tmp_path}" in r.output
    named = {}
    for line in r.output.splitlines():
        line = re.sub(r"^\d\. ", "", line.strip())
        if line.startswith(("specir ", "sldb ")):
            words, options = _command_and_options(line)
            named.setdefault(" ".join(words), set()).update(options)
    assert {"specir diagram validate", "specir diagram render", "specir diagram lint", "specir catalog build",
            "sldb notations sync", "sldb notations from-graph", "sldb notations view", "sldb serve", "sldb models add"} <= set(named)
    assert "spec2viz diagram" not in r.output and "spec2viz catalog" not in r.output
    for command, options in named.items():
        _assert_answers_help(command.split(), sorted(options))


def test_about_shows_the_store_above_the_current_directory(tmp_path, monkeypatch):
    subprocess.run(["timeout", "120", SLDB, "stores", "init", "--path", str(tmp_path)], check=True, capture_output=True)
    (tmp_path / "docs").mkdir()
    monkeypatch.chdir(tmp_path / "docs")
    r = runner.invoke(main, ["about"])
    assert r.exit_code == 0 and f"store            : {tmp_path / '.sldb'}" in r.output


# ── catalog build and its alias ───────────────────────────────────────────────


def test_catalog_build_alias_matches_legacy_build(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("\ntemplate: template.html\nvistas:\n  - id: sample\n    src: view.mmd\n", encoding="utf-8")

    legacy = tmp_path / "legacy.html"
    grouped = tmp_path / "grouped.html"
    r1 = runner.invoke(main, ["build", "--config", str(config), "--out", str(legacy)])
    r2 = runner.invoke(main, ["catalog", "build", "--config", str(config), "--out", str(grouped)])
    assert r1.exit_code == 0, r1.output
    assert r2.exit_code == 0, r2.output
    assert legacy.read_text(encoding="utf-8") == grouped.read_text(encoding="utf-8")


def test_build_command(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("\ntemplate: template.html\nvistas:\n  - id: sample\n    src: view.mmd\n", encoding="utf-8")

    out = tmp_path / "out.html"
    r = runner.invoke(main, ["build", "--config", str(config), "--out", str(out)])
    assert r.exit_code == 0
    assert out.exists()
    assert "Rendered catalog" in r.output
    html = out.read_text(encoding="utf-8")
    assert "catalog-search" in html


def test_build_command_supports_store_of_stores(tmp_path):
    root = tmp_path
    child = root / "child"
    child.mkdir()

    (root / "template.html").write_text(
        "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>",
        encoding="utf-8",
    )
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-component.yml").write_text(
        "id: spec-component\ntitle: Example\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8"
    )
    (child / "vistas.yml").write_text(
        """
template: unused.html
vistas:
  - id: sample
    category: Arquitectura
    title: Sample Diagram
    nav: Sample
    desc: Demo child vista
    src: view.mmd
    specs:
      - spec-component
""",
        encoding="utf-8",
    )
    (root / "catalog.yml").write_text(
        """
template: template.html
title: Repo Catalog
brand_name: Diagram Catalog
stores:
  - path: child/vistas.yml
    project: demo/project
    tags:
      - domain:crm
""",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "Repo Catalog" in html
    assert "Diagram Catalog" in html
    assert "catalog-search" in html
    assert 'data-project="demo/project"' in html
    assert 'data-type="component"' in html
    assert "domain:crm" in html
    assert "Sample Diagram" in html


def test_build_command_supports_brand_subtitle_in_builtin_template(tmp_path):
    root = tmp_path
    (root / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (root / "spec-component.yml").write_text(
        "id: spec-component\ntitle: Example\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8"
    )
    (root / "catalog.yml").write_text(
        "template: missing-template.html\ntitle: Repo Catalog\nbrand_name: Diagram Catalog\nbrand_subtitle: Repo subtitle from config\nvistas:\n  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n    src: view.mmd\n    specs:\n      - spec-component.yml\n",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "Repo subtitle from config" in html
    assert "Visor transversal de diagramas de spec2viz" not in html


def test_build_command_warns_on_local_template_override(tmp_path):
    root = tmp_path
    (root / "template.html").write_text(
        "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>",
        encoding="utf-8",
    )
    (root / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (root / "spec-component.yml").write_text(
        "id: spec-component\ntitle: Example\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8"
    )
    (root / "catalog.yml").write_text(
        "template: template.html\nvistas:\n  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n    src: view.mmd\n    specs:\n      - spec-component.yml\n",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    assert "using local catalog template override" in r.output


def test_build_command_supports_project_yml_envelope(tmp_path):
    root = tmp_path
    child = root / "child"
    child.mkdir()

    (root / "template.html").write_text(
        "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>",
        encoding="utf-8",
    )
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-state.yml").write_text(
        "id: spec-state\ntitle: Example State\ntype: state\nversion: '1.0'\ndata:\n  entity: X\n  initial: a\n  states:\n    - id: a\n      label: A\n  transitions: []\n",
        encoding="utf-8",
    )
    (child / "vistas.yml").write_text(
        """
template: ../template.html
vistas:
  - id: sample-state
    category: Estados
    title: State Diagram
    nav: State
    desc: Demo leaf
    src: view.mmd
    specs:
      - spec-state.yml
""",
        encoding="utf-8",
    )
    (root / "project.yml").write_text(
        """
diagram_store:
  kind: diagram-store
  template: template.html
  title: Project Catalog
  brand_name: Project Brand
  project_name: project/demo
  stores:
    - path: child/vistas.yml
      project: project/demo
      tags:
        - domain:workflow
""",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "project.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "Project Catalog" in html
    assert "Project Brand" in html
    assert "project/demo" in html
    assert "domain:workflow" in html
    assert 'data-type="state"' in html


def test_build_command_extracts_types_from_specs_dir_and_makes_anchor_ids_unique(tmp_path):
    root = tmp_path
    (root / "template.html").write_text("<html><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>", encoding="utf-8")

    for folder in [root / "alpha" / "docs" / "vistas", root / "beta" / "docs" / "vistas"]:
        folder.mkdir(parents=True)
        (folder.parent.parent / "project.yaml").write_text("project_name: Demo\nclient: sample\n", encoding="utf-8")
        (folder.parent.parent / "specs").mkdir(exist_ok=True)
        (folder.parent.parent / "specs" / "same-view.yml").write_text(
            "id: same-view\ntitle: Same\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8"
        )
        (folder.parent.parent / "rendered").mkdir(exist_ok=True)
        (folder.parent.parent / "rendered" / "same-view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
        (folder / "vistas.yml").write_text(
            "template: template.html\nvistas:\n  - id: vista01\n    title: Demo\n    category: Arquitectura\n    specs:\n      - same-view\n    mmd: ../../rendered/same-view.mmd\n",
            encoding="utf-8",
        )

    (root / "catalog.yml").write_text(
        "template: template.html\nstores:\n  - path: alpha/docs/vistas/vistas.yml\n  - path: beta/docs/vistas/vistas.yml\n", encoding="utf-8"
    )

    out = root / "out.html"
    r = runner.invoke(main, ["catalog", "build", "--config", str(root / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert html.count('data-type="component"') == 2
    anchor_ids = set(re.findall(r'id="(sample-demo-vista01-[a-f0-9]{8})"', html))
    assert len(anchor_ids) == 2


def test_build_command_extracts_html_section_fragments(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "bundle.html").write_text(
        '<html><body><section id="d1"><div class="board"><pre class="mermaid">graph TD\\nA-->B</pre></div></section></body></html>',
        encoding="utf-8",
    )
    (tmp_path / "catalog.yml").write_text(
        "template: template.html\nitems:\n  - id: frag\n    title: Fragment\n    src: bundle.html#d1\n    type: component\n    category: Arquitectura\n",
        encoding="utf-8",
    )

    out = tmp_path / "out.html"
    r = runner.invoke(main, ["catalog", "build", "--config", str(tmp_path / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "bundle.html#d1" not in html
    assert '<div class="board"><pre class="mermaid">graph TD\\nA-->B</pre></div>' in html


def test_build_command_reports_errors(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("template: template.html\nvistas: [\n  {id: broken, src: missing.mmd}\n]\n", encoding="utf-8")

    out = tmp_path / "out.html"
    r = runner.invoke(main, ["build", "--config", str(config), "--out", str(out)])
    assert r.exit_code != 0
    assert "Error building catalog" in r.output


def test_catalog_build_embeds_the_annotations_saver_of_ir13b(tmp_path):
    """`--sldb-url`/`--annotations-doc` build the page IR13b's `render_catalog` builds with that target
    (the round trip through a real `sldb serve` is `test_catalog_annotations.py`); without them the page
    is spec2viz's, and `--annotations` alone leaves the server to the page URL."""
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("title: Demo\nvistas:\n  - id: sample\n    title: Sample\n    src: view.mmd\n", encoding="utf-8")
    cases = {
        (): None,
        ("--annotations",): AnnotationsTarget(),
        ("--sldb-url", "http://127.0.0.1:8765"): AnnotationsTarget(server="http://127.0.0.1:8765"),
        ("--sldb-url", "http://127.0.0.1:8765", "--annotations-doc", "catalog-annotations-x"): AnnotationsTarget("http://127.0.0.1:8765", "catalog-annotations-x"),
    }
    for i, (args, target) in enumerate(cases.items()):
        out = tmp_path / f"out-{i}.html"
        r = runner.invoke(main, ["catalog", "build", "--config", str(config), "--out", str(out), *args])
        assert r.exit_code == 0, r.output
        page = out.read_text(encoding="utf-8")
        assert page == render_catalog(config, annotations=target), args
        assert ("window.SPECIR_ANNOTATIONS" in page) == (target is not None), args


# ── the correspondence table ──────────────────────────────────────────────────


def correspondence_rows() -> list[list[str]]:
    rows = []
    for line in CORRESPONDENCE.read_text(encoding="utf-8").splitlines():
        if line.startswith("| SV-K"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def _command_and_options(text: str) -> tuple[list[str], list[str]]:
    """`specir diagram render --renderer --out` -> (["specir", "diagram", "render"], ["--renderer", "--out"])."""
    words, options, done = [], [], False
    for token in text.split():
        token = token.strip("[]")
        if token.startswith("-"):
            options.append(token)
            done = True
        elif not done and re.fullmatch(r"[a-z][a-z0-9-]*", token):
            words.append(token)
        else:
            done = True
    return words, options


def _assert_answers_help(words: list[str], options: list[str]) -> None:
    if words[0] == "specir":
        r = runner.invoke(main, [*words[1:], "--help"])
        assert r.exit_code == 0, f"{' '.join(words)}: {r.output}"
        output = r.output
    else:
        assert words[0] == "sldb", words
        p = subprocess.run(["timeout", "120", SLDB, *words[1:], "--help"], capture_output=True, text=True)
        assert p.returncode == 0, f"{' '.join(words)}: {p.stderr}"
        output = p.stdout
    for option in options:
        assert re.search(rf"(?<![\w-]){re.escape(option)}(?![\w-])", output), f"{' '.join(words)} has no {option}"


def test_the_table_covers_exactly_the_command_tree_of_spec2viz():
    if not (matrix.PACKAGE / "cli.py").is_file():
        pytest.skip(f"spec2viz sources not found at {matrix.SPEC2VIZ}")
    listed = {re.fullmatch(r"`([^`]+)`", row[1]).group(1) for row in correspondence_rows()}
    assert listed == matrix.commands_from_source() | {"spec2viz --help"}
    ids = [row[0] for row in correspondence_rows()]
    assert sorted(ids) == [f"SV-K{n:02d}" for n in range(1, 31)]


def test_every_equivalent_of_the_table_answers_its_help():
    import sldb.notations as notations

    checked = 0
    for row in correspondence_rows():
        equivalent = re.match(r"`([^`]+)`", row[3]).group(1)
        if equivalent.startswith("sldb.notations."):
            function = getattr(notations, equivalent.rsplit(".", 1)[1])
            builtins = notations.builtin_notations() if function is notations.load_notation else notations.builtin_palettes()
            assert builtins and all(function(name) for name in builtins), equivalent
        else:
            words, options = _command_and_options(equivalent)
            _assert_answers_help(words, options)
        checked += 1
    assert checked == 30


def test_specir_defines_no_command_the_table_gives_to_sldb():
    for row in correspondence_rows():
        command = re.fullmatch(r"`([^`]+)`", row[1]).group(1)
        if row[3].startswith("`sldb"):
            path = command.split()[1:]
            group = main
            for part in path[:-1]:
                group = group.commands.get(part)
                if group is None:
                    break
            assert group is None or path[-1] not in getattr(group, "commands", {}), f"specir duplicates {command}"


# ── the agent skill ───────────────────────────────────────────────────────────


def skill_commands() -> set[str]:
    """Every `specir ...`/`sldb ...` the skill names: inline code spans and lines of its code blocks."""
    text = SKILL.read_text(encoding="utf-8")
    found = set()
    blocks = re.findall(r"```[a-z]*\n(.*?)```", text, flags=re.DOTALL)
    for block in blocks:
        for line in block.splitlines():
            for part in line.split("->"):
                part = part.strip()
                if part.startswith(("specir ", "sldb ")):
                    found.add(part)
    prose = re.sub(r"```[a-z]*\n.*?```", "", text, flags=re.DOTALL)
    found |= {span for span in re.findall(r"`([^`\n]+)`", prose) if span.startswith(("specir ", "sldb "))}
    return found


def test_the_skill_names_only_commands_that_exist():
    commands = skill_commands()
    assert len(commands) > 20
    seen = set()
    for command in sorted(commands):
        words, options = _command_and_options(command)
        key = (tuple(words), tuple(options))
        if key in seen:
            continue
        seen.add(key)
        _assert_answers_help(words, options)
    named = {" ".join(words) for words, _ in seen}
    assert {"specir about", "specir diagram render", "specir diagram validate", "specir diagram lint", "specir catalog build",
            "specir catalog schema", "sldb notations sync", "sldb notations from-graph", "sldb serve"} <= named


def test_the_skill_names_no_spec2viz_command():
    text = SKILL.read_text(encoding="utf-8")
    assert not re.search(r"(?m)^\s*(python -m )?spec2viz[ .]", text)
    assert not re.search(r"`(python -m )?spec2viz[ .][^`]*`", text)
    assert re.search(r"^name: use-specir$", text, flags=re.MULTILINE)

FILE:tests/visual/test_api.py
"""The public Python API of specIR's visual layer (IR13d): spec2viz's `tests/test_api.py` ported.

spec2viz's package exported `load`, `validate`, `compile_ir`, `render`, `json_schema`,
`write_json_schema`, `render_to_file`, `with_provenance`, `provenance_header`, `provenance_text`,
`EXT_MAP`, `DEFAULT_RENDERER` and `BaseDiagram`. `load` and `validate` are sldb's (`load_spec` and
`validate_spec` of `sldb.api.notations`, D3) and are used directly, not re-exported by specIR (SV-J01);
the rest is `specir.visual` (SV-J02, SV-J03). Every case of spec2viz's file runs here over the same
fixtures (`fixtures/spec2viz/`), with only the imports changed: `load`/`validate` from sldb, the
models and the IR from `specir.visual`, `ValidationError` from sldb (D3)."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest
import sldb.api.notations as sldb_notations
from sldb.api.notations import load_spec as load
from sldb.api.notations import validate_spec as validate

import specir.visual as visual
from specir.visual import (
    ActivityDiagram,
    ActivityIR,
    ComponentDiagram,
    ComponentIR,
    DeploymentDiagram,
    DeploymentIR,
    MatrixDiagram,
    MatrixIR,
    SequenceDiagram,
    SequenceIR,
    StateDiagram,
    StateIR,
    compile_ir,
    json_schema,
    render,
    render_to_file,
    write_json_schema,
)

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures" / "spec2viz" / "tests" / "fixtures"
SPEC2VIZ_INIT = HERE.parents[2] / "spec2viz" / "spec2viz" / "__init__.py"

#: What spec2viz's package exported that is sldb's, and the sldb name that replaces it.
FROM_SLDB = {"load": "load_spec", "validate": "validate_spec"}


def _validation_error() -> type[Exception]:
    from sldb.notations import ValidationError  # the error D3 raises (re-exported by sldb.notations)

    return ValidationError


# ── load ──────────────────────────────────────────────────────────────────────


def test_load_sequence():
    assert isinstance(load(FIXTURES / "sequence.create-quotation.yml"), SequenceDiagram)


def test_load_state():
    assert isinstance(load(FIXTURES / "state.quotation.yml"), StateDiagram)


def test_load_component():
    assert isinstance(load(FIXTURES / "component.quotation.yml"), ComponentDiagram)


def test_load_activity():
    assert isinstance(load(FIXTURES / "activity.validation.yml"), ActivityDiagram)


def test_load_deployment():
    assert isinstance(load(FIXTURES / "deployment.runtime.yml"), DeploymentDiagram)


def test_load_matrix():
    assert isinstance(load(FIXTURES / "matrix.quotation-view.yml"), MatrixDiagram)


# ── validate ──────────────────────────────────────────────────────────────────


def test_validate_passes():
    validate(load(FIXTURES / "component.quotation.yml"))


def test_validate_fails():
    with pytest.raises(_validation_error()):
        validate(load(FIXTURES / "invalid" / "unknown_node.yml"))


# ── compile_ir ────────────────────────────────────────────────────────────────


def test_compile_sequence():
    assert isinstance(compile_ir(load(FIXTURES / "sequence.create-quotation.yml")), SequenceIR)


def test_compile_state():
    assert isinstance(compile_ir(load(FIXTURES / "state.quotation.yml")), StateIR)


def test_compile_component():
    assert isinstance(compile_ir(load(FIXTURES / "component.quotation.yml")), ComponentIR)


def test_compile_activity():
    assert isinstance(compile_ir(load(FIXTURES / "activity.validation.yml")), ActivityIR)


def test_compile_deployment():
    assert isinstance(compile_ir(load(FIXTURES / "deployment.runtime.yml")), DeploymentIR)


def test_compile_matrix():
    assert isinstance(compile_ir(load(FIXTURES / "matrix.quotation-view.yml")), MatrixIR)


# ── render ────────────────────────────────────────────────────────────────────


def test_render_str():
    ir = compile_ir(load(FIXTURES / "sequence.create-quotation.yml"))
    assert "@startuml" in render(ir)


def test_render_dict():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    assert isinstance(render(ir), dict)


def test_render_mermaid_override():
    ir = compile_ir(load(FIXTURES / "state.quotation.yml"))
    assert "stateDiagram-v2" in render(ir, renderer="mermaid")


# ── render_to_file ────────────────────────────────────────────────────────────


def test_render_to_file_puml(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "@startuml" in p.read_text()


def test_render_to_file_vega(tmp_path):
    p = render_to_file(FIXTURES / "matrix.quotation-view.yml", out=tmp_path)
    assert p.name.endswith(".vega.json")
    assert "$schema" in json.loads(p.read_text())


def test_render_to_file_state(tmp_path):
    p = render_to_file(FIXTURES / "state.quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "[*] -->" in p.read_text()


def test_render_to_file_activity(tmp_path):
    p = render_to_file(FIXTURES / "activity.validation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "start" in p.read_text()


def test_render_to_file_deployment(tmp_path):
    p = render_to_file(FIXTURES / "deployment.runtime.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "Browser" in p.read_text()


def test_render_to_file_component(tmp_path):
    p = render_to_file(FIXTURES / "component.quotation.yml", out=tmp_path)
    assert p.name.endswith(".graph.html")
    assert "QuotationFlow" in p.read_text()


def test_render_to_file_override(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path, renderer="mermaid")
    assert p.suffix == ".mmd"
    assert "sequenceDiagram" in p.read_text()


# ── json_schema ───────────────────────────────────────────────────────────────


def test_json_schema_for_all_types():
    schema = json_schema()

    assert "$defs" in schema
    assert "SequenceDiagram" in schema["$defs"]


def test_json_schema_for_specific_type():
    schema = json_schema("sequence")

    assert schema["title"] == "SequenceDiagram"
    assert schema["properties"]["data"]["description"] == "Sequence-specific participants and messages."


def test_write_json_schema(tmp_path):
    path = write_json_schema(tmp_path / "sequence.schema.json", diagram_type="sequence")

    assert path.exists()
    assert json.loads(path.read_text())["title"] == "SequenceDiagram"


# ── the API covers spec2viz's ─────────────────────────────────────────────────


def spec2viz_public_names() -> set[str]:
    """The public names spec2viz's `__init__` defines or imports (read from its source, not imported)."""
    tree = ast.parse(SPEC2VIZ_INIT.read_text(encoding="utf-8"))
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("spec2viz"):
            names |= {alias.asname or alias.name for alias in node.names}
    return {name for name in names if not name.startswith("_")}


def test_every_public_name_of_spec2viz_has_its_equivalent():
    if not SPEC2VIZ_INIT.is_file():
        pytest.skip(f"spec2viz sources not found at {SPEC2VIZ_INIT}")
    names = spec2viz_public_names()
    assert {"load", "validate", "compile_ir", "render", "render_to_file", "json_schema", "write_json_schema"} <= names
    for name in sorted(names):
        if name in FROM_SLDB:
            assert callable(getattr(sldb_notations, FROM_SLDB[name])), name
            assert name not in visual.__all__ and FROM_SLDB[name] not in visual.__all__, f"specIR re-exports sldb's {name}"
        else:
            assert name in visual.__all__ and getattr(visual, name) is not None, name


def test_every_name_of_the_public_api_resolves():
    for name in visual.__all__:
        assert hasattr(visual, name), name
    assert visual.EXT_MAP.keys() == visual.RENDERER_MAP.keys()
    assert set(visual.DEFAULT_RENDERER.values()) <= set(visual.RENDERER_MAP)


def test_the_api_renders_a_catalog_and_lints_mermaid(tmp_path):
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("title: Demo\nvistas:\n  - id: sample\n    title: Sample\n    src: view.mmd\n", encoding="utf-8")
    out = visual.build_catalog(config, tmp_path / "catalog.html")
    assert out.read_text(encoding="utf-8") == visual.render_catalog(config)
    assert "window.SPECIR_ANNOTATIONS" in visual.render_catalog(config, annotations=visual.AnnotationsTarget(server="http://127.0.0.1:1"))
    text = visual.render(compile_ir(load(FIXTURES / "state.quotation.yml")), "mermaid")
    assert visual.lint_mermaid(text, check_html=True) == []
    with pytest.raises(visual.MermaidLintError):
        visual.assert_mermaid_ok("graph TD\nA[<b>x</b>]-->B\n", source="bad.mmd")


def test_the_provenance_helpers_name_specir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "s.yml").write_text("x", encoding="utf-8")
    assert visual.provenance_text("s.yml").startswith("specir: generated from s.yml;")
    assert visual.provenance_header("plantuml", "s.yml").startswith("' specir:")
    assert visual.with_provenance("d2", "s.yml", "a -> b\n").startswith("# specir:")

FILE:tests/visual/test_packaging.py
"""Packaging of the `specir` command (IR13d, SV-J07).

- spec2viz's `tests/test_packaging.py::test_primary_cli_still_exposes_commands`, ported (its other three
  cases are IR12's, in `test_render_cases.py` and `test_schema.py`).
- The script `specir` is declared in `pyproject.toml` and points at `specir.cli:main`.
- The package installs in a clean environment (a new venv with sldb and the wheel of specIR, without
  spec2viz) and the command starts there: `specir --help`, `specir about` and `specir diagram render`
  run, and `import spec2viz` fails."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from click.testing import CliRunner

from specir.cli import main as specir_main

PROJECT = Path(__file__).resolve().parents[2]
SLDB_SOURCE = PROJECT.parent / "sldb"
SPEC = PROJECT / "tests" / "visual" / "fixtures" / "spec2viz" / "tests" / "fixtures" / "state.quotation.yml"


def test_primary_cli_still_exposes_commands():
    runner = CliRunner()
    result = runner.invoke(specir_main, ["--help"])

    assert result.exit_code == 0
    assert "render" in result.output
    assert "validate" in result.output


def test_the_script_is_the_command_of_specir_cli():
    scripts = tomllib.loads((PROJECT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["scripts"]
    assert scripts["specir"] == "specir.cli:main"
    installed = Path(sys.executable).with_name("specir")
    if installed.exists():
        result = subprocess.run(["timeout", "120", str(installed), "--help"], capture_output=True, text=True)
        assert result.returncode == 0 and "Taxonomy:" in result.stdout, result.stderr
    result = subprocess.run(["timeout", "120", sys.executable, "-m", "specir.cli", "--help"], capture_output=True, text=True)
    assert result.returncode == 0 and "Taxonomy:" in result.stdout, result.stderr


def _run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(["timeout", "600", *command], capture_output=True, text=True, **kwargs)


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv is not installed: no backend to build the wheel and the venv")
@pytest.mark.skipif(not (SLDB_SOURCE / "pyproject.toml").is_file(), reason=f"sldb sources not found at {SLDB_SOURCE}")
def test_the_package_installs_in_a_clean_environment_and_starts_without_spec2viz(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    shutil.copy(PROJECT / "pyproject.toml", project / "pyproject.toml")
    shutil.copytree(PROJECT / "src" / "specir", project / "src" / "specir", ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
    built = _run(["uv", "build", "--wheel", "--offline", "--out-dir", str(tmp_path / "dist"), str(project)])
    assert built.returncode == 0, built.stderr[-800:]
    wheel = next((tmp_path / "dist").glob("specir-*.whl"))

    venv = tmp_path / "venv"
    created = _run(["uv", "venv", "--offline", "--python", sys.executable, str(venv)])
    assert created.returncode == 0, created.stderr[-800:]
    python = venv / "bin" / "python"
    install = ["uv", "pip", "install", "--python", str(python), str(SLDB_SOURCE), str(wheel)]
    installed = _run([*install, "--offline"])  # from uv's cache when it holds every dependency
    if installed.returncode != 0:
        installed = _run(install)
        if installed.returncode != 0 and "network" in installed.stderr.lower():
            pytest.skip(f"the dependencies are neither in uv's cache nor reachable: {installed.stderr[-300:]}")
    assert installed.returncode == 0, installed.stderr[-1500:]

    listed = _run(["uv", "pip", "list", "--python", str(python)])
    assert "spec2viz" not in listed.stdout.lower(), listed.stdout
    no_spec2viz = _run([str(python), "-c", "import spec2viz"], cwd=tmp_path)
    assert no_spec2viz.returncode != 0 and "ModuleNotFoundError" in no_spec2viz.stderr

    specir = venv / "bin" / "specir"
    for args in (["--help"], ["about"], ["diagram", "--help"], ["catalog", "build", "--help"]):
        result = _run([str(specir), *args], cwd=tmp_path)
        assert result.returncode == 0, (args, result.stderr[-800:])
    assert "Taxonomy:" in _run([str(specir), "--help"], cwd=tmp_path).stdout

    out = tmp_path / "out"
    rendered = _run([str(specir), "render", str(SPEC), "--out", str(out), "--renderer", "mermaid"], cwd=tmp_path)
    assert rendered.returncode == 0, rendered.stderr[-800:]
    assert (out / "state.quotation.mmd").read_text(encoding="utf-8")
    validated = _run([str(specir), "validate", str(SPEC)], cwd=tmp_path)
    assert validated.returncode == 0 and validated.stdout == "state.quotation.yml: OK\n", validated.stderr
    # the package that runs is the installed wheel, not the source tree
    where = _run([str(python), "-c", "import specir, sys; print(specir.__file__)"], cwd=tmp_path)
    assert str(venv) in where.stdout, where.stdout

FILE:tests/visual/test_render_commands.py
"""Rendering through the API and the commands (SV-C01, SV-C04, SV-C05, SV-C10 to SV-C12, SV-C15).

Ported from spec2viz (revision 2de1056), over the same fixtures (`fixtures/spec2viz/`):

- `tests/test_api.py`: `test_render_str`, `test_render_dict`, `test_render_mermaid_override` and the
  seven `test_render_to_file_*` (on `specir.visual.render_file.render_to_file`).
- `tests/test_cli.py`: every `test_render_*` (on `diagram render`, the command the top-level alias of
  IR13d calls) and `test_rendered_text_projections_carry_a_provenance_header`, whose header now names
  specIR's command (`specir diagram validate`).
- `tests/test_rendering_bug.py`: `test_direct_render_to_file`."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner
from sldb.api.notations import load_spec as load

from specir.cli import main
from specir.visual.compilers import compile_ir
from specir.visual.render_file import provenance_header, render_to_file
from specir.visual.renderers import render

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_parity  # noqa: E402

CORPUS = Path(__file__).resolve().parent / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLES = CORPUS / "examples"
runner = CliRunner()


# ── tests/test_api.py ───────────────────────────────────────────────────────────────────────────


def test_render_str():
    ir = compile_ir(load(FIXTURES / "sequence.create-quotation.yml"))
    assert "@startuml" in render(ir)


def test_render_dict():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    assert isinstance(render(ir), dict)


def test_render_mermaid_override():
    ir = compile_ir(load(FIXTURES / "state.quotation.yml"))
    assert "stateDiagram-v2" in render(ir, renderer="mermaid")


def test_render_to_file_puml(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "@startuml" in p.read_text()


def test_render_to_file_vega(tmp_path):
    p = render_to_file(FIXTURES / "matrix.quotation-view.yml", out=tmp_path)
    assert p.name.endswith(".vega.json")
    assert "$schema" in json.loads(p.read_text())


def test_render_to_file_state(tmp_path):
    p = render_to_file(FIXTURES / "state.quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "[*] --> browsing" in p.read_text()


def test_render_to_file_activity(tmp_path):
    p = render_to_file(FIXTURES / "activity.validation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "start" in p.read_text()


def test_render_to_file_deployment(tmp_path):
    p = render_to_file(FIXTURES / "deployment.runtime.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "Browser" in p.read_text()


def test_render_to_file_component(tmp_path):
    p = render_to_file(FIXTURES / "component.quotation.yml", out=tmp_path)
    assert p.name.endswith(".graph.html")
    assert "QuotationFlow" in p.read_text()


def test_render_to_file_override(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path, renderer="mermaid")
    assert p.suffix == ".mmd"
    assert "sequenceDiagram" in p.read_text()


# ── tests/test_cli.py ───────────────────────────────────────────────────────────────────────────


def _render(*args: str):
    return runner.invoke(main, ["diagram", "render", *args])


def test_render_sequence(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()


def test_render_matrix(tmp_path):
    r = _render(str(FIXTURES / "matrix.quotation-view.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "matrix.quotation-view.vega.json").exists()


def test_render_state(tmp_path):
    r = _render(str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_activity(tmp_path):
    r = _render(str(FIXTURES / "activity.validation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "activity.validation.puml").exists()


def test_render_deployment(tmp_path):
    r = _render(str(FIXTURES / "deployment.runtime.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "deployment.runtime.puml").exists()


def test_render_component(tmp_path):
    r = _render(str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.graph.html").exists()


def test_render_override(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.mmd").exists()


def test_render_backend_alias(tmp_path):
    r = _render(str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path), "--backend", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.mmd").exists()


def test_render_multiple(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_invalid_fails(tmp_path):
    r = _render(str(FIXTURES / "invalid" / "unknown_node.yml"), "--out", str(tmp_path))
    assert r.exit_code != 0
    assert r.output.startswith("Error: ")


def test_render_help_lists_the_renderers():
    """The renderer part of `test_help_mentions_taxonomy_groups_and_renderers` (the rest is IR13d's)."""
    r = runner.invoke(main, ["diagram", "render", "--help"])
    assert r.exit_code == 0
    for name in ["plantuml", "mermaid", "vega", "d2", "antonia-html", "json"]:
        assert name in r.output
    r = runner.invoke(main, ["diagram", "--help"])
    assert r.exit_code == 0
    assert "render" in r.output and "validate" in r.output and "schema" in r.output and "lint" in r.output


def test_render_d2(tmp_path):
    r = _render(str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path), "--renderer", "d2")
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.d2").exists()


def test_render_antonia_html(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "antonia-html")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.html").exists()


def test_render_json_reflection_artifact(tmp_path):
    r = _render(str(EXAMPLES / "reflection" / "canonical.yml"), "--out", str(tmp_path), "--renderer", "json")
    assert r.exit_code == 0
    assert (tmp_path / "canonical.artifact.json").exists()


def test_rendered_text_projections_carry_a_provenance_header(tmp_path, monkeypatch):
    """Una proyeccion generada dice de que spec sale y como se valida; el JSON no lleva cabecera."""
    monkeypatch.chdir(CORPUS)
    spec = Path("examples/component/example.yml")
    for renderer, prefix in (("mermaid", "%%"), ("plantuml", "'"), ("d2", "#")):
        text = render_to_file(spec, out=tmp_path, renderer=renderer).read_text(encoding="utf-8")
        lines = text.splitlines()
        # en mermaid el frontmatter de config (ELK) va primero; la cabecera, justo despues
        first = lines[lines.index("---", 1) + 1] if renderer == "mermaid" else lines[0]
        assert first.startswith(f"{prefix} specir: generated from examples/component/example.yml;")
        assert "`specir diagram validate examples/component/example.yml`" in first
    assert provenance_header("vega", spec) == "" and provenance_header("json", spec) == ""
    matrix = render_to_file(Path("tests/fixtures/matrix.quotation-view.yml"), out=tmp_path, renderer="vega").read_text(encoding="utf-8")
    assert matrix.lstrip().startswith("{")


def test_the_header_names_a_command_that_validates(tmp_path, monkeypatch):
    """The command the provenance header names exists and validates the spec."""
    monkeypatch.chdir(CORPUS)
    r = runner.invoke(main, ["diagram", "validate", "examples/component/example.yml"])
    assert r.exit_code == 0 and r.output == "example.yml: OK\n"
    r = runner.invoke(main, ["diagram", "validate", "tests/fixtures/invalid/unknown_node.yml"])
    assert r.exit_code == 1 and "unknown_node.yml: ERROR: " in r.output


# ── tests/test_rendering_bug.py ─────────────────────────────────────────────────────────────────


def test_direct_render_to_file(tmp_path):
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    fixture_path = fixture_dir / "canonical.yml"
    fixture_path.write_text("""
id: canonical-arch
title: Canonical Architecture
type: component
version: "1.0"
data:
  nodes:
    core: {label: Core, kind: internal}
    api: {label: API, kind: boundary}
  edges:
    - {from: api, to: core, relation: uses}
""")
    out_dir = tmp_path / "out"
    output_path = render_to_file(fixture_path, out=out_dir, renderer="mermaid")
    assert output_path.exists()
    assert "flowchart TD" in output_path.read_text()
    assert "core" in output_path.read_text()
    assert "api" in output_path.read_text()


@pytest.mark.parity
@pytest.mark.parametrize("renderer", ["plantuml", "mermaid", "d2", "vega", "graph", "bpmn"])
def test_render_to_file_writes_what_spec2viz_writes_but_the_command_it_names(tmp_path, monkeypatch, renderer):
    """Every file spec2viz's `render_to_file` writes for a spec, specIR writes with the same bytes,
    except that the provenance header names `specir` where spec2viz named `spec2viz`."""
    pytest.importorskip("spec2viz")
    monkeypatch.chdir(CORPUS)
    monkeypatch.setenv("SPECIR_MMDC", "0")
    monkeypatch.setenv("SPEC2VIZ_MMDC", "0")
    spec = {
        "vega": "tests/fixtures/matrix.quotation-view.yml", "graph": "tests/fixtures/component.quotation.yml",
        "bpmn": "tests/fixtures/activity.mepu-decision.yml",
    }.get(renderer, "tests/fixtures/deployment.nested.yml")
    ours, theirs = tmp_path / "specir", tmp_path / "spec2viz"
    render_to_file(spec, out=ours, renderer=renderer)
    render_parity.spec2viz_render_to_file(spec, theirs, renderer)
    assert sorted(os.listdir(ours)) == sorted(os.listdir(theirs))
    for name in os.listdir(theirs):
        expected = (theirs / name).read_text(encoding="utf-8").replace("spec2viz: generated from", "specir: generated from")
        expected = expected.replace("`spec2viz diagram validate", "`specir diagram validate")
        actual = (ours / name).read_text(encoding="utf-8")
        if renderer == "vega":
            # spec2viz built the kindColor domain from a set (order depends on PYTHONHASHSEED,
            # SV-C05): compare the scale as a kind -> color mapping, everything else exactly.
            wrap = lambda text: render_parity.comparable({"vega": {"out": json.loads(text)}})  # noqa: E731
            assert wrap(actual) == wrap(expected), name
            continue
        assert actual == expected, name

FILE:tests/visual/test_schema.py
"""JSON Schema export of specs and catalogs (SV-A15, SV-A16), migrated from `spec2viz.schema`.

The models are sldb's (D3); specIR only exports their schema. The export equals spec2viz's for all
types, each type and the diagram store envelope: against the saved goldens and spec2viz's checked-in
schemas (`examples/schema/`) always, against spec2viz live when it is installed. Ported from spec2viz
(revision 2de1056): `test_json_schema_for_all_types`, `test_json_schema_for_specific_type` and
`test_write_json_schema` of `tests/test_api.py`; `test_schema_stdout`, `test_schema_outfile`,
`test_schema_diagram_store_stdout`, `test_schema_invalid_type_fails` and `test_catalog_schema_stdout`
of `tests/test_cli.py` (on `diagram schema`, the command the top-level alias of IR13d calls); and
`test_schema_examples_match_generated_output` and `test_every_model_field_has_a_description` of
`tests/test_packaging.py` (the second over the exported schema, since the model classes are sldb's)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import render_parity  # noqa: E402

from specir.cli import main  # noqa: E402
from specir.visual.schema import json_schema, write_json_schema  # noqa: E402

SCHEMAS = HERE / "fixtures" / "spec2viz" / "examples" / "schema"
runner = CliRunner()


def test_schema_goldens_cover_every_type():
    assert set(render_parity.schema_goldens()) == {str(t or "all") for t in render_parity.SCHEMA_TYPES}


def test_specir_exports_what_the_goldens_say():
    assert render_parity.schemas(json_schema) == render_parity.schema_goldens()


@pytest.mark.parity
def test_specir_exports_what_spec2viz_exports():
    pytest.importorskip("spec2viz")
    assert render_parity.schemas(json_schema) == render_parity.schemas(render_parity.spec2viz_json_schema())


# ── tests/test_api.py ───────────────────────────────────────────────────────────────────────────


def test_json_schema_for_all_types():
    schema = json_schema()

    assert "$defs" in schema
    assert "SequenceDiagram" in schema["$defs"]


def test_json_schema_for_specific_type():
    schema = json_schema("sequence")

    assert schema["title"] == "SequenceDiagram"
    assert schema["properties"]["data"]["description"] == "Sequence-specific participants and messages."


def test_write_json_schema(tmp_path):
    path = write_json_schema(tmp_path / "sequence.schema.json", diagram_type="sequence")

    assert path.exists()
    assert json.loads(path.read_text())["title"] == "SequenceDiagram"


# ── tests/test_cli.py ───────────────────────────────────────────────────────────────────────────


def test_schema_stdout():
    r = runner.invoke(main, ["diagram", "schema", "--type", "sequence"])
    assert r.exit_code == 0
    assert '"title": "SequenceDiagram"' in r.output


def test_schema_outfile(tmp_path):
    out = tmp_path / "schema.json"
    r = runner.invoke(main, ["diagram", "schema", "--type", "state", "--out", str(out)])
    assert r.exit_code == 0
    assert out.exists()


def test_schema_diagram_store_stdout():
    r = runner.invoke(main, ["diagram", "schema", "--type", "diagram-store"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output
    assert '"diagram_store"' in r.output


def test_schema_invalid_type_fails():
    r = runner.invoke(main, ["diagram", "schema", "--type", "unknown"])
    assert r.exit_code != 0


def test_catalog_schema_stdout():
    r = runner.invoke(main, ["catalog", "schema"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output
    assert json.loads(r.output) == json_schema("diagram-store")


# ── tests/test_packaging.py ─────────────────────────────────────────────────────────────────────


def test_schema_examples_match_generated_output():
    assert json.loads((SCHEMAS / "spec2viz.schema.json").read_text()) == json_schema()
    assert json.loads((SCHEMAS / "sequence.schema.json").read_text()) == json_schema("sequence")


#: The models spec2viz's test checked, by the name of their schema definition. `BaseDiagram` has no
#: definition of its own: its fields are in each `*Diagram`.
DESCRIBED_MODELS = (
    "Metadata", "Style", "ParticipantModel", "MessageModel", "SequenceData", "SequenceDiagram",
    "StateModel", "TransitionModel", "StateData", "StateDiagram", "NodeModel", "EdgeModel", "ComponentData",
    "ComponentDiagram", "StepModel", "ActivityData", "ActivityDiagram", "DeploymentNodeModel", "ArtifactModel",
    "ConnectionModel", "DeploymentData", "DeploymentDiagram", "MatrixStageModel", "MatrixViewModel",
    "MatrixComponentModel", "MatrixData", "MatrixDiagram",
)


def test_every_model_field_has_a_description():
    """Every field of the models spec2viz checked has a description in the exported schema."""
    definitions = json_schema()["$defs"]
    missing = [
        f"{name}.{field}"
        for name in DESCRIBED_MODELS
        for field, prop in definitions[name]["properties"].items()
        if not prop.get("description")
    ]
    assert not missing, missing

FILE:tests/visual/test_lint_mermaid.py
"""The mermaid linter of specIR (SV-D01), migrated from `spec2viz.linters.mermaid`.

- `tests/test_mermaid_mmdc.py` of spec2viz (revision 2de1056) ported case by case: the real-engine
  (mmdc) cases skip when mermaid-cli is not installed, as in spec2viz; the regex cases force the
  engine off (`SPECIR_MMDC=0`, and spec2viz's `SPEC2VIZ_MMDC=0` still works).
- The same findings as spec2viz on the lint fixtures (`render_parity.lint_cases`: spec2viz's lint
  texts and the mermaid of every spec of the corpus), with and without the raw-angle-bracket rule:
  against the saved goldens always, against spec2viz live when it is installed.
- `diagram lint` reports a clean spec, a clean `.mmd` and a broken `.mmd` as spec2viz's did."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import render_parity  # noqa: E402

from specir.cli import main  # noqa: E402
from specir.visual.exceptions import RenderError  # noqa: E402
from specir.visual.lint_mermaid import MermaidLintError, assert_mermaid_ok, lint_mermaid, mmdc_path  # noqa: E402

_MMDC = mmdc_path() is not None
requires_mmdc = pytest.mark.skipif(not _MMDC, reason="mmdc (mermaid-cli) not installed")

BROKEN = {name: render_parity.LINT_TEXTS[name] for name in ("paren-edge-label", "brace-edge-label", "nested-quotes", "html-entity-seq")}
CLEAN = {name: render_parity.LINT_TEXTS[name] for name in ("simple-graph", "quoted-paren-edge", "sequence-ok")}


# ── tests/test_mermaid_mmdc.py ──────────────────────────────────────────────────────────────────


@requires_mmdc
@pytest.mark.parametrize("case", BROKEN)
def test_mmdc_catches_broken(case):
    problems = lint_mermaid(BROKEN[case])
    assert problems, f"{case}: expected mmdc to reject but lint was clean"
    assert any("mmdc" in p for p in problems)


@requires_mmdc
@pytest.mark.parametrize("case", CLEAN)
def test_mmdc_passes_clean(case):
    assert lint_mermaid(CLEAN[case]) == []


@pytest.mark.parametrize("variable", ["SPECIR_MMDC", "SPEC2VIZ_MMDC"])
def test_mmdc_disabled_skips_engine(monkeypatch, variable):
    # With the engine forced off, a paren edge label passes the regex-only pass.
    monkeypatch.delenv("SPECIR_MMDC", raising=False)
    monkeypatch.setenv(variable, "0")
    assert mmdc_path() is None
    assert lint_mermaid(BROKEN["paren-edge-label"]) == []


def test_regex_rules_still_fire_without_engine(monkeypatch):
    # The pre-existing heuristics must keep working when the engine is off.
    monkeypatch.setenv("SPECIR_MMDC", "0")
    problems = lint_mermaid("sequenceDiagram\n    A<<--B: bad\n")
    assert any("<<--" in p for p in problems)


# ── same findings as spec2viz ───────────────────────────────────────────────────────────────────


def test_lint_goldens_cover_the_fixtures_and_flag_the_bad_ones():
    goldens = render_parity.lint_goldens()
    assert sorted(goldens) == sorted(render_parity.lint_cases())
    flagged = {name for name, found in goldens.items() if found["check_html"]}
    assert {"invalid-return-arrow", "raw-angle-brackets", "bad-return-arrow", "empty-decision"} <= flagged
    assert any(name.startswith("mermaid:") for name in goldens)


def test_specir_finds_what_the_goldens_say(monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    assert render_parity.lint_findings(lint_mermaid) == render_parity.lint_goldens()


@pytest.mark.parity
def test_specir_finds_what_spec2viz_finds(monkeypatch):
    pytest.importorskip("spec2viz")
    monkeypatch.setenv("SPECIR_MMDC", "0")
    monkeypatch.setenv("SPEC2VIZ_MMDC", "0")
    assert render_parity.lint_findings(lint_mermaid) == render_parity.lint_findings(render_parity.spec2viz_lint())


def test_assert_mermaid_ok_raises_a_render_error(monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    assert_mermaid_ok(CLEAN["sequence-ok"])
    with pytest.raises(MermaidLintError, match=r"Mermaid lint failed in x\.mmd \(2 issue\(s\)\)") as caught:
        assert_mermaid_ok(render_parity.LINT_TEXTS["invalid-return-arrow"], source="x.mmd")
    assert isinstance(caught.value, RenderError)


# ── diagram lint ────────────────────────────────────────────────────────────────────────────────


def test_diagram_lint_command(tmp_path, monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    runner = CliRunner()
    spec = render_parity.parity.FIXTURES / "tests" / "fixtures" / "sequence.create-quotation.yml"
    ok = runner.invoke(main, ["diagram", "lint", str(spec)])
    assert ok.exit_code == 0 and "sequence.create-quotation.yml: OK" in ok.output
    good = tmp_path / "good.mmd"
    good.write_text(CLEAN["simple-graph"], encoding="utf-8")
    bad = tmp_path / "bad.mmd"
    bad.write_text(render_parity.LINT_TEXTS["invalid-return-arrow"], encoding="utf-8")
    result = runner.invoke(main, ["diagram", "lint", str(good), str(bad)])
    assert result.exit_code == 1
    assert "good.mmd: OK" in result.output and "bad.mmd: 2 issue(s)" in result.output and "<<--" in result.output

FILE:tests/visual/test_render_cases.py
"""The render cases of spec2viz (revision 2de1056) that live outside `tests/test_renderers.py`, ported to
specIR over the same fixtures (`fixtures/spec2viz/`):

- `tests/test_class_diagram.py` and `tests/test_class_packages.py`: the cases that render (SV-B03,
  SV-C13). Their validation cases are D3's (sldb) and their sync case is D1's.
- `tests/test_activity_lanes.py` and `tests/test_deployment_nested.py`: the cases that render
  (SV-C02 to SV-C04, SV-C11). Their validation and sync cases are sldb's (D3, D1).
- `tests/test_catalog_resolved_views.py`: the four `view_to_mermaid` cases (SV-C14), over the view
  that sldb resolves (`sldb.api.notations.resolve_view`) from a spec synced with sldb's `SpecSync`
  into a fresh store. Its `catalog build` cases are IR13b's.
- `tests/test_exceptions.py`: the asserts on `Spec2VizError`, `CompileError` and `RenderError`
  (SV-A14). Those on `ParseError` and `ValidationError` are D3's.

The cases that need the real mermaid engine (mmdc) skip when it is not installed, as in spec2viz."""

from __future__ import annotations

import html as _html
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from sldb.api.notations import load_spec as load
from sldb.api.notations import validate_spec as validate

from specir.visual.compilers import compile_ir
from specir.visual.exceptions import CompileError, RenderError, Spec2VizError
from specir.visual.ir import ClassIR
from specir.visual.lint_mermaid import MermaidLintError, lint_mermaid, mmdc_path
from specir.visual.renderers import render
from specir.visual.renderers.antonia_html import AntoniaHtmlRenderer
from specir.visual.renderers.class_diagram import render_mermaid_class, render_plantuml_class
from specir.visual.renderers.d2 import D2Renderer
from specir.visual.renderers.mermaid import MermaidRenderer
from specir.visual.renderers.plantuml import PlantUMLRenderer
from specir.visual.renderers.view_mermaid import view_to_mermaid
from specir.visual.spec_models import ClassDiagram

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_parity  # noqa: E402

CORPUS = Path(__file__).resolve().parent / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLE = CORPUS / "examples" / "class" / "runtime.yml"
PACKAGES = FIXTURES / "class.packages.yml"
LANES = FIXTURES / "activity.lanes.yml"
NESTED = FIXTURES / "deployment.nested.yml"
requires_mmdc = pytest.mark.skipif(mmdc_path() is None, reason="mmdc (mermaid-cli) not installed")


def _valid_ir(path: Path):
    diagram = load(path)
    validate(diagram)
    return compile_ir(diagram)


# ── tests/test_class_diagram.py ─────────────────────────────────────────────────────────────────


def test_schema_and_compiler_preserve_structured_signatures():
    from specir.visual.schema import json_schema

    ir = _valid_ir(EXAMPLE)
    assert isinstance(ir, ClassIR)
    method = ir.classes[0].methods[0]
    assert method.name == "execute"
    assert [(p.name, p.type) for p in method.parameters] == [("context", "ExecutionContext"), ("input", "PortValues")]
    assert method.returns == "ExecutionResult"
    assert ir.classes[1].attributes[0].visibility == "private"
    assert ir.relations[1].to_multiplicity == "1"
    schema = json_schema("class")
    assert schema["properties"]["type"]["const"] == "class"
    assert schema["$defs"]["ClassMethod"]["additionalProperties"] is False
    assert "class" in json_schema()["discriminator"]["mapping"]


def test_backends_preserve_realization_direction_and_generic_types():
    ir = compile_ir(load(EXAMPLE))
    mermaid = render(ir)
    plantuml = render(ir, "plantuml")
    assert mermaid.startswith("classDiagram")
    assert "DataNode ..|> ExecutableNode" in mermaid
    assert "DataNode ..|> ExecutableNode" in plantuml
    assert "+List~InputPort~ inputs" in mermaid
    assert "+inputs: List<InputPort>" in plantuml
    assert "+execute(context: ExecutionContext, input: PortValues)* ExecutionResult" in mermaid
    assert "{abstract} +execute(context: ExecutionContext, input: PortValues): ExecutionResult" in plantuml


def test_cli_schema_validate_and_render(tmp_path, monkeypatch):
    """`test_cli_schema_validate_render_and_catalog` without its `catalog build` step (IR13b)."""
    from click.testing import CliRunner

    from specir.cli import main

    monkeypatch.setenv("SPECIR_MMDC", "0")
    runner = CliRunner()
    for args in [
        ["diagram", "schema", "--type", "class", "--out", str(tmp_path / "class.schema.json")],
        ["diagram", "validate", str(EXAMPLE)],
        ["diagram", "render", str(EXAMPLE), "--out", str(tmp_path)],
        ["diagram", "render", str(EXAMPLE), "--backend", "plantuml", "--out", str(tmp_path)],
    ]:
        result = runner.invoke(main, args)
        assert result.exit_code == 0, result.output
    assert (tmp_path / "runtime.mmd").exists()
    assert (tmp_path / "runtime.puml").exists()


@requires_mmdc
def test_real_mermaid_engine_accepts_members_kinds_and_all_relations():
    data = yaml.safe_load(EXAMPLE.read_text())
    data["data"]["classes"]["DataNode"]["attributes"].append(
        {"name": "instances", "type": "Integer", "static": True, "visibility": "protected"})
    data["data"]["classes"]["DataNode"]["methods"].append(
        {"name": "create", "static": True, "returns": "DataNode", "visibility": "package"})
    for kind in ["class", "interface", "abstract", "record", "protocol", "enum"]:
        data["data"]["classes"][f"Kind_{kind}"] = {"kind": kind}
    for relation in ["inheritance", "composition", "aggregation", "association", "dependency"]:
        edge = {"from": "DataNode", "to": "NodeSpec", "relation": relation, "label": "contract & data"}
        if relation != "inheritance":
            edge.update(from_multiplicity="1", to_multiplicity="0..*")
        data["data"]["relations"].append(edge)
    diagram = ClassDiagram.model_validate(data)
    validate(diagram)
    assert lint_mermaid(render(compile_ir(diagram))) == []


# ── tests/test_class_packages.py ────────────────────────────────────────────────────────────────


def test_mermaid_namespaces_by_path_and_colors_classes_by_package_kind():
    out = render_mermaid_class(_valid_ir(PACKAGES))
    lines = [l.strip() for l in out.splitlines()]
    assert "namespace Core.Billing {" in lines and "namespace Core.Identity {" in lines and "namespace Shared {" in lines
    assert "namespace Core {" not in lines  # sin clases propias, el paquete raiz no abre namespace vacio
    assert "classDef pkg0 fill:#fff1c2,stroke:#7a5c00" in lines and 'cssClass "Invoice,Payment" pkg0' in lines
    assert "classDef pkg1 fill:#dbebf4,stroke:#0072b2" in lines and 'cssClass "User" pkg1' in lines
    assert not any("AuditLog" in l for l in lines if l.startswith("cssClass"))


def test_plantuml_nests_packages_with_their_fill():
    out = render_plantuml_class(_valid_ir(PACKAGES))
    assert 'package "Core" as core {\n    package "Billing" as billing #fff1c2 {\n        class "Invoice" as Invoice {' in out
    assert 'package "Shared" as shared {' in out


def test_without_packages_the_output_is_unchanged():
    diagram = load(PACKAGES)
    diagram.data.packages = {}
    diagram.style = None
    out = render_mermaid_class(compile_ir(diagram))
    assert "namespace" not in out and "classDef" not in out


@pytest.mark.skipif(shutil.which("mmdc") is None, reason="mmdc not installed")
def test_real_mermaid_engine_accepts_the_packages(tmp_path):
    source = tmp_path / "p.mmd"
    source.write_text(render_mermaid_class(_valid_ir(PACKAGES)), encoding="utf-8")
    result = subprocess.run(["mmdc", "-i", str(source), "-o", str(tmp_path / "p.svg"), "-q"], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr[-400:]


# ── tests/test_activity_lanes.py ────────────────────────────────────────────────────────────────


def test_mermaid_draws_one_lane_per_partition_merge_as_diamond_and_notes():
    out = MermaidRenderer().render(_valid_ir(LANES))
    lanes = [l.strip() for l in out.splitlines() if l.strip().startswith("subgraph")]
    assert lanes == ['subgraph __lane0 ["Dev"]', 'subgraph __lane1 ["Approver"]', 'subgraph __lane2 ["Script"]', 'subgraph __lane3 ["AWS"]']
    assert 'joined{" "}' in out and 'review{"Approve?"}' in out
    assert 'review__note["Two approvals for production"]:::note' in out and "review -.- review__note" in out
    assert "classDef note" in out


def test_mermaid_without_the_new_fields_is_unchanged():
    out = MermaidRenderer().render(_valid_ir(FIXTURES / "activity.validation.yml"))
    assert "subgraph" not in out and "note" not in out
    assert out.splitlines()[:8] == ["---", "config:", "  layout: elk", "  flowchart:", "    curve: linear", "---", "flowchart TD", "    __start([Start])"]


def test_plantuml_swimlanes_and_note():
    out = PlantUMLRenderer().render(_valid_ir(LANES))
    lines = out.splitlines()
    assert lines[:3] == ["@startuml", "|Dev|", "start"]
    assert "|Approver|" in lines and "note right: Two approvals for production" not in lines  # la nota es de una decision
    assert "|Script|" in lines


def test_plantuml_note_on_an_action():
    diagram = load(LANES)
    diagram.data.steps["deploy"].notes = "Blue/green"
    out = PlantUMLRenderer().render(compile_ir(diagram))
    assert ":Deploy;\nnote right: Blue/green" in out


def test_d2_lanes_are_containers_and_edges_use_qualified_ids():
    out = D2Renderer().render(_valid_ir(LANES))
    assert '__lane0: "Dev"' in out and '__lane0.open_pr: "Open pull request"' in out
    assert "__lane2.joined.shape: diamond" in out and "__lane0.open_pr -> __lane1.review" in out
    assert "__lane1.review__note.shape: page" in out


# ── tests/test_deployment_nested.py ─────────────────────────────────────────────────────────────


def test_mermaid_nests_subgraphs_and_marks_deploy_and_manifest():
    out = MermaidRenderer().render(_valid_ir(NESTED))
    lines = out.splitlines()
    order = [l.strip() for l in lines if l.strip().startswith("subgraph")]
    assert order == ['subgraph vpc ["VPC"]', 'subgraph subnet ["Private subnet"]', 'subgraph cluster ["ECS cluster"]', 'subgraph db ["Postgres"]', 'subgraph edge ["CDN"]']
    assert '            subgraph cluster ["ECS cluster"]' in lines and '                api_service["api service"]' in lines
    assert '    cluster -->|"queries · :5432"| db' in lines and '    edge -->|"HTTPS"| cluster' in lines
    assert '    api_image -.->|"«deploy»"| cluster' in lines and '    api_image -.->|"«manifest»"| api_service' in lines


def test_plantuml_and_d2_nest_and_d2_edges_use_container_paths():
    puml = PlantUMLRenderer().render(_valid_ir(NESTED))
    assert 'node "VPC" as vpc {\n  node "Private subnet" as subnet {\n    node "ECS cluster" as cluster {' in puml
    assert "api_image ..> cluster : «deploy»" in puml
    d2 = D2Renderer().render(_valid_ir(NESTED))
    assert 'vpc.subnet.cluster.api_service: "api service"' in d2
    assert 'edge -> vpc.subnet.cluster: "HTTPS"' in d2 and "api_image -> vpc.subnet.cluster: \"«deploy»\" {style.stroke-dash: 3}" in d2


def test_antonia_html_draws_every_connection_of_a_deployment():
    ir = _valid_ir(NESTED)
    page = AntoniaHtmlRenderer().render(ir)
    source = _html.unescape(re.search(r'<pre class="mermaid">(.*?)</pre>', page, re.S).group(1))
    expected = MermaidRenderer().render(ir)
    assert source.strip() == expected.strip()
    arrows = [l for l in source.splitlines() if re.search(r"\s(-->|-\.->)", l)]
    connections = yaml.safe_load(NESTED.read_text(encoding="utf-8"))["data"]["connections"]
    assert len(arrows) == len(connections) > 0


# ── tests/test_catalog_resolved_views.py (view_to_mermaid) ──────────────────────────────────────

NOTATION = {
    "name": "infra-own", "title": "Infra", "diagram_type": "deployment", "layout": {"kind": "graph", "direction": "LR"},
    "glyphs": [
        {"id": "db", "model": "SpecNodeDoc", "where": 'kind = "database"', "shape": "cylinder", "keyword": "«{kind}»", "fill": {"light": "#fff1c2", "dark": "#3d3200"}},
        {"id": "node", "model": "SpecNodeDoc", "where": 'collection = "nodes"', "shape": "node-box", "keyword": "«node»"},
        {"id": "any", "model": "SpecNodeDoc", "shape": "rounded-box"},
    ],
    "links": [
        {"id": "contains", "relation": "contains", "draw": "nest"},
        {"id": "deploy", "relation": "deploy", "line": "dashed", "label": "«deploy»"},
        {"id": "any", "relation": "*", "color": "#0072b2", "target_end": "none", "label": "{data.protocol}"},
    ],
}


def resolved_view(tmp_path: Path, spec: Path = NESTED, notation: Path | None = None) -> dict:
    """The view sldb resolves for `spec` once sldb's SpecSync wrote it into a fresh store."""
    import sldb.api as sldb_api
    from sldb.api.notations import SpecSync, resolve_view

    root = tmp_path / "scratch"
    sldb_api.init_store(root)
    (root / "docs").mkdir()
    copy = Path(shutil.copy(spec, root / "docs" / spec.name))
    report = SpecSync(root / ".sldb").sync(copy, notation=notation)
    return resolve_view(root / ".sldb", report.spec_id)


def _notation(tmp_path: Path) -> Path:
    path = tmp_path / "infra-own.yml"
    path.write_text(yaml.safe_dump(NOTATION, allow_unicode=True), encoding="utf-8")
    return path


def test_view_to_mermaid_uses_glyph_shape_keyword_style_nesting_and_links(tmp_path):
    out = view_to_mermaid(resolved_view(tmp_path, notation=_notation(tmp_path)), theme="dark")
    lines = [l.strip() for l in out.splitlines()]
    assert out.startswith("---\nconfig:\n  layout: elk\n") and "flowchart LR" in lines
    assert any(l.startswith("subgraph ") and "«node»<br/>VPC" in l for l in lines)
    assert any('[("«database»<br/>Postgres")]' in l for l in lines)
    assert any(l.startswith("style ") and "fill:#3d3200" in l and "color:#e6edf3" in l for l in lines)
    assert any(l.startswith("linkStyle ") and "stroke:#0072b2" in l for l in lines)
    assert any("-.->|\"«deploy»\"|" in l for l in lines) and any("---|\"HTTPS\"|" in l for l in lines)


def test_view_to_mermaid_compartments_and_pseudonodes(tmp_path):
    klass = view_to_mermaid(resolved_view(tmp_path, PACKAGES))
    assert "<hr/>id: int<br/>total: Decimal" in klass and "@{ shape: notch-rect" not in klass
    act = view_to_mermaid(resolved_view(tmp_path / "a", LANES))
    assert "@{ shape: sm-circ }" in act and "@{ shape: fr-circ }" in act and '{" "}' in act


def test_view_to_mermaid_refuses_non_graph_layouts(tmp_path):
    view = resolved_view(tmp_path, CORPUS / "docs" / "architecture" / "spec2viz" / "sequence-sync-pipeline.yml")
    with pytest.raises(ValueError, match="not a graph"):
        view_to_mermaid(view)


@requires_mmdc
def test_view_to_mermaid_is_accepted_by_the_real_engine(tmp_path):
    for name, spec in (("dep", NESTED), ("cls", PACKAGES), ("act", LANES)):
        source = tmp_path / f"{name}.mmd"
        source.write_text(view_to_mermaid(resolved_view(tmp_path / name, spec, _notation(tmp_path) if name == "dep" else None)), encoding="utf-8")
        result = subprocess.run(["mmdc", "-i", str(source), "-o", str(tmp_path / f"{name}.svg"), "-q"], capture_output=True, text=True, timeout=120)
        assert result.returncode == 0, (name, result.stderr[-300:])


@pytest.mark.parity
@pytest.mark.parametrize("spec, own_notation", [(NESTED, True), (NESTED, False), (PACKAGES, False), (LANES, False)])
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_view_to_mermaid_matches_spec2viz_on_the_same_resolved_view(tmp_path, spec, own_notation, theme):
    pytest.importorskip("spec2viz")
    view = resolved_view(tmp_path, spec, _notation(tmp_path) if own_notation else None)
    assert view_to_mermaid(view, theme=theme) == render_parity.spec2viz_view_to_mermaid(view, theme)


# ── tests/test_exceptions.py (the visual layer's errors) ────────────────────────────────────────


def test_exception_hierarchy():
    assert issubclass(CompileError, Spec2VizError)
    assert issubclass(RenderError, Spec2VizError)
    assert issubclass(MermaidLintError, RenderError)


def test_exceptions_are_catchable_as_base():
    with pytest.raises(Spec2VizError):
        raise RenderError("cannot render")

FILE:tests/visual/test_bpmn.py
"""BPMN renderer: XML structure, DI coverage and the offline bpmn-js viewer page.

`tests/test_bpmn.py` of spec2viz (revision 2de1056) ported case by case to specIR (SV-C06 to SV-C08),
over the same fixtures (`fixtures/spec2viz/`), loading with sldb (`load_spec`, D3). The two cases
that checked the activity model (`tone`, groups and detail) go through sldb's `load_spec` on a spec
file, since the model is sldb's; the CLI cases run specIR's `diagram render`."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner
from sldb.api.notations import load_spec as load

from specir.cli import main
from specir.visual.compilers import compile_ir
from specir.visual.exceptions import RenderError
from specir.visual.ir import ActivityGroup, ActivityIR, ActivityStep, ComponentIR
from specir.visual.render_file import render_to_file
from specir.visual.renderers import render
from specir.visual.renderers.bpmn import BpmnRenderer, render_bpmn_html

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "spec2viz" / "tests" / "fixtures"
NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}
NODE_TAGS = ("startEvent", "endEvent", "task", "exclusiveGateway")


def _parse(xml: str) -> ET.Element:
    return ET.fromstring(xml.encode("utf-8"))


def _check_structure(root: ET.Element) -> dict[str, int]:
    """Common invariants; returns the element counts."""
    assert root.tag == f"{{{NS['bpmn']}}}definitions"
    processes = root.findall("bpmn:process", NS)
    assert len(processes) == 1
    proc = processes[0]
    nodes = {el.get("id"): el for tag in NODE_TAGS for el in proc.findall(f"bpmn:{tag}", NS)}
    flows = proc.findall("bpmn:sequenceFlow", NS)
    ids = [el.get("id") for el in proc] + [proc.get("id")]
    assert len(ids) == len(set(ids)), "ids must be unique"
    for f in flows:
        assert f.get("sourceRef") in nodes and f.get("targetRef") in nodes
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    assert plane.get("bpmnElement") == proc.get("id")
    shapes = {s.get("bpmnElement"): s for s in plane.findall("bpmndi:BPMNShape", NS)}
    edges = {e.get("bpmnElement"): e for e in plane.findall("bpmndi:BPMNEdge", NS)}
    assert set(shapes) == set(nodes), "every node has exactly one DI shape"
    assert set(edges) == {f.get("id") for f in flows}, "every flow has exactly one DI edge"
    for s in shapes.values():
        b = s.find("dc:Bounds", NS)
        assert int(b.get("width")) > 0 and int(b.get("height")) > 0
    for e in edges.values():
        pts = [(int(w.get("x")), int(w.get("y"))) for w in e.findall("di:waypoint", NS)]
        assert len(pts) >= 2
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            assert x0 == x1 or y0 == y1, "waypoints are orthogonal"
    # no two shapes overlap
    boxes = [tuple(int(s.find("dc:Bounds", NS).get(k)) for k in ("x", "y", "width", "height")) for s in shapes.values()]
    for i, (x, y, w, h) in enumerate(boxes):
        for (x2, y2, w2, h2) in boxes[i + 1:]:
            assert x + w <= x2 or x2 + w2 <= x or y + h <= y2 or y2 + h2 <= y
    return {
        **{tag: len(proc.findall(f"bpmn:{tag}", NS)) for tag in NODE_TAGS},
        "sequenceFlow": len(flows),
    }


def test_small_activity_counts():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    root = _parse(xml)
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 4, "exclusiveGateway": 1, "sequenceFlow": 7}
    proc = root.find("bpmn:process", NS)
    gw = proc.find("bpmn:exclusiveGateway", NS)
    assert gw.get("id") == "Gateway_check_validity"
    assert gw.get("name") == "Is quotation valid?"
    names = {f.get("name") for f in proc.findall("bpmn:sequenceFlow", NS) if f.get("sourceRef") == gw.get("id")}
    assert names == {"yes", "no"}


def test_mepu_decision_example_counts():
    xml = render(compile_ir(load(FIXTURES / "activity.mepu-decision.yml")), "bpmn")
    root = _parse(xml)
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 12, "exclusiveGateway": 5, "sequenceFlow": 28}
    proc = root.find("bpmn:process", NS)
    # two branches of r5 go to the same step: two distinct flows with distinct paths
    to_peor = [f for f in proc.findall("bpmn:sequenceFlow", NS)
               if (f.get("sourceRef"), f.get("targetRef")) == ("Gateway_r5", "Task_peor")]
    assert len(to_peor) == 2
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    paths = [
        [(w.get("x"), w.get("y")) for w in plane.find(f"bpmndi:BPMNEdge[@bpmnElement='{f.get('id')}']", NS)
         .findall("di:waypoint", NS)]
        for f in to_peor
    ]
    assert paths[0] != paths[1]


def test_layout_is_deterministic_and_left_to_right():
    ir = compile_ir(load(FIXTURES / "activity.mepu-decision.yml"))
    a, b = render(ir, "bpmn"), render(ir, "bpmn")
    assert a == b
    root = _parse(a)
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    x = {s.get("bpmnElement"): int(s.find("dc:Bounds", NS).get("x")) for s in plane.findall("bpmndi:BPMNShape", NS)}
    for f in root.find("bpmn:process", NS).findall("bpmn:sequenceFlow", NS):
        assert x[f.get("sourceRef")] < x[f.get("targetRef")]


def _ir(steps, start="a", end="end"):
    return ActivityIR(title="T", start=start, steps=steps, end=end)


def test_cycles_terminal_steps_and_escaping():
    steps = [
        ActivityStep(id="a", label='Load <data> & "quote"', next="b?"),
        ActivityStep(id="b?", label="Valid?", kind="decision", branches={"retry <x>": "a", "ok": "done", "drop": "dead"}),
        ActivityStep(id="done", label="Done", next="end"),
        ActivityStep(id="dead", label="Dead end, no next"),  # terminal: flows to the end event
    ]
    xml = BpmnRenderer().render(_ir(steps))
    root = _parse(xml)
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 3, "exclusiveGateway": 1, "sequenceFlow": 7}
    proc = root.find("bpmn:process", NS)
    assert proc.find("bpmn:task[@id='Task_a']", NS).get("name") == 'Load <data> & "quote"'
    assert proc.find("bpmn:exclusiveGateway", NS).get("id") == "Gateway_b_"
    assert "&lt;data&gt; &amp;" in xml
    ends = [f for f in proc.findall("bpmn:sequenceFlow", NS) if f.get("targetRef").startswith("EndEvent_")]
    assert {f.get("sourceRef") for f in ends} == {"Task_done", "Task_dead"}


def test_end_that_is_also_a_step_and_id_collisions():
    steps = [
        ActivityStep(id="a b", label="A", next="a_b"),
        ActivityStep(id="a_b", label="A2", next="fin"),
        ActivityStep(id="fin", label="Finish"),
    ]
    root = _parse(BpmnRenderer().render(_ir(steps, start="a b", end="fin")))
    counts = _check_structure(root)
    assert counts["task"] == 3 and counts["endEvent"] == 1


def test_rejects_other_ir():
    with pytest.raises(RenderError):
        BpmnRenderer().render(ComponentIR(title="x", nodes=[], edges=[]))


def test_viewer_html_inlines_bpmn_js_and_the_xml():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    page = render_bpmn_html(xml, "T <1>", {"description": "Desc & more", "preguntas_abiertas": ["¿Q1 <b>?"]})
    assert "bpmn-js - bpmn-navigated-viewer v" in page
    assert ".djs-container" in page  # diagram-js.css
    assert "new BpmnJS(" in page and "fit-viewport" in page
    # nothing is loaded from outside the file
    assert "<script src=" not in page and "<link" not in page
    assert not re.search(r"url\(['\"]?https?:|@import", page)
    assert "T &lt;1&gt;" in page and "Desc &amp; more" in page and "¿Q1 &lt;b&gt;?" in page
    literal = re.search(r"var xml = (\".*?\");\n", page, re.S).group(1)
    assert json.loads(literal) == xml
    assert "</bpmn:" not in page  # the XML is inside a JSON string with `<` escaped


def test_cli_render_writes_bpmn_and_html(tmp_path):
    result = CliRunner().invoke(
        main,
        ["diagram", "render", str(FIXTURES / "activity.mepu-decision.yml"), "--out", str(tmp_path), "--renderer", "bpmn"],
    )
    assert result.exit_code == 0, result.output
    bpmn = tmp_path / "activity.mepu-decision.bpmn"
    page = tmp_path / "activity.mepu-decision.bpmn.html"
    assert bpmn.exists() and page.exists()
    text = bpmn.read_text(encoding="utf-8")
    assert text.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<!-- specir: generated from')
    _check_structure(_parse(text))
    html = page.read_text(encoding="utf-8")
    assert "Preguntas abiertas" in html and "R2 parcial" in html
    assert "MEPU · Cómo se decide una línea" in html
    assert str(page) in result.output


def test_render_to_file_returns_the_bpmn_path(tmp_path):
    out = render_to_file(FIXTURES / "activity.complex.yml", out=tmp_path, renderer="bpmn")
    assert out.name == "activity.complex.bpmn"
    assert (tmp_path / "activity.complex.bpmn.html").exists()


COLOR_NS = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
COLOR = {"color": COLOR_NS}


def _shapes(xml: str) -> dict[str, ET.Element]:
    plane = _parse(xml).find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    return {s.get("bpmnElement"): s for s in plane.findall("bpmndi:BPMNShape", NS)}


def _edges(xml: str) -> dict[str, ET.Element]:
    plane = _parse(xml).find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    return {e.get("bpmnElement"): e for e in plane.findall("bpmndi:BPMNEdge", NS)}


def test_tones_emit_bpmn_in_color_attributes_and_namespace():
    steps = [
        ActivityStep(id="a", label="Prepare", tone="info", next="ok"),
        ActivityStep(id="ok", label="Accepted", tone="success", next="gate"),
        ActivityStep(id="gate", label="Decide", kind="decision", tone="rule2",
                     branches={"yes": "warn", "no": "bad"}),
        ActivityStep(id="warn", label="Review", tone="warning", next="end"),
        ActivityStep(id="bad", label="Rejected", tone="danger"),
        ActivityStep(id="plain", label="Neutral task", tone="neutral", next="end"),
    ]
    xml = BpmnRenderer().render(_ir(steps, start="a", end="end"))
    assert f'xmlns:color="{COLOR_NS}"' in xml
    shapes = _shapes(xml)
    assert shapes["Task_a"].get(f"{{{COLOR_NS}}}background-color") == "#E1EEFB"
    assert shapes["Task_a"].get(f"{{{COLOR_NS}}}border-color") == "#1D4ED8"
    assert shapes["Task_ok"].get(f"{{{COLOR_NS}}}background-color") == "#E3F4E6"
    assert shapes["Task_warn"].get(f"{{{COLOR_NS}}}border-color") == "#B26A00"
    assert shapes["Task_bad"].get(f"{{{COLOR_NS}}}border-color") == "#B42318"
    assert shapes["Task_plain"].get(f"{{{COLOR_NS}}}border-color") == "#6B7280"
    # the gateway carries its own tone; its outgoing flows take that border colour
    assert shapes["Gateway_gate"].get(f"{{{COLOR_NS}}}border-color") == "#C2410C"
    edges = _edges(xml)
    gw_flows = [e for name, e in edges.items() if name.startswith("Flow_gate__")]
    assert len(gw_flows) == 2
    assert all(e.get(f"{{{COLOR_NS}}}border-color") == "#C2410C" for e in gw_flows)
    # flows that do not leave a gateway stay unstyled
    assert edges["Flow_start__a"].get(f"{{{COLOR_NS}}}border-color") is None


def test_events_and_untinted_gateway_get_default_colors():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", next="d"),
        ActivityStep(id="d", label="Decide", kind="decision", branches={"x": "end"}),
    ], start="a"))
    shapes = _shapes(xml)
    start = next(v for k, v in shapes.items() if k.startswith("StartEvent_"))
    end = next(v for k, v in shapes.items() if k.startswith("EndEvent_"))
    assert start.get(f"{{{COLOR_NS}}}background-color") == "#E3F4E6"
    assert end.get(f"{{{COLOR_NS}}}border-color") == "#8B1A1A"
    assert shapes["Gateway_d"].get(f"{{{COLOR_NS}}}background-color") == "#F4F0FB"
    # a task without tone stays at the default BPMN white, no colour attributes
    assert shapes["Task_a"].get(f"{{{COLOR_NS}}}background-color") is None


def test_rule_tones_are_five_distinct_soft_colors():
    from specir.visual.renderers.bpmn import TONE_PALETTE

    rules = [TONE_PALETTE[f"rule{i}"] for i in range(1, 6)]
    assert len(set(rules)) == 5
    assert len({bg for bg, _ in TONE_PALETTE.values()}) == len(TONE_PALETTE)


def test_tasks_are_wrapped_and_sized_to_their_text():
    long_label = "Una línea de una OC abierta de Laboratorio Chile con un texto bastante largo que debe envolverse"
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="short", label="Do it", next="long"),
        ActivityStep(id="long", label=long_label, next="end"),
    ], start="short"))
    shapes = _shapes(xml)

    def bounds(nid):
        b = shapes[nid].find("dc:Bounds", NS)
        return int(b.get("width")), int(b.get("height"))

    w_short, h_short = bounds("Task_short")
    w_long, h_long = bounds("Task_long")
    assert w_long <= 240 and w_long >= 120
    assert h_long > h_short, "a long label grows the box in height instead of overflowing"
    assert w_short <= w_long
    assert h_short >= 60


def _column_gaps(xml: str) -> list[int]:
    """Horizontal space between consecutive columns: shapes plus their gateway labels."""
    plane = _parse(xml).find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    spans: list[tuple[int, int]] = []
    for shape in plane.findall("bpmndi:BPMNShape", NS):
        for bounds in shape.iter(f"{{{NS['dc']}}}Bounds"):
            x, w = int(bounds.get("x")), int(bounds.get("width"))
            spans.append((x, x + w))
    spans.sort()
    merged: list[list[int]] = []
    for a, b in spans:
        if merged and a < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    ends = [m[1] for m in merged]
    starts = [m[0] for m in merged[1:]]
    return [start - end for end, start in zip(ends, starts)]


def test_text_width_is_estimated_per_character_class():
    from specir.visual.renderers.bpmn import TASK_PAD, _task_box, _text_w, _wrap

    # uppercase, '_' and 'm'/'w' are wider than the old flat 7.7px, narrow signs are thinner
    assert _text_w("PARTIAL_STOCK") > len("PARTIAL_STOCK") * 7.7
    assert _text_w("mmmm") > _text_w("iiii")
    assert _text_w("...") < _text_w("III")
    # PARTIAL_STOCK (the label that used to break in two) fits on a single line
    w, _h = _task_box("PARTIAL_STOCK")
    assert w - TASK_PAD + 4 >= _text_w("PARTIAL_STOCK")
    assert _wrap("PARTIAL_STOCK", w - TASK_PAD + 4) == 1
    # even the widest label of the real specs stays whole inside its box
    w2, _h2 = _task_box("Revisar + RESERVA_INSTITUCIONAL · Customer Service")
    assert _wrap("RESERVA_INSTITUCIONAL", w2 - TASK_PAD + 4) == 1
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="Aceptar + PARTIAL_STOCK", next="end"),
    ], start="a"))
    bounds = _shapes(xml)["Task_a"].find("dc:Bounds", NS)
    assert int(bounds.get("width")) - TASK_PAD + 4 >= _text_w("PARTIAL_STOCK")


def test_column_gaps_shrink_without_labels_and_grow_with_the_longest_one():
    from specir.visual.renderers.bpmn import COL_GAP, MIN_COL_GAP, _text_w

    # a linear plan with no edge labels only pays the minimum gap at every column
    steps = [ActivityStep(id=f"s{i}", label=f"Paso {i}", next=f"s{i + 1}") for i in range(5)]
    steps.append(ActivityStep(id="s5", label="Fin del camino"))
    linear = _column_gaps(BpmnRenderer().render(_ir(steps, start="s0")))
    assert linear and all(gap == MIN_COL_GAP for gap in linear)

    # a labelled flow widens only the gap it crosses, up to the old COL_GAP ceiling
    label = "etiqueta de rama"
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", next="d"),
        ActivityStep(id="d", label="¿Sigue?", kind="decision", branches={label: "b", "no": "end"}),
        ActivityStep(id="b", label="B", next="end"),
    ], start="a"))
    gaps = _column_gaps(xml)
    assert int(min(COL_GAP, max(MIN_COL_GAP, _text_w(label) + 40))) in gaps
    assert MIN_COL_GAP in gaps and max(gaps) < COL_GAP
    long_label = "una etiqueta considerablemente mas larga que el hueco maximo permitido"
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", next="d"),
        ActivityStep(id="d", label="¿Sigue?", kind="decision", branches={long_label: "b", "no": "end"}),
        ActivityStep(id="b", label="B", next="end"),
    ], start="a"))
    assert max(_column_gaps(xml)) == COL_GAP


def _activity_spec(tmp_path: Path, data: dict) -> Path:
    spec = tmp_path / "activity.yml"
    spec.write_text(yaml.safe_dump({"id": "a", "title": "A", "type": "activity", "version": "1", "data": data}), encoding="utf-8")
    return spec


def test_tone_field_is_validated_by_the_model(tmp_path):
    """The step model is sldb's (D3): a step's `tone` is one of the palette's tones or nothing."""
    from sldb.api.notations import validate_spec

    steps = {"a": {"label": "x", "tone": "rule5", "next": "b"}, "b": {"label": "y", "next": "end"}}
    diagram = load(_activity_spec(tmp_path, {"start": "a", "end": "end", "steps": steps}))
    validate_spec(diagram)
    assert diagram.data.steps["a"].tone == "rule5" and diagram.data.steps["b"].tone is None
    steps["a"]["tone"] = "chartreuse"
    with pytest.raises(Exception, match="tone"):
        load(_activity_spec(tmp_path, {"start": "a", "end": "end", "steps": steps}))


def test_viewer_has_a_compact_header_full_height_canvas_and_collapsed_meta():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    page = render_bpmn_html(xml, "T", {"description": "Desc", "preguntas_abiertas": ["¿Q?"]})
    # title, buttons and legend stay in the bar; description and questions are collapsed
    assert "<details class=\"meta\">" in page and "<summary>Descripción y preguntas abiertas</summary>" in page
    assert " open" not in page.split("<details")[1].split(">")[0]
    assert 'class="legend"' in page and "white-space: nowrap" in page
    # the canvas takes whatever the bar leaves, on a full-viewport flex column
    assert "height: 100vh" in page and "flex-direction: column" in page
    assert "#canvas { flex: 1 1 auto" in page
    assert "<header>" in page


def test_viewer_font_size_and_initial_zoom():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    page = render_bpmn_html(xml, "T", None)
    assert "textRenderer" in page and "defaultStyle" in page and "externalStyle" in page
    assert "fontSize: 14" in page
    assert "MIN_ZOOM = 0.6" in page and "canvas.zoom(MIN_ZOOM)" in page
    # Fit really fits, it does not re-apply the minimum-zoom initial view
    assert "function fitViewport()" in page
    assert "document.getElementById('fit').addEventListener('click', fitViewport)" in page
    assert ".zoom('fit-viewport', 'auto')" in page
    assert "getAbsoluteBBox(start)" in page  # the initial view is anchored on the start event
    # entering a subprocess applies the same rule as the initial view
    assert "viewer.on('root.set', function () { try { initialView(); }" in page


def test_legend_shows_only_used_tones_with_generic_spanish_labels():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", tone="success", next="bad"),
        ActivityStep(id="bad", label="Bad", tone="danger", next="d"),
        ActivityStep(id="d", label="Decide", kind="decision", branches={"x": "end"}),
    ], start="a"))
    page = render_bpmn_html(xml, "T", None)
    assert ">favorable</span>" in page and ">rechazo</span>" in page
    assert ">gateway por defecto</span>" in page
    # start/end events never take a legend colour
    assert ">inicio</span>" not in page and ">fin</span>" not in page
    # unused tones are not in the legend
    for unused in ("atención", "informativo", "neutro", "regla 1", "regla 5"):
        assert f">{unused}</span>" not in page


def test_legend_reads_custom_labels_from_metadata():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", tone="rule2", next="ok"),
        ActivityStep(id="ok", label="OK", tone="success", next="end"),
    ], start="a"))
    page = render_bpmn_html(xml, "T", {"legend": {"rule2": "R2 · Stock", "success": "Aceptar"}})
    assert ">R2 · Stock</span>" in page and ">Aceptar</span>" in page
    assert ">regla 2</span>" not in page


def test_cli_render_takes_legend_and_questions_from_the_metadata_model(tmp_path):
    spec = tmp_path / "leyenda.yml"
    raw = yaml.safe_load((FIXTURES / "activity.mepu-decision.yml").read_text(encoding="utf-8"))
    raw["metadata"]["preguntas_abiertas"] = "¿Una sola pregunta?"
    raw["metadata"]["legend"] = {"gateway": "Decisión de negocio"}
    spec.write_text(yaml.safe_dump(raw, allow_unicode=True, sort_keys=False), encoding="utf-8")
    result = CliRunner().invoke(main, ["diagram", "render", str(spec), "--out", str(tmp_path), "--renderer", "bpmn"])
    assert result.exit_code == 0, result.output
    page = (tmp_path / "leyenda.bpmn.html").read_text(encoding="utf-8")
    assert "<li>¿Una sola pregunta?</li>" in page and ">Decisión de negocio</span>" in page


def _group_ir() -> ActivityIR:
    return ActivityIR(
        title="Grupos", start="a", end="e",
        steps=[
            ActivityStep(id="a", label="Entrada", group="g1", detail="Texto largo de a.", next="b"),
            ActivityStep(id="b", label="¿Sigue?", kind="decision", group="g1",
                         branches={"ok": "c", "no": "x"}),
            ActivityStep(id="c", label="Cierre interno", group="g1", next="d"),
            ActivityStep(id="x", label="Afuera", next="d"),
            ActivityStep(id="d", label="Evaluar", group="g2", next="e"),
            ActivityStep(id="e", label="Fin del grupo", group="g2"),
        ],
        groups={
            "g1": ActivityGroup(id="g1", label="Grupo uno", tone="info", detail="Detalle del grupo uno."),
            "g2": ActivityGroup(id="g2", label="Grupo dos", tone="warning", detail="Detalle del grupo dos."),
        },
    )


def test_groups_are_collapsed_subprocesses_with_their_own_planes():
    from specir.visual.renderers.bpmn import TONE_PALETTE

    root = _parse(BpmnRenderer().render(_group_ir()))
    proc = root.find("bpmn:process", NS)
    subs = {el.get("id"): el for el in proc.findall("bpmn:subProcess", NS)}
    assert set(subs) == {"SubProcess_g1", "SubProcess_g2"}
    assert subs["SubProcess_g1"].get("name") == "Grupo uno"
    planes = {p.get("bpmnElement"): p for p in root.findall("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)}
    assert set(planes) == {"Process_1", "SubProcess_g1", "SubProcess_g2"}
    top_shapes = {s.get("bpmnElement"): s for s in planes["Process_1"].findall("bpmndi:BPMNShape", NS)}
    for sid in subs:
        assert top_shapes[sid].get("isExpanded") == "false"
        assert top_shapes[sid].get(f"{{{COLOR_NS}}}background-color") in {
            background for background, _ in TONE_PALETTE.values()
        }
    # ids are unique across every plane
    ids = [el.get("id") for el in root.iter() if el.get("id")]
    assert len(ids) == len(set(ids))
    # each subprocess plane has its own start, its steps and its external end events
    g1 = planes["SubProcess_g1"]
    g1_nodes = [el.get("bpmnElement") for el in g1.findall("bpmndi:BPMNShape", NS)]
    assert {"StartEvent_g1__in", "Task_a", "Gateway_b", "Task_c"} <= set(g1_nodes)
    g1_ends = {el.get("bpmnElement") for el in g1.findall("bpmndi:BPMNShape", NS)
               if el.get("bpmnElement", "").startswith("EndEvent_g1__")}
    assert len(g1_ends) == 2  # one per distinct external destination (step x, group g2)
    g1_flows = g1.findall("bpmndi:BPMNEdge", NS)
    assert len(g1_flows) == 5
    g2 = planes["SubProcess_g2"]
    g2_ends = [el.get("bpmnElement") for el in g2.findall("bpmndi:BPMNShape", NS)
               if el.get("bpmnElement", "").startswith("EndEvent_g2__")]
    assert len(g2_ends) == 1  # terminal step e exits to the process end
    # top level: flows enter the subprocess and leave it toward the real destinations
    top_flows = proc.findall("bpmn:sequenceFlow", NS)
    assert {(f.get("sourceRef"), f.get("targetRef")) for f in top_flows} == {
        ("StartEvent_a", "SubProcess_g1"),
        ("SubProcess_g1", "Task_x"),
        ("SubProcess_g1", "SubProcess_g2"),
        ("Task_x", "SubProcess_g2"),
        ("SubProcess_g2", "EndEvent_e"),
    }
    labels = {f.get("name") for f in top_flows if f.get("sourceRef") == "SubProcess_g1"}
    assert labels == {"Afuera", "Grupo dos"}
    # the inner flows reach those end events
    inner = {(f.get("sourceRef"), f.get("targetRef")) for f in subs["SubProcess_g1"].findall("bpmn:sequenceFlow", NS)}
    assert ("Gateway_b", "Task_c") in inner and ("Task_c", "EndEvent_g1__g2") in inner


def test_group_and_step_detail_reach_the_viewer_json():
    xml = BpmnRenderer().render(_group_ir())
    page = render_bpmn_html(xml, "T", None)
    literal = re.search(r"var info = (\{.*?\});\n", page, re.S).group(1)
    info = json.loads(literal)
    assert info["Task_a"]["detail"] == "Texto largo de a."
    assert info["SubProcess_g1"]["detail"] == "Detalle del grupo uno."
    assert info["SubProcess_g1"]["label"] == "Grupo uno"
    assert info["SubProcess_g1"]["subprocess"] is True
    assert info["Gateway_b"]["branches"] == [
        {"label": "ok", "target": "Cierre interno"},
        {"label": "no", "target": "Afuera"},
    ]
    assert "id=\"panel\"" in page and "340px" in page and "toggle-panel" in page


def test_spec_without_groups_produces_one_plane_and_no_subprocess():
    xml = render(compile_ir(load(FIXTURES / "activity.mepu-decision.yml")), "bpmn")
    root = _parse(xml)
    assert root.findall(".//bpmn:subProcess", NS) == []
    assert len(root.findall("bpmndi:BPMNDiagram", NS)) == 1
    _check_structure(root)


def test_other_renderers_accept_groups_and_detail():
    ir = compile_ir(load(FIXTURES / "activity.groups.yml"))
    for name in ("mermaid", "plantuml", "d2"):
        assert render(ir, name)


def test_model_validates_groups_and_detail(tmp_path):
    """The step and group models are sldb's (D3)."""
    from sldb.api.notations import validate_spec

    groups = {"g": {"label": "G", "tone": "info", "detail": "GD"}}
    data = {"start": "a", "end": "end", "steps": {"a": {"label": "A", "detail": "D", "group": "g", "next": "end"}}, "groups": groups}
    diagram = load(_activity_spec(tmp_path, data))
    validate_spec(diagram)
    step = diagram.data.steps["a"]
    assert step.detail == "D" and step.group == "g"
    assert diagram.data.groups["g"].label == "G"
    data["steps"]["a"]["group"] = "missing"
    with pytest.raises(Exception, match="unknown group 'missing'"):
        validate_spec(load(_activity_spec(tmp_path, data)))

FILE:instruccion
Cold-bundle de la tarea task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Cada comando y subgrupo que lista la ayuda de spec2viz tiene una fila en la tabla de correspondencia con su equivalente en specIR, y una prueba invoca cada equivalente.
- Las pruebas de API de spec2viz portadas pasan contra la API pública de specIR.
- La habilidad de agente nombra solo comandos que existen en el comando de specIR (comprobado por una prueba que los extrae y los invoca con ayuda).
- El paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado.

