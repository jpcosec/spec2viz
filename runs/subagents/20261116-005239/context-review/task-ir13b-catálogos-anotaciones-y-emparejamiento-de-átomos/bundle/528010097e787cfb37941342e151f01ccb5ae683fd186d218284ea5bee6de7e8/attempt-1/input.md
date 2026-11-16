FILE:desk/tasks/task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos.md
---
sldb:
  by: agent
  at: '2026-11-16T00:52:18Z'
  authority: generated
  via: save_document_payload
id: task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos
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
- task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz
- task-espejo-sldb-emparejamiento-de-átomos-en-sldb-api-matching-d4
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/visual/catalog/__init__.py
- src/specir/visual/catalog/loader.py
- src/specir/visual/catalog/sections.py
- src/specir/visual/catalog/views.py
- src/specir/visual/catalog/fragments.py
- src/specir/visual/catalog/atoms.py
- src/specir/visual/catalog/annotations.py
- src/specir/visual/catalog/build.py
- src/specir/visual/templates/annotations-sldb.js
- src/specir/visual/notation_style.py
- src/specir/visual/__init__.py
- tests/visual/test_catalog.py
- tests/visual/test_catalog_parity.py
- tests/visual/test_catalog_annotations.py
- tests/test_imports.py
- tests/visual/test_visual_names.py
- tests/visual/test_resources.py
- docs/spec2viz/matriz-de-cobertura.md
- pyproject.toml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13b Catálogos, anotaciones y emparejamiento de átomos

## Rationale

_Explain why this task exists or the business driver behind it._

Parte de la migración final de spec2viz, separada de IR13 para que cada tarea tenga un solo entregable. El catálogo es la forma en que los repos publican y navegan sus diagramas junto con los átomos que los explican.

## Goal

_Describe the concrete result this task must produce._

specIR construye, sincroniza, valida y sirve catálogos de diagramas con anotaciones, y empareja átomos con elementos de diagrama usando sldb.api.matching (D4); el catálogo se sirve con sldb serve si alcanza. specIR conserva solo la parte visual del catálogo.

## Scope

_State what is in scope and what is out of scope._

Dentro: registro de vistas (vistas.yml) y stores jerárquicos de diagramas; construcción del catálogo HTML autocontenido con los renderers de IR12; sincronización y validación del catálogo; emparejamiento de átomos con elementos de diagrama (explícito y difuso) y cobertura por vista llamando a sldb.api.matching (D4); servicio del catálogo y autoguardado de anotaciones con sldb serve; si sldb serve no alcanza para las anotaciones, se pide por el desk de sldb y solo queda en specIR lo que sea visual. Fuera: implementar el emparejamiento en specIR (se migra a sldb, tarea espejo D4); sincronización de un spec individual; notaciones y paletas, que se usan desde sldb; CLI; migración de consumidores.

## Implementation Path

_Outline the expected implementation route or affected surface._

Capa delgada en el paquete specIR (specir.visual) sobre la sincronización de IR13a, los renderers de IR12, sldb.api.matching y sldb serve. Paridad medida con pruebas de specIR que comparan con las de spec2viz de catálogo, rutas de catálogo, vistas resueltas y emparejamiento de átomos como oráculo de desarrollo. Depende de la tarea espejo D4.

Precisiones (preflight):

1. «Alcanza»: D4 comprobó que `sldb serve` lee un documento por id (`GET /document?id=`) y lo escribe con guarda optimista (`POST /save` con `changes[].expected` igual al payload leído; 409 si cambió). Eso alcanza para el autoguardado: specIR no levanta servidor propio. El catálogo HTML se abre como archivo y su JS habla con `sldb serve --cors`.
2. Pedido a sldb: no hace falta para el servidor. Cualquier carencia que aparezca (por ejemplo nombres que `sldb.api` no exporta) se envía con `deskops message send --to sldb` y se cita en el informe de la tarea.
3. Límite visual. Quedan en specIR: el cargador del registro de vistas y de los stores jerárquicos (vistas, categorías, anchors, tags, `project.yml`), el HTML del catálogo (secciones, navegación, filtros, tableros desde la vista resuelta con el `view_mermaid` de IR12), el adaptador de una vista del catálogo a `SpecView` con el descubrimiento del store de la vista, la inyección de átomos en el HTML (`split_shared_atoms`), el modelo del store que guarda las anotaciones de un catálogo y el JS que las guarda en `sldb serve`. Se usan de sldb, sin envoltorio: la regla de rutas (`sldb.api.notations.catalog_paths`), `check_catalog`, `sync_catalog` y `sldb notations sync --catalog [--check]`, `resolve_view`, `SpecSync` y todo `sldb.api.matching`.
4. «Mismos errores tipados»: por cada entrada que devuelve `check_catalog`, la vista, el spec, el nombre de la clase de la excepción y su mensaje, comparados con `check_catalog` de spec2viz sobre los registros de las pruebas de rutas y notaciones de catálogo de spec2viz y sobre su propio registro de arquitectura (el vistas.yml de su carpeta de documentación).
5. «Mismo contenido» y «mismas vistas»: en el store, los documentos (modelo, nombre y payload) normalizados como en IR13a. En el catálogo, extraídos del HTML: secciones (anchor, id de vista, título, categoría, tipo, proyecto y tags, en orden), bloques de categoría, enlaces de navegación (href y texto, en orden), filtros y tableros. En los átomos, `ATOMS_DB`, `ATOMS_BY_VIEW`, `ATOMS_EXPLICIT`, `ATOMS_LINKED`, `REFS_EXPLICIT` y `COVERAGE_BY_VIEW` iguales como JSON.
6. Modo estricto: el parámetro `strict_atoms` de la construcción del catálogo (el `--strict-atoms` de spec2viz), que lanza `UnknownAtomError` de sldb. Sin él, el aviso queda en el HTML y en stderr.
7. Matriz: `docs/spec2viz/matriz-de-cobertura.md`, filas SV-G01 a SV-G08 y SV-I01 a SV-I05. IR13b cita en ellas sus pruebas sin marcarlas cumplidas; eso lo hace IR13. La CLI (`catalog build`, el alias `build` y lo que reemplaza a `catalog serve`) es de IR13d: los casos de build del módulo de pruebas test_cli de spec2viz se portan sobre la API de specIR.

## Validation

_List the checks required before this task can close._

- La validación de un registro de vistas reporta en specIR los mismos errores tipados que spec2viz sobre los fixtures de catálogo.
- La sincronización del catálogo deja en un store de prueba el mismo contenido que spec2viz, y no escribe nada si alguna vista falla.
- El catálogo construido contiene las mismas vistas, categorías y navegación que el de spec2viz sobre el fixture, y abre sin recursos externos faltantes.
- Una anotación hecha en el servidor local queda guardada y reaparece al recargar.
- El emparejamiento de átomos reporta los mismos átomos por elemento y la misma cobertura por vista que spec2viz sobre los fixtures de átomos; un id de átomo desconocido es advertencia, o error en modo estricto.
- El paquete no importa spec2viz.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan, specIR no define su propio emparejamiento de átomos y las filas de catálogo y de emparejamiento de átomos de la matriz de cobertura tienen su condición de retiro cumplida.

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

FILE:desk/atoms/atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:36Z'
  authority: generated
  via: create_document
id: atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
title: El vocabulario visual y el resolvedor de vistas ya viven en SLDB
five_wh_one_plus: where
tags:
- system:specir
- system:sldb
- system:spec2viz
- topic:vistas
- layer:modelo
provenance: ../sldb-astryx/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/dag.yaml
---

# El vocabulario visual y el resolvedor de vistas ya viven en SLDB

## Answer

Desde el plan absorber-spec2viz-y-modelos-ui de SLDB (entregado el 2026-11-07), los modelos SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc y ViewDoc viven en sldb/src/sldb/models/notation/, las notaciones y paletas builtin en sldb/src/sldb/notations/, y el resolvedor de vistas y proyecciones en sldb/src/sldb/api/notations/. Un alias en sldb/src/sldb/api/model_registry/model_reference.py resuelve las referencias antiguas spec2viz.sldb_models. specIR usa esas piezas desde SLDB y no las redefine. En spec2viz quedan, sin equivalente en SLDB, la autoría de specs YAML, los compiladores, los renderizadores, el catálogo y la sincronización de specs al store.

FILE:src/specir/visual/catalog/__init__.py
"""specIR's HTML catalog of diagrams (IR13b): the visual part of spec2viz's catalog.

- `loader`: the registry (`vistas.yml`, hierarchical diagram stores, `project.yml` envelope) as a
  flat list of views; paths by sldb's catalog rule (`sldb.api.notations.catalog_paths`).
- `sections`, `views`, `fragments`: the HTML of the views, drawn from sldb's resolved view
  (`resolve_view`) with IR12's `view_to_mermaid`, or from their rendered source.
- `atoms`: a view as sldb's `SpecView` and the atoms the page embeds; the matching and the coverage
  are `sldb.api.matching` (D4), called directly.
- `annotations`: the store document of the page's annotations and the script that saves them with
  `sldb serve` (which replaces spec2viz's `catalog serve`).
- `build`: the page (`render_catalog`, `build_catalog`).

Syncing and validating a catalog are sldb's, used directly: `sldb.api.notations.sync_catalog` and
`check_catalog`, or `sldb notations sync --catalog [--check]` (D1)."""

from specir.visual.catalog.annotations import AnnotationsTarget, CatalogAnnotationsDoc, annotations_id, register_annotations_model
from specir.visual.catalog.atoms import CatalogAtoms, catalog_atoms, spec_view, split_shared_atoms
from specir.visual.catalog.build import build_catalog, render_catalog
from specir.visual.catalog.loader import CatalogConfig, CatalogItem, CatalogLoader, load_catalog
from specir.visual.catalog.sections import render_catalog_metadata, render_filter_bar, render_nav, render_sections, resolve_item_path
from specir.visual.catalog.views import resolved_board, resolved_views

__all__ = [
    "AnnotationsTarget", "CatalogAnnotationsDoc", "CatalogAtoms", "CatalogConfig", "CatalogItem", "CatalogLoader",
    "annotations_id", "build_catalog", "catalog_atoms", "load_catalog", "register_annotations_model", "render_catalog",
    "render_catalog_metadata", "render_filter_bar", "render_nav", "render_sections", "resolve_item_path", "resolved_board",
    "resolved_views", "spec_view", "split_shared_atoms",
]

FILE:src/specir/visual/catalog/loader.py
"""The registry of a catalog: a `vistas.yml`, a hierarchical diagram store or a `project.yml`
envelope, loaded into the flat list of views the HTML catalog draws (migrated from spec2viz's
`orchestrator`: `CatalogItem`, `CatalogConfig`, `CatalogLoader`, `load_catalog`).

Every relative path follows sldb's catalog rule (`sldb.api.notations.catalog_paths`): next to
the config first, then from the repository root, ambiguous when both exist. A spec id without an
extension keeps the inherited search (`<id>.yml` or `specs/<id>.yml` in the config's folder or
its ancestors). The models of the envelope are sldb's (`DiagramStoreEnvelope`, D3)."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from sldb.api.notations.catalog_paths import resolve_catalog_path

from specir.visual.notation_style import UnknownReferenceError

DEFAULT_TITLE = "spec2viz Catalog"
DEFAULT_SUBTITLE = "Visor transversal de diagramas de spec2viz"
DEFAULT_PROJECT_NAME = "spec2viz"
DEFAULT_CATEGORY = "Otras Vistas"

#: Words of a view's title, description or labels that name its diagram type, when no spec says it.
TYPE_HINTS = (
    (("component diagram", "diagrama de componentes", "componentes", "arquitectura logica de componentes"), "component"),
    (("deployment diagram", "diagrama de despliegue", "topologia de despliegue", "despliegue"), "deployment"),
    (("sequence diagram", "diagrama de secuencia", "secuencia", "interacciones"), "sequence"),
    (("state diagram", "state uml", "state diagram-v2", "diagrama de estados", "estados", "ciclo de vida"), "state"),
    (("activity diagram", "actividad", "flujo de atencion", "flujo"), "activity"),
    (("diagrama de clases", "class diagram", "clases"), "class"),
    (("casos de uso", "use case"), "use-case"),
)


def safe_token(value: str) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")


def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii").lower()


def string_list(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, str):
        return [value]
    return [str(v) for v in value if str(v).strip()]


@dataclass
class CatalogItem:
    """One view of the catalog, with the store (config) that declares it."""

    id: str
    anchor_id: str
    title: str
    desc: str = ""
    category: str = DEFAULT_CATEGORY
    nav: str = ""
    lbl: str = ""
    src: str | None = None
    specs: list[str] = field(default_factory=list)
    puml: str | None = None
    notes: list[str] = field(default_factory=list)
    project: str = ""
    diagram_type: str = ""
    tags: list[str] = field(default_factory=list)
    store_path: str = ""
    source_base_dir: str = ""
    notation: str | None = None  # the view's `notation:` (a path, a builtin name or one of the store)


@dataclass
class CatalogConfig:
    """The catalog's page (template, title, brand) and its views, flattened."""

    template: str
    title: str = DEFAULT_TITLE
    brand_name: str = DEFAULT_TITLE
    brand_subtitle: str = DEFAULT_SUBTITLE
    project_name: str = DEFAULT_PROJECT_NAME
    html_artifact: str = ""
    items: list[CatalogItem] = field(default_factory=list)


def _page(data: dict, template: str, title_keys: tuple[str, ...]) -> CatalogConfig:
    return CatalogConfig(
        template=template,
        title=next((data.get(k) for k in title_keys if data.get(k)), None) or DEFAULT_TITLE,
        brand_name=data.get("brand_name") or data.get("title") or DEFAULT_TITLE,
        brand_subtitle=data.get("brand_subtitle") or DEFAULT_SUBTITLE,
        project_name=data.get("project_name") or data.get("project") or DEFAULT_PROJECT_NAME,
        html_artifact=data.get("html_artifact", ""),
    )


def resolve_spec_path(spec: str, base_dir: Path) -> Path | None:
    """A spec with an extension follows the catalog rule (next to the config, then the repo root;
    `AmbiguousPathError` when both exist), then the inherited `specs/` folder; an id without an
    extension keeps the inherited search (`<id>.yml` or `specs/<id>.yml` in the config or its
    ancestors)."""
    spec_path = Path(spec)
    roots = [base_dir, *base_dir.parents[:6]]
    if spec_path.suffix:
        try:
            return resolve_catalog_path(spec, base_dir, "spec")
        except UnknownReferenceError:
            pass  # the inherited `specs/` folder, below
        candidates = [c for root in roots for c in (root / spec_path, root / "specs" / spec_path)]
    else:
        names = (f"{spec}.yml", f"{spec}.yaml", f"specs/{spec}.yml", f"specs/{spec}.yaml")
        candidates = [root / name for root in roots for name in names]
    return next((c.resolve() for c in candidates if c.exists()), None)


def find_project_file(base_dir: Path) -> Path | None:
    for root in [base_dir, *base_dir.parents[:6]]:
        for name in ("project.yaml", "project.yml"):
            if (root / name).exists():
                return (root / name).resolve()
    return None


def find_monorepo_root(start: Path, depth: int | None = None) -> Path | None:
    """The nearest ancestor with a README.md and a `projects/` or `software/` folder."""
    chain = [start, *start.parents] if depth is None else [start, *start.parents[:depth]]
    for root in chain:
        if (root / "README.md").exists() and ((root / "projects").exists() or (root / "software").exists()):
            return root.resolve()
    return None


def _project_from_file(project_file: Path) -> str | None:
    try:
        data = yaml.safe_load(project_file.read_text(encoding="utf-8")) or {}
    except Exception:
        return None
    client = str(data.get("client") or "").strip()
    project_name = str(data.get("project_name") or "").strip()
    if client and project_name:
        return f"{client}/{project_name}"
    return project_name or project_file.parent.resolve().name


def infer_project(base_dir: Path) -> str | None:
    """The project of a config: its folder relative to the monorepo root, or what its
    `project.yml` names (`client/project_name`), or the folder's name."""
    project_file = find_project_file(base_dir)
    if not project_file:
        return None
    project_dir = project_file.parent.resolve()
    root = find_monorepo_root(project_dir, depth=8)
    if root and project_dir.is_relative_to(root):
        return project_dir.relative_to(root).as_posix()
    return _project_from_file(project_file)


def infer_diagram_type(specs: list[str], base_dir: Path) -> str:
    for spec in specs:
        spec_path = resolve_spec_path(spec, base_dir)
        if not spec_path:
            continue
        try:
            data = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        if data.get("type"):
            return str(data["type"])
    return ""


def infer_diagram_type_from_item(item: dict) -> str:
    text = normalize_text(" ".join(str(item.get(key, "")) for key in ["title", "desc", "lbl", "nav", "category", "id"]))
    return next((kind for needles, kind in TYPE_HINTS if any(n in text for n in needles)), "")


def make_anchor_id(item_id: str, project: str | None, store_path: Path) -> str:
    digest = hashlib.md5(str(store_path.resolve()).encode("utf-8")).hexdigest()[:8]
    return "-".join(part for part in (safe_token(project or ""), safe_token(item_id), digest) if part)


def _with_tags(tags: list[str], project: str, diagram_type: str, exact: bool) -> list[str]:
    def has(prefix: str, value: str) -> bool:
        return any(tag == f"{prefix}{value}" if exact else tag.startswith(prefix) for tag in tags)

    if project and not has("project:", project):
        tags.append(f"project:{project}")
    if diagram_type and not has("type:", diagram_type):
        tags.append(f"type:{diagram_type}")
    return tags


@dataclass
class _Defaults:
    project: str
    category: str
    tags: list[str]
    diagram_type: str


def make_item(item: dict, base_dir: Path, store_path: Path, defaults: _Defaults) -> CatalogItem:
    specs = string_list(item.get("specs"))
    project = item.get("project") or defaults.project or infer_project(base_dir)
    diagram_type = item.get("type") or defaults.diagram_type or infer_diagram_type(specs, base_dir) or infer_diagram_type_from_item(item)
    tags = _with_tags(list(dict.fromkeys(defaults.tags + string_list(item.get("tags")))), project, diagram_type, exact=False)
    return CatalogItem(
        id=item["id"], anchor_id=make_anchor_id(item["id"], project, store_path), title=item.get("title", item["id"]),
        desc=item.get("desc", ""), category=item.get("category") or defaults.category, nav=item.get("nav", item.get("lbl", item["id"])),
        lbl=item.get("lbl", ""), src=item.get("src") or item.get("mmd"), specs=specs, puml=item.get("puml"),
        notes=string_list(item.get("notes")), project=project or "", diagram_type=diagram_type, tags=tags,
        store_path=str(store_path), source_base_dir=str(base_dir), notation=item.get("notation"),
    )


def apply_overrides(item: CatalogItem, overrides: dict) -> CatalogItem:
    """A child store's view with the `project`, `category`, `type` and `tags` of its parent's entry."""
    project = overrides.get("project") or item.project
    diagram_type = overrides.get("type") or item.diagram_type
    tags = _with_tags(list(dict.fromkeys(item.tags + string_list(overrides.get("tags")))), project, diagram_type, exact=True)
    return CatalogItem(
        **{**item.__dict__, "anchor_id": make_anchor_id(item.id, project, Path(item.store_path)), "category": overrides.get("category") or item.category,
           "project": project, "diagram_type": diagram_type, "tags": tags},
    )


