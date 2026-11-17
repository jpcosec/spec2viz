# Acta de retiro de spec2viz

Tarea IR13 (`task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz`). Evaluación del
2026-11-15 sobre IR `dc5496a`, sldb `d4aeb4b1` y el inventario de consumidores de
`docs/spec2viz/matriz-de-cobertura.md`.

**Retiro: no declarado.** El comprobador `specir retirement check` sale con código 1: quedan 63
dependencias de spec2viz en el universo auditado y 8 filas de la matriz sin acreditar (corrida del
2026-11-17 de IR13j, que acreditó SV-H01 con el mensaje de sldb para un `diagram_type` desconocido; eran 9
en la del 2026-11-16 de IR13h, con 0 dependencias de deskops tras su migración a specir; la de IR13g acreditó
SV-H03 y SV-K22 tras la migración de graph_ui en `79d63ee`; eran 11
tras el ciclo de corrección 1 de IR13e, que portó contra sldb las pruebas de notaciones, paletas y vistas
y acreditó SV-G08 y SV-I02; antes de IR13e eran 23, y 30 antes de las decisiones de JP y la corrida con mermaid-cli real). Archivar o borrar
spec2viz lo decide JP cuando el gate se cumpla; esta tarea no lo hace.

## Comprobador

`specir retirement check` (`src/specir/visual/retirement.py`, pruebas en
`tests/visual/test_retirement_gate.py`) audita en solo lectura exactamente los repos y stores del
inventario de la matriz más el repo de specIR, y la sección «Acreditación (IR13)» de la matriz. Cada
dependencia sale con repo o store, ruta, línea y clase (importación, dependencia declarada, invocación del
comando, habilidad de agente, modelo registrado). Un nombre fuera del inventario o uno del inventario sin
ruta es un error de uso (código 2). Las menciones en prosa, documentación, comentarios, docstrings,
changelogs y documentos del desk no cuentan.

Corrida real:

```
cd IR && .venv/bin/specir retirement check \
  --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron \
  --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb
```

rc 1; 85 dependencias; 11 filas no acreditadas (SV-A17, H01, H03, K09, K16, K18, K21, K22, K23, K26 y
K29). Corrida del 2026-11-16, ciclo de corrección 1 de IR13e
(`task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb`), sobre
sldb `3c2186de`, graph_ui `b868673` (con cambios sin commitear en su árbol) y spec2viz `91ba1d0` (b624b75
más un commit solo de desk/store). Antes de IR13e eran 23 filas (SV-A17, E02, G08, H01 a H06, I02, J06,
K09, K16, K18 a K26 y K29) y 119 dependencias; la corrida del intento 1 de IR13e dejó 13 filas (SV-G08 y
SV-I02 seguían abiertas por el xfail de `label_key`, quitado en `4dc8946` tras el arreglo de sldb
`06dbcf02`). Las dependencias bajan de 119 a 85 por cambios ajenos a IR13e: (a) graph_ui pasa de 34 a 0,
pero solo en su árbol de trabajo, que tiene 48 rutas modificadas sin commitear; en su HEAD `b868673`
siguen `from spec2viz.notation_view import …` (`frontends/mindmap/sldb_adapter.py:245`, `:437`) y
`spec2viz>=0.1.0` (`pyproject.toml:19`, `:24`), así que G4 de graph_ui sigue pendiente hasta que lo
commitee y responda; (b) en sldb la importación de `tests/notations/test_component_spec_python.py:43`
desapareció con `ce0bd384` (oráculo de D2 congelado en un golden) y aparece en su lugar
`runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5`. Las 122 de la corrida del 2026-11-15 ya habían
bajado a 119 porque no aparecen las 3 invocaciones de pron (`docs/spec2viz/build.py:22` a `:24`). La prueba
`test_the_real_universe_has_no_dependency_and_every_row_is_accredited` es un xfail estricto mientras esto
siga así: cuando pase, la suite lo marca y hay que quitar el xfail y declarar el retiro aquí.

