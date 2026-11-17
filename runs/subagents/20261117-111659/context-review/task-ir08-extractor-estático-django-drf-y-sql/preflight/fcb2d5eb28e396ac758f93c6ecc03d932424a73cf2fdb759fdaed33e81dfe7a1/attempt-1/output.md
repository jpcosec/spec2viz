REFORMULACION
Propósito: derivar el grafo de dominio de backend y datos de una app DRF+Postgres desde los facts genéricos de sldb, sin lectores de código en specIR. Resultado: módulo `specir.extract` con reglas Django/DRF/SQL que, usando solo la API pública de sldb (`code_facts`, `write_anchor`, `apply_batch`), crea documentos y relaciones con procedencia e idempotencia, validado sobre `tests/fixtures/blog_app` (commit ad51a0f). Repo: specIR; sldb es dependencia pública. Límites: sin tree-sitter/ast/pglast ni parsers propios, sin otros dialectos, frontend, runtime, impacto ni reglas no deducibles; el fixture solo se toca en copia temporal. Nodo ejecutable (`task.code`).

AMBIGUEDADES
1. "con los mismos tipos y relaciones": el grafo esperado está en `tests/models/test_blog_chain.py`, ausente del input; obliga a inventarlo.
2. "HandlerDoc = PostViewSet.publish" frente a "lo que arma una regla de specIR sobre facts observados ... es origen derivado": no aclara si HandlerDoc es observado o derivado; obliga a inventar la clasificación.
3. "queda en desconocidos": no define tipo, campo ni representación; obliga a inventar el destino.
4. "lo dice en evidencia": no fija formato ni contenido; obliga a inventar su estructura.
5. "source_hash, tomada de code_facts y de las anclas de sldb (write_anchor)": no dice cuál prevalece si difieren; obliga a inventar precedencia.
6. "traducida a la taxonomía de la tarea de procedencia" y "señala como cambiados": la taxonomía y el mecanismo de reporte no están en el input; obligan a inventarlos.
7. "el extra test de IR pasa a pedir structuredLanguageDB[mcp,code,postgres]": no indica archivo ni forma; obliga a inventar el punto de edición.

DRY-RUN
Un ejecutor futuro leería el TaskDoc, `domain.py`, `relation_types.yaml`, el documento de procedencia, la API de sldb y el fixture. Crearía `src/specir/extract` con la tabla de reglas y el mapeo; ajustaría el extra test y añadiría pruebas. Depende de IR05, IR06, espejos B2 y C1–C5, commits de sldb y extra postgres. Validaría: cadena del blog, constraints SQL, procedencia, doble ejecución idéntica, copia temporal, ausencia de inferido/declarado, RelationTypeDoc/RuleDoc, grep prohibido, pytest y `deskops graph missing`.

FUTURO
Fuera del ejecutor: taxonomía y tipos de IR05/IR06, grafo esperado de `test_blog_chain.py`, commits/API de sldb, disponibilidad del extra postgres y validación humana de nodos verificados.
