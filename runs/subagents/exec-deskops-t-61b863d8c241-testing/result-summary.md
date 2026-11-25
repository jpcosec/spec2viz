PASA

# Resultado de testing — task-ir-borra-los-goldens-de-spec2viz...

## Trabajo revisado

- Commit del ejecutor: `735cd5766919f452caa33e93d114d5cc1bcac32a`
  (`test: remove spec2viz goldens and the tests that only compared against them`)
- Toca solo `tests/` y `pyproject.toml` (no hay código de producción en `src/`), por lo que no
  corresponde ejecutar `tests/test_<modulo>.py` adicionales.
- Los archivos `test_*.py` modificados o añadidos por el commit se corrieron uno a uno.

## Verificación de aceptación

Presencia/ausencia (todo confirmado en el árbol de trabajo):

- Ausentes: `tests/visual/goldens/`, `oracle.py`, `parity.py`, `render_parity.py`,
  `test_render_parity.py`, `test_catalog_parity.py`, `test_visual_parity.py`,
  `test_notations_parity.py`, `test_sync_generation_parity.py`, `test_retirement_gate.py`,
  `tests/test_matriz_cobertura_spec2viz.py`, `tests/visual/fixtures/spec2viz-notations/`.
- Sin marcador `parity` en `pyproject.toml` ni referencias en `tests/conftest.py`.
- `grep -rniE 'spec2viz-2de1056|oracle|goldens|parity' tests/ pyproject.toml` sobre archivos
  versionados: **sin coincidencias**.
- `grep -rn 'spec2viz-notations|goldens|oracle|render_parity|...' tests/ --include='*.py'`:
  sin referencias a módulos o fixtures borrados.
- Se conservó y movió el caso de comportamiento pedido:
  `tests/visual/test_render_projections.py::test_the_projected_states_of_the_blog_render`
  (proyección de la cadena del blog), y pasa.
- `pytest --collect-only tests/visual`: 378 tests recolectados sin errores de importación.

## Pruebas ejecutadas

Entorno del contenedor: el `.venv` del workspace fue creado con Python 3.12, pero su
`bin/python3` apunta a `/usr/bin/python3` (3.11 en este contenedor) y su `pytest` no es
importable con ese intérprete. Para no tocar el venv compartido se usó el Python 3.12.16 de
uv (`uv python install 3.12`) con el `site-packages` 3.12 del venv en `PYTHONPATH` y un
directorio shim `/tmp/ir-testbin` que aporta los ejecutables `sldb` y `specir` junto al
intérprete (los tests los buscan con `Path(sys.executable).with_name("sldb")`).
`TMPDIR=/tmp` y `--basetemp` en `/tmp` en todas las corridas.

| Archivo | Resultado |
|---|---|
| `tests/visual/test_cli.py` | 40 passed |
| `tests/visual/test_lint_mermaid.py` | 6 passed, 7 skipped (sin `mmdc`) |
| `tests/visual/test_refs_models.py` | 12 passed |
| `tests/visual/test_render_cases.py` | 19 passed, 3 skipped (sin `mmdc`) |
| `tests/visual/test_render_commands.py` | 27 passed |
| `tests/visual/test_render_projections.py` | 7 passed |
| `tests/visual/test_renderers.py` | 56 passed |
| `tests/visual/test_resources.py` | 6 passed (con `uv` en PATH) |
| `tests/visual/test_schema.py` | 10 passed |
| `tests/visual/test_visual_names.py` | 4 passed |

Todos con rc=0. Los skips son los esperados por ausencia de `mmdc` (mermaid-cli) en el
contenedor; las reglas regex de lint sí se ejercitaron. El test de wheel de
`test_resources.py` se saltaba sin `uv` en PATH, por eso se repitió con
`/home/scion/.local/bin` en PATH y pasó.

No se corrió la suite completa, según la instrucción del tester.

## Observaciones (fuera de alcance, no bloquean)

- `src/specir/visual/notation_style.py:10` conserva un docstring que menciona
  `tests/visual/test_notations_parity.py`, archivo ya borrado. `src/` está explícitamente
  fuera del alcance y el grep de aceptación solo cubre `tests/` y `pyproject.toml`.
- Quedan `__pycache__/*.pyc` no versionados de los módulos de paridad borrados; no son
  archivos del repositorio ni se recolectan. El grep sobre archivos versionados está limpio.

## Veredicto

PASA: se borró lo que solo comparaba contra spec2viz, se conservó/movió la prueba de
comportamiento de la cadena del blog, el marcador `parity` desapareció y todos los archivos
de prueba tocados pasan.