def normalize_store_entry(store_entry, base_dir: Path) -> tuple[Path, dict]:
    if isinstance(store_entry, str):
        return (base_dir / store_entry).resolve(), {}
    if not isinstance(store_entry, dict) or "path" not in store_entry:
        raise ValueError("Store entries must be a relative path or an object with 'path'.")
    return (base_dir / str(store_entry["path"])).resolve(), {k: v for k, v in store_entry.items() if k != "path"}


class CatalogLoader:
    """Loads a registry and the stores it includes, refusing a store that includes itself."""

    def __init__(self):
        self._visited: set[Path] = set()

    def load(self, config_path: Path) -> CatalogConfig:
        config_path = Path(config_path).resolve()
        if config_path in self._visited:
            raise ValueError(f"Recursive store reference detected: {config_path}")
        self._visited.add(config_path)
        try:
            return self._load_store(config_path)
        finally:
            self._visited.remove(config_path)

    def _load_store(self, config_path: Path) -> CatalogConfig:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        data = raw["diagram_store"] if isinstance(raw.get("diagram_store"), dict) else raw
        if "vistas" in data:
            return self._load_vistas(config_path, data)
        catalog = _page(data, data.get("template", "template.html"), ("title", "catalog_title"))
        base_dir = config_path.parent
        defaults = _Defaults(data.get("project") or infer_project(base_dir) or "", data.get("category", DEFAULT_CATEGORY),
                             string_list(data.get("tags")), data.get("type", ""))
        catalog.items += [make_item(item, base_dir, config_path, defaults) for item in data.get("items", [])]
        for store_entry in data.get("stores", []):
            self._include(catalog, *normalize_store_entry(store_entry, base_dir))
        return catalog

    def _include(self, catalog: CatalogConfig, child_path: Path, overrides: dict) -> None:
        child = self.load(child_path)
        if not catalog.html_artifact and child.html_artifact:
            catalog.html_artifact = child.html_artifact
        catalog.items += [apply_overrides(item, overrides) for item in child.items]

    def _load_vistas(self, config_path: Path, data: dict) -> CatalogConfig:
        catalog = _page(data, data.get("template", "template.html"), ("title", "brand_name"))
        base_dir = config_path.parent
        defaults = _Defaults(data.get("project") or infer_project(base_dir) or "", DEFAULT_CATEGORY, string_list(data.get("tags")), "")
        catalog.items += [make_item(view, base_dir, config_path, defaults) for view in data.get("vistas", [])]
        return catalog


def load_catalog(config_path: Path) -> CatalogConfig:
    return CatalogLoader().load(config_path)


__all__ = [
    "CatalogConfig", "CatalogItem", "CatalogLoader", "infer_project", "load_catalog", "make_anchor_id", "resolve_spec_path",
]

FILE:src/specir/visual/catalog/sections.py
"""The HTML of the catalog's views: navigation, filter bar, sections by category and the board of
each view (migrated from spec2viz's `orchestrator`: `render_filter_bar`, `render_sections`,
`render_nav`, `render_catalog_metadata`, `resolve_item_path`, `_read_item_source`,
`_resolved_item_board`).

A view with specs whose resolved view is a graph is drawn from it (`views.resolved_board`);
otherwise the catalog embeds its rendered source (`src`): a `.mmd` linted as mermaid, an `.svg`, an
HTML snippet or `#fragment`, a Vega `.json` for vega-embed, or any other text as it is."""

from __future__ import annotations

import html
import json
from pathlib import Path

from sldb.api.notations.catalog_paths import resolve_catalog_path

from specir.visual.catalog.fragments import extract_html_fragment
from specir.visual.catalog.loader import DEFAULT_CATEGORY, CatalogConfig, CatalogItem, resolve_spec_path
from specir.visual.catalog.views import resolved_board
from specir.visual.lint_mermaid import assert_mermaid_ok
from specir.visual.notation_style import UnknownNotationError, UnknownReferenceError


def _slug(value: str) -> str:
    return "-".join(value.strip().lower().split()) if value else ""


def by_category(items: list[CatalogItem]) -> dict[str, list[CatalogItem]]:
    categories: dict[str, list[CatalogItem]] = {}
    for item in items:
        categories.setdefault(item.category or DEFAULT_CATEGORY, []).append(item)
    return categories


def _options(values: list[str], label: str) -> str:
    opts = ['<option value="">Todos</option>'] + [f'<option value="{html.escape(v)}">{html.escape(v)}</option>' for v in values]
    return f'<label>{label}<select data-filter="{_slug(label)}">{"".join(opts)}</select></label>'


def render_filter_bar(items: list[CatalogItem]) -> str:
    types = sorted({item.diagram_type for item in items if item.diagram_type})
    projects = sorted({item.project for item in items if item.project})
    categories = sorted({item.category for item in items if item.category})
    tags = sorted({tag for item in items for tag in item.tags if tag})
    tag_buttons = "".join(f'<button type="button" class="tag-chip" data-tag="{html.escape(t)}">{html.escape(t)}</button>' for t in tags)
    return (
        '<div class="catalog-toolbar">'
        '<div class="catalog-toolbar-row">'
        f'{_options(types, "Tipo")}'
        f'{_options(projects, "Proyecto")}'
        f'{_options(categories, "Categoría")}'
        '<label>Búsqueda<input type="search" id="catalog-search" placeholder="Título, tag o descripción"></label>'
        '</div>'
        f'<div class="catalog-tags">{tag_buttons}</div>'
        '</div>'
    )


def _attrs(item: CatalogItem) -> list[str]:
    attrs = [f'data-spec="{html.escape(spec)}"' for spec in item.specs]
    if item.puml:
        attrs.append(f'data-puml="{html.escape(item.puml)}"')
    attrs += [f'data-type="{html.escape(item.diagram_type)}"', f'data-project="{html.escape(item.project)}"',
              f'data-category="{html.escape(item.category)}"', f'data-tags="{html.escape(" ".join(item.tags))}"',
              f'data-view-id="{html.escape(item.id)}"', 'class="catalog-item"']
    return attrs


def _badges(item: CatalogItem) -> str:
    badges = [f'<span class="meta-badge">{html.escape(v)}</span>' for v in (item.diagram_type, item.project) if v]
    badges += [f'<span class="meta-badge subtle">{html.escape(tag)}</span>' for tag in item.tags]
    return f'<div class="section-meta">{"".join(badges)}</div>' if badges else ""


def _notes(item: CatalogItem) -> str:
    if not item.notes:
        return ""
    items_html = "".join(f"<li>{html.escape(note)}</li>" for note in item.notes)
    return f'\n  <div class="gap-notes"><strong>Gaps de implementación</strong><ul>{items_html}</ul></div>'


def render_section(item: CatalogItem) -> str:
    content = resolved_item_board(item) or read_item_source(item)
    return (
        f'<section id="{html.escape(item.anchor_id)}" {" ".join(_attrs(item))}>'
        f'\n  <div class="lbl">{html.escape(item.lbl)}</div>'
        f'\n  <h2>{html.escape(item.title)}</h2>'
        f'\n  <p class="desc">{html.escape(item.desc)}</p>'
        f'\n  {_badges(item)}'
        f'\n{content}{_notes(item)}\n</section>'
    )


def render_sections(items: list[CatalogItem], base_dir: Path | None = None) -> str:
    blocks = []
    for category, cat_items in by_category(items).items():
        sections = "".join(render_section(item) for item in cat_items)
        blocks.append(
            f'<div class="category-block" data-category-block="{html.escape(category)}">'
            f'<div class="macro-separator"><h2>— {html.escape(category)} —</h2></div>'
            f'{sections}</div>'
        )
    return "\n".join(blocks)


def render_nav(items: list[CatalogItem]) -> str:
    parts = []
    for category, cat_items in by_category(items).items():
        links = "".join(f'<a href="#{html.escape(item.anchor_id)}">{html.escape(item.nav or item.lbl or item.id)}</a>' for item in cat_items)
        parts.append(f'<div class="nav-category"><span>{html.escape(category)}</span>{links}</div>')
    return "\n".join(parts)


def render_catalog_metadata(catalog: CatalogConfig, items: list[CatalogItem]) -> str:
    return json.dumps({
        "title": catalog.title, "brand_name": catalog.brand_name, "brand_subtitle": catalog.brand_subtitle,
        "project_name": catalog.project_name, "item_count": len(items),
    })


def split_src_fragment(src: str) -> tuple[str, str | None]:
    if ".html#" in src:
        path, fragment = src.split("#", 1)
        return path, fragment
    return src, None


def resolve_item_path(value: str, base_dir: Path, field: str) -> Path:
    """A view's `src` by the catalog rule; when it exists nowhere, the path next to the config (the
    missing-file error is the usual one). Ambiguous -> `AmbiguousPathError`."""
    try:
        return resolve_catalog_path(value, base_dir, field)
    except UnknownReferenceError:
        return Path(base_dir) / value


def resolved_item_board(item: CatalogItem) -> str | None:
    """The board of a view from its resolved view, with the view's notation; None when the view has
    no specs that resolve or its layout is not a graph (then its `src` is used)."""
    if not item.specs:
        return None
    base = Path(item.source_base_dir)
    spec_paths = [p for p in (resolve_spec_path(spec, base) for spec in item.specs) if p is not None]
    if not spec_paths:
        return None
    notation: str | Path | None = None
    if item.notation:
        text = str(item.notation)
        looks_like_path = "/" in text or text.endswith((".yml", ".yaml"))
        notation = resolve_catalog_path(text, base, "notation", UnknownNotationError) if looks_like_path else text
    return resolved_board(spec_paths, notation, base)


def _markup_board(content: str) -> str:
    is_markup = content.lstrip().startswith("<div") or "<style>" in content
    indent = "" if is_markup else "    "
    style = "" if is_markup else ' style="font-family:\'JetBrains Mono\',monospace; font-size:12px; white-space:pre-wrap; color:var(--bone-dim);"'
    indented = "\n".join(indent + line for line in content.splitlines())
    return f'  <div class="board"{style}>\n{indented}\n  </div>'


def _vega_board(content: str, src_value: str) -> str:
    try:
        json.loads(content)
    except ValueError as exc:
        raise ValueError(f"{src_value}: not valid JSON for a Vega board ({exc})") from exc
    escaped = content.replace("</", "<\\/")
    return f'  <div class="board vega-board">\n    <script type="application/json" class="vega-spec">\n{escaped}\n    </script>\n  </div>'


def _mermaid_board(content: str, src_value: str) -> str:
    # lint the raw mermaid before it is embedded: a broken .mmd fails the build, not the browser
    assert_mermaid_ok(content, source=str(src_value), check_html=False)
    indented = "\n".join("      " + line for line in html.escape(content).splitlines())
    return f'  <div class="board">\n    <pre class="mermaid">\n{indented}\n    </pre>\n  </div>'


def read_item_source(item: CatalogItem) -> str:
    if not item.src:
        return '  <div class="board"><div style="color:#94a3b8">Sin fuente renderizada configurada.</div></div>'
    src_value, fragment = split_src_fragment(item.src)
    content = resolve_item_path(src_value, Path(item.source_base_dir), "src").read_text(encoding="utf-8").strip()
    if fragment:
        return f'  {extract_html_fragment(content, fragment)}'
    name = str(src_value)
    if name.endswith(".svg"):
        return f'  <div class="board puml-board">\n{content}\n  </div>'
    if name.endswith(".html"):
        return _markup_board(content)
    if name.endswith(".json"):
        return _vega_board(content, src_value)
    if not name.endswith((".mmd", ".mermaid")):
        # any other text projection (.puml, .d2, .txt) is shown as it is; only mermaid is drawn and linted
        return f'  <div class="board"><pre class="source-board">{html.escape(content)}</pre></div>'
    return _mermaid_board(content, src_value)


__all__ = [
    "read_item_source", "render_catalog_metadata", "render_filter_bar", "render_nav", "render_section", "render_sections",
    "resolve_item_path", "resolved_item_board",
]

FILE:src/specir/visual/catalog/views.py
"""The boards of the HTML catalog from the resolved view, the same source graph_ui draws from
(migrated from spec2viz's `catalog_views`).

For each spec of a view, the catalog draws the mermaid of its resolved view
(`sldb.api.notations.resolve_view`) with the view's notation (`notation:` in vistas.yml, or the
builtin of its type), through IR12's `view_to_mermaid`. The resolved view comes:

1. from the project's store (the nearest `.sldb` above the vistas.yml) when the spec is synced
   there with the same content (sha256) and the same notation: exactly what graph_ui shows;
2. otherwise from a scratch store where sldb's `SpecSync` syncs the spec with that notation (the
   repository is not touched).

With a notation that only lives in a store where the spec is not synced, or a layout that is not a
graph (sequence, matrix), the view keeps its rendered source (`src`)."""

from __future__ import annotations

import hashlib
import html
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import sldb.api as api
import yaml
from sldb.api.notations import SpecSync, find_store, resolve_view

from specir.visual.lint_mermaid import assert_mermaid_ok
from specir.visual.notation_style import DEFAULT_NOTATIONS, builtin_notations
from specir.visual.renderers.view_mermaid import view_to_mermaid


def _warn(message: str) -> None:
    print(f"catalog: {message}", file=sys.stderr)


def _project_view(store: Path, spec_id: str, spec_path: Path, notation_ref: str | None) -> dict[str, Any] | None:
    sha = hashlib.sha256(spec_path.read_bytes()).hexdigest()
    for doc in api.load_runtime_documents(store, None, include_linked=False):
        if str(doc.model_name) == "SpecDoc" and doc.name == spec_id:
            payload = dict(doc.payload or {})
            if payload.get("sha256") != sha or (notation_ref and payload.get("notation") != notation_ref):
                return None
            return resolve_view(store, spec_id)
    return None


def _scratch_view(spec_path: Path, notation: str | Path | None) -> dict[str, Any]:
    root = Path(tempfile.mkdtemp(prefix="specir-catalog-"))
    try:
        api.init_store(root)
        report = SpecSync(root / ".sldb", out_dir=root / "sldb" / "specs").sync(spec_path, notation=notation)
        return resolve_view(root / ".sldb", report.spec_id)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _notation_ref(chosen: str | Path) -> str | None:
    if isinstance(chosen, Path):
        name = (yaml.safe_load(Path(chosen).read_text(encoding="utf-8")) or {}).get("name")
        return f"NotationDoc:{name}" if name else None
    return f"NotationDoc:{chosen}"


def _view_of(spec_path: Path, notation: str | Path | None, store: Path | None) -> dict[str, Any] | None:
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
    spec_id, diagram_type = str(spec.get("id") or ""), str(spec.get("type") or "")
    chosen = notation if notation is not None else DEFAULT_NOTATIONS.get(diagram_type)
    if chosen is None:
        return None
    view = None
    if store is not None:
        try:
            view = _project_view(Path(store), spec_id, spec_path, _notation_ref(chosen))
        except Exception as exc:  # a broken store does not stop the catalog: the view is resolved apart
            _warn(f"{spec_id}: project store not usable ({type(exc).__name__}: {exc})")
    if view is None:
        if not isinstance(chosen, Path) and str(chosen) not in builtin_notations():
            _warn(f"{spec_id}: notation {chosen!r} lives only in the store and the spec is not synced there; using the view's src")
            return None
        view = _scratch_view(spec_path, chosen)
    return view if (view.get("layout") or {}).get("kind", "graph") == "graph" else None


def resolved_views(spec_paths: list[Path], notation: str | Path | None, config_dir: Path) -> list[dict[str, Any]] | None:
    """The resolved views of a catalog view's specs, or None when one cannot be resolved (a layout
    that is not a graph, a store-only notation the spec is not synced with)."""
    store = find_store(config_dir)
    views = []
    for spec_path in spec_paths:
        view = _view_of(spec_path, notation, store)
        if view is None:
            return None
        views.append(view)
    return views


def resolved_board(spec_paths: list[Path], notation: str | Path | None, config_dir: Path) -> str | None:
    """The HTML of a view's mermaid boards, from its resolved views; None when it does not apply."""
    views = resolved_views(spec_paths, notation, config_dir)
    if not views:
        return None
    boards = []
    for view in views:
        source = view_to_mermaid(view, theme="dark")
        assert_mermaid_ok(source, source=view["spec"], check_html=False)
        indented = "\n".join("      " + line for line in html.escape(source).splitlines())
        boards.append(f'  <div class="board" data-resolved-from="{html.escape(view["spec"])}" data-notation="{html.escape(view["notation"])}">\n'
                      f'    <pre class="mermaid">\n{indented}\n    </pre>\n  </div>')
    return "\n".join(boards)


__all__ = ["resolved_board", "resolved_views"]

FILE:src/specir/visual/catalog/fragments.py
"""One element of an HTML artifact, by id or by class, as the catalog embeds a `src: x.html#id`
(migrated from spec2viz's `orchestrator`: `_ElementByIdExtractor`, `_ElementByClassExtractor`,
`_extract_html_fragment`)."""

from __future__ import annotations

from html.parser import HTMLParser


class _ElementExtractor(HTMLParser):
    """The markup of the first element `wanted(attrs)` accepts, as written."""

    def __init__(self, keep_decl: bool):
        super().__init__(convert_charrefs=False)
        self.depth = 0
        self.capturing = False
        self.parts: list[str] = []
        self.keep_decl = keep_decl

    def wanted(self, attrs: dict[str, str | None]) -> bool:
        raise NotImplementedError

    def handle_starttag(self, tag, attrs):
        if not self.capturing and self.wanted(dict(attrs)):
            self.capturing, self.depth = True, 1
            self.parts.append(self.get_starttag_text())
            return
        if self.capturing:
            self.depth += 1
            self.parts.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if self.capturing:
            self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.capturing:
            self.parts.append(f"</{tag}>")
            self.depth -= 1
            self.capturing = self.depth != 0

    def _keep(self, text: str) -> None:
        if self.capturing:
            self.parts.append(text)

    def handle_data(self, data):
        self._keep(data)

    def handle_comment(self, data):
        self._keep(f"<!--{data}-->")

    def handle_entityref(self, name):
        self._keep(f"&{name};")

    def handle_charref(self, name):
        self._keep(f"&#{name};")

    def handle_decl(self, decl):
        if self.keep_decl:
            self._keep(f"<!{decl}>")

    def get_html(self) -> str:
        return "".join(self.parts).strip()


class ElementByIdExtractor(_ElementExtractor):
    def __init__(self, target_id: str):
        super().__init__(keep_decl=True)
        self.target_id = target_id

    def wanted(self, attrs):
        return attrs.get("id") == self.target_id


class ElementByClassExtractor(_ElementExtractor):
    def __init__(self, class_name: str):
        super().__init__(keep_decl=False)
        self.class_name = class_name

    def wanted(self, attrs):
        return self.class_name in set((attrs.get("class") or "").split())


def extract_html_fragment(content: str, fragment: str) -> str:
    """The `.board` inside the element `#fragment` (or the element itself if it has none)."""
    extractor = ElementByIdExtractor(fragment)
    extractor.feed(content)
    element_html = extractor.get_html()
    if not element_html:
        raise ValueError(f"HTML fragment '#{fragment}' not found in source artifact.")
    board = ElementByClassExtractor("board")
    board.feed(element_html)
    return board.get_html() or element_html


__all__ = ["ElementByClassExtractor", "ElementByIdExtractor", "extract_html_fragment"]