rc 1; 85 dependencias; 11 filas no acreditadas (SV-A17, H01, H03, K09, K16, K18, K21, K22, K23, K26 y
K29). Corrida del 2026-11-16, IR13f
(`task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5`),
con el mismo comando y `timeout 300`, sobre IR `2e3aab8`, sldb `23140fac`, graph_ui `b868673` (con 52
rutas sin commitear en su árbol), deskops `4e3f657d`, pron `39ea972` y spec2viz `91ba1d0`. Por repo o
store: deskops 22, sldb 1, IR 43, `spec2viz/.sldb` 19, graph_ui 0 (solo por su árbol sin commitear) y pron
0 (no hay filas de pron; su HEAD contiene `4224186`, ver «Consumidores»). Sin cambios en el recuento respecto
de la corrida anterior.

rc 1; 85 dependencias; 9 filas no acreditadas (SV-A17, H01, K09, K16, K18, K21, K23, K26 y K29), las
mismas que quedan abiertas en «Acreditación (IR13)» de la matriz. Corrida del 2026-11-16, IR13g
(`task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee`), con el
mismo comando y `timeout 300`, sobre IR `3ec37f2` (con la matriz de IR13g sin commitear), sldb `b0e4f649`,
graph_ui `824c135` (contiene `79d63ee`; 39 rutas sin commitear en su árbol), deskops `aa25fdb0`, pron
`39ea972` y spec2viz `91ba1d0`. Por repo o store: deskops 22, sldb 1, IR 43, `spec2viz/.sldb` 19,
graph_ui 0 y pron 0. graph_ui ya no depende de spec2viz en su HEAD: `git -C ../UIs/graph_ui grep -nE
'from spec2viz|import spec2viz|spec2viz>=' HEAD` solo encuentra notas y evidencia bajo `desk/` y `runs/`
(ver «Consumidores»). Las 85 dependencias son las mismas de la salida de abajo; las filas bajan de 11 a 9
porque SV-H03 y SV-K22 pasan a cumplidas.

rc 1; 63 dependencias; 9 filas no acreditadas (SV-A17, H01, K09, K16, K18, K21, K23, K26 y K29), las
mismas que quedan abiertas en «Acreditación (IR13)» de la matriz. Corrida del 2026-11-16 a las 19:33
(-03:00), IR13h
(`task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4`), con el mismo
comando y `timeout 300`, sobre IR `4f1e108` (con el acta y la matriz de IR13h sin commitear), sldb
`12e9b191`, graph_ui `824c135` (39 rutas sin commitear en su árbol), deskops `12c5c2ce` (origin/main
`ee9bc3cd`), pron `39ea972` y spec2viz `91ba1d0`. Por repo o store: deskops 0, sldb 1, IR 43,
`spec2viz/.sldb` 19, graph_ui 0 y pron 0. deskops ya no depende de spec2viz: `git -C ../deskops
merge-base --is-ancestor` de `2421ca29`, `74ffdb63` y `b716bf85` contra `origin/main` sale con rc 0, y
`../deskops/.sldb/core/store_index.yaml` solo federa sldb, pron y scion (la única coincidencia de
`grep -n spec2viz` es la etiqueta semántica `system.spec2viz` del modelo `ViewDoc` de sldb, línea 308, no un
enlace de store; ver «Consumidores»). Las dependencias bajan de 85 a 63 porque desaparecen las 22 de
deskops; las 63 son las de la salida de abajo.

rc 1; 63 dependencias; 8 filas no acreditadas (SV-A17, K09, K16, K18, K21, K23, K26 y K29), las mismas
que quedan abiertas en «Acreditación (IR13)» de la matriz. Corrida del 2026-11-17 a las 01:23 (-03:00),
IR13j
(`task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s`),
con el mismo comando y `timeout 300`, sobre IR `c1a1a46` (con la prueba, el acta y la matriz de IR13j sin
commitear), sldb `472f1c80`, graph_ui `440a5683` (44 rutas sin commitear en su árbol), deskops `cfda261b`,
pron `39ea972` y spec2viz `91ba1d0`. Por repo o store: deskops 0, sldb 1, IR 43, `spec2viz/.sldb` 19,
graph_ui 0 y pron 0. sldb conserva como contrato su mensaje, «diagram_type 'mindmap' is not a valid
diagram type» (nota de inbox 20261116-232335, respuesta a la 20261116-022332 de IR13e): el caso changes1 de
test_invalid_notations_are_rejected lo espera sin xfail y `tests/visual/test_notations_parity.py` sale con
89 passed, sin xfailed ni xpassed. Las 63 dependencias son las mismas de la salida de abajo; las filas bajan
de 9 a 8 porque SV-H01 pasa a cumplida.

