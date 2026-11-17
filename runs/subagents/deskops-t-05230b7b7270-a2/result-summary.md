# Resultado del tester deskops-t-05230b7b7270-a2 (IR08, intento 2)

task: task-ir08-extractor-estático-django-drf-y-sql · rol: tester · run_id: deskops-t-05230b7b7270-a2 · contract_sha256 714ea9a9…526b
Entorno: `.venv/bin/python` apunta a /home/robocop/... (no existe en el contenedor); usé `/dev/shm/t05-venv` (python3.13 del sistema + site-packages de `.venv`: sldb editable, pglast 8.8). Evidencia: `validation.log`, `suite.log`, `probe_lib.py`, `probe1..5.py` y sus `.out`.

## VEREDICTO: **FAIL** (un defecto concreto, de guardrail; el comportamiento y la suite están en verde)

### Defecto D1 — specIR lee los bytes de los fuentes
`src/specir/extract/write.py:52`: `hashlib.sha256((root / fact["path"]).read_bytes())` lee los `.py`/`.sql` del fixture para recomputar el `source_hash` y compararlo con el del fact. La pill «specIR solo usa la API pública» y la tarea («specIR no lee código… ni open/read_text sobre fuentes») lo prohíben aunque sea solo para hashear (no interpreta el contenido). `record_anchor` no devuelve `source_hash` (solo `seen`), por eso lo hizo así. Arreglo posible: obtener el hash por `sldb.api` (p. ej. segunda llamada a `code_facts` tras `write_anchor` y comparar `source_hash`), o pedir a sldb que el bloque lo incluya. Ningún otro acceso a archivos fuera de `code_facts`/`record_anchor`/`write_anchor`/`apply_batch` (revisé `open|read_text|read_bytes|glob|subprocess` en `src/specir/extract/`).
Nota: `test_the_extractor_reads_no_code_itself` solo busca los patrones del grep y no lo detecta.

## Tabla de verificaciones
| # | Verificación | Resultado | Evidencia |
|---|---|---|---|
| 1 | Validation: `sldb stores check --store .sldb` | PASS rc=0 (solo alertas `doc_lost` de ReviewDoc ajenos a IR08, preexistentes) | validation.log |
| 1 | grep de lectores de código en `src/specir/extract` | PASS rc=1 (sin coincidencias) | validation.log |
| 1 | `tests/test_imports.py` | PASS 9 passed rc=0 | validation.log |
| 1 | `tests/extract` + `tests/models/test_blog_chain.py` | PASS 22 passed, 2 xfailed (xfails preexistentes de IR04, no del extractor) rc=0 | validation.log |
| 1 | `deskops graph missing --root .` | PASS rc=0 | validation.log |
| 2 | Sin lectura de código | **FAIL** D1 (resto PASS: solo `sldb.api`, `sldb.api.code`, `sldb.api.anchors`; sin ast/tree-sitter/pglast/regex sobre fuentes; `re` solo sobre descripciones propias) | write.py:52 |
| 3 | Sin datos fabricados | PASS con observaciones | ver abajo; mutaciones en probe3/4 |
| 4 | Procedencia/anclas | PASS: 13 docs (8 nodos+5 relaciones), 21 anclas, 0 desajustes de archivo/línea/source_hash/fingerprints frente a `code_facts`; todo observado/derivado, sin_verificar, evidencia vacía, regla nombrada | probe5.out |
| 5 | Idempotencia / cambios | PASS: 2ª extracción digest idéntico (0 creados, 0 cambiados, 13 sin cambios); cambio en `.sql` y `.py` en copia → cambiados los anclados, no anclados `unchanged`; TableDoc `verificado` (human:jp) intacto tras cambio de SQL y de models.py; no verificados se actualizan y luego estable; `sldb edges check` rc=0 | probe1.out, probe4.out |
| 6 | Golden `tests/models/blog.py` | PASS: mismos 8 tipos de nodo (1 de cada, 2 StateDoc) y triples handled_by/executes/governed_by/writes/persisted_in; `not_derived`: `transitions` (la asignación `self.status = …` está en el cuerpo, no es fact de módulo/clase → bien justificado) y CRUD heredado de ModelViewSet (sin método en los facts; bien) | probe1.out |
| 7 | Alcance de archivos | PASS: solo `pyproject.toml` (extra test `[mcp,code,postgres]`), `src/specir/extract/`, `tests/extract/` (+ runs/, `.scion/`) | git status |
| 8 | Suite completa con lock | PASS: `753 passed, 12 skipped, 3 xfailed`, rc=0, 0 errores. Los 7 errores de `test_mcp_extension.py` desaparecieron (store estable, `stores check` PASS); las 2 pruebas de `test_sync_generation_parity.py` pasan | suite.log |

## Mutaciones (3)
- Renombrar tabla (modelo `db_table` y SQL a `entries`) → TableDoc `entries`, `persisted_in/writes entries`. Solo en el modelo → `persisted_in` y `writes` desaparecen y se informa en `not_derived` (no inventa).
- Sin `Meta` → intenta `blog_post` (convención Django `<app>_<modelo>`), no existe → `not_derived`. Observación: el fallback es convención documentada de Django, declarada en la nota de la relación; correcto como regla, no como dato fabricado.
- Renombrar modelo (Post→Article, viewset intacto) → `Article`, `Article.publish`, y las relaciones lo siguen. 
- Router `"posts"`→`"articles"` → `POST /articles/{id}/publish`; `methods=["put"]` → `PUT /posts/{id}/publish`; método `publish`→`release` → `POST /posts/{id}/release`, handler `PostViewSet.release`. La ruta sale de `register`+`action`, no de literales.
- Estados: añadir miembro `ARCHIVED` crea StateDoc y `not_derived` lo lista.
- OBS-1: `can_publish`→`ensure_publishable`: sin PolicyDoc ni governed_by; la función sale en `not_derived` con su motivo (blog/models.py:33); `is_allowed` sí se toma como política. Funciones de terceros (`has_perm`, `timezone.now`) no aparecen.
- OBS-2 (m8): quitar `self.save(...)` → la relación `writes` sigue en el store con payload idéntico y sale en `changed`; el TableDoc `verificado` sigue intacto.

## Observaciones (no bloqueantes)
- O1: la regla de PolicyDoc por prefijo `can_/is_/has_/may_` es una heurística de nombre de specIR, no un fact ni algo acordado literalmente en el contrato (que pide «su resultado decide un raise»; los facts no dan esa condición). Está declarada en `notes` de cada governed_by y las llamadas a funciones del proyecto que no pasan el filtro se informan en `not_derived`. Aceptable si el coordinador la ratifica; si no, debería quedar como `not_derived` siempre.
- O2: «13 vs 15 creados». La extracción sobre el fixture crea **13** documentos (8 nodos + 5 relaciones; `extraction-report.txt` y mi probe1 lo confirman; las 21 CodeAnchorDoc son aparte). El «15» del resumen de la corrección es un error de redacción: en realidad es el número de pruebas de `tests/extract` (15 tras sumar 3). No hay diferencia de comportamiento; los 13 coinciden con el golden.
- O3: el resumen del intento 1 dice «7 nodos de dominio» y enumera 8; es solo un descuido de conteo.
- O4: xfails de `test_blog_chain.py` son de sldb/IR04, ajenos a esta tarea.

## Pendiente antes del cierre
Corregir D1 (quitar la lectura de bytes en `write.py:52` y obtener el hash vía `sldb.api`) y reejecutar `tests/extract` y la Validation 8; o que el coordinador decida aceptar la excepción de lectura de hash por escrito.
