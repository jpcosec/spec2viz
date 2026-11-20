---
sldb:
  by: agent
  at: '2026-11-20T23:49:17Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import@sha256:cf059a5a1a0de83e35dca40d5c601f202c08e8bdc1cd13f4358f53a0bafed15e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-234819/context-review/task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import/bundle/e07db4b4cefaa73c608d524a9f26a03059c122318eec068267068d2e07f7b1d2/attempt-1
input_sha256: e07db4b4cefaa73c608d524a9f26a03059c122318eec068267068d2e07f7b1d2
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 6557b77e6e8a91e838b9404e9dafcf984aa5fd7c13902165b172006bd11aa49b
output_sha256: dacc67ed5e186792a93871bdfbe85c1cf43567fee5fcfaa11949969a5566447c
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador (API pública de sldb verificada).
  1), 2) y bundle 1) y 2) document_content_hash no se exporta en sldb.api. El criterio
  para el store usa la API pública: se enumeran los documentos con sldb.api.select_documents(store,
  {''model'': <cada modelo de specIR que la prueba escribe>} o {} si acepta vacío,
  expect=''many''), que devuelve filas {export_id, model, name, path}, y para cada
  fila se lee su payload con sldb.api.extract_document_payload, de la misma familia
  que save_document_payload. El estado del store es el dict {export_id: payload},
  y antes y después de deshacer tiene que ser igual. 3) ''Mismo criterio de contenido'':
  igualdad de payloads, que excluyen por construcción el bloque sldb de procedencia
  (at, via, hashes). Para cada .md sigue el sha256 del texto sin el bloque sldb, calculado
  sin módulos internos: con la lectura del payload, o quitando el bloque con una función
  local de la prueba que corte el frontmatter ''sldb:'' igual que hoy, sin importar
  sldb.models. 4) y bundle 3) ''Fallo real'' es que, con el criterio de arriba, el
  store después de deshacer no sea igual al de antes. Si pasa, el ejecutor lo arregla
  en src/specir/mcp_extension.py dentro de este mismo commit y lo explica en result-summary.md;
  no hace falta autorización aparte. 5) y bundle 5) El cierre exige los cuatro archivos
  de tests de p4; la Validation nombra el principal. 6) El helper de digest va en
  tests/test_mcp_undo.py, como función privada del archivo. Bundle 4) El pill se cita
  por contexto y no hace falta ligarlo; la regla que aplica es no importar sldb.models
  ni módulos internos en tests/test_mcp_undo.py. El commit lleva ''git commit -- <rutas>''
  y el trailer ''Task-Id: task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import''.'
# ISO 8601 timestamp
created_at: '2026-11-20T23:48:31.015296+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T23:49:15.655629+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-234819/context-review/task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import/bundle/e07db4b4cefaa73c608d524a9f26a03059c122318eec068267068d2e07f7b1d2/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador (API pública de sldb verificada). 1), 2) y bundle 1) y 2) document_content_hash no se exporta en sldb.api. El criterio para el store usa la API pública: se enumeran los documentos con sldb.api.select_documents(store, {'model': <cada modelo de specIR que la prueba escribe>} o {} si acepta vacío, expect='many'), que devuelve filas {export_id, model, name, path}, y para cada fila se lee su payload con sldb.api.extract_document_payload, de la misma familia que save_document_payload. El estado del store es el dict {export_id: payload}, y antes y después de deshacer tiene que ser igual. 3) 'Mismo criterio de contenido': igualdad de payloads, que excluyen por construcción el bloque sldb de procedencia (at, via, hashes). Para cada .md sigue el sha256 del texto sin el bloque sldb, calculado sin módulos internos: con la lectura del payload, o quitando el bloque con una función local de la prueba que corte el frontmatter 'sldb:' igual que hoy, sin importar sldb.models. 4) y bundle 3) 'Fallo real' es que, con el criterio de arriba, el store después de deshacer no sea igual al de antes. Si pasa, el ejecutor lo arregla en src/specir/mcp_extension.py dentro de este mismo commit y lo explica en result-summary.md; no hace falta autorización aparte. 5) y bundle 5) El cierre exige los cuatro archivos de tests de p4; la Validation nombra el principal. 6) El helper de digest va en tests/test_mcp_undo.py, como función privada del archivo. Bundle 4) El pill se cita por contexto y no hace falta ligarlo; la regla que aplica es no importar sldb.models ni módulos internos en tests/test_mcp_undo.py. El commit lleva 'git commit -- <rutas>' y el trailer 'Task-Id: task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import'.