## Gate G1 a G7

| Ítem | Estado | Evidencia |
|---|---|---|
| G1 Filas cumplidas | abierto | 97 cumplidas y 8 abiertas en «Acreditación (IR13)» de la matriz. IR13j (2026-11-17) acreditó SV-H01: el caso de `diagram_type` desconocido de test_invalid_notations_are_rejected espera el mensaje de sldb, sin xfail (nota 20261116-232335); SV-K21, que dependía de ella, sigue abierta por el comando de sldb que valide una notación. IR13g (2026-11-16) acreditó SV-H03 y SV-K22, al resolverse G4 de graph_ui (`79d63ee`). IR13e (2026-11-16) acreditó SV-E02, SV-H02, SV-H04, SV-H05, SV-H06, SV-J06, SV-K19, SV-K20, SV-K24 y SV-K25, y en su ciclo de corrección 1 SV-G08 y SV-I02 (`tests/visual/test_catalog.py`, 68 passed, sin xfail de `label_key`); la corrida con mermaid-cli real del 2026-11-15 acreditó SV-B03, SV-C13, SV-C14, SV-D01, SV-G03, SV-K12 y SV-K17. |
| G2 Suite de spec2viz | abierto | Portadas contra sldb por IR13e en `tests/visual/test_notations_parity.py` (89 passed desde IR13j, sin xfailed ni xpassed): 42 pruebas de `tests/test_view_doc.py`, `test_notation.py`, `test_notation_view.py`, `test_view_contract_resolved.py` y `test_style_palette.py`, más 9 comparaciones «valida igual» (51); la parte de CLI de las 6 que invocan el CLI de spec2viz tiene su equivalente en las filas K, y la validación tipada sin CLI de dos de ellas está portada (test_notation_load_gives_typed_errors, 7 casos; test_palette_check_is_typed, 6 casos). El caso de `diagram_type` desconocido de test_invalid_notations_are_rejected ya no es xfail: espera el mensaje de sldb, que sldb conserva como contrato (SV-H01, IR13j, nota 20261116-232335). Los casos de mmdc (`test_mermaid_mmdc.py` y los de motor real de `test_class_diagram.py`, `test_class_packages.py` y `test_catalog_resolved_views.py`) ya corren con mermaid-cli real y pasan (2026-11-15). `label_key` frente a `normKey` (`test_atoms_matching.py`): ya no es xfail (sldb `06dbcf02`, IR `4dc8946`; `tests/visual/test_catalog.py` 68 passed). Los 38 archivos tienen fila (`tests/test_matriz_cobertura_spec2viz.py`, 5 passed). |
| G3 CLI | abierto | Los 30 equivalentes existen y los invoca `test_every_equivalent_of_the_table_answers_its_help` (`tests/visual/test_cli.py`, 44 passed). Faltan los comandos de sldb para validar notación y paleta (SV-K21, SV-K26) y el de validar un spec, que hoy da specIR de forma provisional (SV-K16, SV-K29). Nota de sldb `20261115-192054`. |
| G4 Consumidores | abierto | 63 dependencias (abajo; corrida del 2026-11-16 de IR13h): sldb 1 (`runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5`), IR 43 (los oráculos de paridad en pruebas, que se retiran al declarar) y `spec2viz/.sldb` 19 (G5). graph_ui (`79d63ee`), pron (`4224186`) y deskops (`ee9bc3cd`; closeouts `74ffdb63`, `b716bf85` y `2421ca29`) están resueltos y salen con 0 (ver «Consumidores»). |
| G5 Stores | decidido; pendiente de ejecución en IR | `spec2viz/.sldb` registra los 7 modelos de `spec2viz.sldb_models` (19 registros). Es el único store del universo que lo hace. Decisión de JP del 2026-11-16 (transmitida por el supervisor; nota de spec2viz `desk/inbox/20261116-021430-suggestion-g5-decisi-n-de-jp-sobre-spec2viz-sldb.md`): opción A, el store `spec2viz/.sldb` se archiva junto con el repo spec2viz cuando `specir retirement check` dé 0, y no se reapuntan sus 7 modelos. Registro en spec2viz: atom `atom-decisión-de-jp-2026-11-16-g5-el-store-spec2viz-sldb-se-archiva-con-el-repo` y task.decision `task-decisión-de-jp-g5-del-retiro-archivar-el-store-spec2viz-sldb-con-el-repo-o-reapuntar-sus-7-modelos-a`. Resuelta en IR: las pruebas ya no federan ese store (`task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a`, código `b16aab7`, closeout `4f1e108`), después de que deskops quitara su enlace al store de spec2viz (`421d6a27`, closeout `74ffdb63`; pedido en la nota de inbox 20261116-122447). Pendiente: quitar `spec2viz/.sldb` del universo de `specir retirement check` al declarar el retiro (IR13) y archivar el store con el repo spec2viz. |
| G6 specIR limpio | cumplido | `tests/test_imports.py` (9 passed): nada bajo `src/specir/` importa spec2viz; `test_specir_defines_no_command_the_table_gives_to_sldb`. |
| G7 Decisión del YAML | cumplido | JP aceptó el 2026-11-15 (vía supervisor) que el YAML del spec queda como formato de autoría e intercambio subordinado al grafo: `docs/decisiones/fuente-de-verdad-del-diagrama.md` y atom `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al` (la propuesta de IR07 quedó como redirección). |

