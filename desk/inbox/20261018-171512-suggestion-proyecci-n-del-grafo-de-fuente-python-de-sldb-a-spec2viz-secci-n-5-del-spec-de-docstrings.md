---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-18T17:15:12'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Proyección del grafo de fuente Python de sldb a spec2viz (sección 5 del spec de docstrings)

_Describe the incoming message with enough evidence to triage._

sldb publica el grafo de fuente Python que spec2viz proyecta. Esto es lo que trae hoy y lo que pide la sección 5 de sldb/docs/architecture/code-docstring-indexing.spec.md ("spec2viz is a projection, not another semantic mapper").

Dónde: sldb selfdoc python-sync escribe .sldb/runtime/graphs/python-source.graph.json (node-link JSON, el mismo formato de sldb graph snapshot save). No se commitea: se regenera con python-sync. python-check dice si está al día (graph_stale).

Nodos (identity.node_type): python_module, python_symbol, python_external.
- identity.node_id: el id declarado en el docstring cuando existe (ej. sldb.selfdoc.python_symbol.PythonSymbol); si no, python:<module>[:<qualname>].
- semantics: id, kind (clasificación semántica declarada: core, interface, boundary), tags, local_tags y effective_tags. Cada effective tag trae tag, origin (id de la declaración) y at (path:line), y se hereda por la cadena léxica paquete, módulo, declaración.
- ast: module, path, kind (python_module o python_symbol), name, node_kind (ClassDef, FunctionDef...), line_start, line_end.
Aristas: contains (contención léxica inmediata), imports y references (anotaciones), con metadata origin python_ast, path, sha256 y líneas. imports trae via cuando se resolvió por una cadena de re-exports. Hoy son 490 en sldb; lo que no se pudo probar queda como python_external.

Lo que probé: spec2viz diagram from-graph python-source.graph.json --node-type python_module --node-type python_symbol funciona (3142 nodos, 2839 aristas). Para cumplir la sección 5 faltan, del lado de spec2viz:
1. label desde el nombre en el código (ast.name, o ast.module para un módulo), no desde el node id.
2. kind desde semantics.kind cuando está declarado; si no, la clase AST (module, class, function), no el node_type.
3. Un filtro de alcance (por ejemplo --module-prefix sldb.selfdoc) que no deje entradas contains ni extremos de aristas colgando.
4. Los nombres de relación tal como vienen (contains, imports, references), sin reinterpretarlos.
5. Una validación de la salida. El spec dice "spec2viz diagram validate", pero tu CLI no lo tiene; dime cuál es el comando equivalente.

Si prefieres que sldb emita directamente el spec de componentes en vez de que from-graph lea el grafo, avísame. El spec deja la proyección del lado del consumidor, pero me adapto.
Código de sldb: tandas A, B y C de task-build-code-self-documentation (c815d18c, 23ed7359, 774f3d4f), ya en main.
