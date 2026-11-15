# IR12: informe del worker

Tarea: `task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz`, directo en IR main (sin worktrees ni ramas).

## Commits (IR main, sin push)

- `5319a81`: código, pruebas, goldens y matriz.
- `c5e1078`: desk (precisiones de preflight y bundle en `implementation_path`, `files` de la tarea, review bundle-2 dispuesta como `accepted`, evidencia en `runs/subagents/20261115-225724`).
- `dbda5a5`: cierre `resolved-by` (refs 5319a81 y c5e1078; tests: `tests/visual/test_render_parity.py`, `test_renderers.py`, `test_render_cases.py`, `test_bpmn.py`, `test_lint_mermaid.py`, `test_schema.py`, `test_render_commands.py`, `test_resources.py` y `tests/test_imports.py`).
- El commit de este informe va aparte (`runs: informe del worker de IR12`).

## Aviso: carencia de sldb (nota enviada, sin commitear en sldb)

`sldb.api` no exporta seis nombres que la capa visual necesita: `resolve_style`, `load_palette` y `NotationError` (están en `sldb.notations`), y `AnyDiagram`, `DiagramType` y `DiagramStoreEnvelope` (en `sldb.models.notation.diagram_specs`). Mismo patrón que IR11 (reversible):

- `src/specir/visual/notation_style.py` (nuevo) es el único módulo que importa de `sldb.notations`.
- `src/specir/visual/spec_models.py` (el de IR11) añade los tres modelos.
- `tests/test_imports.py` acota ambas excepciones y suma `test_only_notation_style_reaches_sldb_notations`.

Nota en el inbox de sldb: `sldb/desk/inbox/20261115-195349-suggestion-ir-pide-exportar-desde-sldb-api-notations-resolve-style-load-palette-notationerror-anydiagram-diagramtype-y-diagramstoreenvelope.md` (más su `InboxNoteDoc` trackeado por deskops). **No está commiteada en sldb: la debe meter su coordinador.**

## Qué se migró y adónde

Origen: spec2viz `2de1056`, sin tocar. Todo se copió y solo cambiaron los imports, salvo lo que se indica.

| Origen (spec2viz) | Destino (IR) | Cambios |
|---|---|---|
| `renderers/{__init__,mermaid,plantuml,d2,vega,bpmn,bpmn_palette,bpmn_viewer,tree,graph_html,class_diagram,view_mermaid}.py` | `src/specir/visual/renderers/` | Imports a `specir.visual.*`. El estilo sale de sldb (`resolve_style`) y la tinta de la paleta `default` de sldb (`notation_style.default_ink()`, en lugar del `_builtin_default` privado). vega: el dominio de `kindColor` va en orden de primera aparición (ver diferencias). mermaid, plantuml y d2: dibujan `ANY_STATE` (ver más abajo). |
| `renderers/antonia.py` | `renderers/antonia_html.py` | Solo cambia el nombre del archivo, que es el que pedía la tarea. |
| `JsonRenderer` (en `renderers/__init__.py`) | `renderers/json_out.py` | Se importa desde `renderers/__init__.py`. |
| `linters/mermaid.py` | `src/specir/visual/lint_mermaid.py` | `SPECIR_MMDC` sustituye a `SPEC2VIZ_MMDC`, que sigue valiendo. |
| `schema.py` | `src/specir/visual/schema.py` | Los modelos son los de sldb, vía `spec_models.py`. |
| `exceptions.RenderError` | `src/specir/visual/exceptions.py` | Junto a `Spec2VizError` y `CompileError`. También se exporta desde `specir.visual`. |
| `render_to_file`, `with_provenance`, `provenance_header`, `provenance_text`, `_write_bpmn` (de `spec2viz/__init__.py`) | `src/specir/visual/render_file.py` | La cabecera nombra `specir: … run \`specir diagram validate …\``. Se migró aquí porque `diagram render` lo necesita; IR13d lo expone en la API (fila SV-J03 actualizada). |
| `cli.py`: `diagram render/lint/schema/validate`, `catalog schema` | `src/specir/visual/commands.py` | Mismos argumentos y opciones (incluye `--renderer`/`--backend` con sus nueve valores). Se captura `Spec2VizError` y además `NotationError` de sldb. El script `specir` (pyproject) apunta a este grupo hasta que IR13d monte `src/specir/cli.py` con la taxonomía completa y los alias de primer nivel. `diagram validate` usa `load_spec`/`validate_spec` de sldb y es el comando que nombra la cabecera de procedencia. |
| `templates/default.html`, `templates/vendor/bpmn-js/*` (bpmn-js 18.31.1, con LICENSE y README) | `src/specir/visual/templates/` | Copia byte a byte. Declarados como `package-data`; una prueba construye una wheel y comprueba que van dentro. |