## Consumidores

| Consumidor | Dependencias (clase) | Mensaje enviado | Cambio que lo resolvió |
|---|---|---|---|
| graph_ui | 34: 9 importaciones (`frontends/mindmap/sldb_adapter.py:245`, `:437` y pruebas), 3 declaradas (`pyproject.toml:19`, `:24`, `.github/requirements-suite.txt:10`), 22 invocaciones en pruebas (corrida del 2026-11-15); 0 desde la del 2026-11-16 (en las de IR13e e IR13f solo por su árbol sin commitear; en la de IR13g con HEAD `824c135`, que contiene `79d63ee`) | `UIs/graph_ui/desk/inbox/20261115-224814-suggestion-ir13-pide-migrar-graph-ui-de-spec2viz-a-sldb-resolve-view-sync-de-specs-viewdoc-pilotos.md` | resuelto: graph_ui `79d63ee` (master; closeout `c9b09f7`; nota `desk/inbox/20261116-131509-suggestion-ir13-graph-ui-ya-no-depende-de-spec2viz-79d63ee-closeout-c9b09f7.md`): producción, pruebas y empaquetado usan `sldb.api.notations` (`resolve_view`, `resolve_documents`, `ViewError`), `sldb notations sync --spec` y `ViewDoc` de sldb, con los pilotos copiados de spec2viz `2a218b1` en `tests/fixtures/notation-pilots/`. Comprobado desde IR el 2026-11-16 (IR13g): `git -C ../UIs/graph_ui merge-base --is-ancestor 79d63ee HEAD` rc 0 (HEAD `824c135`), `git grep -nE 'from spec2viz\|import spec2viz\|spec2viz>=' HEAD` sin coincidencias fuera de `desk/` y `runs/`, y la corrida de IR13g sin filas de graph_ui. Pendiente sin efecto en specir: `.github/workflows/ci.yml` (líneas 47 y 112) todavía pasa `--src` a pip, sin uso; no cuenta como dependencia para el comprobador |
| deskops | 22: 20 de habilidad de agente (`.claude/skills/deskops-workflow/SKILL.md`, `references/spec2viz-cli.md`, `.opencode/skills/use-spec2viz/SKILL.md`), 2 invocaciones (`desk/drawer/plans/workspace-documental/render_diagram.py:7`, `:9`), corrida del 2026-11-15 (y las de IR13e, IR13f e IR13g); 0 desde la del 2026-11-16 de IR13h (HEAD `12c5c2ce`, origin/main `ee9bc3cd`). Además, la regla de rutas `deskops/graph/desk_graph.py:75` (no es dependencia; decidida, ver «Decisiones» 4) | `deskops/desk/inbox/20261115-224757-suggestion-ir13-pide-migrar-las-habilidades-y-el-script-de-deskops-de-spec2viz-a-specir.md` | resuelto: deskops origin/main `ee9bc3cd` (aviso de su coordinador del 2026-11-16), en tres pares de commit y closeout, todos en origin: el enlace federado al store de spec2viz sale de su `.sldb` (`421d6a27`, closeout `74ffdb63`; G5 opción b), la regla de `deskops/graph/desk_graph.py:75` deja de nombrar spec2viz y reconoce los specs YAML sincronizados (`42b752ea`, closeout `b716bf85`) y las skills y el script `render_diagram.py` dejan de invocar spec2viz y usan specir (`ce66f69e`, closeout `2421ca29`). Comprobado desde IR el 2026-11-16 (IR13h): `git -C ../deskops merge-base --is-ancestor` de `2421ca29`, `74ffdb63` y `b716bf85` (y de `421d6a27`, `42b752ea` y `ce66f69e`) contra `origin/main` rc 0; `../deskops/.sldb/core/store_index.yaml` federa solo sldb, pron y scion (`grep -n spec2viz` solo encuentra la etiqueta `system.spec2viz` del modelo `ViewDoc` de sldb, línea 308); la corrida de IR13h no tiene filas de deskops. Quedan menciones en prosa (la remisión de `.opencode/skills/use-spec2viz/SKILL.md` a use-specir), que no cuentan para el comprobador |
| pron | 3 invocaciones (`docs/spec2viz/build.py:22`, `:23`, `:24`), corrida del 2026-11-15; 0 desde la del 2026-11-16 | `pron/desk/inbox/20261115-224816-suggestion-ir13-pide-pasar-docs-spec2viz-build-py-de-pron-de-spec2viz-a-specir.md` | resuelto: pron `4224186527a894da6a7842ffa03c313292437425` (master, pusheado; nota `desk/inbox/20261116-040635-suggestion-pron-ir13-resuelto-4224186.md`): `docs/spec2viz/build.py` usa specir en las tres llamadas de las líneas 22 a 24 (`diagram validate`, `diagram render`, `catalog build`). Su tester independiente verificó build.py rc 0 con specir y `specir retirement check` sin filas de pron. Comprobado desde IR el 2026-11-16 (IR13f): `grep -n specir ../pron/docs/spec2viz/build.py` muestra las líneas 22 a 24, `git -C ../pron merge-base --is-ancestor 4224186 HEAD` rc 0 (HEAD `39ea972`) y la corrida de IR13f no tiene filas de pron |
| sldb | 1 importación: el oráculo de D2 de `tests/notations/test_component_spec_python.py:43` se congeló en un golden en `ce0bd384` y queda el generador `runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5`. Además, el registro `docs/architecture/spec2viz/vistas.yml` que se construye con `spec2viz catalog build` y `contracts/identity.toml:299` (no son dependencias para el comprobador) | `sldb/desk/inbox/20261115-224828-suggestion-ir13-pide-migrar-lo-que-queda-de-sldb-sobre-spec2viz-or-culo-de-d2-vistas-yml-identity-toml.md` | pendiente |
| store `spec2viz/.sldb` | 19 modelos registrados | `spec2viz/desk/inbox/20261115-225013-suggestion-ir13-el-store-de-spec2viz-es-el-nico-que-registra-spec2viz-sldb-models-gate-g5.md` | pendiente |
| IR (specIR) | 43 importaciones, todas en pruebas: los oráculos de paridad (`tests/visual/parity.py`, `render_parity.py` y los `importorskip("spec2viz")` de las pruebas de paridad) y la lectura del CLI de spec2viz en `tests/test_matriz_cobertura_spec2viz.py:31`. Se saltan sin spec2viz. | propio: se resuelve en IR al declarar el retiro (quitar oráculos que ya tienen goldens, guardar como golden la corrida de paridad del catálogo de IR13b) | pendiente |

