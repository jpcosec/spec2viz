---
sldb:
  by: agent
  at: '2026-11-17T15:57:22Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester@sha256:7294bddb73fbbc7c5aa2a3b6865399efcdec6e6b43454be6adc23d97df10c870
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-155641/context-review/task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester/preflight/d07ee812e149e1111bfe337ec5ff2c3a127f633ffd6ca36381f9eeca03133191/attempt-1
input_sha256: d07ee812e149e1111bfe337ec5ff2c3a127f633ffd6ca36381f9eeca03133191
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 4d51572d18e074ee27ad412990f695e82dfa610d586ccf85c586c5d9371c70e6
output_sha256: ba14367c7f1defbba4219459ab93f2afc2c6f62164946e7e50629073ecb77968
# pending | accepted | rejected | incomplete
verdict: accepted
reason: '1: vía code_facts de sldb.api; no se pide nada a sldb. 2: la misma llamada
  que ya usa src/specir/extract/__init__.py (code_facts(root, paths)[''facts'']);
  tras record_anchor se vuelve a pedir code_facts(root, [fact[''path'']]) y se compara
  el source_hash de cualquier fact de esa ruta (todos los de un archivo lo comparten)
  con el del fact del plan. 3: sobre la copia del fixture blog_app en /dev/shm que
  ya usa tests/extract/extraction.py, se envuelven builtins.open, io.open, Path.read_bytes
  y Path.read_text y se registra toda llamada cuyo marco llamador esté en un módulo
  specir.extract y cuya ruta esté bajo la copia; las lecturas de sldb no cuentan;
  la prueba falla si hay alguna y se demuestra que falla contra el código actual (write.py:52).
  4: el grep sobre src/specir/extract debe salir vacío (rc 1), sin filtrar. 5: si
  code_facts no devuelve source_hash para la ruta, EJECUTOR BLOQUEADO con la salida;
  decide el coordinador.'
# ISO 8601 timestamp
created_at: '2026-11-17T15:57:03.154759+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T15:57:21.077432+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-155641/context-review/task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester/preflight/d07ee812e149e1111bfe337ec5ff2c3a127f633ffd6ca36381f9eeca03133191/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: 1: vía code_facts de sldb.api; no se pide nada a sldb. 2: la misma llamada que ya usa src/specir/extract/__init__.py (code_facts(root, paths)['facts']); tras record_anchor se vuelve a pedir code_facts(root, [fact['path']]) y se compara el source_hash de cualquier fact de esa ruta (todos los de un archivo lo comparten) con el del fact del plan. 3: sobre la copia del fixture blog_app en /dev/shm que ya usa tests/extract/extraction.py, se envuelven builtins.open, io.open, Path.read_bytes y Path.read_text y se registra toda llamada cuyo marco llamador esté en un módulo specir.extract y cuya ruta esté bajo la copia; las lecturas de sldb no cuentan; la prueba falla si hay alguna y se demuestra que falla contra el código actual (write.py:52). 4: el grep sobre src/specir/extract debe salir vacío (rc 1), sin filtrar. 5: si code_facts no devuelve source_hash para la ruta, EJECUTOR BLOQUEADO con la salida; decide el coordinador.
