# IR11: informe del worker

Tarea: `task-ir11-compiladores-y-proyecciones-de-spec2viz`, directo en IR main.

## Aviso: carencia de sldb

`sldb.api.notations` exporta `load_spec` y `validate_spec`, pero **no exporta las clases** de los modelos
de spec de D3: `ClassDiagram`, `SequenceDiagram`, `StateDiagram`, `ComponentDiagram`, `ActivityDiagram`,
`DeploymentDiagram`, `MatrixDiagram`, `ReflectionDiagram`, `BaseDiagram`, `EnforcementArtifact` y
`EnforcementFact`. Solo se alcanzan en `sldb.models.notation.diagram_specs`. El brief daba por hecho
que se exportaban. El compilador de reflexión necesita construir `EnforcementArtifact`/`EnforcementFact`,
y redefinirlas en specIR duplicaría código de sldb.

Decisión (reversible): un único módulo, `src/specir/visual/spec_models.py`, importa esas clases de
`sldb.models.notation.diagram_specs`. `tests/test_imports.py` tiene una excepción limitada a ese módulo,
y una prueba nueva (`test_only_spec_models_reaches_the_diagram_spec_models`) comprueba que ningún otro
módulo las alcanza. Se pidió a sldb que las reexporte
(`sldb/desk/inbox/20261115-193320-suggestion-ir-pide-exportar-desde-sldb-api-notations-los-modelos-de-spec-de-d3-y-guardar-style-y-entity-en-specdoc.md`,
sin commitear en sldb: lo debe meter su coordinador). Cuando sldb las exporte, solo cambian los imports de
`spec_models.py` y se quita la excepción. La carencia quedó escrita en el `implementation_path` de la tarea.

## Commits (IR main, sin push)

- `465d5a6`: código y pruebas.
- `33efec7`: desk (precisiones de preflight y bundle, `files` de la tarea, reviews preflight-5 y bundle-2 dispuestas, evidencia en `runs/subagents/20261115-222129` y `20261115-223526`).
- `c4eb451`: cierre `resolved-by` (refs 465d5a6 y 33efec7; tests: los 6 `tests/visual/test_visual_*.py` y `tests/test_imports.py`).

## Qué se migró y adónde

Origen: spec2viz `2de1056`, sin tocar.

| Origen (spec2viz) | Destino (IR) | Cómo |
|---|---|---|
| `spec2viz/ir.py` | `src/specir/visual/ir.py` | Copiado tal cual; solo cambia el docstring. |
| `spec2viz/compilers/{__init__,activity,class_diagram,component,deployment,matrix,reflection,sequence,state}.py` | `src/specir/visual/compilers/` | Copiados tal cual. Solo cambian los imports: modelos desde `specir.visual.spec_models` (sldb D3), IR desde `specir.visual.ir`. Se quitó el import sin uso de `MatrixComponentModel`. |
| `spec2viz/exceptions.py` (`Spec2VizError`, `CompileError`) | `src/specir/visual/exceptions.py` | `RenderError` le queda a IR12. `Spec2VizError` entra ya porque es la base de `CompileError`. |
| Las 44 especificaciones del corpus (`tests/fixtures` con `invalid/`, `examples/`, `docs/architecture/spec2viz/`) | `tests/visual/fixtures/spec2viz/` con las mismas rutas | Copia. |
| `tests/test_ir.py` (3) | `tests/visual/test_visual_ir.py` | Portadas. |
| `tests/test_compilers.py` (17), `test_compile_*` de `tests/test_api.py` (6), `tests/test_reflection_compiler.py` (1), los casos de compilación de `test_class_diagram.py` (sin el `json_schema`, que es de IR12), `test_class_packages.py::test_ir_knows_paths_and_owners`, `test_activity_lanes.py::test_fields_reach_the_ir` y los asertos de `CompileError` de `test_exceptions.py` | `tests/visual/test_visual_compilers.py` (28) | Portadas, cargando con `sldb.api.notations.load_spec`/`validate_spec`. |

Lo nuevo en specIR:

- `normalize.py`: normalización estructural. Ordena nodos, aristas, estados, transiciones, artefactos, conexiones, paquetes, relaciones, spans y `contains`. Conserva el orden de pasos, participantes, mensajes, miembros, stages, rows y facts. Excluye la procedencia (`origen`, marcas de tiempo, rutas, `sha256`). Expone `equivalent` y `differences`.
- `projections.py`: proyecciones a la IR, todo por la API pública de sldb.
  - Un ViewDoc de proyección se evalúa con `evaluate_projection_view`.
  - Un ViewDoc compuesto se evalúa con `run_view`; las secciones se leen con `list_projection_views`.
  - Un SpecDoc se resuelve con `resolve_view`. Las notas de `RelationDoc` y el `contains` de `SpecNodeDoc` salen de `load_runtime_documents`.
  - Componentes: el grafo pasa por `component_spec_from_graph` de D2, se valida como `ComponentDiagram` de sldb y se compila con el compilador migrado.
  - Estados: se construyen a partir de `StateDoc`, `DomainEntityDoc` y las aristas `transitions`. El grafo no dice desde qué estado parte una operación, así que `from_` queda `ANY_STATE = "*"`. El estado inicial es el único estado al que no lleva ninguna operación.
- `spec_models.py`: el módulo que reúne los modelos de sldb (ver el aviso).
- `__init__.py`: exporta la IR, los compiladores, la normalización, las proyecciones y los modelos de spec. `load_spec` y `validate_spec` no se reexportan: se usan desde sldb directamente.