Para enviar los mensajes se registraron en `desk/registry` de IR los repos deskops, pron, graph_ui (id
`graph-ui`) y spec2viz con `deskops repo register`; antes solo estaba sldb.

## Salida del comprobador (dependencias)

```
sldb	runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5	importación	from spec2viz.generators import python_ast
IR	tests/test_matriz_cobertura_spec2viz.py:31	importación	main = importlib.import_module("spec2viz.cli").main
IR	tests/visual/parity.py:52	importación	from spec2viz.compilers import compile_ir
IR	tests/visual/parity.py:53	importación	from spec2viz.loader import load
IR	tests/visual/parity.py:54	importación	from spec2viz.validator import validate
IR	tests/visual/render_parity.py:74	importación	from spec2viz.compilers import compile_ir
IR	tests/visual/render_parity.py:75	importación	from spec2viz.loader import load
IR	tests/visual/render_parity.py:76	importación	from spec2viz.renderers import render
IR	tests/visual/render_parity.py:77	importación	from spec2viz.renderers.bpmn import render_bpmn_html
IR	tests/visual/render_parity.py:87	importación	from spec2viz.cli import DIAGRAM_RENDERERS
IR	tests/visual/render_parity.py:88	importación	from spec2viz.renderers import DEFAULT_RENDERER, EXT_MAP
IR	tests/visual/render_parity.py:94	importación	from spec2viz.renderers.view_mermaid import view_to_mermaid
IR	tests/visual/render_parity.py:100	importación	from spec2viz.linters.mermaid import lint_mermaid
IR	tests/visual/render_parity.py:106	importación	from spec2viz.schema import json_schema
IR	tests/visual/render_parity.py:112	importación	from spec2viz import render_to_file
IR	tests/visual/render_parity.py:119	importación	import spec2viz
IR	tests/visual/render_parity.py:190	importación	from spec2viz.linters.mermaid import lint_mermaid
IR	tests/visual/render_parity.py:191	importación	from spec2viz.schema import json_schema
IR	tests/visual/test_catalog_parity.py:39	importación	spec2viz = pytest.importorskip("spec2viz")
IR	tests/visual/test_catalog_parity.py:49	importación	from spec2viz.sldb_sync import check_catalog as oracle
IR	tests/visual/test_catalog_parity.py:102	importación	from spec2viz.sldb_sync import SpecSync as OracleSync
IR	tests/visual/test_catalog_parity.py:103	importación	from spec2viz.sldb_sync import sync_catalog as oracle_sync
IR	tests/visual/test_catalog_parity.py:122	importación	from spec2viz.cli import main
IR	tests/visual/test_catalog_parity.py:154	importación	from spec2viz.deskops import render_deskops
IR	tests/visual/test_catalog_parity.py:203	importación	from spec2viz.deskops import render_deskops
IR	tests/visual/test_lint_mermaid.py:86	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_cases.py:314	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_commands.py:251	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_parity.py:53	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_parity.py:59	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_parity.py:83	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_resources.py:62	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_schema.py:44	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:105	importación	spec2viz = pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:117	importación	from spec2viz.sldb_sync import SpecSync as Spec2VizSync
IR	tests/visual/test_sync_generation_parity.py:201	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:229	importación	import spec2viz.graph_import as oracle
IR	tests/visual/test_sync_generation_parity.py:258	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:259	importación	from spec2viz.graph_import import component_spec_from_graph as oracle_from_graph
IR	tests/visual/test_sync_generation_parity.py:260	importación	from spec2viz.graph_import import load_store_index
IR	tests/visual/test_sync_generation_parity.py:302	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:303	importación	from spec2viz.generators.python_ast import generate_python_ast_spec
IR	tests/visual/test_visual_parity.py:35	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_visual_parity.py:43	importación	pytest.importorskip("spec2viz")
spec2viz/.sldb	store.yaml:44	modelo registrado	model_ref: spec2viz.sldb_models:SpecDoc
spec2viz/.sldb	store.yaml:47	modelo registrado	model_ref: spec2viz.sldb_models:SpecNodeDoc
spec2viz/.sldb	store.yaml:50	modelo registrado	model_ref: spec2viz.sldb_models:NotationDoc
spec2viz/.sldb	store.yaml:53	modelo registrado	model_ref: spec2viz.sldb_models:GlyphDoc
spec2viz/.sldb	store.yaml:56	modelo registrado	model_ref: spec2viz.sldb_models:LinkDoc
spec2viz/.sldb	core/store_index.yaml:141	modelo registrado	model_ref: spec2viz.sldb_models:SpecDoc
spec2viz/.sldb	core/store_index.yaml:154	modelo registrado	model_ref: spec2viz.sldb_models:SpecNodeDoc
spec2viz/.sldb	core/store_index.yaml:167	modelo registrado	model_ref: spec2viz.sldb_models:NotationDoc
spec2viz/.sldb	core/store_index.yaml:180	modelo registrado	model_ref: spec2viz.sldb_models:GlyphDoc
spec2viz/.sldb	core/store_index.yaml:193	modelo registrado	model_ref: spec2viz.sldb_models:LinkDoc
spec2viz/.sldb	core/store_index.yaml:246	modelo registrado	model_ref: spec2viz.sldb_models:ViewDoc
spec2viz/.sldb	core/store_index.yaml:259	modelo registrado	model_ref: spec2viz.sldb_models:PaletteDoc
spec2viz/.sldb	core/models/GlyphDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:GlyphDoc
spec2viz/.sldb	core/models/LinkDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:LinkDoc
spec2viz/.sldb	core/models/NotationDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:NotationDoc
spec2viz/.sldb	core/models/PaletteDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:PaletteDoc
spec2viz/.sldb	core/models/SpecDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:SpecDoc
spec2viz/.sldb	core/models/SpecNodeDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:SpecNodeDoc
spec2viz/.sldb	core/models/ViewDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:ViewDoc
```