Lo que queda tal cual a propósito (para no romper la paridad ni los datos de los usuarios):

- `exporter="spec2viz"` y `targetNamespace="http://spec2viz/bpmn"` en el XML BPMN.
- La clave de `localStorage` `spec2viz.catalog.annotations.v1` de la plantilla del catálogo.

Ver pendientes.

pyproject: `click>=8.1` declarado como dependencia directa (ya llegaba por sldb), script `specir` y package-data de las plantillas. Reinstalado editable en `IR/.venv` con `uv pip install --no-deps -e .`.

## Decisión sobre el origen "*" (`ANY_STATE`)

- `ANY_STATE = "*"` pasa de `projections.py` a `ir.py`, como parte del contrato de la IR. `projections.py` lo importa de allí con el mismo valor. `specir.visual` lo exporta vía `ir`.
- Una transición con `from_ == ANY_STATE` sale de **un único pseudoestado punteado con rótulo `*`** (id `__any_state`, constante `ANY_STATE_ID` en `renderers/mermaid.py`), distinto del estado inicial:
  - mermaid: `state "*" as __any_state` + `classDef anyState stroke-dasharray:4 4`.
  - plantuml: `state "*" as __any_state ##[dashed]`.
  - d2: `__any_state: "*" {style.stroke-dash: 3}`.
  - Se descartó expandir la transición a todos los estados. La proyección no dice "desde cualquiera", dice "origen no conocido", y expandirla fabricaría aristas.
- Un `StateIR` sin estado inicial (la proyección deja `initial=""` si no hay exactamente uno) ya no emite `[*] --> ` vacío.
- Ningún spec de spec2viz produce estos casos, así que la paridad no cambia.
- Pruebas: los 4 casos de `ANY_STATE` en `tests/visual/test_render_parity.py`. Uno de ellos renderiza la proyección real `ViewDoc:post-states` del blog de IR06.
- El linter de regex la da por limpia. **No se verificó con el motor real de mermaid (no hay mmdc)**: ids con guion como `post-published` en `stateDiagram-v2` quedan sin verificar contra mmdc.

## Diferencias con spec2viz

- **SV-C05 (vega)**: spec2viz listaba el dominio de la escala `kindColor` iterando un `set`, así que el orden cambiaba con `PYTHONHASHSEED` de una ejecución a otra. specIR lo lista en orden de primera aparición; el color de cada kind es el mismo. Declarada en la condición de retiro de la fila, con su prueba (`test_vega_lists_the_kinds_in_order_of_first_appearance`). La paridad compara esa escala como correspondencia kind → color. Se comprobó con `PYTHONHASHSEED` 0, 1 y 7.
- **Cabecera de procedencia**: nombra `specir` donde spec2viz nombraba `spec2viz`. Es lo que pide SV-J03. `test_render_to_file_writes_what_spec2viz_writes_but_the_command_it_names` compara byte a byte todo lo demás: mermaid, plantuml, d2, vega, graph y bpmn más su `.bpmn.html`.

Fuera de eso, todo es idéntico:

- Los 36 specs válidos del corpus por los 9 renderers (salida, o clase y mensaje de `RenderError`) y el SHA-256 del visor BPMN de cada actividad: `goldens/spec2viz-2de1056-renders.json`.
- Los hallazgos del linter sobre 43 casos (los textos de lint de spec2viz y el mermaid de cada spec del corpus), con y sin la regla de `<…>`: `goldens/spec2viz-2de1056-lint.json`.
- El JSON Schema de todos los tipos, de cada tipo y del envelope del catálogo (`diagram-store`, `catalog`, `project`): `goldens/spec2viz-2de1056-schema.json`.
- `view_to_mermaid` sobre la misma vista resuelta por sldb (4 specs × 2 temas, contra el vivo).
- Los recursos byte a byte.

`tests/visual/render_parity.py` regenera los tres goldens. Junto a `parity.py`, es el único archivo que importa spec2viz; `test_visual_names.py` se actualizó para aceptar los dos.

## Pruebas portadas y lo que no se porta aquí

Portadas, desde spec2viz `tests/`:

