PASA

# Resultado del tester — `specir ux extract` extrae la interfaz de un árbol y avisa de los saltados

- Tarea: `task-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados`.
- Commit del ejecutor: `1f196cb189df9e80f7ccb4a6de420e3218583d28` — *specir ux extract: extrae la interfaz de un arbol y avisa de los archivos saltados*.
- Archivos del commit: `src/specir/cli.py`, `src/specir/extract/__init__.py`, `src/specir/extract/write.py`, `tests/extract/test_ux_extract_cli.py` (nuevo). No toca `sldb/`.
- Entorno: `/mnt/ssd/proyectos/SLDB_1/IR`, Python 3.13.18 del `.venv` del repo, `PYTHONPATH=src`, `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-4fe82aa7eac2`. Nota: el intérprete de la validación del encargo (`/mnt/ssd/proyectos/SLDB_1/.venv/bin/python`) es un Python 3.11 sin `click`/`pytest` instalados; se usó el `.venv` del repo, que sí tiene las dependencias.
- El árbol de trabajo/HEAD siguió avanzando durante la prueba (U1b, solo `ui/`), pero `git diff 1f196cb..HEAD -- src/specir tests/extract/test_ux_extract_cli.py` está vacío: el código validado es exactamente el del commit del ejecutor.

## Comprobaciones del código

| Requisito | Resultado |
|---|---|
| Grupo click `ux` nuevo en `src/specir/cli.py`, siguiendo el estilo de `catalog`/`retirement` | OK: `ux` agrupa `extract`. |
| Comando `ux extract ROOT [--store PATH] [--path P ...] [--strict]` | OK: `ROOT` es directorio existente; `--path` es repetible; `--store` por defecto `<ROOT>/.sldb`. `--help` responde con todos ellos. |
| Llama a `specir.extract.extract_frontend` | OK. |
| Resumen de nodos creados/actualizados/no derivados | OK: imprime `created`, `updated`, `unchanged`, `not derived` y lista cada `not_derived`. |
| Propaga los saltados de `code_facts` al `ExtractionReport` | OK: `extract_frontend` lee `result["skipped"]` y rellena `report.skipped`; el campo `skipped: list` tiene `default_factory=list` en `ExtractionReport`. |
| Aviso en **stderr** con cuenta y los primeros 10 | OK: `warning: code_facts skipped N file(s) ...`, seguido de las 10 primeras rutas; añade `(+N more)` cuando hay más. |
| Motivo del salto si sldb lo da | OK: `sldb.api.code.code_facts` devuelve `skipped` como `list[str]` de rutas, sin motivo; el aviso imprime la ruta y explica la causa genérica («no installed grammar or unreadable»). No hay motivo adicional que propagar. |
| Sin `--strict`: rc 0 aunque haya saltados (avisar no es fallar) | OK, cubierto por el test (b). |
| Con `--strict`: rc 1 si hubo saltados | OK, cubierto por el test (b). |
| Tests (a) árbol con `.tsx` extrae y rc 0; (b) saltados avisados y `--strict` rc 1 | OK: `tests/extract/test_ux_extract_cli.py` (2 casos, usa `CliRunner` y `monkeypatch` de `code_facts`). |

## Tests ejecutados (de a uno)

| Comando | Resultado |
|---|---|
| `pytest -q -p no:cacheprovider tests/extract/test_ux_extract_cli.py` | **2 passed** (17,82 s), rc 0 |
| `pytest -q -p no:cacheprovider tests/extract/test_frontend_extraction.py` | **12 passed** (54,41 s), rc 0 |
| `pytest -q -p no:cacheprovider tests/extract/test_blog_extraction.py` (regresión de `write.py`/`extract/__init__.py`) | **16 passed** (118,09 s), rc 0 |
| `pytest -q -p no:cacheprovider tests/extract/test_edge_name_bounded.py` (regresión de `write.py`) | **5 passed** (17,22 s), rc 0 |
| `pytest -q -p no:cacheprovider tests/extract/test_declared_routes.py` (regresión de `extract/__init__.py`) | **8 passed** (63,52 s), rc 0 |

No existe `tests/test_cli.py`, `tests/test_write.py` ni `tests/test_extract.py`; las regresiones aplicables se cubrieron con los `tests/extract/*.py` anteriores.

Observación no atribuible al commit: `tests/test_imports.py` falla en 2 casos (`test_package_imports_only_the_public_sldb_api`, `test_only_the_extension_reaches_mcp`) porque `src/specir/cli.py` importa `sldb.mcp` desde el commit `564a82e`, anterior a esta tarea. El commit del ejecutor no toca ni ese archivo ni ese test; el fallo ya estaba en `1f196cb^`.

## Veredicto

**PASA**: `specir ux extract` existe, extrae con `extract_frontend`, resume creados/cambiados/no derivados, propaga e imprime en stderr los archivos saltados por `code_facts` (cuenta, primeros 10 y `+N`), devuelve 0 avisando y 1 con `--strict`, y los tests exigidos (`test_ux_extract_cli.py` y `test_frontend_extraction.py`) pasan junto con las regresiones del extractor.