## Medición de `specir catalog build` (pendiente de IR13d)

`specir catalog build --config tests/visual/fixtures/catalog/examples/catalog/project.yml` dentro de IR
no termina en 300 s (`timeout 300`, rc 124, 3 min 50 s de CPU). Con cProfile (corrida cortada a los
150 s), 146 de los 149 s se van en `sldb.api.matching.attach_atom_edges`. Esa función hace 31 llamadas a
`StoreReader.edges_of`, que suman 62 llamadas a `load_edge_index` de ~1,1 s cada una:

- `with_live_stale` recalcula el stale vivo en cada llamada (284 251 `_moved`, 63 s).
- `EdgeIndex._ensure_maps` reconstruye los mapas en cada copia (61 veces, 66 s).

El store que descubre el catálogo es el `.sldb` de IR, que federa 8 stores (con `deskops` y `sldb`
duplicados desde `/mnt/ssd/herramientas`). Ahí `load_edge_index` tarda 28,6 s la primera vez y 0,4 s las
siguientes, pero devuelve un objeto nuevo cada vez (1963 stale).

Es de sldb, no de specIR: specIR solo usa la API pública. Pedido en
`sldb/desk/inbox/20261115-224941-suggestion-matching-edges-catalog-build-con-tomos-tarda-minutos-porque-cada-edges-of-recompone-live-stale-y-mapas-del-ndice-federado.md`.