- `test_renderers.py` (56/56).
- `test_bpmn.py` (26/26). Los 2 casos de modelo pasan por `load_spec` de sldb sobre un YAML, porque el modelo es de sldb.
- `test_mermaid_mmdc.py` (4).
- `test_rendering_bug.py` (1).
- `test_exceptions.py`: los asertos de `Spec2VizError`, `CompileError` y `RenderError`.
- `test_api.py`: los 3 `render_*`, los 7 `render_to_file_*` y los 3 de `json_schema`.
- `test_cli.py`: todos los `test_render_*`, los 4 `test_schema_*`, `test_catalog_schema_stdout`, `test_rendered_text_projections_carry_a_provenance_header` y la parte de renderers de `test_help_*`. Se ejecutan sobre `diagram …`; los alias de primer nivel son de IR13d.
- `test_packaging.py`: `test_examples_render_successfully`, `test_schema_examples_match_generated_output` y `test_every_model_field_has_a_description`. Este último recorre el schema exportado sobre los mismos modelos, porque las clases son de sldb.
- Los casos de render de `test_class_diagram.py`, `test_class_packages.py`, `test_activity_lanes.py` y `test_deployment_nested.py`.
- Los 4 casos `view_to_mermaid` de `test_catalog_resolved_views.py`, sobre la vista que resuelve sldb tras su `SpecSync` en un store nuevo.

No se portan aquí, porque son de otra tarea:

- Los casos de validación y de sync de esos mismos archivos (D3/D1).
- `catalog build` (IR13b).
- `test_primary_cli_still_exposes_commands` y el resto de `test_help_*` (IR13d).

## Pruebas saltadas y por qué

**`mmdc` (mermaid-cli) no está instalado.** Hay node 22 en `~/.local/bin`, pero no `mmdc`. No instalé paquetes globales. Se saltan 10 casos, como en spec2viz:

- 7 de `test_lint_mermaid.py` (`test_mmdc_catches_broken` ×4 y `test_mmdc_passes_clean` ×3).
- `test_real_mermaid_engine_accepts_members_kinds_and_all_relations`.
- `test_real_mermaid_engine_accepts_the_packages`.
- `test_view_to_mermaid_is_accepted_by_the_real_engine`.

También se comprobó que las pruebas de paridad se saltan limpiamente sin spec2viz. Con spec2viz oculto con un `ModuleNotFoundError` en `PYTHONPATH`, `tests/visual/` da rc 0, 290 passed y 110 skipped; los goldens siguen sosteniendo la paridad.

## Tests (TMPDIR=/dev/shm)

| Prueba | rc | Resultado |
|---|---|---|
| `tests/test_imports.py` | 0 | 6 passed |
| `tests/visual/test_visual_names.py` | 0 | 4 passed |
| `tests/visual/test_render_parity.py` | 0 | 81 passed |
| `tests/visual/test_render_cases.py` | 0 | 27 passed, 3 skipped (mmdc) |
| `tests/visual/test_lint_mermaid.py` | 0 | 8 passed, 7 skipped (mmdc) |
| `tests/visual/test_schema.py` | 0 | 13 passed |
| `tests/visual/test_render_commands.py` | 0 | 33 passed |
| `tests/visual/test_resources.py` | 0 | 7 passed (incluye la wheel construida con `uv build --offline` en tmp) |
| `tests/visual/test_renderers.py` | 0 | 56 passed |
| `tests/visual/test_bpmn.py` | 0 | 26 passed |
| `tests/visual/test_visual_projections.py` | 0 | 9 passed |
| `tests/test_matriz_cobertura_spec2viz.py` | 0 | 5 passed |
| **Suite completa de IR**: `pytest -q -n 4 tests/` | 0 | **425 passed, 10 skipped (mmdc), 2 xfailed** (los 2 xfail estrictos de `test_blog_chain.py` ya existían) |

Flake observado, no introducido por IR12: en una corrida de `tests/visual/` con `-n 4`, `test_visual_projections.py::test_a_composed_view_projects_like_a_projection_view` (IR11) falló una vez con `ViewDoc:post-persistence is not in the store`. Pasó en la suite completa y en 4 corridas secuenciales posteriores. Parece una carrera entre la escritura por MCP y la lectura del store bajo carga.

## Validación de la tarea

- **Paridad de cada renderer contra su golden**: `test_render_parity.py`. Contra los goldens siempre, y contra spec2viz vivo con el marker `parity`. Los casos portados están en `test_renderers.py`, `test_render_cases.py`, `test_bpmn.py` y `test_render_commands.py`. La única diferencia declarada es SV-C05.
- **Mismos hallazgos del linter**: `test_lint_mermaid.py`, contra goldens y contra el vivo.
- **JSON Schema igual al de spec2viz**: `test_schema.py`. Es idéntico en todos los tipos, incluido el `KeyError` de `reflection`, que spec2viz también tiene.
- **HTML del visor BPMN y del grafo sin recursos externos**: `test_resources.py`. Revisa que no haya `<script src>`, `<link>`, `@import`, `url(//…)` ni `src=` de red; también comprueba el árbol. La plantilla del catálogo y antonia-html cargan mermaid, vega y fuentes por CDN, igual que en spec2viz; esto no lo exige la tarea.
- **Los 9 valores del selector**: `test_the_selector_has_the_nine_values_of_spec2viz` y, contra el vivo, `test_selector_extensions_and_defaults_are_spec2viz`.
- **El paquete no importa spec2viz**: `tests/test_imports.py`.

