# Resumen del ejecutor deskops-e-0539a70e078c-a2 (IR08, corrección 1/2)

Entorno: `.venv/bin/python` de IR no existe en este contenedor (solo `activate`). Usé un venv en `/dev/shm/a2-venv` (python3.13 del sistema) que reutiliza los site-packages de `IR/.venv` (pglast 8.8, sldb editable); borrado al terminar. Se tocó solo `src/specir/extract/` y `tests/extract/`.

## OBS-1 (`django_drf.py`)
- Se mantiene `PREDICATE_PREFIXES`. La nota de `governed_by` ahora dice que es una convención de specIR (prefijo `can_/is_/has_/may_`), no un fact del código.
- Nuevo `_unfiltered`: toda llamada simple a una función de módulo del árbol (del módulo del método o de uno que importa, vía facts) que no pasa el filtro va a `not_derived`: «<op> governed_by: llamada a función del proyecto sin señal de política: <nombre> (archivo:línea, …)». Sin duplicados. Las funciones de terceros no se listan.
- Pruebas: `test_a_function_of_the_project_without_a_policy_signal_is_reported_not_dropped` (copia con `can_publish` → `ensure_publishable`: 0 PolicyDoc, 0 governed_by, función en `not_derived`) y `test_the_predicate_convention_is_named_in_what_it_creates`.

## OBS-2 (`write.py`, `write_plan`)
- Tras el bucle del plan, todo documento/relación del store que no está en el plan, con `origen` observado/derivado y con anclas `[anchor-…]` en su descripción/notas, se lista en `changed` si alguna de sus anclas no está `intact` (estado de `check_anchors` tomado antes de reescribir anclas). No se borra ni modifica.
- Prueba: `test_a_relation_the_new_plan_no_longer_produces_is_flagged_and_kept` (caso m8: se quita `self.save(...)` de `Post.publish`; `RelationDoc:edge-op-post-publish--writes--table-posts` sigue en el store con payload idéntico y sale en `changed`).
- Límite: el criterio es «ancla no intact», lo que cubre el cambio de `source_hash` del archivo y también fact desaparecido; un documento sin marcas de ancla no se considera del extractor.

## Validación (`validation.log`)
- grep de lectores de código en `src/specir/extract`: rc=1 (sin coincidencias, lo esperado).
- `tests/test_imports.py`: 9 passed, rc=0.
- `tests/extract tests/models/test_blog_chain.py`: 22 passed, 2 xfailed, rc=0 (15 pruebas del extractor, 3 nuevas).
- `deskops graph missing --root .`: rc=0.
- Las 3 nuevas por separado: 3 passed.

## Extracción sobre el fixture (`extraction-report.txt`)
created 15, unchanged 0, changed 0; `not_derived`: rutas CRUD heredadas de ModelViewSet y `transitions` de Post.publish (sin fact de asignación). Sin `ensure_publishable` en el fixture original, así que no aparece nada nuevo.

Para el supervisor: `diff.patch` incluye los archivos nuevos y el `pyproject.toml` del intento 1. Nada commiteado ni añadido al índice.