## Lo que falta para declarar el retiro

1. Consumidores (G4): que sldb resuelva su pedido y responda con el commit
   (`runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5`); lo demás que queda en G4 es de IR (los
   oráculos de paridad en pruebas, punto 6, que se retiran al declarar) y `spec2viz/.sldb` (G5, punto 2).
   pron quedó resuelto con `4224186`, graph_ui con `79d63ee` y deskops con `ee9bc3cd` (closeouts
   `74ffdb63`, `b716bf85` y `2421ca29`).
2. Store (G5): decidido por JP el 2026-11-16 (opción A): `spec2viz/.sldb` se archiva con el repo spec2viz
   cuando `specir retirement check` dé 0, sin reapuntar sus 7 modelos. Las pruebas ya no lo federan:
   `task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a` quedó resuelta en IR
   (`b16aab7`, closeout `4f1e108`), después de que deskops quitara su enlace (`421d6a27`, closeout
   `74ffdb63`; pedido en la nota 20261116-122447). Queda quitarlo del universo del comprobador al declarar
   el retiro y archivarlo con el repo.
3. Filas «usar sldb directamente»: portadas por IR13e (`tests/visual/test_notations_parity.py`). Quedan
   SV-A17 (solo G5), y SV-K18 y SV-K23 (dependen de SV-K21 y SV-K26). SV-H03 y su dependiente SV-K22
   quedaron cumplidas en IR13g (graph_ui `79d63ee`), y SV-H01 en IR13j (el caso de `diagram_type`
   desconocido espera el mensaje de sldb, nota 20261116-232335); SV-K21, que dependía de SV-H01, sigue
   abierta por el comando de sldb (punto 4).
