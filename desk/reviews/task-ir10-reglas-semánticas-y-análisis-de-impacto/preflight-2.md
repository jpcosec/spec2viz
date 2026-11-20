---
sldb:
  by: agent
  at: '2026-11-20T22:37:24Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir10-reglas-semánticas-y-análisis-de-impacto-preflight-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir10-reglas-semánticas-y-análisis-de-impacto@sha256:582ad556733a024f6ce468abf52618043f52a34d471289782c8fa9768b458643
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-220249/context-review/task-ir10-reglas-semánticas-y-análisis-de-impacto/preflight/243ae6f1a6966e722e20aeafc964f26d7993697ec9a84822e729f92c168d0097/attempt-1
input_sha256: 243ae6f1a6966e722e20aeafc964f26d7993697ec9a84822e729f92c168d0097
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: d47e50efd509c0acd83626feb9bbfc3cd2560f47f4d819c43d061ade83a3eaea
output_sha256: f7733ec2d8f2cf8338ee860f9bb014d96ed3ebe3363adc81c83b65b1862e541f
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador. Reglas: el lenguaje es RuleDoc de
  sldb (sldb/models/rule_doc.py: title, subject ''model <= X'', where, condition según
  docs/architecture/rules-language.md de sldb, severity error|alert, moment, message),
  con moment on_check. Se evalúan con las operaciones públicas de reglas de sldb.api
  (lo que usa ''sldb rules check''). specIR las distribuye como documentos RuleDoc
  en su paquete, igual que sus modelos. Severidad: error para los eslabones rotos
  de la cadena (acción sin operación de API, operación sin handler, entidad sin persistencia);
  alert para campo de interfaz ausente del serializer y para política sin representación
  en la interfaz. Tool: se registra en register() de src/specir/mcp_extension.py con
  server.add_tool(..., annotations=READ_ONLY), junto a specir_types y specir_nodes,
  en el nivel 0 (solo lectura). Se llama specir_impact. Entrada: el export_id o el
  nombre del nodo de origen. Salida: la lista de afectados, cada uno con export_id,
  tipo, nombre y el camino (las aristas de graph_paths de sldb.api.graph.analyze)
  que lo justifica, con el page() y la explanation que ya usan las otras tools. Mapeo
  de impacto: afectado es todo nodo de un tipo de dominio de specIR (InterfaceControlDoc,
  InterfaceActionDoc, ApiOperationDoc, HandlerDoc, DomainOperationDoc, DomainEntityDoc,
  TableDoc, PolicyDoc, ViewDoc, StateDoc) desde el que hay un camino hacia el nodo
  de origen siguiendo las relaciones de la cadena, es decir los que dependen de él.
  Se nombra por su name y su export_id. Stores de prueba: los tests arman el store
  del blog como tests/models/blog.py (new_blog_project y populate desde tests/fixtures/blog_chain.yaml,
  por las tools MCP de escritura). Para cada regla, un test siembra la brecha borrando
  o cambiando un documento o arista de ese store temporal por las mismas tools, sin
  escribir archivos a mano. Grafo completo: el store de tests/models/blog.py sin cambios
  tiene que dar 0 hallazgos de error de estas reglas. PublishButton: en blog_chain.yaml,
  el campo status de la tabla de posts lo lee o escribe la operación de API de publicar,
  que invoca PublishAction, que dispara PublishButton. El impacto desde posts.status
  devuelve PublishButton con ese camino; si el fixture usa otros nombres, vale el
  camino equivalente del fixture y el test lo dice. Dependencia: el ejecutor parte
  de main después de que entre IR04b, que también toca mcp_extension.py. Commit con
  ''git commit -- <rutas>'' y trailer ''Task-Id: task-ir10-reglas-semánticas-y-análisis-de-impacto''.'
# ISO 8601 timestamp
created_at: '2026-11-20T22:02:58.080155+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T22:37:23.598591+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-ir10-reglas-semánticas-y-análisis-de-impacto

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-220249/context-review/task-ir10-reglas-semánticas-y-análisis-de-impacto/preflight/243ae6f1a6966e722e20aeafc964f26d7993697ec9a84822e729f92c168d0097/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. Reglas: el lenguaje es RuleDoc de sldb (sldb/models/rule_doc.py: title, subject 'model <= X', where, condition según docs/architecture/rules-language.md de sldb, severity error|alert, moment, message), con moment on_check. Se evalúan con las operaciones públicas de reglas de sldb.api (lo que usa 'sldb rules check'). specIR las distribuye como documentos RuleDoc en su paquete, igual que sus modelos. Severidad: error para los eslabones rotos de la cadena (acción sin operación de API, operación sin handler, entidad sin persistencia); alert para campo de interfaz ausente del serializer y para política sin representación en la interfaz. Tool: se registra en register() de src/specir/mcp_extension.py con server.add_tool(..., annotations=READ_ONLY), junto a specir_types y specir_nodes, en el nivel 0 (solo lectura). Se llama specir_impact. Entrada: el export_id o el nombre del nodo de origen. Salida: la lista de afectados, cada uno con export_id, tipo, nombre y el camino (las aristas de graph_paths de sldb.api.graph.analyze) que lo justifica, con el page() y la explanation que ya usan las otras tools. Mapeo de impacto: afectado es todo nodo de un tipo de dominio de specIR (InterfaceControlDoc, InterfaceActionDoc, ApiOperationDoc, HandlerDoc, DomainOperationDoc, DomainEntityDoc, TableDoc, PolicyDoc, ViewDoc, StateDoc) desde el que hay un camino hacia el nodo de origen siguiendo las relaciones de la cadena, es decir los que dependen de él. Se nombra por su name y su export_id. Stores de prueba: los tests arman el store del blog como tests/models/blog.py (new_blog_project y populate desde tests/fixtures/blog_chain.yaml, por las tools MCP de escritura). Para cada regla, un test siembra la brecha borrando o cambiando un documento o arista de ese store temporal por las mismas tools, sin escribir archivos a mano. Grafo completo: el store de tests/models/blog.py sin cambios tiene que dar 0 hallazgos de error de estas reglas. PublishButton: en blog_chain.yaml, el campo status de la tabla de posts lo lee o escribe la operación de API de publicar, que invoca PublishAction, que dispara PublishButton. El impacto desde posts.status devuelve PublishButton con ese camino; si el fixture usa otros nombres, vale el camino equivalente del fixture y el test lo dice. Dependencia: el ejecutor parte de main después de que entre IR04b, que también toca mcp_extension.py. Commit con 'git commit -- <rutas>' y trailer 'Task-Id: task-ir10-reglas-semánticas-y-análisis-de-impacto'.