FILE:src/specir/visual/catalog/atoms.py
"""The atoms of the HTML catalog: the adapter from a catalog view to sldb's `SpecView` and what the
page embeds (migrated from spec2viz's `deskops`: the `CatalogItem` adapter, the store discovery of
`SldbAtomResolver`, `split_shared_atoms` and the atom part of `render_deskops`).

The matching itself is sldb's (`sldb.api.matching`, D4), called directly: the atoms of each view's
store or of an atoms folder (`build_atoms_by_view`), the explicit `atoms:` and `refs:` of the
elements (`build_explicit_atoms`, `build_explicit_refs`), the sldb edges of the atoms
(`attach_atom_edges`) and the coverage per view (`build_coverage_by_view`). An unknown atom id is a
`matching/unknown-atom` finding, an error with `strict` (`UnknownAtomError`). specIR only adapts a
view and lays the result in the page; the fuzzy matching in the browser is the template's
(`findAtomData`, `normKey`, which sldb's `label_key` matches)."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from sldb.api.matching import (
    SpecView,
    StoreReader,
    attach_atom_edges,
    build_coverage_by_view,
    build_explicit_atoms,
    build_explicit_refs,
    filter_atoms_payload,
    raw_atoms_by_view,
)
from sldb.api.notations import find_store

from specir.visual.catalog.loader import CatalogItem, find_monorepo_root, resolve_spec_path
from specir.visual.catalog.sections import resolve_item_path


def item_specs(item: CatalogItem) -> list[dict]:
    """The YAML specs of a view that could be read, as dicts."""
    specs = []
    for spec_ref in item.specs:
        spec_path = resolve_spec_path(spec_ref, Path(item.source_base_dir))
        if spec_path is None:
            continue
        try:
            spec = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        if isinstance(spec, dict):
            specs.append(spec)
    return specs


def _src_path(item: CatalogItem) -> Path | None:
    if not item.src:
        return None
    return resolve_item_path(item.src.split("#", 1)[0], Path(item.source_base_dir), "src").resolve()


def _boundary(item: CatalogItem, src_path: Path | None) -> Path | None:
    """The project's folder (`<monorepo root>/<project>`) a view's store must live in, if any."""
    if not item.project:
        return None
    probe = src_path.parent if src_path is not None else Path(item.source_base_dir)
    root = find_monorepo_root(probe.resolve())
    boundary = (root / item.project).resolve() if root is not None else None
    return boundary if boundary is not None and boundary.exists() else None


def view_store(item: CatalogItem) -> Path | None:
    """The `.sldb` of a view: the nearest one sldb recognizes above its `src`, then above its
    config, inside its project's folder when it has one."""
    src_path = _src_path(item)
    boundary = _boundary(item, src_path)
    for start in [*([src_path.parent] if src_path is not None else []), Path(item.source_base_dir)]:
        store = find_store(start)
        if store is not None and (boundary is None or store.parent.is_relative_to(boundary)):
            return store
    return None


def spec_view(item: CatalogItem) -> SpecView:
    """A catalog view as sldb's `SpecView`: its specs loaded and its store found."""
    return SpecView(
        key=item.anchor_id, id=item.id, specs=item_specs(item), source=item.src or "", base_dir=item.source_base_dir,
        store=view_store(item), title=item.title, diagram_type=item.diagram_type, scope=item.project,
    )


def split_shared_atoms(atoms_by_view: dict[str, dict[str, dict]]) -> tuple[dict[str, dict], dict[str, dict[str, dict]]]:
    """Moves the most repeated (non empty) payload to a common `ATOMS_DB`, emitted once: the
    template falls back to `ATOMS_DB` when a view is not in `ATOMS_BY_VIEW`."""
    counts: dict[str, int] = {}
    for payload in (p for p in atoms_by_view.values() if p):
        key = json.dumps(payload, sort_keys=True)
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return {}, atoms_by_view
    shared_key, shared_count = max(counts.items(), key=lambda kv: kv[1])
    if shared_count < 2:
        return {}, atoms_by_view
    rest = {view: payload for view, payload in atoms_by_view.items() if not (payload and json.dumps(payload, sort_keys=True) == shared_key)}
    return json.loads(shared_key), rest


@dataclass
class CatalogAtoms:
    """What the page embeds about atoms, as the template reads it (`window.*`)."""

    shared: dict[str, dict] = field(default_factory=dict)
    by_view: dict[str, dict] = field(default_factory=dict)
    explicit: dict[str, dict] = field(default_factory=dict)
    linked: dict[str, dict] = field(default_factory=dict)
    refs: dict[str, dict] = field(default_factory=dict)
    coverage: dict[str, dict] = field(default_factory=dict)
    warnings: list[dict] = field(default_factory=list)
    coverage_warnings: list[dict] = field(default_factory=list)


def _report(findings: list[Any]) -> list[dict]:
    for finding in findings:
        print(f"[specir][atoms] {finding.subject}: {finding.what}", file=sys.stderr)
    return [finding.as_dict() for finding in findings]


def catalog_atoms(items: list[CatalogItem], atoms_dir: Path | None = None, atoms_tags: list[str] | None = None, strict: bool = False) -> CatalogAtoms:
    """The atoms of the catalog's views through `sldb.api.matching`; with `strict` an unknown atom
    or ref raises sldb's `UnknownAtomError`."""
    views, reader = [spec_view(item) for item in items], StoreReader()
    raw, warnings = raw_atoms_by_view(views, atoms_dir, reader)
    explicit, complete, explicit_warnings, linked = build_explicit_atoms(views, raw, strict=strict)
    refs, ref_warnings = build_explicit_refs(views, reader, strict=strict)
    attach_atom_edges(views, explicit, linked, reader, raw)
    by_view = {view: filter_atoms_payload(payload, atoms_tags) if atoms_tags else payload for view, payload in raw.items()}
    by_view.update({view: {} for view in complete})  # every node explicit: no fuzzy matching, nothing else embedded
    shared, by_view = split_shared_atoms(by_view)
    coverage, coverage_warnings = build_coverage_by_view(views)
    return CatalogAtoms(shared, by_view, explicit, linked, refs, coverage, _report([*warnings, *explicit_warnings, *ref_warnings]),
                        [finding.as_dict() for finding in coverage_warnings])


def atoms_script(atoms: CatalogAtoms, metadata: str) -> str:
    """The `<script>` that hands the atoms to the template, right before `</body>`."""
    return (
        "\n<script>"
        f"window.ATOMS_DB = {json.dumps(atoms.shared)}; "
        f"window.ATOMS_BY_VIEW = {json.dumps(atoms.by_view)}; "
        f"window.ATOMS_EXPLICIT = {json.dumps(atoms.explicit)}; "
        f"window.ATOMS_LINKED = {json.dumps(atoms.linked)}; "
        f"window.REFS_EXPLICIT = {json.dumps(atoms.refs)}; "
        f"window.COVERAGE_BY_VIEW = {json.dumps(atoms.coverage)}; "
        f"window.SPEC2VIZ_ATOM_WARNINGS = {json.dumps(atoms.warnings)}; "
        f"window.SPEC2VIZ_COVERAGE_WARNINGS = {json.dumps(atoms.coverage_warnings)}; "
        f"window.SPEC2VIZ_CATALOG = {metadata};"
        "</script>\n</body>"
    )


__all__ = ["CatalogAtoms", "atoms_script", "catalog_atoms", "item_specs", "spec_view", "split_shared_atoms", "view_store"]

FILE:src/specir/visual/catalog/annotations.py
"""The annotations of an HTML catalog, kept in an sldb store and saved through `sldb serve`
(replaces spec2viz's `catalog serve`, which wrote them to a JSON file next to the page).

specIR runs no server: the catalog page talks to `sldb serve --cors` with the two routes D4
checked, `GET /document?id=` to read the annotations and `POST /save` to write them, with the
payload read as the optimistic guard (`changes[].expected`; 409 when someone else changed it).
What stays here is visual: the model of the document that holds a catalog's annotations
(`CatalogAnnotationsDoc`, registered in the store with sldb's `add_model`) and the page's script
(`templates/annotations-sldb.js`), which the build embeds when an annotations target is given.
Without one, the page keeps its annotations in the browser (`localStorage`), as before."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

import sldb.api as api
from pydantic import Field
from sldb.api import StructuredNLDoc

SCRIPT = "annotations-sldb.js"
MODEL_NAME = "CatalogAnnotationsDoc"


class CatalogAnnotationsDoc(StructuredNLDoc):
    """The annotations of one HTML catalog: one comment per diagram element of a view."""

    __authority__ = "authored"
    __semantics__ = {"type": ["specir", "catalog", "annotations"], "layer": ["visual"]}
    __template__ = """---