4. sldb: comando para validar spec, notación y paleta (SV-K16, K21, K26, K29; después hay que retirar
   `specir diagram validate`/`validate`). El `label_key` con `_` (SV-G08 y SV-I02) quedó resuelto
   (sldb `06dbcf02`, IR `4dc8946`).
5. mmdc: resuelto el 2026-11-15. Con mermaid-cli real (`SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc`)
   pasan los casos de motor real; quedaron cumplidas SV-B03, C13, C14, D01, G03, K12 y K17. SV-K09 sigue
   abierta por SV-K16.
6. IR: quitar o congelar los oráculos de paridad en las pruebas (la federación del store de spec2viz ya
   salió de las pruebas con `b16aab7`; ver punto 2).
7. G7: resuelto el 2026-11-15 (decisión aceptada por JP; ver «Decisiones»).
8. En el momento del retiro: el BPMN pasa a `exporter="specir"` y a un `targetNamespace` de specir, y la
   página del catálogo a una clave de `localStorage` de specir, con goldens nuevos y migración de las
   anotaciones guardadas con `spec2viz.catalog.annotations.v1` (decisión 3).
9. Archivar spec2viz cuando `specir retirement check` salga con 0 (decisión 6).

## Decisiones

Registradas el 2026-11-15. Todas aceptadas por JP (transmitidas por el supervisor con autorización
explícita).

1. **G7, el YAML del spec** (decisión del dueño, JP): el YAML del spec queda como formato de autoría e
   intercambio subordinado al grafo, según `docs/decisiones/fuente-de-verdad-del-diagrama.md`. Registro:
   atom `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`
   (la propuesta `atom-propuesta-pendiente-de-jp-…` se fusionó en él con `deskops atoms merge`). No hay
   task.decision asociada a G7 en el desk de IR.
2. **mmdc con motor real**: JP autorizó lanzar `/usr/bin/google-chrome` para mermaid-cli. Instalado en
   `/mnt/ssd/herramientas/mermaid-cli` (fuera de los repos), con un envoltorio `mmdc` que corre Chrome en
   headless con `timeout` y perfil temporal en `/dev/shm`. Cómo apuntar `SPECIR_MMDC`: habilidad
   `skills/use-specir/SKILL.md`, sección «Real mermaid engine (mmdc)».
3. **Exporter de BPMN y clave de `localStorage`** (elegida por el coordinador): mientras dure la paridad se
   mantienen `exporter="spec2viz"`, `targetNamespace="http://spec2viz/bpmn"` (SV-C06) y la clave
   `spec2viz.catalog.annotations.v1` (SV-G06). En el momento del retiro pasan a specir con goldens nuevos
   y migración de anotaciones (paso 8 de la lista anterior).
4. **deskops, regla de rutas** (elegida por el coordinador; la ejecuta el desk de deskops, no IR):
   `deskops/graph/desk_graph.py:75` deja de nombrar spec2viz y reconoce los specs YAML como artefactos de
   autoría sincronizados con `sldb notations sync`.
5. **sldb, `docs/architecture/spec2viz`** (elegida por el coordinador; la ejecuta el desk de sldb, no IR):
   los specs se quedan como fixtures durante la paridad; el catálogo se construye con
   `specir catalog build` y se sincroniza con `sldb notations sync --catalog`.
6. **Archivo de spec2viz**: spec2viz se archiva cuando `specir retirement check` salga con 0.
