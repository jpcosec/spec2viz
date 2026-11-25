PASA

# Resultado del tester — nombres de relación acotados a 255 bytes

- Tarea: `task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash`
- Commit del ejecutor: `6d2d1699df7b603c74873866033b0512ff6da52e` — *edge_name bounded to 200 bytes with sha256 digest*
- Archivos del commit: `src/specir/extract/plan.py` (nuevo `bounded_name`, `MAX_NAME_BYTES = 200`, `edge_name` pasa por él) y `tests/extract/test_edge_name_bounded.py` (nuevo).
- El commit es ancestro de `HEAD`; `src/` y `tests/` no tienen cambios sin commitear. Las pruebas se corrieron tanto en `HEAD` como en un worktree detachado en el commit exacto del ejecutor.

## Pruebas ejecutadas

Entorno: `PYTHONPATH=src`, `TMPDIR=/tmp`, `PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-fc77ced1248e..."`.
Nota: el intérprete indicado en la Validation (`/mnt/ssd/proyectos/SLDB_1/.venv/bin/python`) no es ejecutable en este contenedor porque su symlink apunta a `/home/robocop/...`; se usó el venv válido del repo, `IR/.venv/bin/python` (Python 3.13.18, pytest 9.2.0), con las mismas dependencias.

| Archivo / alcance | Resultado |
|---|---|
| `tests/extract/test_edge_name_bounded.py` (HEAD) | **5 passed** en 21.57 s |
| `tests/extract/test_frontend_extraction.py` (HEAD) | **12 passed** en 56.65 s |
| Ambos archivos juntos (HEAD) | **17 passed** en 90.74 s |
| Ambos archivos juntos en worktree del commit exacto `6d2d169` | **17 passed** en 62.27 s |
| Regresión `tests/extract/test_blog_extraction.py` (usa `plan.py`) | **16 passed** en 100.45 s |

## Cobertura del contrato (a)-(e)

- (a) Nombre corto sin cambios: `test_a_short_name_is_unchanged`.
- (b) Origen con ruta profunda (> 300 bytes) produce nombre <= 200 bytes, termina en `-<12 hex>` y es determinista: `test_a_deep_source_gives_a_bounded_name_ending_in_the_hash`.
- (c) Dos destinos largos que difieren solo al final dan nombres distintos; se comprueba también `len(Path(p.path).name.encode()) <= 255` para el `.md` y `len((name + ".yaml").encode()) <= 255` para el shard `.yaml`: `test_two_long_targets_differing_at_the_end_differ`.
- (d) `extract_frontend` sobre un árbol temporal con un TSX en ruta profunda escribe sin `OSError`; todos los nombres de archivo bajo `.sldb` quedan <= 255 y al menos una arista termina en hash: `test_extract_frontend_writes_a_component_in_a_deep_path`. En el artefacto de prueba, el nombre más largo medido fue 205 bytes para `<name>.yaml` y 203 para `<name>.md`, es decir, `<name>` <= 200.
- (e) El recorte cae en límite UTF-8 válido para `ñ`, `€`, emoji y mezclas; el resultado decodifica como UTF-8 y conserva el sufijo hash: `test_the_cut_is_on_a_utf8_boundary`.

## Comprobación manual adicional

- `bounded_name` sobre entradas de 201, 600, 901 y 1200 bytes devolvió longitudes 200, 199, 200 y 197 bytes respectivamente, siempre decodificando como UTF-8 y terminando en `-<12 hex>`.
- Nombres cortos existentes (p. ej. `entity-a--invokes--entity-b`) permanecen byte a byte iguales.

## Veredicto

**PASA**. El trabajo cumple el Goal y las comprobaciones (a)-(e), y no rompe las pruebas existentes del extractor.
