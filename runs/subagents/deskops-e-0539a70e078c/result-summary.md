# IR08 — extractor estático Django/DRF y SQL (ejecutor deskops-e-0539a70e078c, intento 1)

## Qué hice
Módulo nuevo `src/specir/extract/` y pruebas en `tests/extract/`; `pyproject.toml` solo cambia el extra `test` (`structuredLanguageDB[mcp,code,postgres]`). Nada commiteado ni cerrado.

- `facts.py` (índices y ayudas sobre facts), `sql.py` (regla `sql-create-table`), `django_drf.py` (reglas Django/DRF), `plan.py` (nodos/relaciones planeados, procedencia, `ref_of`), `write.py` (comprobación de anclas, `write_anchor`, `apply_batch`, informe), `__init__.py` (`extract(root, store=None, paths=None) -> ExtractionReport`).
- `ExtractionReport(created, unchanged, changed, not_derived)` es el valor que devuelve `specir.extract.extract`; no hay otro canal.

## API de sldb usada
`sldb.api.code.code_facts`; `sldb.api.anchors.record_anchor`, `write_anchor`, `check_anchors` (y `check_doc_anchors` en las pruebas); `sldb.api.apply_batch`, `load_runtime_documents`, `is_model_registered`, `add_model` (registra `CodeAnchorDoc` si el store no lo tiene). Nada de tree-sitter, ast, pglast ni regex sobre fuentes (grep de la Validation: sin coincidencias).

## Reglas Django/DRF/SQL → tipos
| Regla | Fact de entrada | Salida | Origen |
|---|---|---|---|
| sql-create-table | `table`, `column` (`attrs.primary_key/identity/type`), `constraint` (`constraint_type`, `columns`, `references`) | TableDoc (columns = nombres; claves en la description) | observado |
| django-model | class con base `models.Model` | DomainEntityDoc (symbol) | observado |
| django-textchoices-state | class `*Choices` anidada en un modelo + sus assignment (`attrs.items`) | StateDoc por miembro (título = etiqueta) | observado |
| django-meta-db-table | assignment `Meta.db_table` (o convención `<app>_<modelo>`) + table | persisted_in entidad→tabla | derivado |
| drf-router-register-action | call `router.register`, assignment del router (`trailing_slash`), `urlpatterns` (`router.urls`, `path(.., include(..))`), decorador `action(detail, methods)` de un método del viewset | ApiOperationDoc (método y ruta) | derivado |
| drf-viewset-method | method con `@action` | HandlerDoc | observado |
| (handled_by) | register + method | handled_by api→handler | derivado |
| django-model-method | method del modelo servido por el viewset (`queryset = X.objects…` o `serializer_class`→`Meta.model`), llamado por `x.m()` desde el handler (`attrs.calls`) | DomainOperationDoc | observado |
| drf-handler-calls-model-method | method del handler + facts del modelo + method destino | executes handler→operación | derivado |
| django-predicate-function / django-method-calls-predicate | `calls` de la operación a una función de módulo con prefijo `can_/is_/has_/may_` | PolicyDoc (statement = docstring) + governed_by | observado / derivado (la regla usa solo la llamada: los facts no dan la condición del raise; lo dice la nota) |
| django-method-calls-save | `calls` con `self.save`/`self.delete` + tabla del modelo | writes operación→tabla | derivado |
| django-method-assigns-choice | assignment dentro del método con valor `…<MIEMBRO>` | transitions | solo con fact; en el fixture no hay |

Procedencia: nodos y relaciones solo `observado` o `derivado`, siempre `sin_verificar`, `verificado_por`/`evidencia` vacíos. La description (nodos) o `notes` (relaciones) es una frase que nombra la regla, los facts (`archivo:línea símbolo`) y el nombre del `CodeAnchorDoc` de cada uno. Las relaciones llevan además `attributes.anchors` con las refs. Cada ancla (`specir/anchors/anchor-<hash>.md`) guarda fingerprints, y en `claim` archivo, líneas y `source_hash` del fact.

Comprobación de anclas: antes de escribir nada, `record_anchor` de cada ref debe dar los mismos fingerprints que el fact y el `source_hash` del archivo debe ser el del fact; si no, `ValueError` con la ref y no se escribe nada (prueba con un archivo cambiado entre facts y escritura). Re-extracción: los documentos con `verificacion` distinta de `sin_verificar` no se tocan (solo se listan como cambiados si su ancla cambió); los demás se actualizan; nunca se borra nada.

