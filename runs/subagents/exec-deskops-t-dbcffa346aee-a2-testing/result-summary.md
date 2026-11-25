PASA

# Resultado del tester — operaciones de API declaradas en YAML

- Tarea: `task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml`.
- Commit del ejecutor: `9a093a25cbdc9092e2dffdd85508b4c8acf16a92` — *extract_routes: ApiOperationDoc declaradas desde una tabla de rutas YAML*.
- Archivos del commit: `src/specir/extract/__init__.py`, `src/specir/extract/plan.py`, `src/specir/extract/routes.py` (nuevo), `src/specir/extract/write.py`, `tests/extract/test_declared_routes.py` (nuevo).
- El grupo CLI `specir ux` no existe todavía (T2 no lo trajo), así que basta la función pública, tal como permite el alcance.

## Comprobaciones del código

| Requisito | Resultado |
|---|---|
| Lee `routes:` con `{method, route, title?}` y escribe un `ApiOperationDoc` por entrada con `origen: declarado` | OK (`read_routes`/`extract_routes`; `title` por defecto `METHOD route`) |
| Valida `method` en `GET/POST/PUT/PATCH/DELETE` mayúsculas y `route` con `/` inicial, con error legible que nombra la entrada | OK (`ValueError` con `routes[N]` y el valor inválido) |
| Escritura idempotente con `write_plan` | OK (segunda ejecución: `created == []`, `unchanged` con las dos operaciones) |
| Exportada en `specir.extract.__all__` | OK |
| `Planned.payload` admite `declarado` solo para `ApiOperationDoc` sin facts; docstring y assert actualizados | OK (`plan.py:53-57`) |
| Choque con una `ApiOperationDoc` derivada del mismo nombre: falla sin escribir nada | OK (`routes.py:66-69`; el test comprueba que el store queda intacto) |
| Entradas borradas de la tabla: se reportan en `stale_declared`, no se borran | OK (campo nuevo en `ExtractionReport`, calculado en `extract_routes`) |
| Enlace de `invokes` del frontend a la operación declarada y hueco esperado para `fetch` sin método | OK (`test_declared_route_links_the_invoke...`) |

Los tests (a)–(f) del encargo están cubiertos por los 8 casos de `tests/extract/test_declared_routes.py` (incluye parametrizados de entrada inválida).

## Tests ejecutados

El `.venv` del repo no arranca en este contenedor (fue creado para Python 3.12 pero su `python` apunta a `/usr/bin/python3` 3.11). Usé el intérprete Python 3.12.16 de `/dev/shm/uvpy` con `PYTHONPATH` absoluto a `IR/src`, los `site-packages` 3.12 del `.venv` y `sldb/src`, un envoltorio `sldb` equivalente al console script, `TMPDIR=/tmp` y `--basetemp=/tmp/pytest-deskops-t-dbcffa346aee-a2`.

| Comando | Resultado |
|---|---|
| `pytest -q -p no:cacheprovider tests/extract/test_declared_routes.py` | **8 passed** (63,75 s) |
| `pytest -q -p no:cacheprovider tests/extract/test_frontend_extraction.py` | **12 passed** (49,21 s) |
| `pytest -q -p no:cacheprovider tests/extract/test_blog_extraction.py` (regresión de `plan.py`/`write.py`) | **16 passed** (120,69 s) |
| `pytest -q -p no:cacheprovider tests/extract/test_edge_name_bounded.py` (regresión de `plan.py`) | **5 passed** (17,62 s) |

Observación no atribuible al commit: `tests/test_imports.py` falla en 2 casos porque `src/specir/cli.py` importa `sldb.mcp` (venía así del commit `564a82e`); el commit del ejecutor no toca ese archivo ni el test. No afecta a la validación pedida.

## Veredicto

**PASA**: `extract_routes` escribe las `ApiOperationDoc` declaradas de forma idempotente, rechaza el choque con una derivada sin escribir, reporta las que salieron de la tabla, el contrato de `Planned.payload` admite `declarado` solo en ese caso, y los tests (a)–(f) más `test_frontend_extraction.py` pasan.