Matriz (`docs/spec2viz/matriz-de-cobertura.md`): se declaró la diferencia de SV-C05 y se corrigieron destinos (SV-C13, SV-C14, SV-D01 con `SPECIR_MMDC`, SV-J03 migrado aquí y pendiente 5 resuelto). No se marcó ninguna fila como cumplida: eso lo hace IR13.

Filas cuya condición de retiro queda cumplida por estas pruebas, para que IR13 las cite: SV-A14, SV-A15, SV-A16, SV-C01 a SV-C15, SV-D01, SV-J04, SV-J05 y la parte de plantilla de SV-G08. Matices:

- SV-C01 cita `test_render_override` y `test_render_backend_alias` sobre `diagram render`; el alias `render` de primer nivel es de IR13d.
- SV-J04 cita `tests/test_packaging.py` portado; `test_primary_cli_still_exposes_commands` es de IR13d (SV-J07).

## Revisión (deskops review)

- **Preflight**: `deskops review preflight` respondió `unchanged (already reviewed)`. Era preflight-1 (2026-11-12), ya dispuesta como `accepted`. Sus 6 ambigüedades se resolvieron igualmente con `deskops edit task` en el bloque «Precisiones (preflight)» de `implementation_path`, que también recoge la carencia de sldb y la decisión de `ANY_STATE`.
- **Bundle**: bundle-2 dejó 4 ambigüedades: paridad de los pares que no dibujan, quién edita la matriz, `ANY_STATE` en `ir.py` y si la carencia de sldb bloquea. Se resolvieron en «Precisiones (bundle)» y la review se dispuso como `accepted` (`review-task-ir12-…-bundle-2`).
- Las dos reviews quedan `stale` porque la tarea se editó después, igual que en IR11.

`deskops graph missing --root .`: **7 (rc 0)**, antes 11. Ninguno es de IR12; los 7 restantes son de IR13 e IR13d.

## Limpieza de /dev/shm

Se borró todo lo que creé:

- Logs y temporales: `ir12-preflight.log`, `ir12-bundle.log`, `ir12-closeout.log`, `ir12-suite.log`, `ir12-nospec2viz.log`, `ir12-files.json` e `ir12-implpath.txt`.
- El directorio `ir12-nospec2viz/` (el falso spec2viz de la prueba de saltos) y `ir12-wheel/`, de una prueba manual.
- Mis basetemps `pytest-of-robocop/pytest-25`, `-26` y `-27`, y el symlink `pytest-current` que apuntaba a ellos. Las demás ya las había rotado pytest.

El directorio `pytest-of-robocop/` queda vacío y no se borró. Tampoco se tocó `/dev/shm/pi-review.lock` ni nada ajeno.

En el repo también se borró el `build/` que dejó una construcción manual de la wheel. `src/specir.egg-info/` y los `__pycache__` ya estaban sin versionar.

## Pendientes

1. **sldb**: reexportar desde `sldb.api.notations` `resolve_style`, `load_palette`, `NotationError`, `AnyDiagram`, `DiagramType` y `DiagramStoreEnvelope` (nota enviada). Después hay que cambiar los imports de `notation_style.py` y `spec_models.py` y quitar las excepciones de `tests/test_imports.py`. La nota está sin commitear en sldb: la mete su coordinador.
2. **IR13d**: montar `src/specir/cli.py` con la taxonomía completa y los alias de primer nivel (`render`, `lint`, `schema`, `validate`, `build`), usando los grupos de `specir.visual.commands`, y repuntar el script `specir`. Exponer en la API pública `render`, `render_to_file`, `json_schema`, `write_json_schema` y la cabecera. Decidir SV-K16: hoy existe `specir diagram validate` sobre `load_spec`/`validate_spec` de sldb.
3. **IR13 / JP**: decidir si el XML BPMN deja de declarar `exporter="spec2viz"` y `targetNamespace="http://spec2viz/bpmn"`, y si la clave de `localStorage` del catálogo se renombra (con migración de anotaciones). Se dejaron igual para no romper paridad ni datos.
4. **Motor real de mermaid**: con mmdc instalado deberían correr los 10 casos saltados y validarse el pseudoestado `*` y los ids con guion de la proyección de estados.
5. **IR13**: citar en la matriz las pruebas de arriba para las filas de IR12.