## Validation (rc en `validation.log`)
1. Nodos/relaciones del blog = golden (`test_it_extracts_the_nodes_and_relations_of_the_hand_made_chain`, `test_the_route_is_made_from_register_and_action`): rc 0.
2. SQL (PK identity, FK de author_id con constraint) llega al grafo, con pglast: `test_the_tables_columns_and_keys_come_from_the_sql_facts`: rc 0.
3. Archivo, línea, source_hash y procedencia por nodo/relación: `test_every_node_and_edge_names_anchors…` y `test_provenance_is_observed_or_derived…`: rc 0.
4. Idempotencia (árbol de `.sldb` y `specir/` idéntico): `test_a_second_run_leaves_the_store_identical`: rc 0.
5. Copia temporal con archivo modificado: cambiados señalados, verificados intactos: `test_a_changed_file_flags_its_nodes…`, `…updates_what_was_not_verified`: rc 0.
6. Sin inferido/declarado ni verificacion ≠ sin_verificar: rc 0.
7. `sldb edges check` rc 0 y `sldb rules check` sin nivel error (`test_relations_pass_their_relation_types_and_the_rules`): rc 0.
8. grep sin coincidencias (rc 1 del grep) y `tests/test_imports.py` rc 0.
9. `pytest tests/extract tests/models/test_blog_chain.py`: 19 passed, 2 xfailed (los xfail estrictos de IR06), rc 0.
10. `deskops graph missing --root .`: rc 0.

## Informe de la extracción sobre el fixture (`extraction-report.txt`)
13 creados (7 nodos de dominio: TableDoc posts, DomainEntityDoc Post, StateDoc Draft y Published, HandlerDoc PostViewSet.publish, ApiOperationDoc `POST /posts/{id}/publish`, DomainOperationDoc Post.publish, PolicyDoc can_publish; y 5 relaciones: persisted_in, handled_by, executes, governed_by, writes). Segunda ejecución: 0 creados, 0 cambiados, 13 sin cambios.

## No derivado (y por qué)
- `transitions` Post.publish → Published: los facts de assignment son de módulo y de clase; `self.status = self.Status.PUBLISHED` está en el cuerpo del método y sldb no lo publica como fact. Va en `not_derived`; la regla ya está lista para cuando exista el fact. Posible nota a sldb (no la envié: no es mía la decisión).
- Rutas CRUD heredadas de `ModelViewSet`: no hay método handler en los facts; va en `not_derived`.
- `schema_name` de la tabla: null con motivo en `desconocidos`.

## Para el supervisor / pendiente
- **Entorno**: `.venv/bin/python` de IR apunta a `/home/robocop/.local/share/uv/python/...`, que no existe en este contenedor, y no hay `uv`. No pude hacer `uv pip install -e '.[test]'` en `.venv` (no lo toqué). Usé un venv de trabajo en `/dev/shm` (python3.13 del sistema + site-packages de `.venv` + `pglast 8.8` con pip), ya borrado al terminar. Hay que instalar el extra `postgres` en `.venv` desde el host (`uv pip install --python .venv/bin/python -e '.[test]'`); `pyproject.toml` ya lo pide.
- Autoridad del bloque `sldb`: `apply_batch` no deja fijar la autoridad por documento; los nodos quedan `authored` (la de su modelo) y las relaciones `generated`, no `generated`/`theorem` según la tabla de IR05 D1-B. El origen/verificación está en los campos, como exige la tarea. Si se quiere la tabla, falta una vía pública en sldb.
- `check_doc_anchors` devuelve [] porque los nodos no tienen campo `__doc_anchors__` (sus modelos son de IR06); el vínculo nodo→ancla es el nombre en la description y `attributes.anchors` en las relaciones; el estado de código lo da `check_anchors`.
- Sin cobertura (fuera del fixture): `path()`/`+=` en urlpatterns más allá de `include(...)`, `url_path` en `@action`, y serializers/viewsets sin `queryset`; las reglas los contemplan en parte (include, url_path) pero no tienen prueba.