## Diferencias declaradas en la matriz

Ninguna. En las 44 especificaciones del corpus, specIR da el mismo resultado que spec2viz: mismo error
tipado (clase y texto) en las 8 que spec2viz rechaza y una IR estructuralmente idéntica en las 36 válidas,
de los 8 tipos. La matriz no se tocó.

Fuera de la paridad con spec2viz (spec2viz no tenía SpecDoc→IR), queda una diferencia documentada en
`projections.SPEC_DOC_GAPS`, con su prueba. SpecSync (D1) no guarda en el store el `style.kinds` del
spec ni el `data.entity` de un spec de estado, así que la IR de un SpecDoc tiene `style_kinds` vacío
(componentes) y `entity` vacío (estados). Se pidió a sldb en la misma nota.

## Validación (tests con TMPDIR=/dev/shm)

| Prueba | rc | Resultado |
|---|---|---|
| `tests/test_imports.py` | 0 | 5 passed |
| `tests/visual/test_visual_ir.py` + `test_visual_compilers.py` | 0 | 31 passed |
| `tests/visual/test_visual_parity.py` | 0 | 90 passed: 44 contra los goldens, 44 contra spec2viz vivo, goldens iguales a la última ejecución de spec2viz, y cobertura de los 8 tipos y de los errores tipados |
| `tests/visual/test_visual_normalize.py` | 0 | 5 passed |
| `tests/visual/test_visual_names.py` | 0 | 4 passed |
| `tests/visual/test_visual_projections.py` | 0 | 9 passed |
| **Suite completa de IR**: `pytest -q -n 4 tests/` | 0 | **173 passed, 2 xfailed** (los 2 xfail estrictos ya existían en `test_blog_chain.py`) |

Cómo se cubre cada punto de la sección Validation:

- **Los 8 tipos y la paridad**: `test_visual_parity`. El oráculo vivo está marcado `parity` y se salta si spec2viz no está instalado; los goldens se comprueban siempre.
- **La normalización**: `test_visual_normalize`. Comprueba que el orden y la procedencia no cuentan, y que un cambio de campo, de nodo, de arista o de extremos sí.
- **Errores tipados**: incluidos en el resultado de la paridad (clase y texto).
- **Post**: las proyecciones de componentes y de estados del blog de IR06 muestran Post. El store sigue con un solo documento (`DomainEntityDoc:post`) y su digest no cambia.
- **Spec autorado frente a proyección**: `fixtures/blog/component.publish-components.yml` y `ViewDoc:publish-components` dan IR equivalentes. También un ViewDoc compuesto (`run_view`) frente a su proyección equivalente; ese ViewDoc se crea por MCP y se borra al terminar la prueba.
- **SpecDoc**: 5 especificaciones (3 de componentes y 2 de estados) sincronizadas con `sldb notations sync --spec` en un store nuevo dan la IR de su YAML, salvo `SPEC_DOC_GAPS`.
- **Nombres**: `test_visual_names` comprueba que specIR no define ninguna clase con el nombre de un modelo de vocabulario visual de sldb (los `*Doc` de notación y los `*Spec` de `sldb.notations`) ni de un modelo de spec (los 8 y todos sus submodelos), y que spec2viz solo lo importa `tests/visual/parity.py`.

`deskops graph missing --root .`: 11 (rc 0), igual que antes.

Reviews: preflight-5 (la anterior había llegado al tope de intentos; se forzó porque la tarea cambió con
D3) y bundle-2. Las ambigüedades se resolvieron con `deskops edit task` (`implementation_path`
«Precisiones (preflight)» y «Precisiones (bundle)», y `files`) y ambas reviews quedaron dispuestas como
`accepted`.

## Entorno

Se instaló en `IR/.venv`: spec2viz editable desde `../spec2viz` (con `--no-deps`; el repo spec2viz
sigue limpio), `pytest-xdist` 3.8.0 y `execnet` 2.1.2.

## Limpieza de /dev/shm

Se borró todo lo que creé:

- Logs: `ir11-preflight.log`, `ir11-bundle.log`, `ir11-suite.log`.
- Temporales: `ir11-implpath.txt`, `ir11-files.txt`.
- Stores de prueba: `ir11-probe/` (blog y store de specs).
- basetemps de pytest: `pytest-of-robocop/` (pytest-18, pytest-19, pytest-20, `pytest-current`, más `core/` y `.sldb_cache/` que dejaron las corridas), y el directorio vacío.

`/dev/shm/pi-review.lock` es el lock compartido y no se tocó.

## Pendientes

1. sldb: reexportar los modelos de spec desde `sldb.api.notations`. Después, cambiar los imports de `spec_models.py` y quitar la excepción de `tests/test_imports.py`.
2. sldb (D1): guardar `style` y `data.entity` en el SpecDoc. Después, vaciar `SPEC_DOC_GAPS`.
3. La nota en el inbox de sldb está sin commitear allí: la mete el coordinador de sldb.
4. IR12: `RenderError` va en `src/specir/visual/exceptions.py`, junto a `Spec2VizError`/`CompileError`. Los casos de render de `test_class_*`, `test_activity_lanes` y `test_deployment_nested` le corresponden a IR12. Los casos de validación de esos archivos son de D3 y ya los cubre la paridad de errores.
5. IR13 acredita las filas SV-B01 a SV-B10 y SV-A14 citando estas pruebas. Esta tarea no marca nada como cumplido en la matriz.
6. Convención de la proyección de estados (`from_="*"`): el renderer de IR12 debe saber dibujarla.