catalog: ⸢rev•catalog⸥
annotations: ⸢rev,list•annotations⸥
---
# ⸢rev•title⸥
""".strip()

    title: str = Field(description="The catalog's title, shown as the H1 heading.")
    catalog: str = Field(default="", description="The catalog these annotations belong to (its project name).")
    annotations: list[dict] = Field(
        default_factory=list,
        description="One entry per comment, as the catalog page writes it: key (`<view anchor>::<label>`), vista, label, comentario and ts.",
    )


def model_ref() -> str:
    return f"{CatalogAnnotationsDoc.__module__}:{CatalogAnnotationsDoc.__name__}"


def package_pythonpath() -> str:
    """The directory `specir` is imported from: what sldb needs to import the model."""
    return str(Path(__file__).resolve().parents[3])


def register_annotations_model(store: Path) -> None:
    """Registers `CatalogAnnotationsDoc` in the store (sldb's model registry); twice changes nothing."""
    if not api.is_model_registered(store, MODEL_NAME):
        api.add_model(store, model_ref(), pythonpath=package_pythonpath())


def annotations_id(catalog_name: str) -> str:
    """The id of a catalog's annotations document: what `sldb serve` accepts as a new id."""
    token = re.sub(r"[^a-zA-Z0-9_-]+", "-", catalog_name).strip("-_") or "catalog"
    return f"catalog-annotations-{token}"[:160]


@dataclass(frozen=True)
class AnnotationsTarget:
    """Where a catalog page saves its annotations: the base URL of `sldb serve` and the document id.
    The page also reads both from its URL (`?sldb=<url>&annotations=<id>`), which win."""

    server: str = ""
    doc: str = ""


def annotations_script(target: AnnotationsTarget, title: str, catalog: str) -> str:
    """The `<script>` that makes the page read and save its annotations with `sldb serve`."""
    config = {"server": target.server, "doc": target.doc or annotations_id(catalog or title), "model": MODEL_NAME, "title": title, "catalog": catalog}
    code = resources.files("specir.visual").joinpath("templates", SCRIPT).read_text(encoding="utf-8")
    return f"\n<script>\nwindow.SPECIR_ANNOTATIONS = {json.dumps(config)};\n{code}\n</script>\n"


__all__ = [
    "AnnotationsTarget", "CatalogAnnotationsDoc", "annotations_id", "annotations_script", "model_ref", "package_pythonpath",
    "register_annotations_model",
]

FILE:src/specir/visual/catalog/build.py
"""The self-contained HTML catalog of a registry (migrated from spec2viz's `deskops.render_deskops`
and `build_deskops`): the template (a local override next to the config, or the packaged
`templates/default.html` of IR12) filled with the navigation, the filter bar, the sections and the
page metadata, and the atoms of each view right before `</body>`.

With an `AnnotationsTarget` the page also reads and saves its annotations with `sldb serve`
(`annotations.py`); without one it is what spec2viz built."""

from __future__ import annotations

import sys
from importlib import resources
from pathlib import Path

from specir.visual.catalog.annotations import AnnotationsTarget, annotations_script
from specir.visual.catalog.atoms import atoms_script, catalog_atoms
from specir.visual.catalog.loader import CatalogConfig, load_catalog
from specir.visual.catalog.sections import render_catalog_metadata, render_filter_bar, render_nav, render_sections


def catalog_template(catalog: CatalogConfig, base_dir: Path) -> str:
    """The local template the config names, if it exists; otherwise the packaged one."""
    local = base_dir / catalog.template if catalog.template else None
    if local and local.exists():
        print(f"specir: using local catalog template override: {local}", file=sys.stderr)
        return local.read_text(encoding="utf-8")
    return resources.files("specir.visual").joinpath("templates", "default.html").read_text(encoding="utf-8")


def _fill(template: str, catalog: CatalogConfig, base_dir: Path) -> str:
    nav, filters, sections = render_nav(catalog.items), render_filter_bar(catalog.items), render_sections(catalog.items, base_dir)
    values = {
        "{{NAV}}": nav, "{{FILTERS}}": filters, "{{SECTIONS}}": sections, "{{PROJECT_NAME}}": catalog.project_name,
        "{{BRAND_NAME}}": catalog.brand_name, "{{BRAND_SUBTITLE}}": catalog.brand_subtitle, "{{CATALOG_TITLE}}": catalog.title,
        "{{CATALOG_METADATA}}": render_catalog_metadata(catalog, catalog.items),
    }
    page = template
    for marker, value in values.items():
        page = page.replace(marker, value)
    if "{{FILTERS}}" not in template and "{{SECTIONS}}" in template:
        page = page.replace(sections, filters + sections, 1)
    return page


def render_catalog(
    config_path: Path,
    base_dir: Path | None = None,
    atoms_dir: Path | None = None,
    atoms_tags: list[str] | None = None,
    strict_atoms: bool = False,
    annotations: AnnotationsTarget | None = None,
) -> str:
    """The catalog's HTML. `strict_atoms` turns an unknown `atoms:`/`refs:` id into sldb's
    `UnknownAtomError`; otherwise it is a warning on stderr and in the page."""
    catalog = load_catalog(config_path)
    base_dir = base_dir if base_dir is not None else config_path.parent
    page = _fill(catalog_template(catalog, base_dir), catalog, base_dir)
    atoms = catalog_atoms(catalog.items, atoms_dir, atoms_tags, strict_atoms)
    page = page.replace("{{ATOMS_DB}}", "{}")
    tail = atoms_script(atoms, render_catalog_metadata(catalog, catalog.items))
    if annotations is not None:
        tail = annotations_script(annotations, catalog.title, catalog.project_name) + tail
    return page.replace("</body>", tail)


def build_catalog(config_path: Path, out_path: Path, base_dir: Path | None = None, atoms_dir: Path | None = None,
                  atoms_tags: list[str] | None = None, strict_atoms: bool = False, annotations: AnnotationsTarget | None = None) -> Path:
    """Writes the catalog's HTML to `out_path`."""
    out_path.write_text(render_catalog(config_path, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations), encoding="utf-8")
    return out_path


__all__ = ["build_catalog", "catalog_template", "render_catalog"]

FILE:src/specir/visual/templates/annotations-sldb.js
// <sldb-annotations>
// The catalog's annotations saved in an sldb store through `sldb serve --cors` (specIR, IR13b).
// Reads with GET /document?id=<doc>; writes with POST /save, guarded by the payload it read
// (`expected`): a 409 means someone else saved first, so it merges with what is stored and retries
// once. The browser's localStorage stays as the local copy; the store wins when the page loads.
function sldbAnnotationsConfig(config, search) {
  const params = new URLSearchParams(search || '');
  const server = (params.get('sldb') || (config && config.server) || '').replace(/\/+$/, '');
  return { ...(config || {}), server, doc: params.get('annotations') || (config && config.doc) || '' };
}

function sldbAnnotationsStore(config, fetchImpl) {
  let current = null;
  const url = path => `${config.server}${path}`;

  async function read() {
    const response = await fetchImpl(url(`/document?id=${encodeURIComponent(config.doc)}`));
    if (response.status === 404) {
      current = null;
      return [];
    }
    if (!response.ok) throw new Error(`sldb serve answered ${response.status} reading ${config.doc}`);
    current = (await response.json()).payload;
    return Array.isArray(current.annotations) ? current.annotations : [];
  }

  function change(items) {
    if (!current) {
      const payload = { title: config.title || config.doc, catalog: config.catalog || '', annotations: items };
      return { id: config.doc, action: 'create', model: config.model, payload };
    }
    return { id: config.doc, action: 'update', model: config.model, payload: { ...current, annotations: items }, expected: current };
  }

  function post(items) {
    const body = JSON.stringify({ changes: [change(items)] });
    return fetchImpl(url('/save'), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body });
  }

  function merge(stored, local) {
    const seen = new Set();
    return [...stored, ...local].filter(a => {
      const key = JSON.stringify([a.key, a.comentario, a.ts]);
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  async function write(items) {
    let response = await post(items);
    if (response.status === 409) {
      items = merge(await read(), items);
      response = await post(items);
    }
    if (!response.ok) throw new Error(`sldb serve answered ${response.status} saving ${config.doc}: ${await response.text()}`);
    await read();
    return items;
  }

  return { read, write, merge };
}

function installSldbAnnotations(config, fetchImpl) {
  if (!config.server || !config.doc || typeof annoWriteStore !== 'function') return null;
  const store = sldbAnnotationsStore(config, fetchImpl);
  const keepLocal = annoWriteStore;
  let queue = Promise.resolve();
  globalThis.annoWriteStore = function (items) {
    keepLocal(items);
    queue = queue
      .then(() => store.write(items))
      .then(saved => { if (saved !== items) { keepLocal(saved); annoRender(); } })
      .catch(error => console.warn('[specir] annotations not saved in sldb:', error.message));
    return queue;
  };
  globalThis.annoLoad = function () {
    return store.read()
      .then(items => { keepLocal(items); annoRender(); })
      .catch(error => {
        console.warn('[specir] annotations not read from sldb, using the local copy:', error.message);
        annoCache = annoReadStore();
        annoRender();
      });
  };
  return store;
}

installSldbAnnotations(sldbAnnotationsConfig(window.SPECIR_ANNOTATIONS, (globalThis.location || {}).search), globalThis.fetch && globalThis.fetch.bind(globalThis));
// </sldb-annotations>

FILE:src/specir/visual/notation_style.py
"""Style resolution and the error root of sldb's notations, taken from SLDB, never defined here.

The renderers color elements with the one precedence that sldb owns (glyph > `style.kinds` of the
spec > palette, `sldb.notations.resolve_style`) and write text in the ink of sldb's builtin
`default` palette (`sldb.notations.load_palette`). The commands report sldb's loading and
validation errors (`sldb.notations.NotationError`, the root of `ParseError` and `ValidationError`).
The catalog (IR13b) reports the typed errors of the catalog path rule (`AmbiguousPathError`,
`UnknownReferenceError`, `UnknownNotationError`) and picks a view's notation with
`DEFAULT_NOTATIONS` and `builtin_notations`.
`sldb.api` does not export these yet (asked to sldb's desk), so this module is the only one of
specIR that reaches `sldb.notations` (tests/test_imports.py allows it here and nowhere else). When
sldb exports them from `sldb.api.notations`, only these imports change."""

from __future__ import annotations

from functools import lru_cache

from sldb.notations import (
    DEFAULT_NOTATIONS,
    AmbiguousPathError,
    NotationError,
    UnknownNotationError,
    UnknownReferenceError,
    builtin_notations,
    load_palette,
    resolve_style,
)


@lru_cache(maxsize=1)
def default_ink() -> dict[str, str]:
    """The text color (`{light, dark}`) of sldb's builtin `default` palette."""
    return load_palette().ink.model_dump()


__all__ = [
    "DEFAULT_NOTATIONS", "AmbiguousPathError", "NotationError", "UnknownNotationError", "UnknownReferenceError",
    "builtin_notations", "default_ink", "resolve_style",
]

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
D1)."""

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
from specir.visual.normalize import differences, equivalent, normalize
from specir.visual.projections import component_from_view, from_spec_doc, state_from_view, view_graph
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
]

FILE:tests/visual/test_catalog.py
"""spec2viz's catalog tests, ported to specIR's catalog (IR13b) and to sldb's catalog operations.

Ported from spec2viz `2de1056` (`tests/test_catalog_paths.py`, `tests/test_catalog_notation.py`,
the catalog build cases of `tests/test_catalog_resolved_views.py`, `tests/test_deskops.py`,
`tests/test_atoms_matching.py`, the build cases of `tests/test_explicit_atoms.py` and the
`build`/`catalog build` cases of `tests/test_cli.py`). What changes, and why:

- `catalog validate` and `catalog sync` are sldb's now: `sldb notations sync --catalog [--check]`
  (D1), run as the real CLI. The path rule is `sldb.api.notations.catalog_paths`.
- `catalog build` is `specir.visual.catalog.render_catalog`/`build_catalog`; the command and its
  `build` alias are IR13d's, so the CLI cases run on the API: "Rendered catalog" and "Error building
  catalog" were the command's messages, the build's error is the exception it raises.
- The atoms are matched by `sldb.api.matching` (D4): warnings are sldb findings, strict mode raises
  sldb's `UnknownAtomError`. Where spec2viz faked a store with monkeypatch, a real sldb store is used.
- spec2viz monkeypatched its scratch store or its resolver to prove the project store is used or that
  the build falls back to `src`; here the project store is made unusable for the scratch path (a
  notation that only lives there) and a sequence spec (not a graph) shows the fallback."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import sldb.api as sldb_api
import yaml
from sldb.api.matching import UnknownAtomError, filter_atoms_payload, parse_atoms
from sldb.api.notations import SpecSync, catalog_entries, sync_catalog
from sldb.api.notations.catalog_paths import candidates, repo_root, resolve_catalog_path

from specir.visual.catalog import build_catalog, render_catalog, resolve_item_path, split_shared_atoms
from specir.visual.notation_style import AmbiguousPathError, UnknownNotationError, UnknownReferenceError

HERE = Path(__file__).resolve().parent
SPECS = HERE / "fixtures" / "spec2viz" / "tests" / "fixtures"
ARCH_SPECS = HERE / "fixtures" / "spec2viz" / "docs" / "architecture" / "spec2viz"
TEMPLATE = Path(__file__).resolve().parents[2] / "src" / "specir" / "visual" / "templates" / "default.html"
SLDB = str(Path(sys.executable).with_name("sldb"))
NOTATION = {"name": "flow-own", "diagram_type": "activity", "glyphs": [{"id": "step", "model": "SpecNodeDoc", "shape": "box"}],
            "links": [{"id": "next", "relation": "next"}]}
OWN_NOTATION = {**NOTATION, "title": "Own flow", "layout": {"kind": "graph"}}
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node runs the template's code")


def sldb_cli(*args, cwd: Path | None = None) -> tuple[int, str]:
    done = subprocess.run([SLDB, *map(str, args)], capture_output=True, text=True, cwd=cwd)
    return done.returncode, done.stdout + done.stderr


def check(config: Path, store: Path | None = None) -> tuple[int, str]:
    """`catalog validate` of spec2viz: `sldb notations sync --catalog <config> --check`."""
    return sldb_cli("notations", "sync", "--catalog", config, "--check", *(["--store", store] if store else []))


def sync(config: Path, store: Path) -> tuple[int, str]:
    """`catalog sync` of spec2viz: `sldb notations sync --catalog <config> --store <store>`."""
    return sldb_cli("notations", "sync", "--catalog", config, "--store", store)


def spec_docs(store: Path) -> list:
    return [d for d in sldb_api.load_runtime_documents(store, None, include_linked=False) if str(d.model_name) == "SpecDoc"]


# --- tests/test_catalog_paths.py ----------------------------------------------------------------

def _repo(tmp_path):
    """repo/ with .git; the registry in repo/docs/architecture/vistas.yml."""
    root = tmp_path / "repo"
    arch = root / "docs" / "architecture"
    (root / ".git").mkdir(parents=True)
    (arch / "flows").mkdir(parents=True)
    (arch / "notations").mkdir()
    shutil.copy(SPECS / "activity.lanes.yml", arch / "flows" / "lanes.yml")
    (arch / "notations" / "flow-own.yml").write_text(yaml.safe_dump(NOTATION), encoding="utf-8")
    (arch / "flows" / "lanes.mmd").write_text("flowchart TD\n  a --> b\n", encoding="utf-8")
    return root, arch


def _vistas(arch, **view):
    vista = {"id": "lanes", "category": "Flujos", "nav": "Carriles", **view}
    (arch / "vistas.yml").write_text(yaml.safe_dump({"vistas": [vista]}), encoding="utf-8")
    return arch / "vistas.yml"


def test_repo_root_and_candidates(tmp_path):
    root, arch = _repo(tmp_path)
    assert repo_root(arch) == root.resolve()
    assert candidates("x/y.yml", arch) == [(arch / "x/y.yml").resolve(), (root / "x/y.yml").resolve()]
    assert candidates("x/y.yml", root) == [(root / "x/y.yml").resolve()]


@pytest.mark.parametrize("specs, notation, src", [
    ("flows/lanes.yml", "notations/flow-own.yml", "flows/lanes.mmd"),
    ("docs/architecture/flows/lanes.yml", "docs/architecture/notations/flow-own.yml", "docs/architecture/flows/lanes.mmd"),
])
def test_the_three_fields_resolve_both_ways(tmp_path, specs, notation, src):
    root, arch = _repo(tmp_path)
    config = _vistas(arch, specs=[specs], notation=notation, src=src)
    rc, output = check(config)
    assert rc == 0, output
    entry = catalog_entries(config)[0]
    assert entry["spec"] == (arch / "flows" / "lanes.yml").resolve()
    assert entry["notation"] == (arch / "notations" / "flow-own.yml").resolve()
    assert entry["src"] == (arch / "flows" / "lanes.mmd").resolve() and entry["errors"] == []


def test_reported_case_root_relative_notation_is_not_doubled(tmp_path):
    root, arch = _repo(tmp_path)
    config = _vistas(arch, specs=["docs/architecture/flows/lanes.yml"], notation="docs/architecture/notations/flow-own.yml")
    rc, output = check(config)
    assert rc == 0 and "docs/architecture/docs/architecture" not in output


@pytest.mark.parametrize("field", ["specs", "notation", "src"])
def test_two_different_files_are_ambiguous_in_validate_and_sync(tmp_path, field):
    root, arch = _repo(tmp_path)
    sldb_api.init_store(root)
    rel = {"specs": "flows/lanes.yml", "notation": "notations/flow-own.yml", "src": "flows/lanes.mmd"}[field]
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text((arch / rel).read_text(encoding="utf-8") + "\n# otra copia\n", encoding="utf-8")
    config = _vistas(arch, specs=["flows/lanes.yml"], notation="notations/flow-own.yml", src="flows/lanes.mmd")
    for command in (check, sync):
        rc, output = command(config, root / ".sldb")
        assert rc == 1 and "AmbiguousPathError" in output, (command.__name__, output)
        assert str((arch / rel).resolve()) in output and str((root / rel).resolve()) in output
    assert not spec_docs(root / ".sldb")


def test_same_file_both_ways_is_not_ambiguous(tmp_path):
    root, arch = _repo(tmp_path)
    (root / "flows").symlink_to(arch / "flows", target_is_directory=True)
    assert resolve_catalog_path("flows/lanes.yml", arch, "spec") == (arch / "flows" / "lanes.yml").resolve()


@pytest.mark.parametrize("field, value, error", [
    ("specs", "flows/missing.yml", "UnknownReferenceError"),
    ("notation", "notations/missing.yml", "UnknownNotationError"),
    ("src", "flows/missing.mmd", "UnknownReferenceError"),
])
def test_not_found_lists_the_paths_tried(tmp_path, field, value, error):
    root, arch = _repo(tmp_path)
    config = _vistas(arch, **{"specs": ["flows/lanes.yml"], field: [value] if field == "specs" else value})
    rc, output = check(config)
    assert rc == 1 and error in output and "tried:" in output
    assert str((arch / value).resolve()) in output and str((root / value).resolve()) in output


def test_missing_src_does_not_block_sync_but_ambiguity_does(tmp_path):
    root, arch = _repo(tmp_path)
    sldb_api.init_store(root)
    rc, output = sync(_vistas(arch, specs=["flows/lanes.yml"], src="flows/missing.mmd"), root / ".sldb")
    assert rc == 0, output


def test_resolver_types(tmp_path):
    root, arch = _repo(tmp_path)
    with pytest.raises(UnknownNotationError, match="tried:"):
        resolve_catalog_path("nope.yml", arch, "notation", UnknownNotationError)
    with pytest.raises(UnknownReferenceError):
        resolve_catalog_path("nope.yml", arch, "spec")
    (root / "flows").mkdir()
    (root / "flows" / "lanes.yml").write_text("id: other\n", encoding="utf-8")
    with pytest.raises(AmbiguousPathError):
        resolve_catalog_path("flows/lanes.yml", arch, "spec")


def test_catalog_build_reads_src_with_the_same_rule(tmp_path):
    root, arch = _repo(tmp_path)
    assert resolve_item_path("docs/architecture/flows/lanes.mmd", arch, "src") == (arch / "flows" / "lanes.mmd").resolve()
    (root / "flows").mkdir()
    (root / "flows" / "lanes.mmd").write_text("flowchart LR\n", encoding="utf-8")
    with pytest.raises(AmbiguousPathError):
        resolve_item_path("flows/lanes.mmd", arch, "src")


# --- tests/test_catalog_notation.py -------------------------------------------------------------

def _notation_project(tmp_path, view_notation=None):
    sldb_api.init_store(tmp_path)
    docs = tmp_path / "docs"
    (docs / "notations").mkdir(parents=True)
    shutil.copy(SPECS / "activity.lanes.yml", docs / "lanes.yml")
    (docs / "notations" / "flow-own.yml").write_text(yaml.safe_dump(OWN_NOTATION), encoding="utf-8")
    vista = {"id": "lanes", "category": "Flujos", "nav": "Carriles", "desc": "Aprobacion", "specs": ["lanes.yml"]}
    if view_notation is not None:
        vista["notation"] = view_notation
    (docs / "vistas.yml").write_text(yaml.safe_dump({"vistas": [vista]}), encoding="utf-8")
    return docs / "vistas.yml"


def _spec_doc(tmp_path):
    return next(d.payload for d in spec_docs(tmp_path / ".sldb") if d.name == "activity.lanes")


def test_diagram_sync_with_notation_keeps_the_catalog_metadata(tmp_path):
    config = _notation_project(tmp_path)
    assert sync(config, tmp_path / ".sldb")[0] == 0
    rc, output = sldb_cli("notations", "sync", "--spec", config.parent / "lanes.yml", "--store", tmp_path / ".sldb",
                          "--notation", config.parent / "notations" / "flow-own.yml")
    assert rc == 0, output
    doc = _spec_doc(tmp_path)
    assert (doc["category"], doc["nav"], doc["summary"]) == ("Flujos", "Carriles", "Aprobacion")
    assert doc["notation"] == "NotationDoc:flow-own"


def test_view_notation_path_is_relative_to_the_vistas_yml(tmp_path):
    config = _notation_project(tmp_path, "notations/flow-own.yml")
    rc, output = sync(config, tmp_path / ".sldb")
    assert rc == 0, output
    doc = _spec_doc(tmp_path)
    assert doc["notation"] == "NotationDoc:flow-own" and doc["category"] == "Flujos"


def test_view_notation_name_resolves_against_the_store(tmp_path):
    config = _notation_project(tmp_path, "flow-own")
    rc, output = sync(config, tmp_path / ".sldb")
    assert rc == 1 and "UnknownNotationError" in output
    assert not spec_docs(tmp_path / ".sldb")  # nothing written
    assert sldb_cli("notations", "sync", "--notation", config.parent / "notations" / "flow-own.yml", "--store", tmp_path / ".sldb")[0] == 0
    rc, output = sync(config, tmp_path / ".sldb")
    assert rc == 0, output
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:flow-own"


def test_view_notation_builtin_name_and_absent_field(tmp_path):
    config = _notation_project(tmp_path, "activity")
    assert sync(config, tmp_path / ".sldb")[0] == 0
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:activity"


@pytest.mark.parametrize("value, error", [
    ("notations/missing.yml", "UnknownNotationError"),
    ("no-such-notation", "UnknownNotationError"),
    ("deployment", "NotationMismatchError"),
])
def test_catalog_validate_and_sync_give_typed_errors(tmp_path, value, error):
    config = _notation_project(tmp_path, value)
    for command in (check, sync):
        rc, output = command(config, tmp_path / ".sldb")
        assert rc == 1 and error in output, (command.__name__, output)
    assert not spec_docs(tmp_path / ".sldb")


def test_catalog_validate_passes(tmp_path):
    config = _notation_project(tmp_path, "notations/flow-own.yml")
    rc, output = check(config, tmp_path / ".sldb")
    assert rc == 0 and "Valid: lanes" in output


def test_a_failing_view_writes_nothing_even_after_valid_ones(tmp_path):
    """IR13b: with one invalid view among valid ones, the catalog sync writes nothing at all."""
    config = _notation_project(tmp_path)
    data = yaml.safe_load(config.read_text(encoding="utf-8"))
    shutil.copy(SPECS / "state.quotation.yml", config.parent / "state.yml")
    data["vistas"].append({"id": "estado", "specs": ["state.yml"], "notation": "activity"})  # wrong type: NotationMismatchError
    config.write_text(yaml.safe_dump(data), encoding="utf-8")
    rc, output = sync(config, tmp_path / ".sldb")
    assert rc == 1 and "NotationMismatchError" in output and "Invalid: estado" in output
    assert not spec_docs(tmp_path / ".sldb")


# --- catalog build cases of tests/test_catalog_resolved_views.py --------------------------------

RESOLVED_NOTATION = {
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


def _resolved_project(tmp_path, view_notation=None):
    root = tmp_path / "repo"
    arch = root / "docs" / "architecture"
    (root / ".git").mkdir(parents=True)
    arch.mkdir(parents=True)
    shutil.copy(SPECS / "deployment.nested.yml", arch / "nested.yml")
    shutil.copy(ARCH_SPECS / "sequence-sync-pipeline.yml", arch / "seq.yml")
    (arch / "seq.mmd").write_text("sequenceDiagram\n  A->>B: hi\n", encoding="utf-8")
    (arch / "nested.mmd").write_text("flowchart TD\n  legacy_src_marker --> x\n", encoding="utf-8")
    (arch / "infra-own.yml").write_text(yaml.safe_dump(RESOLVED_NOTATION, allow_unicode=True), encoding="utf-8")
    vista = {"id": "nested", "title": "Nested", "category": "Infra", "src": "nested.mmd", "specs": ["nested.yml"]}
    if view_notation:
        vista["notation"] = view_notation
    vistas = [vista, {"id": "seq", "title": "Seq", "category": "Flows", "src": "seq.mmd", "specs": ["seq.yml"]}]
    (arch / "vistas.yml").write_text(yaml.safe_dump({"vistas": vistas}), encoding="utf-8")
    return root, arch


def test_catalog_build_draws_graph_views_from_the_view_notation(tmp_path, monkeypatch):
    monkeypatch.setenv("TMPDIR", str(tmp_path / "scratch"))
    (tmp_path / "scratch").mkdir()
    import tempfile
    monkeypatch.setattr(tempfile, "tempdir", None)
    root, arch = _resolved_project(tmp_path, "infra-own.yml")
    page = render_catalog(arch / "vistas.yml")
    assert 'data-resolved-from="SpecDoc:deployment.nested"' in page and 'data-notation="NotationDoc:infra-own"' in page
    assert "legacy_src_marker" not in page and "«database»&lt;br/&gt;Postgres" in page
    # a sequence is not a graph: it keeps its src
    assert "A-&gt;&gt;B: hi" in page and 'data-resolved-from="SpecDoc:sequence' not in page
    assert not list((tmp_path / "scratch").glob("specir-catalog-*"))  # the scratch store is removed


def test_catalog_build_uses_the_builtin_notation_without_the_field(tmp_path):
    root, arch = _resolved_project(tmp_path)
    page = render_catalog(arch / "vistas.yml")
    assert 'data-notation="NotationDoc:deployment"' in page and "«database»" in page


def test_catalog_build_prefers_the_project_store_when_the_spec_is_synced(tmp_path, capsys):
    # a notation that only lives in the project store: the build can only draw it from there
    root, arch = _resolved_project(tmp_path, "infra-own")
    sldb_api.init_store(root)
    page = render_catalog(arch / "vistas.yml")
    assert "legacy_src_marker" in page and "lives only in the store" in capsys.readouterr().err
    assert sldb_cli("notations", "sync", "--notation", arch / "infra-own.yml", "--store", root / ".sldb")[0] == 0
    sync_catalog(SpecSync(root / ".sldb"), arch / "vistas.yml")
    page = render_catalog(arch / "vistas.yml")
    assert 'data-resolved-from="SpecDoc:deployment.nested"' in page and 'data-notation="NotationDoc:infra-own"' in page


def test_catalog_build_falls_back_to_src_when_the_view_does_not_resolve(tmp_path):
    root, arch = _resolved_project(tmp_path)
    data = yaml.safe_load((arch / "vistas.yml").read_text(encoding="utf-8"))
    data["vistas"][0]["specs"] = ["nested.yml", "seq.yml"]  # one spec that is not a graph: the whole view keeps its src
    (arch / "vistas.yml").write_text(yaml.safe_dump(data), encoding="utf-8")
    page = render_catalog(arch / "vistas.yml")
    assert "legacy_src_marker" in page and "data-resolved-from" not in page


# --- tests/test_deskops.py ----------------------------------------------------------------------

def test_parse_atoms_handles_missing_dir(tmp_path):
    assert parse_atoms(tmp_path / "missing") == "{}"


def test_parse_atoms_builds_index_and_skips_bad_files(tmp_path):
    atoms_dir = tmp_path / "atoms"
    atoms_dir.mkdir()
    (atoms_dir / "good.md").write_text("---\ntitle: Architecture\nfive_wh_one_plus: what\nid: atom-1\n---\nBody text.\n", encoding="utf-8")
    (atoms_dir / "bad.md").write_text("---\n: bad yaml\n---\nBroken.\n", encoding="utf-8")
    findings = []
    payload = json.loads(parse_atoms(atoms_dir, findings))
    assert payload["architecture"]["title"] == "Architecture" and "architecture" in payload["architecture"]["aliases"]
    assert payload["architecture"]["atoms"]["what"] == {**payload["architecture"]["atoms"]["what"], "id": "atom-1", "body": "Body text."}
    assert [f.code for f in findings] == ["matching/atom-parse-failed"]


def _sources(base):
    (base / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (base / "diagram.svg").write_text("<svg><text>Diagram</text></svg>", encoding="utf-8")
    (base / "snippet.html").write_text("plain html snippet", encoding="utf-8")
    (base / "matrix.vega.json").write_text('{"$schema": "https://vega.github.io/schema/vega/v5.json", "marks": []}', encoding="utf-8")
    (base / "deploy.puml").write_text("@startuml\nnode A\n@enduml\n", encoding="utf-8")


def test_render_catalog_renders_mermaid_svg_html_and_notes(tmp_path):
    base = tmp_path
    (base / "template.html").write_text(
        "<html><body><nav>{{NAV}}</nav><main>{{SECTIONS}}</main><script>window.ATOMS_DB = {{ATOMS_DB}};</script></body></html>", encoding="utf-8")
    _sources(base)
    atoms_dir = base / "atoms"
    atoms_dir.mkdir()
    (atoms_dir / "atom.md").write_text("---\ntitle: Runtime\nfive_wh_one_plus: why\n---\nBecause reasons.\n", encoding="utf-8")
    (base / "vistas.yml").write_text("""
template: template.html
vistas:
  - {id: flow, category: Core, title: Flow, lbl: Flow label, desc: Flow desc, src: flow.mmd, specs: [spec-a, spec-b], puml: flow.puml, notes: [gap one, gap two]}
  - {id: picture, category: Core, title: Picture, src: diagram.svg}
  - {id: html-view, category: Extras, title: Html View, src: snippet.html}
  - {id: matrix, category: Extras, title: Matrix, src: matrix.vega.json}
  - {id: deploy, category: Extras, title: Deploy, src: deploy.puml}
""", encoding="utf-8")
    html = render_catalog(base / "vistas.yml", atoms_dir=atoms_dir)
    assert re.search(r'<a href="#flow-[a-f0-9]{8}">Flow label</a>', html)
    assert 'data-spec="spec-a"' in html and 'data-spec="spec-b"' in html and 'data-puml="flow.puml"' in html
    assert '<pre class="mermaid">' in html and '<div class="board puml-board">' in html and "plain html snippet" in html
    assert '<div class="board vega-board">' in html and 'class="vega-spec"' in html and "vega.github.io/schema/vega/v5.json" in html
    assert '<pre class="source-board">@startuml' in html
    assert "Gaps de implementación" in html
    assert "window.ATOMS_DB = {}" in html and "window.ATOMS_BY_VIEW" in html and "window.COVERAGE_BY_VIEW" in html
    assert "because reasons." in html.lower()


def test_render_catalog_injects_atoms_before_body_when_placeholder_missing(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (tmp_path / "vistas.yml").write_text("template: template.html\nvistas:\n  - id: flow\n    src: flow.mmd\n", encoding="utf-8")
    html = render_catalog(tmp_path / "vistas.yml", atoms_dir=tmp_path / "missing")
    assert "window.ATOMS_DB = {}" in html and "window.ATOMS_BY_VIEW" in html and "window.COVERAGE_BY_VIEW" in html
    assert html.count("</body>") == 1


def test_coverage_by_view_is_projected_from_the_snapshot_of_the_views_project(tmp_path):
    """test_build_coverage_by_view_projects_snapshot_payload, through the catalog: the snapshot is
    found above the vistas.yml and the view is matched by its `src`."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "view.html").write_text('<section id="d1"><div class="board">x</div></section>', encoding="utf-8")
    (tmp_path / "vistas.yml").write_text("vistas:\n  - {id: view-1, title: View 1, src: docs/view.html#d1, type: component}\n", encoding="utf-8")
    snapshot = tmp_path / ".sldb/runtime/knowledge_graph.kg.json"
    snapshot.parent.mkdir(parents=True)
    element = "diagram_element:view-1:node:runtime"
    snapshot.write_text(json.dumps({"nodes": [
        {"identity": {"node_id": "view:view-1", "node_type": "view"},
         "semantics": {"view_id": "view-1", "diagram_type": "component", "title": "Projected View", "source_ref": "docs/view.html#d1"},
         "edges": [{"target_id": element, "relation_type": "contains", "metadata": {}}]},
        {"identity": {"node_id": element, "node_type": "diagram_element"},
         "semantics": {"view_id": "view-1", "diagram_type": "component", "element_id": "node:runtime", "element_kind": "node", "label": "Runtime"},
         "edges": [{"target_id": "facet:what", "relation_type": "expects_facet", "metadata": {"facet": "what", "source_field": "label"}},
                   {"target_id": "atom:runtime", "relation_type": "covers_facet", "metadata": {
                       "atom_id": "runtime", "facet": "what", "score": 1.0, "match_basis": "title", "evidence": 'label="Runtime" matched atom.title="Runtime"'}}]},
        {"identity": {"node_id": "facet:what", "node_type": "facet"}, "semantics": {"facet": "what"}, "edges": []},
    ]}), encoding="utf-8")
    html = render_catalog(tmp_path / "vistas.yml")
    coverage = json.loads(re.search(r"window\.COVERAGE_BY_VIEW = (\{.*?\}); window\.SPEC2VIZ_ATOM_WARNINGS", html, re.S).group(1))
    (payload,) = coverage.values()
    assert payload["summary"]["elements_fully_covered"] == 1
    assert payload["elements"][0]["covered_facets"][0]["atom_id"] == "runtime" and payload["elements"][0]["missing_facets"] == []
    assert "window.SPEC2VIZ_COVERAGE_WARNINGS = [];" in html


def test_build_catalog_writes_output_file(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("template: template.html\nvistas:\n  - id: flow\n    src: flow.mmd\n", encoding="utf-8")
    out = build_catalog(config, tmp_path / "architecture.html")
    assert out.exists() and "graph TD" in out.read_text(encoding="utf-8")


# --- tests/test_atoms_matching.py ---------------------------------------------------------------

HARNESS = """
const norm = (str) => str ? str.trim().toLowerCase().replace(/\\s+/g, ' ') : '';
const getViewAtomsDb = () => DB;
%s
const [db, text, explicit] = JSON.parse(process.argv[1]);
globalThis.DB = db;
globalThis.window = { ATOMS_EXPLICIT: explicit || {} };
const nodeEl = { closest: () => ({ id: 'v1' }) };
const hit = findAtomData(text, nodeEl);
console.log(JSON.stringify(hit ? (hit.explicit ? hit.list.map(a => a.id) : hit.title) : null));
"""


def _match(db: dict, text: str, explicit: dict | None = None):
    block = re.search(r"// <atom-match>.*?// </atom-match>", TEMPLATE.read_text(encoding="utf-8"), re.S)
    assert block, "the template lacks its <atom-match> block"
    out = subprocess.run(["node", "-e", HARNESS % block.group(0), json.dumps([db, text, explicit])], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def _entry(title, aliases=None):
    return {"title": title, "aliases": aliases or [], "atoms": {"what": {"id": "a", "body": "b"}}}


DB = {
    "evaluacion de ordenes": _entry("Evaluación de órdenes", ["evaluacion de ordenes", "evaluacion", "ordenes"]),
    "homologacion de producto": _entry("Homologación de producto", ["homologacion de producto", "homologacion", "producto"]),
}


@needs_node
class TestTemplateMatching:
    def test_one_shared_word_is_not_a_match(self):
        assert _match(DB, "Cerrar producto vencido") is None
        assert _match(DB, "Revisar ordenes") is None

    def test_unrelated_node_has_no_atom(self):
        assert _match(DB, "Enviar correo al cliente") is None

    def test_exact_title_matches_ignoring_accents_punctuation_case(self):
        assert _match(DB, "Evaluación de órdenes") == "Evaluación de órdenes"
        assert _match(DB, "HOMOLOGACION DE PRODUCTO (R1)") == "Homologación de producto"

    def test_phrase_contained_matches(self):
        assert _match(DB, "Paso: homologacion de producto nuevo") == "Homologación de producto"

    def test_two_shared_tokens_matching_most_of_the_alias(self):
        assert _match(DB, "Evaluacion ordenes") == "Evaluación de órdenes"

    def test_explicit_atoms_win_and_all_are_returned(self):
        explicit = {"v1": {"producto": {"title": "producto", "explicit": True, "list": [
            {"id": "a1", "title": "T", "question": "what", "body": "x"}, {"id": "a2", "title": "T", "question": "what", "body": "y"}]}}}
        assert _match(DB, "Producto", explicit) == ["a1", "a2"]

    def test_node_without_explicit_falls_back_to_fuzzy(self):
        explicit = {"v1": {"otro": {"title": "otro", "explicit": True, "list": [{"id": "a1", "title": "T", "question": "what", "body": "x"}]}}}
        assert _match(DB, "Evaluación de órdenes", explicit) == "Evaluación de órdenes"


def _norm_keys(texts: list[str]) -> list[str]:
    """The template's own `normKey` (with its `norm`) over `texts`, run by node."""
    src = TEMPLATE.read_text(encoding="utf-8")
    code = "".join(re.search(rf"    function {name}\(str\) \{{.*?\n    \}}\n", src, re.S).group(0) for name in ("norm", "normKey"))
    out = subprocess.run(["node", "-e", code + "console.log(JSON.stringify(JSON.parse(process.argv[1]).map(normKey)));", json.dumps(texts)],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


@needs_node
def test_label_key_of_sldb_is_the_template_s_norm_key():
    """sldb's `label_key` (D4) and the template's `normKey` give the same key (SV-G08)."""
    from sldb.api.matching import label_key

    texts = ["Evaluación de órdenes", "  HOMOLOGACION   DE producto (R1) ", "a-b.c/d", "4 Nueva", "Ñandú 2º", ""]
    assert _norm_keys(texts) == [label_key(t) for t in texts]


@needs_node
@pytest.mark.xfail(strict=True, reason="sldb's label_key keeps '_' (\\w) and normKey does not: asked to sldb's desk (matching/label-key-underscore)")
def test_label_key_of_sldb_splits_underscores_like_norm_key():
    """An element without a label is drawn with its id: `post_published` must key the same in both."""
    from sldb.api.matching import label_key

    assert _norm_keys(["post_published"]) == [label_key("post_published")]


def _two_atoms(tmp_path):
    d = tmp_path / "atoms"
    d.mkdir()
    for i, (title, tags) in enumerate([("Uno", ["dominio:oc"]), ("Dos", ["dominio:stock"])]):
        (d / f"a{i}.md").write_text(f"---\ntitle: {title}\nfive_wh_one_plus: what\nid: a{i}\ntags: {json.dumps(tags)}\n---\nCuerpo {i}.\n", encoding="utf-8")
    return d


def test_filter_atoms_payload_by_full_tag_or_value(tmp_path):
    payload = json.loads(parse_atoms(_two_atoms(tmp_path)))
    assert set(filter_atoms_payload(payload, ["dominio:oc"])) == {"uno"}
    assert set(filter_atoms_payload(payload, ["stock"])) == {"dos"}
    assert set(filter_atoms_payload(payload, None)) == {"uno", "dos"}
    assert filter_atoms_payload(payload, ["nada"]) == {}


def test_split_shared_atoms_emits_repeated_payload_once():
    p = {"x": {"title": "X", "atoms": {}}}
    shared, rest = split_shared_atoms({"v1": p, "v2": p, "v3": {}, "v4": {"y": {}}})
    assert shared == p and set(rest) == {"v3", "v4"}
    assert split_shared_atoms({"v1": p}) == ({}, {"v1": p})


def test_catalog_build_embeds_atoms_once_and_honors_atoms_tag(tmp_path):
    atoms = _two_atoms(tmp_path)
    (tmp_path / "f.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    cfg = tmp_path / "vistas.yml"
    cfg.write_text("vistas:\n" + "".join(f"  - id: v{i}\n    title: V{i}\n    src: f.mmd\n    type: mermaid\n" for i in range(3)), encoding="utf-8")
    html = render_catalog(cfg, atoms_dir=atoms)
    assert html.count("Cuerpo 0.") == 1 and html.count("Cuerpo 1.") == 1
    html = render_catalog(cfg, atoms_dir=atoms, atoms_tags=["dominio:oc"])
    assert "Cuerpo 0." in html and "Cuerpo 1." not in html


MD_HARNESS = """
const escapeHtmlUnused = null;
%s
const [body, known] = JSON.parse(process.argv[1]);
console.log(JSON.stringify(renderAtomBody(body, id => known[id] || null)));
"""


def _md(body: str, known: dict | None = None) -> str:
    block = re.search(r"// <atom-md>.*?// </atom-md>", TEMPLATE.read_text(encoding="utf-8"), re.S)
    assert block
    out = subprocess.run(["node", "-e", MD_HARNESS % block.group(0), json.dumps([body, known or {}])], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


@needs_node
class TestAtomMarkdown:
    def test_html_is_escaped(self):
        html = _md('<script>alert(1)</script> & "x"')
        assert "<script>" not in html and "&lt;script&gt;" in html and "&amp;" in html

    def test_inline_formatting(self):
        html = _md("**fuerte** y *suave* y `cod <b>`")
        assert "<strong>fuerte</strong>" in html and "<em>suave</em>" in html and "<code>cod &lt;b&gt;</code>" in html

    def test_paragraphs_breaks_and_lists(self):
        html = _md("uno\ndos\n\n- a\n- b")
        assert "<p>uno<br>dos</p>" in html and "<ul><li>a</li><li>b</li></ul>" in html

    def test_external_link_only_safe_schemes(self):
        assert 'href="https://x.cl/a"' in _md("[t](https://x.cl/a)")
        assert "<a " not in _md("[t](javascript:alert(1))")

    def test_atom_link_present_and_absent(self):
        known = {"a-1": {"id": "a-1", "title": "Plazo <48h>", "question": "what", "body": "x"}}
        html = _md("ver [[a-1]]", known)
        assert 'data-atom-id="a-1"' in html and "Plazo &lt;48h&gt;" in html
        html = _md("ver [[a-9]]", known)
        assert "atom-link-missing" in html and "data-atom-id" not in html and ">a-9<" in html

    def test_predicate_link(self):
        known = {"a-1": {"id": "a-1", "title": "Destino", "question": "what", "body": "x"}}
        html = _md("[depende de:: [[a-1]]]", known)
        assert "<em>depende de</em>: <a" in html and ">Destino</a>" in html


@needs_node
def test_tabs_follow_the_target_atom():
    src = TEMPLATE.read_text(encoding="utf-8")
    block = re.search(r"// <atom-md>.*?// </atom-md>", src, re.S).group(0)
    code = block + """
const target = { id: 't', title: 'Etapa', question: 'what' };
console.log(JSON.stringify([atomTabLabels([target], false), atomTabLabels([{question:'how_not',title:'T'}], true)]));
"""
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True)
    assert json.loads(out.stdout) == [["what"], ["how not · T"]]
    assert "showAtoms([target], false)" in src


# --- build cases of tests/test_explicit_atoms.py ------------------------------------------------

def _atom(d: Path, atom_id: str, title: str, q="what"):
    (d / f"{atom_id}.md").write_text(f"---\ntitle: {title}\nfive_wh_one_plus: {q}\nid: {atom_id}\n---\nCuerpo de {atom_id}.\n", encoding="utf-8")


def _explicit_project(tmp_path, state_atoms_a, state_atoms_b):
    atoms = tmp_path / "atoms"
    atoms.mkdir()
    _atom(atoms, "atom-uno", "Uno")
    _atom(atoms, "atom-dos", "Dos", "why")
    _atom(atoms, "atom-ruido", "Otro tema")
    spec = {
        "id": "ciclo", "title": "Ciclo", "type": "state", "version": "1.0",
        "data": {"entity": "OC", "initial": "nueva", "transitions": [{"from": "nueva", "to": "cerrada", "on": "cierra"}], "states": [
            {"id": "nueva", "label": "4 Nueva", **({"atoms": state_atoms_a} if state_atoms_a is not None else {})},
            {"id": "cerrada", "label": "Cerrada", **({"atoms": state_atoms_b} if state_atoms_b is not None else {})}]},
    }
    (tmp_path / "ciclo.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    (tmp_path / "f.mmd").write_text("stateDiagram-v2\n  nueva --> cerrada\n", encoding="utf-8")
    (tmp_path / "vistas.yml").write_text("vistas:\n  - id: v1\n    title: V1\n    src: f.mmd\n    type: state\n    specs: [ciclo.yml]\n", encoding="utf-8")
    return atoms


def _explicit(html):
    data = json.loads(re.search(r"window\.ATOMS_EXPLICIT = (\{.*?\}); window\.ATOMS_LINKED", html, re.S).group(1))
    assert len(data) == 1
    return {"v1": next(iter(data.values()))}


def test_build_exposes_explicit_map_by_label_and_id(tmp_path):
    atoms = _explicit_project(tmp_path, ["atom-uno", "atom-dos"], None)
    view = _explicit(render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms))["v1"]
    assert [a["id"] for a in view["4 nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert [a["id"] for a in view["nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert "cerrada" not in view


def test_unknown_atom_is_warning_unless_strict(tmp_path, capsys):
    atoms = _explicit_project(tmp_path, ["atom-uno", "no-existe"], None)
    html = render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms)
    warnings = json.loads(re.search(r"SPEC2VIZ_ATOM_WARNINGS = (\[.*?\]);", html).group(1))
    # one per key of the element (its label and its id), as in spec2viz
    assert sorted((w["level"], w["code"], w["subject"].split("#")[1]) for w in warnings) == [
        ("warning", "matching/unknown-atom", "4 nueva"), ("warning", "matching/unknown-atom", "nueva")]
    assert all("no-existe" in w["what"] for w in warnings)
    assert "no-existe" in capsys.readouterr().err
    assert [a["id"] for a in _explicit(html)["v1"]["4 nueva"]["list"]] == ["atom-uno"]
    with pytest.raises(UnknownAtomError, match="no-existe"):
        render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms, strict_atoms=True)


def test_fully_explicit_view_embeds_no_fuzzy_payload(tmp_path):
    atoms = _explicit_project(tmp_path, ["atom-uno"], ["atom-dos"])
    html = render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms)
    assert "Cuerpo de atom-ruido." not in html
    assert "Cuerpo de atom-uno." in html and "Cuerpo de atom-dos." in html


def test_partially_explicit_view_keeps_fuzzy_payload(tmp_path):
    atoms = _explicit_project(tmp_path, ["atom-uno"], None)
    assert "Cuerpo de atom-ruido." in render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms)


def test_atoms_linked_from_explicit_are_embedded_one_level(tmp_path):
    atoms = _explicit_project(tmp_path, ["atom-uno"], ["atom-dos"])
    (atoms / "atom-uno.md").write_text("---\ntitle: Uno\nfive_wh_one_plus: what\nid: atom-uno\n---\nVer [depende:: [[atom-ruido]]] y [[atom-lejano]].\n", encoding="utf-8")
    _atom(atoms, "atom-lejano", "Lejano")
    (atoms / "atom-ruido.md").write_text("---\ntitle: Otro tema\nfive_wh_one_plus: what\nid: atom-ruido\n---\nSigue [[atom-lejano2]].\n", encoding="utf-8")
    _atom(atoms, "atom-lejano2", "Nivel dos")
    html = render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms)
    linked = json.loads(re.search(r"window\.ATOMS_LINKED = (\{.*?\}); window\.REFS_EXPLICIT", html, re.S).group(1))
    assert set(linked) == {"atom-ruido", "atom-lejano"}


# --- build cases of tests/test_cli.py -----------------------------------------------------------

def _simple(tmp_path, template="<html><body>{{NAV}}{{SECTIONS}}</body></html>"):
    (tmp_path / "template.html").write_text(template, encoding="utf-8")
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("template: template.html\nvistas:\n  - id: sample\n    src: view.mmd\n", encoding="utf-8")
    return config


def test_catalog_build_alias_matches_legacy_build(tmp_path):
    """The `build` alias is IR13d's; on the API, building twice gives the same page."""
    config = _simple(tmp_path, "<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>")
    legacy = build_catalog(config, tmp_path / "legacy.html")
    grouped = build_catalog(config, tmp_path / "grouped.html")
    assert legacy.read_text(encoding="utf-8") == grouped.read_text(encoding="utf-8")


def test_build_command(tmp_path):
    out = build_catalog(_simple(tmp_path), tmp_path / "out.html")
    assert out.exists() and "catalog-search" in out.read_text(encoding="utf-8")


COMPONENT_SPEC = "id: spec-component\ntitle: Example\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n"
LOCAL_TEMPLATE = "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>"


def test_build_command_supports_store_of_stores(tmp_path):
    child = tmp_path / "child"
    child.mkdir()
    (tmp_path / "template.html").write_text(LOCAL_TEMPLATE, encoding="utf-8")
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-component.yml").write_text(COMPONENT_SPEC, encoding="utf-8")
    (child / "vistas.yml").write_text("template: unused.html\nvistas:\n  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n"
                                      "    nav: Sample\n    desc: Demo child vista\n    src: view.mmd\n    specs:\n      - spec-component\n", encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\ntitle: Repo Catalog\nbrand_name: Diagram Catalog\nstores:\n"
                                          "  - path: child/vistas.yml\n    project: demo/project\n    tags:\n      - domain:crm\n", encoding="utf-8")
    html = build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    for text in ("Repo Catalog", "Diagram Catalog", "catalog-search", 'data-project="demo/project"', 'data-type="component"', "domain:crm", "Sample Diagram"):
        assert text in html, text


def test_build_command_supports_brand_subtitle_in_builtin_template(tmp_path):
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (tmp_path / "spec-component.yml").write_text(COMPONENT_SPEC, encoding="utf-8")
    (tmp_path / "catalog.yml").write_text(
        "template: missing-template.html\ntitle: Repo Catalog\nbrand_name: Diagram Catalog\nbrand_subtitle: Repo subtitle from config\nvistas:\n"
        "  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n    src: view.mmd\n    specs:\n      - spec-component.yml\n", encoding="utf-8")
    html = build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    assert "Repo subtitle from config" in html and "Visor transversal de diagramas de spec2viz" not in html


def test_build_command_warns_on_local_template_override(tmp_path, capsys):
    (tmp_path / "template.html").write_text(LOCAL_TEMPLATE, encoding="utf-8")
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (tmp_path / "spec-component.yml").write_text(COMPONENT_SPEC, encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\nvistas:\n  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n"
                                          "    src: view.mmd\n    specs:\n      - spec-component.yml\n", encoding="utf-8")
    build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html")
    assert "using local catalog template override" in capsys.readouterr().err


def test_build_command_supports_project_yml_envelope(tmp_path):
    child = tmp_path / "child"
    child.mkdir()
    (tmp_path / "template.html").write_text(LOCAL_TEMPLATE, encoding="utf-8")
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-state.yml").write_text(
        "id: spec-state\ntitle: Example State\ntype: state\nversion: '1.0'\ndata:\n  entity: X\n  initial: a\n  states:\n    - id: a\n      label: A\n  transitions: []\n",
        encoding="utf-8")
    (child / "vistas.yml").write_text("template: ../template.html\nvistas:\n  - id: sample-state\n    category: Estados\n    title: State Diagram\n"
                                      "    nav: State\n    desc: Demo leaf\n    src: view.mmd\n    specs:\n      - spec-state.yml\n", encoding="utf-8")
    (tmp_path / "project.yml").write_text(
        "diagram_store:\n  kind: diagram-store\n  template: template.html\n  title: Project Catalog\n  brand_name: Project Brand\n"
        "  project_name: project/demo\n  stores:\n    - path: child/vistas.yml\n      project: project/demo\n      tags:\n        - domain:workflow\n",
        encoding="utf-8")
    html = build_catalog(tmp_path / "project.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    for text in ("Project Catalog", "Project Brand", "project/demo", "domain:workflow", 'data-type="state"'):
        assert text in html, text


def test_build_command_extracts_types_from_specs_dir_and_makes_anchor_ids_unique(tmp_path):
    (tmp_path / "template.html").write_text("<html><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>", encoding="utf-8")
    for folder in [tmp_path / "alpha" / "docs" / "vistas", tmp_path / "beta" / "docs" / "vistas"]:
        folder.mkdir(parents=True)
        project = folder.parent.parent
        (project / "project.yaml").write_text("project_name: Demo\nclient: sample\n", encoding="utf-8")
        (project / "specs").mkdir(exist_ok=True)
        (project / "specs" / "same-view.yml").write_text(COMPONENT_SPEC.replace("spec-component", "same-view"), encoding="utf-8")
        (project / "rendered").mkdir(exist_ok=True)
        (project / "rendered" / "same-view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
        (folder / "vistas.yml").write_text("template: template.html\nvistas:\n  - id: vista01\n    title: Demo\n    category: Arquitectura\n"
                                           "    specs:\n      - same-view\n    mmd: ../../rendered/same-view.mmd\n", encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\nstores:\n  - path: alpha/docs/vistas/vistas.yml\n  - path: beta/docs/vistas/vistas.yml\n", encoding="utf-8")
    html = build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    assert html.count('data-type="component"') == 2
    assert len(set(re.findall(r'id="(sample-demo-vista01-[a-f0-9]{8})"', html))) == 2


def test_build_command_extracts_html_section_fragments(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "bundle.html").write_text(
        "<html><body><section id=\"d1\"><div class=\"board\"><pre class=\"mermaid\">graph TD\\nA-->B</pre></div></section></body></html>", encoding="utf-8")
    (tmp_path / "catalog.yml").write_text(
        "template: template.html\nitems:\n  - id: frag\n    title: Fragment\n    src: bundle.html#d1\n    type: component\n    category: Arquitectura\n", encoding="utf-8")
    html = build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    assert "bundle.html#d1" not in html
    assert '<div class="board"><pre class="mermaid">graph TD\\nA-->B</pre></div>' in html


def test_build_command_reports_errors(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("template: template.html\nvistas: [\n  {id: broken, src: missing.mmd}\n]\n", encoding="utf-8")
    with pytest.raises(FileNotFoundError, match="missing.mmd"):
        build_catalog(config, tmp_path / "out.html")
    assert not (tmp_path / "out.html").exists()


# --- the built page opens without missing resources (IR13b) -------------------------------------

FIXTURE_TREE = HERE / "fixtures" / "catalog"


def fixture_repo(tmp_path: Path) -> Path:
    """spec2viz's catalog fixtures (its `docs/architecture/` and `examples/catalog/`) in a repo of their own."""
    root = tmp_path / "spec2viz-repo"
    shutil.copytree(FIXTURE_TREE, root)
    (root / ".git").mkdir()
    return root


@pytest.mark.parametrize("config", ["docs/architecture/vistas.yml", "examples/catalog/project.yml"])
def test_the_built_catalog_opens_without_missing_resources(tmp_path, config):
    root = fixture_repo(tmp_path)
    page = build_catalog(root / config, tmp_path / "catalog.html").read_text(encoding="utf-8")
    ids = set(re.findall(r'\sid="([^"]+)"', page))
    for kind, ref in re.findall(r'\s(src|href)="([^"$]*)"', page):
        if ref.startswith("https://") or ref == "#":
            continue
        assert ref.startswith("#") and ref[1:] in ids, (kind, ref)  # nothing next to the page is needed
    assert '<div class="nav-category">' in page and '<div class="catalog-toolbar">' in page and "window.ATOMS_BY_VIEW" in page
    sections = re.findall(r'<section id="([^"]+)"', page)
    assert sections and all(f'href="#{anchor}"' in page for anchor in sections)

FILE:tests/visual/test_catalog_parity.py
"""specIR's catalog against spec2viz's, as the development oracle (IR13b; `parity` marker, skipped
without spec2viz).

- Validating a registry: sldb's `check_catalog` (what `sldb notations sync --catalog --check` runs)
  gives, entry by entry, the same view, spec, error class and message as spec2viz's, over the
  registries of spec2viz's catalog path and notation tests and its own `docs/architecture/vistas.yml`.
- Syncing a registry: `sldb notations sync --catalog` leaves the same documents as `spec2viz catalog
  sync` (IR13a's comparison), and with one failing view neither writes anything.
- Building the catalog: `render_catalog` gives spec2viz's page byte for byte over spec2viz's catalog
  fixtures and the cases of its tests (sources of every kind, stores of stores, `project.yml`,
  fragments, resolved views, atoms from a folder, explicit atoms and refs, atoms of a view's store,
  coverage from a snapshot). One declared difference: the atom and coverage warnings are sldb
  findings (`level`, `code`, `subject`, `what`, `fix`) where spec2viz wrote `{scope, message}`;
  they are compared by their text. So the same views, categories, navigation, atoms per element
  (`ATOMS_EXPLICIT`, `ATOMS_LINKED`, `ATOMS_BY_VIEW`, `ATOMS_DB`, `REFS_EXPLICIT`) and coverage per
  view (`COVERAGE_BY_VIEW`) are embedded."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import pytest
import sldb.api as sldb_api
import yaml
from sldb.api.notations import SpecSync, check_catalog, sync_catalog

from specir.visual.catalog import render_catalog
from test_catalog import (
    NOTATION, OWN_NOTATION, RESOLVED_NOTATION, SPECS, _explicit_project, _repo, _resolved_project, _simple, _sources, _two_atoms, _vistas,
    fixture_repo, sldb_cli, spec_docs,
)
from test_sync_generation_parity import _assert_same_store

pytestmark = pytest.mark.parity
spec2viz = pytest.importorskip("spec2viz")

WARNINGS = re.compile(r"window\.SPEC2VIZ_(ATOM|COVERAGE)_WARNINGS = (\[.*?\]); ")


def _ours(entry, exc):
    return (entry["vista"], Path(entry["spec"]).name, type(exc).__name__ if exc else None, str(exc) if exc else None)


def _same_check(config: Path, store: Path | None = None) -> list:
    from spec2viz.sldb_sync import check_catalog as oracle

    ours = [_ours(entry, exc) for entry, exc in check_catalog(config, store)]
    assert ours == [_ours(entry, exc) for entry, exc in oracle(config, store)]
    return ours


# --- validating a registry ----------------------------------------------------------------------

@pytest.mark.parametrize("view", [
    {"specs": ["flows/lanes.yml"], "notation": "notations/flow-own.yml", "src": "flows/lanes.mmd"},
    {"specs": ["docs/architecture/flows/lanes.yml"], "notation": "docs/architecture/notations/flow-own.yml"},
    {"specs": ["flows/missing.yml"]},
    {"specs": ["flows/lanes.yml"], "notation": "notations/missing.yml"},
    {"specs": ["flows/lanes.yml"], "src": "flows/missing.mmd"},
    {"specs": ["flows/lanes.yml"], "notation": "no-such-notation"},
    {"specs": ["flows/lanes.yml"], "notation": "deployment"},
    {"specs": ["flows/lanes.yml"], "notation": "activity"},
])
def test_check_catalog_reports_what_spec2viz_reports(tmp_path, view):
    root, arch = _repo(tmp_path)
    _same_check(_vistas(arch, **view))


@pytest.mark.parametrize("field", ["specs", "notation", "src"])
def test_check_catalog_reports_ambiguity_like_spec2viz(tmp_path, field):
    root, arch = _repo(tmp_path)
    rel = {"specs": "flows/lanes.yml", "notation": "notations/flow-own.yml", "src": "flows/lanes.mmd"}[field]
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text((arch / rel).read_text(encoding="utf-8") + "\n# otra copia\n", encoding="utf-8")
    errors = _same_check(_vistas(arch, specs=["flows/lanes.yml"], notation="notations/flow-own.yml", src="flows/lanes.mmd"))
    assert errors[0][2] == "AmbiguousPathError"


def test_check_catalog_of_spec2viz_s_own_registry(tmp_path):
    root = fixture_repo(tmp_path)
    results = _same_check(root / "docs" / "architecture" / "vistas.yml")
    assert len(results) == 11


def test_check_catalog_with_a_store_notation(tmp_path):
    root, arch = _repo(tmp_path)
    sldb_api.init_store(root)
    config = _vistas(arch, specs=["flows/lanes.yml"], notation="flow-own")
    assert _same_check(config, root / ".sldb")[0][2] == "UnknownNotationError"
    (arch / "own.yml").write_text(yaml.safe_dump(OWN_NOTATION), encoding="utf-8")
    assert sldb_cli("notations", "sync", "--notation", arch / "own.yml", "--store", root / ".sldb")[0] == 0
    assert _same_check(config, root / ".sldb")[0][2] is None


# --- syncing a registry -------------------------------------------------------------------------

def _sync_both(tmp_path: Path, config_rel: str) -> tuple[Path, Path]:
    from spec2viz.sldb_sync import SpecSync as OracleSync
    from spec2viz.sldb_sync import sync_catalog as oracle_sync

    roots = []
    for name, sync_class, sync in (("sldb", SpecSync, sync_catalog), ("spec2viz", OracleSync, oracle_sync)):
        root = fixture_repo(tmp_path / name)
        sldb_api.init_store(root)
        sync(sync_class(root / ".sldb"), root / config_rel)
        roots.append(root)
    return roots[0], roots[1]


def test_catalog_sync_leaves_what_spec2viz_leaves(tmp_path):
    ours, oracle = _sync_both(tmp_path, "docs/architecture/vistas.yml")
    _assert_same_store(ours, oracle)
    assert len(spec_docs(ours / ".sldb")) == 11


def test_a_failing_view_makes_both_write_nothing(tmp_path):
    from click.testing import CliRunner
    from spec2viz.cli import main

    outputs = []
    for name in ("sldb", "spec2viz"):
        root = fixture_repo(tmp_path / name)
        sldb_api.init_store(root)
        config = root / "docs" / "architecture" / "vistas.yml"
        data = yaml.safe_load(config.read_text(encoding="utf-8"))
        data["vistas"][-1]["notation"] = "deployment"  # the last view draws with the wrong type
        config.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        if name == "sldb":
            rc, output = sldb_cli("notations", "sync", "--catalog", config, "--store", root / ".sldb")
        else:
            result = CliRunner().invoke(main, ["catalog", "sync", "--config", str(config), "--store", str(root / ".sldb")])
            rc, output = result.exit_code, result.output
        assert rc == 1 and "NotationMismatchError" in output, output
        assert not spec_docs(root / ".sldb")
        outputs.append([line.replace(str(root), "<root>") for line in output.splitlines() if line.startswith("Invalid:")])
    assert outputs[0] == outputs[1]


# --- building the catalog -----------------------------------------------------------------------

def _warnings(page: str) -> tuple[str, list]:
    """The page without its warnings, and the warnings' text (subject or scope, and message)."""
    found = []
    for kind, raw in WARNINGS.findall(page):
        found.append((kind, sorted((w.get("message") or w.get("what"), (w.get("scope") or w.get("subject")).split("#")[0]) for w in json.loads(raw))))
    return WARNINGS.sub(lambda m: f"window.SPEC2VIZ_{m.group(1)}_WARNINGS = <warnings>; ", page), found


def _same_page(config: Path, **options) -> str:
    from spec2viz.deskops import render_deskops

    ours, oracle = render_catalog(config, **options), render_deskops(config, **{k.replace("strict_atoms", "strict_atoms"): v for k, v in options.items()})
    ours_page, ours_warnings = _warnings(ours)
    oracle_page, oracle_warnings = _warnings(oracle)
    assert ours_page == oracle_page
    assert ours_warnings == oracle_warnings
    return ours


@pytest.mark.parametrize("config", ["docs/architecture/vistas.yml", "examples/catalog/project.yml", "examples/catalog/leaves/architecture-vistas.yml"])
def test_the_catalog_of_spec2viz_s_fixtures_is_spec2viz_s(tmp_path, config):
    root = fixture_repo(tmp_path)
    page = _same_page(root / config)
    assert page.count("<section id=") >= 1


def test_the_catalog_of_a_synced_project_is_spec2viz_s(tmp_path):
    root = fixture_repo(tmp_path)
    sldb_api.init_store(root)
    sync_catalog(SpecSync(root / ".sldb"), root / "docs" / "architecture" / "vistas.yml")
    _same_page(root / "docs" / "architecture" / "vistas.yml")


def test_every_kind_of_source_with_atoms_is_spec2viz_s(tmp_path):
    (tmp_path / "template.html").write_text("<html><body><nav>{{NAV}}</nav><main>{{SECTIONS}}</main><script>window.ATOMS_DB = {{ATOMS_DB}};</script></body></html>", encoding="utf-8")
    _sources(tmp_path)
    (tmp_path / "vistas.yml").write_text("""
template: template.html
vistas:
  - {id: flow, category: Core, title: Flow, lbl: Flow label, desc: Flow desc, src: flow.mmd, specs: [spec-a], puml: flow.puml, notes: [gap one]}
  - {id: picture, category: Core, title: Picture, src: diagram.svg, tags: [x:y]}
  - {id: html-view, category: Extras, title: Html View, src: snippet.html}
  - {id: matrix, category: Extras, title: Matrix, src: matrix.vega.json}
  - {id: deploy, category: Extras, title: Deploy, src: deploy.puml}
""", encoding="utf-8")
    atoms = _two_atoms(tmp_path)
    _same_page(tmp_path / "vistas.yml", atoms_dir=atoms)
    _same_page(tmp_path / "vistas.yml", atoms_dir=atoms, atoms_tags=["stock"])


@pytest.mark.parametrize("atoms_a, atoms_b", [(["atom-uno", "atom-dos"], None), (["atom-uno", "no-existe"], None), (["atom-uno"], ["atom-dos"])])
def test_explicit_atoms_are_spec2viz_s(tmp_path, atoms_a, atoms_b):
    atoms = _explicit_project(tmp_path, atoms_a, atoms_b)
    (atoms / "atom-uno.md").write_text("---\ntitle: Uno\nfive_wh_one_plus: what\nid: atom-uno\n---\nVer [[atom-ruido]].\n", encoding="utf-8")
    _same_page(tmp_path / "vistas.yml", atoms_dir=atoms)


def test_strict_atoms_fail_both(tmp_path):
    from spec2viz.deskops import render_deskops

    atoms = _explicit_project(tmp_path, ["no-existe"], None)
    with pytest.raises(Exception, match="no-existe") as ours:
        render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms, strict_atoms=True)
    with pytest.raises(Exception, match="no-existe") as oracle:
        render_deskops(tmp_path / "vistas.yml", atoms_dir=atoms, strict_atoms=True)
    assert type(ours.value).__name__ == type(oracle.value).__name__ == "UnknownAtomError"


@pytest.mark.parametrize("view_notation", [None, "infra-own.yml"])
def test_resolved_views_are_spec2viz_s(tmp_path, view_notation):
    root, arch = _resolved_project(tmp_path, view_notation)
    page = _same_page(arch / "vistas.yml")
    assert "data-resolved-from" in page


def test_stores_of_stores_and_unique_anchors_are_spec2viz_s(tmp_path):
    (tmp_path / "template.html").write_text("<html><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>", encoding="utf-8")
    for folder in [tmp_path / "alpha" / "docs" / "vistas", tmp_path / "beta" / "docs" / "vistas"]:
        folder.mkdir(parents=True)
        project = folder.parent.parent
        (project / "project.yaml").write_text("project_name: Demo\nclient: sample\n", encoding="utf-8")
        (project / "specs").mkdir()
        (project / "specs" / "same-view.yml").write_text("id: same-view\ntitle: Same\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8")
        (project / "rendered").mkdir()
        (project / "rendered" / "same-view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
        (folder / "vistas.yml").write_text("template: template.html\nvistas:\n  - id: vista01\n    title: Demo\n    category: Arquitectura\n"
                                           "    specs:\n      - same-view\n    mmd: ../../rendered/same-view.mmd\n", encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\ncategory: Raiz\ntags: [t:1]\nstores:\n  - path: alpha/docs/vistas/vistas.yml\n"
                                          "  - {path: beta/docs/vistas/vistas.yml, project: otro/p, category: Beta, type: component, tags: [d:x]}\n"
                                          "items:\n  - {id: own, title: Propia, desc: un diagrama de secuencia}\n", encoding="utf-8")
    _same_page(tmp_path / "catalog.yml")


def test_a_fragment_and_a_simple_registry_are_spec2viz_s(tmp_path):
    _same_page(_simple(tmp_path, "<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>"))
    (tmp_path / "bundle.html").write_text('<html><body><section id="d1"><div class="board"><pre class="mermaid">graph TD\\nA-->B</pre></div></section></body></html>', encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\nitems:\n  - id: frag\n    title: Fragment\n    src: bundle.html#d1\n    type: component\n", encoding="utf-8")
    _same_page(tmp_path / "catalog.yml")


# --- atoms of a view's store --------------------------------------------------------------------

MODULE = "ir13b_atom_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class AtomDoc(StructuredNLDoc):
    __template__ = "---\\nid: ⸢rev•id⸥\\ntitle: ⸢rev•title⸥\\nfive_wh_one_plus: ⸢rev•five_wh_one_plus⸥\\ntags: ⸢rev,list•tags⸥\\n---\\n\\n⸢rev•answer⸥"
    id: str = Field(description="Atom id.")
    title: str = Field(description="Title.")
    five_wh_one_plus: str = Field(description="The question.")
    tags: list[str] = Field(default_factory=list, description="Tags.")
    answer: str = Field(description="Body.")
'''


def test_atoms_of_the_view_s_store_and_its_refs_are_spec2viz_s(tmp_path, monkeypatch):
    root = tmp_path / "proj"
    root.mkdir()
    (root / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    monkeypatch.syspath_prepend(str(root))
    sldb_api.init_store(root)
    assert sldb_cli("models", "add", f"{MODULE}:AtomDoc", "--store", root / ".sldb", "--pythonpath", root)[0] == 0
    for atom_id, title, q in (("atom-runtime", "Runtime", "what"), ("atom-core", "Core", "why")):
        sldb_api.create_document(root / ".sldb", "AtomDoc", f"desk/atoms/{atom_id}.md",
                                 {"id": atom_id, "title": title, "five_wh_one_plus": q, "tags": ["dominio:x"], "answer": f"Cuerpo {atom_id}"}, pythonpath=str(root))
    assert sldb_cli("edges", "rebuild", "--store", root / ".sldb", cwd=root)[0] == 0
    docs = root / "docs"
    docs.mkdir()
    spec = {"id": "arq", "title": "Arq", "type": "component", "version": "1.0",
            "data": {"nodes": {"cli": {"label": "CLI", "atoms": ["atom-core"], "refs": ["AtomDoc:atom-runtime", "AtomDoc:no-existe"]}, "core": {"label": "Core"}}, "edges": []}}
    (docs / "arq.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    (docs / "arq.mmd").write_text("graph TD\ncli-->core\n", encoding="utf-8")
    (docs / "vistas.yml").write_text("vistas:\n  - {id: arq, title: Arq, src: arq.mmd, specs: [arq.yml], type: component}\n  - {id: otra, title: Otra, src: arq.mmd}\n", encoding="utf-8")
    monkeypatch.setenv("PYTHONPATH", str(root))
    page = _same_page(docs / "vistas.yml")
    assert "Cuerpo atom-core" in page and '"ref": "AtomDoc:atom-runtime"' in page

FILE:tests/visual/test_catalog_annotations.py
"""The catalog's annotations are saved with `sldb serve` (IR13b, replaces spec2viz's `catalog serve`).

A real store with `CatalogAnnotationsDoc` registered, a real `sldb serve --cors` on a free port
(under `timeout`, closed at the end of each test) and the page's own code run by node: the
template's `annoReadStore`, `annoWriteStore` and `annoLoad`, taken from the built HTML, and the
script the build embeds (`templates/annotations-sldb.js`). Only the DOM is left out (`annoRender`
draws nothing and `localStorage` is a map), because node has none. A reload is a new node process
with an empty `localStorage`: what it shows comes from the store."""

from __future__ import annotations

import json
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest
import sldb.api as api

from specir.visual.catalog import AnnotationsTarget, build_catalog, register_annotations_model, render_catalog
from specir.visual.catalog.annotations import MODEL_NAME, annotations_id, package_pythonpath

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node runs the page's code")

SLDB = str(Path(sys.executable).with_name("sldb"))
DOC = "catalog-annotations-demo"

HARNESS = """
globalThis.window = globalThis;
globalThis.location = { search: process.argv[2] || '' };
const memory = new Map();
globalThis.localStorage = { getItem: k => memory.get(k) ?? null, setItem: (k, v) => memory.set(k, String(v)) };
const ANNO_STORE_KEY = 'spec2viz.catalog.annotations.v1';
let annoCache = [];
let renders = 0;
function annoRender() { renders += 1; }
%(template)s
%(injected)s
(async () => {
  const steps = JSON.parse(process.argv[1]);
  await annoLoad();
  for (const step of steps) await annoWriteStore([...annoCache, step]);
  console.log(JSON.stringify({ annoCache, renders, local: JSON.parse(localStorage.getItem(ANNO_STORE_KEY) || '[]') }));
})();
"""


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@contextmanager
def sldb_serve(root: Path) -> Iterator[str]:
    """`sldb serve --cors` over `root/.sldb` on a free port, under `timeout`; stopped on exit."""
    port = _free_port()
    command = ["timeout", "120", SLDB, "serve", "--store", str(root / ".sldb"), "--pythonpath", package_pythonpath(), "--port", str(port), "--cors"]
    process = subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(200):
            try:
                with urllib.request.urlopen(f"{url}/health", timeout=2):
                    break
            except OSError:
                if process.poll() is not None:
                    pytest.fail(f"sldb serve exited: {process.stderr.read()}")
                time.sleep(0.1)
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def _project(tmp_path: Path) -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    api.init_store(root)
    register_annotations_model(root / ".sldb")
    (root / "docs").mkdir()
    (root / "docs" / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (root / "docs" / "vistas.yml").write_text("project_name: demo\nvistas:\n  - id: flow\n    title: Flow\n    src: flow.mmd\n", encoding="utf-8")
    return root


def _page_code(page: str) -> tuple[str, str]:
    """The template's three storage functions and the scripts the build embedded for sldb."""
    template = re.search(r"    function annoReadStore\(\) \{.*?\n    function annoClose", page, re.S).group(0).removesuffix("    function annoClose")
    injected = re.search(r"window\.SPECIR_ANNOTATIONS = .*?// </sldb-annotations>", page, re.S).group(0)
    return template, injected


def _run(page: str, steps: list[dict], search: str = "") -> dict:
    template, injected = _page_code(page)
    code = HARNESS % {"template": template, "injected": injected}
    done = subprocess.run(["node", "-e", code, json.dumps(steps), search], capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr
    assert "not saved" not in done.stderr and "not read" not in done.stderr, done.stderr
    return json.loads(done.stdout)


def _note(label: str, text: str) -> dict:
    return {"key": f"flow-x::{label}", "vista": "flow-x", "label": label, "comentario": text, "ts": "2026-11-15 21:00"}


def _stored(url: str, doc: str = DOC) -> list[dict]:
    """What the store holds, read back by `sldb serve` (`GET /document`)."""
    with urllib.request.urlopen(f"{url}/document?id={doc}", timeout=10) as response:
        body = json.load(response)
    assert body["model_name"] == MODEL_NAME
    return body["payload"]["annotations"]


def test_an_annotation_made_on_the_served_catalog_is_saved_and_reappears_on_reload(tmp_path: Path) -> None:
    root = _project(tmp_path)
    with sldb_serve(root) as url:
        page = render_catalog(root / "docs" / "vistas.yml", annotations=AnnotationsTarget(server=url, doc=DOC))
        first = _run(page, [_note("A", "revisar")])
        assert first["annoCache"] == [_note("A", "revisar")]
        assert _stored(url) == [_note("A", "revisar")]
        reloaded = _run(page, [])
        assert reloaded["annoCache"] == [_note("A", "revisar")] and reloaded["local"] == [_note("A", "revisar")]
        again = _run(page, [_note("B", "otra")])
        assert again["annoCache"] == [_note("A", "revisar"), _note("B", "otra")]
        assert _stored(url) == [_note("A", "revisar"), _note("B", "otra")]
    assert "comentario: otra" in next((root / MODEL_NAME).glob("*.md")).read_text(encoding="utf-8")


def test_a_stale_page_merges_with_what_another_page_saved(tmp_path: Path) -> None:
    root = _project(tmp_path)
    with sldb_serve(root) as url:
        page = render_catalog(root / "docs" / "vistas.yml", annotations=AnnotationsTarget(server=url, doc=DOC))
        _run(page, [_note("A", "uno")])
        template, injected = _page_code(page)
        # two pages loaded the same version; the second one saves after the first: its guard is stale (409)
        code = (HARNESS.split("(async () => {")[0] % {"template": template, "injected": injected}) + """
(async () => {
  const other = sldbAnnotationsStore(sldbAnnotationsConfig(window.SPECIR_ANNOTATIONS, ''), fetch);
  await annoLoad();
  const seen = await other.read();
  await annoWriteStore([...annoCache, %s]);
  const saved = await other.write([...seen, %s]);
  console.log(JSON.stringify(saved));
})();
""" % (json.dumps(_note("B", "dos")), json.dumps(_note("C", "tres")))
        done = subprocess.run(["node", "-e", code], capture_output=True, text=True, timeout=60)
        assert done.returncode == 0, done.stderr
        assert json.loads(done.stdout) == [_note("A", "uno"), _note("B", "dos"), _note("C", "tres")]
        assert _stored(url) == [_note("A", "uno"), _note("B", "dos"), _note("C", "tres")]


def test_the_page_url_names_the_server_and_the_document(tmp_path: Path) -> None:
    root = _project(tmp_path)
    with sldb_serve(root) as url:
        page = render_catalog(root / "docs" / "vistas.yml", annotations=AnnotationsTarget())
        _run(page, [_note("A", "por url")], search=f"?sldb={url}/&annotations=otro-doc")
        assert _stored(url, "otro-doc") == [_note("A", "por url")]


def test_without_a_target_the_page_is_spec2viz_s_and_keeps_annotations_in_the_browser(tmp_path: Path) -> None:
    root = _project(tmp_path)
    page = render_catalog(root / "docs" / "vistas.yml")
    assert "SPECIR_ANNOTATIONS" not in page and "sldb-annotations" not in page
    out = build_catalog(root / "docs" / "vistas.yml", tmp_path / "out.html", annotations=AnnotationsTarget(server="http://127.0.0.1:1"))
    assert '"doc": "catalog-annotations-demo"' in out.read_text(encoding="utf-8")


def test_the_model_registers_once_and_the_id_is_one_sldb_serve_accepts(tmp_path: Path) -> None:
    root = _project(tmp_path)
    register_annotations_model(root / ".sldb")
    assert api.is_model_registered(root / ".sldb", MODEL_NAME)
    assert annotations_id("Mi Catálogo / v2") == "catalog-annotations-Mi-Cat-logo-v2"
    assert re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,159}", annotations_id("x" * 300))

FILE:tests/test_imports.py
"""specIR imports SLDB only through its public API (`sldb.api`), and never pron or spec2viz.

Until `sldb.api.notations` exports the diagram spec models of D3, `specir.visual.spec_models` is the
one module that imports them from `sldb.models.notation.diagram_specs` (and only from there). Until it
exports `resolve_style`, `load_palette` and `NotationError`, `specir.visual.notation_style` is the one
module that imports them from `sldb.notations` (and only from there).

The one exception is specIR's extension of the MCP server of sldb (`specir.mcp_extension`): it
is the only module that reaches `sldb.mcp` (the extension contract of `sldb mcp --extension`)
or `mcp`. specIR implements no MCP server of its own.

SpecSync and the component spec generator (from a graph, a snapshot or the Python AST) are sldb's
(D1, D2): specIR calls them from `sldb.api.notations` and defines none of them (IR13a).

The matching of atoms with diagram elements and the coverage per view are sldb's (D4,
`sldb.api.matching`); the catalog's path rule, validation and sync too (D1). specIR's catalog
(IR13b) calls them and defines none of them, and runs no HTTP server: annotations are saved with
`sldb serve`."""

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1] / "src" / "specir"
FORBIDDEN = ("pron", "spec2viz")
#: The only module allowed to reach the MCP server of sldb and the MCP SDK.
EXTENSION = PACKAGE / "mcp_extension.py"
#: The only module allowed to reach sldb's diagram spec models (D3), which `sldb.api.notations`
#: does not export yet (asked to sldb's desk); it imports them and nothing else of sldb's internals.
SPEC_MODELS = PACKAGE / "visual" / "spec_models.py"
SPEC_MODELS_PACKAGE = "sldb.models.notation.diagram_specs"
#: The only module allowed to reach sldb's notations package (style resolution, the default palette
#: and the notation error root), which `sldb.api` does not export yet (asked to sldb's desk).
NOTATION_STYLE = PACKAGE / "visual" / "notation_style.py"
NOTATIONS_PACKAGE = "sldb.notations"


def is_spec_models(module: str) -> bool:
    return module == SPEC_MODELS_PACKAGE or module.startswith(SPEC_MODELS_PACKAGE + ".")


def is_notations(module: str) -> bool:
    return module == NOTATIONS_PACKAGE or module.startswith(NOTATIONS_PACKAGE + ".")


def is_mcp(module: str) -> bool:
    return module.split(".")[0] == "mcp" or module == "sldb.mcp" or module.startswith("sldb.mcp.")


def imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.append(node.module)
        elif isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", None)) in ("__import__", "import_module"):
            names += [arg.value for arg in node.args if isinstance(arg, ast.Constant) and isinstance(arg.value, str)]
    return names


def test_package_imports_only_the_public_sldb_api() -> None:
    sources = sorted(PACKAGE.rglob("*.py"))
    assert sources, f"no source under {PACKAGE}"
    offending: list[str] = []
    for path in sources:
        for module in imported_modules(path):
            root = module.split(".")[0]
            if path == EXTENSION and is_mcp(module):
                continue
            if path == SPEC_MODELS and is_spec_models(module):
                continue
            if path == NOTATION_STYLE and module == NOTATIONS_PACKAGE:
                continue
            if root in FORBIDDEN or (root == "sldb" and module != "sldb.api" and not module.startswith("sldb.api.")):
                offending.append(f"{path.relative_to(PACKAGE.parent)}: {module}")
    assert not offending, offending


def test_sldb_is_reached_only_through_sldb_api() -> None:
    for path in sorted(PACKAGE.rglob("*.py")):
        assert "sldb" not in {m for m in imported_modules(path)}, f"{path}: bare `import sldb`"


def test_only_the_extension_reaches_mcp() -> None:
    reaching = {str(path.relative_to(PACKAGE.parent)) for path in sorted(PACKAGE.rglob("*.py")) if any(is_mcp(m) for m in imported_modules(path))}
    assert reaching == {str(EXTENSION.relative_to(PACKAGE.parent))}, reaching


def test_specir_has_no_mcp_server_of_its_own() -> None:
    assert not (PACKAGE / "mcp").exists(), "src/specir/mcp was migrated to sldb (sldb.mcp)"
    for path in sorted(PACKAGE.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for server in ("MCPServer", "FastMCP", "build_server", ".run(\"stdio\")"):
            assert server not in text, f"{path}: {server}"
    pyproject = (PACKAGE.parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    assert "specir-mcp" not in pyproject and "specir.mcp." not in pyproject


def test_only_spec_models_reaches_the_diagram_spec_models() -> None:
    reaching = {str(path.relative_to(PACKAGE.parent)) for path in sorted(PACKAGE.rglob("*.py")) if any(is_spec_models(m) for m in imported_modules(path))}
    assert reaching == {str(SPEC_MODELS.relative_to(PACKAGE.parent))}, reaching


def test_only_notation_style_reaches_sldb_notations() -> None:
    reaching = {str(path.relative_to(PACKAGE.parent)) for path in sorted(PACKAGE.rglob("*.py")) if any(is_notations(m) for m in imported_modules(path))}
    assert reaching == {str(NOTATION_STYLE.relative_to(PACKAGE.parent))}, reaching


#: What D1 and D2 migrated to `sldb.api.notations` (IR13a): specIR calls it there and defines none of it.
MIGRATED_TO_SLDB = (
    "SpecSync", "sync_spec", "sync_catalog", "check_catalog", "catalog_entries", "spec_elements", "spec_edges",
    "format_report", "component_spec_from_graph", "component_spec_from_python", "write_component_spec",
    "load_node_link", "load_node_link_graph", "load_store_index", "index_graph", "generate_python_ast_spec",
)


def test_specir_defines_no_spec_sync_and_no_spec_generator() -> None:
    defined = []
    for path in sorted(PACKAGE.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Assign)):
                names = [t.id for t in getattr(node, "targets", []) if isinstance(t, ast.Name)] or [getattr(node, "name", "")]
                defined += [f"{path.relative_to(PACKAGE.parent)}: {name}" for name in names if name in MIGRATED_TO_SLDB]
    assert not defined, defined
    assert not (PACKAGE / "visual" / "generators").exists() and not (PACKAGE / "visual" / "sync.py").exists()


#: What D4 migrated to `sldb.api.matching` and D1 to `sldb.api.notations` for catalogs (IR13b).
MATCHING_IN_SLDB = (
    "SldbAtomResolver", "AtomBuildWarning", "CoverageBuildWarning", "UnknownAtomError", "SpecView", "StoreReader",
    "parse_atoms", "label_key", "filter_atoms_payload", "build_atoms_by_view", "raw_atoms_by_view", "build_explicit_atoms",
    "build_explicit_refs", "attach_atom_edges", "collect_explicit_atoms", "collect_explicit_refs", "build_coverage_by_view",
    "atom_index", "rank_atoms", "edges_of", "resolve_ref", "resolve_catalog_path", "repo_root", "candidates", "split_fragment",
    "resolve_view", "find_store",
)


def test_specir_defines_no_atom_matching_and_no_catalog_path_rule() -> None:
    defined = []
    for path in sorted(PACKAGE.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in MATCHING_IN_SLDB:
                defined.append(f"{path.relative_to(PACKAGE.parent)}: {node.name}")
    assert not defined, defined


def test_the_catalog_runs_no_server_of_its_own() -> None:
    for path in sorted((PACKAGE / "visual").rglob("*.py")):
        modules = set(imported_modules(path))
        assert not modules & {"http.server", "socketserver", "aiohttp", "flask", "fastapi"}, path

FILE:tests/visual/test_visual_names.py
"""specIR's visual layer takes from sldb what is sldb's and does not redefine it.

- No class of specIR has the name of a visual vocabulary model of SLDB (the notation documents
  `sldb.api` exports and the notation and palette specs of `sldb.notations`).
- No class of specIR has the name of a diagram spec model: the eight models (and every model they
  are made of) are sldb's (D3) and `compile_ir` dispatches sldb's classes.
- spec2viz is imported, under tests/, only by the parity oracles (tests/visual/parity.py of IR11
  and tests/visual/render_parity.py of IR12); under src/specir/ never (tests/test_imports.py)."""

from __future__ import annotations

import ast
import inspect
import typing
from pathlib import Path

import sldb.api as api
import sldb.notations as notations
from pydantic import BaseModel
from sldb.api.notations import load_spec

from specir.visual import compile_ir
from specir.visual.spec_models import SPEC_MODELS, BaseDiagram, EnforcementArtifact, EnforcementFact

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "src" / "specir"
TESTS = REPO / "tests"
#: The modules that reach spec2viz as the development oracle (IR11, IR12, IR13a's sync and generation
#: parity and IR13b's catalog parity).
ORACLES = {TESTS / "visual" / "parity.py", TESTS / "visual" / "render_parity.py", TESTS / "visual" / "test_sync_generation_parity.py",
           TESTS / "visual" / "test_catalog_parity.py"}
EIGHT = {"ClassDiagram", "SequenceDiagram", "StateDiagram", "ComponentDiagram", "ActivityDiagram",
         "DeploymentDiagram", "MatrixDiagram", "ReflectionDiagram"}


def specir_classes() -> dict[str, str]:
    found = {}
    for path in sorted(PACKAGE.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ClassDef):
                found[node.name] = str(path.relative_to(REPO))
    return found


def vocabulary() -> set[str]:
    docs = {n for n in dir(api) if inspect.isclass(getattr(api, n)) and getattr(api, n).__module__.startswith("sldb.models.notation")}
    specs = {n for n in notations.__all__ if inspect.isclass(getattr(notations, n)) and not issubclass(getattr(notations, n), Exception)}
    return docs | specs


def models_of(model: type, seen: set[type]) -> None:
    """`model` and every pydantic model its fields are made of."""
    if model in seen:
        return
    seen.add(model)
    for field in model.model_fields.values():
        for part in _types(field.annotation):
            if inspect.isclass(part) and issubclass(part, BaseModel):
                models_of(part, seen)


def _types(annotation) -> list:
    args = typing.get_args(annotation)
    return [annotation] if not args else [t for a in args for t in _types(a)]


def spec_model_names() -> set[str]:
    seen: set[type] = set()
    for model in (*SPEC_MODELS, BaseDiagram, EnforcementArtifact, EnforcementFact):
        models_of(model, seen)
    return {m.__name__ for m in seen}


def test_no_class_has_the_name_of_a_visual_vocabulary_model_of_sldb() -> None:
    names = vocabulary()
    assert {"SpecDoc", "SpecNodeDoc", "NotationDoc", "GlyphDoc", "LinkDoc", "PaletteDoc", "ViewDoc", "NotationSpec", "PaletteSpec"} <= names
    clashes = {name: where for name, where in specir_classes().items() if name in names}
    assert not clashes, clashes


def test_no_class_has_the_name_of_a_diagram_spec_model() -> None:
    names = spec_model_names()
    assert EIGHT <= names and {"NodeModel", "EdgeModel", "EnforcementArtifact"} <= names
    clashes = {name: where for name, where in specir_classes().items() if name in names}
    assert not clashes, clashes


def test_the_eight_spec_models_are_sldb_classes_and_compile() -> None:
    assert {m.__name__ for m in SPEC_MODELS} == EIGHT
    assert all(m.__module__.startswith("sldb.") for m in (*SPEC_MODELS, BaseDiagram, EnforcementArtifact, EnforcementFact))
    examples = REPO / "tests" / "visual" / "fixtures" / "spec2viz" / "examples"
    diagrams = [load_spec(path) for path in sorted(examples.rglob("*.yml"))]
    assert {type(d) for d in diagrams} == set(SPEC_MODELS)
    for diagram in diagrams:
        assert compile_ir(diagram) is not None, diagram.id


def test_spec2viz_is_imported_only_by_the_parity_oracle() -> None:
    importing = set()
    for path in sorted([*TESTS.rglob("*.py"), *PACKAGE.rglob("*.py")]):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
            if any(n.split(".")[0] == "spec2viz" for n in names):
                importing.add(path)
    assert importing == ORACLES, importing

FILE:tests/visual/test_resources.py
"""Resources that specIR's visual layer packages (SV-C07, SV-C10, SV-J04, SV-J05, SV-G08 for the template).

- The catalog template (`templates/default.html`) and the vendored bpmn-js
  (`templates/vendor/bpmn-js/`) are package data of specIR: the installed package reads them, a wheel
  built from the project carries them, and they are spec2viz's own bytes (live, when installed).
- The pages that must open from `file://` with nothing from outside (the offline BPMN viewer and the
  graph HTML; the tree HTML too) reference no external script, stylesheet, font or import; the
  viewer inlines the vendored bpmn-js and its two stylesheets.
- `test_examples_render_successfully` of spec2viz's `tests/test_packaging.py`, over the same
  examples (`fixtures/spec2viz/examples/`)."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import zipfile
from importlib.resources import files
from pathlib import Path

import pytest

from specir.visual.render_file import render_to_file
from specir.visual.renderers.bpmn_viewer import VENDOR_DIR

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_parity  # noqa: E402

PROJECT = HERE.parents[1]
CORPUS = HERE / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLES = CORPUS / "examples"
VENDOR = ("LICENSE", "README.md", "bpmn-js.css", "bpmn-navigated-viewer.production.min.js", "diagram-js.css")
RESOURCES = ("templates/default.html", *(f"templates/vendor/bpmn-js/{name}" for name in VENDOR))
#: specIR's own resources, which spec2viz did not have: the catalog's annotation saving with sldb serve (IR13b).
SPECIR_RESOURCES = ("templates/annotations-sldb.js",)
#: What would make a page fetch something to open: a script by URL, a stylesheet or font link, a CSS
#: import, a CSS url() to the network, or any `src` (image, frame) to the network. A link the reader
#: may follow (`<a href>`, like bpmn.io's watermark inside bpmn-js) fetches nothing.
EXTERNAL = re.compile(r"<script[^>]*\bsrc=|<link\b|@import|url\(\s*['\"]?(?:https?:)?//|\bsrc=['\"]?(?:https?:)?//", re.I)


def _resource(rel: str):
    return files("specir.visual").joinpath(*rel.split("/"))


def test_the_installed_package_reads_its_resources():
    for rel in (*RESOURCES, *SPECIR_RESOURCES):
        assert _resource(rel).is_file(), rel
        assert _resource(rel).read_bytes(), rel
    assert Path(str(_resource("templates/vendor/bpmn-js"))) == VENDOR_DIR
    readme = _resource("templates/vendor/bpmn-js/README.md").read_text(encoding="utf-8")
    js = _resource("templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js").read_text(encoding="utf-8")
    version = re.search(r"`bpmn-js` (\d+\.\d+\.\d+)", readme).group(1)
    assert f"bpmn-navigated-viewer v{version}" in js


@pytest.mark.parity
def test_resources_are_spec2viz_bytes():
    pytest.importorskip("spec2viz")
    origin = render_parity.spec2viz_package_dir()
    for rel in RESOURCES:
        assert _resource(rel).read_bytes() == (origin / rel).read_bytes(), rel


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv is not installed: no backend to build the wheel")
def test_a_wheel_of_the_project_carries_the_resources(tmp_path):
    """The package data is declared (pyproject.toml), not only present in the source tree."""
    project = tmp_path / "project"
    project.mkdir()
    shutil.copy(PROJECT / "pyproject.toml", project / "pyproject.toml")
    shutil.copytree(PROJECT / "src" / "specir", project / "src" / "specir", ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
    result = subprocess.run(
        ["uv", "build", "--wheel", "--offline", "--out-dir", str(tmp_path / "dist"), str(project)],
        capture_output=True, text=True, timeout=300,
    )
    assert result.returncode == 0, result.stderr[-800:]
    wheel = next((tmp_path / "dist").glob("specir-*.whl"))
    names = set(zipfile.ZipFile(wheel).namelist())
    for rel in (*RESOURCES, *SPECIR_RESOURCES):
        assert f"specir/visual/{rel}" in names, rel


def test_bpmn_viewer_opens_without_external_resources(tmp_path):
    out = render_to_file(FIXTURES / "activity.mepu-decision.yml", out=tmp_path, renderer="bpmn")
    page = out.with_name(out.name + ".html").read_text(encoding="utf-8")
    assert not EXTERNAL.search(page), EXTERNAL.search(page)
    for name in ("bpmn-js.css", "diagram-js.css"):
        css = (VENDOR_DIR / name).read_text(encoding="utf-8")
        assert css.strip()[:200] in page, name
    js = (VENDOR_DIR / "bpmn-navigated-viewer.production.min.js").read_text(encoding="utf-8")
    assert js[:200] in page and len(page) > len(js)


@pytest.mark.parametrize("renderer, spec", [("graph", "component.quotation.yml"), ("tree", "component.quotation.yml")])
def test_component_html_opens_without_external_resources(tmp_path, renderer, spec):
    page = render_to_file(FIXTURES / spec, out=tmp_path, renderer=renderer).read_text(encoding="utf-8")
    assert page.lstrip().lower().startswith("<!doctype html")
    assert not EXTERNAL.search(page), EXTERNAL.search(page)
    assert "QuotationFlow" in page


# ── tests/test_packaging.py ─────────────────────────────────────────────────────────────────────


def test_examples_render_successfully(tmp_path):
    example_paths = [
        path
        for path in sorted(EXAMPLES.glob("**/*.yml"))
        if "/catalog/" not in path.as_posix() and path.name not in {"project.yml", "vistas.yml"}
    ]

    assert example_paths

    for example_path in example_paths:
        output_path = render_to_file(example_path, out=tmp_path)
        assert output_path.exists(), f"missing output for {example_path}"

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
| SV-G01 | Construcción del catálogo HTML autocontenido desde un `vistas.yml` o un store de stores (marca, subtítulo, plantilla local, `project.yml`, secciones HTML, anchors únicos) | `spec2viz/orchestrator.py` | migrar tal cual | IR13b con los renderers de IR12 | test_build_command* (7), test_catalog_build_alias_matches_legacy_build y test_build_command_reports_errors de `tests/test_cli.py` portados y en verde; mismas vistas, categorías y navegación que spec2viz sobre el fixture (IR13b). IR13b (`tests/visual/test_catalog.py`, sección de `tests/test_cli.py`): los 9 casos de build portados sobre la API (`specir.visual.catalog.build_catalog`/`render_catalog`; el comando, el alias `build` y sus mensajes «Rendered catalog» y «Error building catalog» son de IR13d; el error de construcción es la excepción). `tests/visual/test_catalog_parity.py`: la página es la de spec2viz byte a byte sobre `docs/architecture/vistas.yml` y `examples/catalog/` de spec2viz, sobre un proyecto sincronizado, stores de stores con overrides, `project.yml`, fragmentos y fuentes de todo tipo; diferencia declarada: los avisos de átomos y cobertura son findings de sldb (`level`, `code`, `subject`, `what`, `fix`) donde spec2viz escribía `{scope, message}`, y se comparan por su texto. `test_the_built_catalog_opens_without_missing_resources`: ninguna referencia local ni anchor roto (mermaid, vega y fuentes por CDN, igual que spec2viz). |
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
| SV-J02 | `compile_ir`, `render`, `json_schema`, `write_json_schema` | `spec2viz/__init__.py` | migrar tal cual | IR13d (API pública de la capa visual de specIR) | El resto de `tests/test_api.py` (27 en total) portado contra la API de specIR y en verde. |
| SV-J03 | `render_to_file` con cabecera de procedencia (`with_provenance`, `provenance_header`, `provenance_text`) y salida BPMN doble (`.bpmn` y `.bpmn.html`) | `spec2viz/__init__.py` | migrar tal cual | IR12 lo migra (`src/specir/visual/render_file.py`, lo necesita `diagram render`); IR13d lo expone en la API pública | test_render_to_file_* (7) de `tests/test_api.py` y test_rendered_text_projections_carry_a_provenance_header de `tests/test_cli.py` portados; la cabecera nombra el comando de specIR que valida. |
| SV-J04 | Recurso empaquetado: bpmn-js vendorizado | `spec2viz/templates/vendor/bpmn-js/` | migrar tal cual | IR12 (prueba de recursos) | El visor BPMN abre offline (SV-C07) y `tests/test_packaging.py` portado (incluido test_examples_render_successfully) en verde. |
| SV-J05 | Recurso empaquetado: plantilla HTML del catálogo | `spec2viz/templates/default.html` | migrar tal cual | IR12 | Ver SV-G08; la plantilla viaja en el paquete instalado de specIR (prueba de recursos de IR12). |
| SV-J06 | Recursos empaquetados: notaciones y paleta builtin | `spec2viz/notations/`, `spec2viz/palettes/` | usar sldb directamente | Builtins de sldb (`src/sldb/notations/builtin/`, `src/sldb/notations/palettes/`) vía `sldb.notations.builtin_notations` y `builtin_palettes` | specIR no empaqueta notaciones ni paletas; SV-H02 y SV-H05 cumplidas. |
| SV-J07 | Punto de entrada `spec2viz` y empaquetado (instala y arranca) | `pyproject.toml` (`[project.scripts]`), `spec2viz/cli.py` (`main`) | reemplazar | Sustituto: el comando de specIR (IR13d) | Prueba de IR13d: el paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado; test_primary_cli_still_exposes_commands de `tests/test_packaging.py` portado. |
| SV-J08 | Comando about (dónde viven los diagramas y cómo llega el flujo al HTML) | `spec2viz/cli.py` (`about`) | migrar tal cual | IR13d | El comando equivalente de specIR existe y lo invoca la prueba de CLI de IR13d; su texto nombra los comandos de specIR y de sldb que sustituyen a los de spec2viz. |
| SV-J09 | Habilidad de agente use-spec2viz | `.pi/skills/use-spec2viz/SKILL.md` (copia distinta en `deskops/.opencode/skills/use-spec2viz/SKILL.md`) | reemplazar | Sustituto: `skills/use-specir/SKILL.md` (IR13d) | Prueba de IR13d que extrae los comandos que nombra la habilidad y los invoca con ayuda; la habilidad no nombra comandos de spec2viz. |

### K. Comandos y subgrupos del CLI

Una fila por cada entrada que lista la ayuda (`spec2viz --help` y la de cada subgrupo). La correspondencia
detallada la escribe IR13d en `docs/spec2viz/correspondencia-cli.md`. Cuando la capacidad vive en sldb, el
equivalente es el comando de sldb y specIR no define subcomando propio.

| ID | Comando | Modo | Equivalente | Condición de retiro |
|---|---|---|---|---|
| SV-K01 | `spec2viz about` | migrar tal cual | Comando about de specIR (IR13d) | SV-J08. |
| SV-K02 | `spec2viz build` (alias de `catalog build`) | migrar tal cual | Alias en el comando de specIR (IR13d) | SV-G01; test_catalog_build_alias_matches_legacy_build portado. |
| SV-K03 | `spec2viz catalog` (subgrupo) | migrar tal cual | Subgrupo catalog de specIR con build y schema; sync, validate y serve remiten a sldb | SV-K04 a SV-K08 cumplidas. |
| SV-K04 | `spec2viz catalog build` | migrar tal cual | specIR (IR13b, IR13d) | SV-G01. |
| SV-K05 | `spec2viz catalog schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A16. |
| SV-K06 | `spec2viz catalog serve` | reemplazar | `sldb serve` sobre el store del catálogo (IR13b) | SV-G06. |
| SV-K07 | `spec2viz catalog sync` | migrado a sldb | `sldb notations sync --catalog` (D1) | SV-G04. |
| SV-K08 | `spec2viz catalog validate` | migrado a sldb | `sldb notations sync --catalog --check` (D1) | SV-G05. |
| SV-K09 | `spec2viz diagram` (subgrupo) | migrar tal cual | Subgrupo diagram de specIR con render, lint y schema (y validate, ver SV-K16); sync, from-graph y generate remiten a sldb | SV-K10 a SV-K16 cumplidas. |
| SV-K10 | `spec2viz diagram from-graph` | migrado a sldb | `sldb notations from-graph --snapshot/--store` (D2) | SV-F01; test_cli_from_graph_* (5) y test_cli_from_graph_module_prefix reescritos contra el comando de sldb (D2). |
| SV-K11 | `spec2viz diagram generate` | migrado a sldb | `sldb notations from-graph --python` (D2) | SV-F02. |
| SV-K12 | `spec2viz diagram lint` | migrar tal cual | specIR (IR12, IR13d) | SV-D01. |
| SV-K13 | `spec2viz diagram render` | migrar tal cual | specIR (IR12, IR13d) | test_render_* de `tests/test_cli.py` portados; SV-C01 a SV-C12. |
| SV-K14 | `spec2viz diagram schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A15. |
| SV-K15 | `spec2viz diagram sync` | migrado a sldb | `sldb notations sync --spec` (D1) | SV-E01. |
| SV-K16 | `spec2viz diagram validate` | migrado a sldb | Lógica en sldb (`load_spec`, `validate_spec`, D3); hoy sldb no tiene comando que valide un spec: o sldb lo añade (pedido por su desk) o el comando de specIR lo invoca sin redefinir nada (IR13d) | test_validate_valid, test_validate_invalid y test_validate_all_types de `tests/test_cli.py` portados contra el comando elegido; SV-A11 y SV-A12. |
| SV-K17 | `spec2viz lint` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K12. |
| SV-K18 | `spec2viz notation` (subgrupo) | usar sldb directamente | `sldb notations` | SV-K19 a SV-K22 cumplidas. |
| SV-K19 | `spec2viz notation list` | usar sldb directamente | `sldb notations list` | SV-H02. |
| SV-K20 | `spec2viz notation sync` | usar sldb directamente | `sldb notations sync --notation` | SV-E02. |
| SV-K21 | `spec2viz notation validate` | usar sldb directamente | `sldb.notations.load_notation`; sldb no tiene hoy comando de validación de notaciones (ver pendientes) | SV-H01 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. |
| SV-K22 | `spec2viz notation view` | usar sldb directamente | `sldb notations view` | SV-H03. |
| SV-K23 | `spec2viz palette` (subgrupo) | usar sldb directamente | `sldb notations` (`list`, `sync --palette`) | SV-K24 a SV-K26 cumplidas. |
| SV-K24 | `spec2viz palette list` | usar sldb directamente | `sldb notations list` (incluye `builtin_palettes`) | SV-H05. |
| SV-K25 | `spec2viz palette sync` | usar sldb directamente | `sldb notations sync --palette` | SV-E02. |
| SV-K26 | `spec2viz palette validate` | usar sldb directamente | `sldb.notations.load_palette` (con contraste WCAG); sldb no tiene hoy comando de validación de paletas (ver pendientes) | SV-H04 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. |
| SV-K27 | `spec2viz render` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K13. |
| SV-K28 | `spec2viz schema` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K14. |
| SV-K29 | `spec2viz validate` (alias) | migrado a sldb | Igual que SV-K16 | SV-K16. |
| SV-K30 | Ayuda raíz con taxonomía (diagram, catalog) y lista de renderers | migrar tal cual | Ayuda del comando de specIR (IR13d) | test_help_mentions_taxonomy_groups_and_renderers de `tests/test_cli.py` portado. |

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
3. SV-K16 y SV-K29: decidir si la validación de un spec por CLI la da sldb (pedido a su desk) o el comando
   de specIR sobre `load_spec`/`validate_spec`.
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
# The visual layer's render, lint and schema commands (IR12); IR13d gives `specir` its full taxonomy.
specir = "specir.visual.commands:main"

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

FILE:instruccion
Cold-bundle de la tarea task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- La validación de un registro de vistas reporta en specIR los mismos errores tipados que spec2viz sobre los fixtures de catálogo.
- La sincronización del catálogo deja en un store de prueba el mismo contenido que spec2viz, y no escribe nada si alguna vista falla.
- El catálogo construido contiene las mismas vistas, categorías y navegación que el de spec2viz sobre el fixture, y abre sin recursos externos faltantes.
- Una anotación hecha en el servidor local queda guardada y reaparece al recargar.
- El emparejamiento de átomos reporta los mismos átomos por elemento y la misma cobertura por vista que spec2viz sobre los fixtures de átomos; un id de átomo desconocido es advertencia, o error en modo estricto.
- El paquete no importa spec2viz.

