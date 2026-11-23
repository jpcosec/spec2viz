---
sldb:
  by: agent
  at: '2026-11-23T18:05:06Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo@sha256:f6177418059992b712dd4bf43df942f1f0fbaf3076f2239466d902c9ec445457
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261123-180404/context-review/task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo/preflight/6f6829406d692ffc63f74b72fd094f5bea7b61ea3b5217205e3b86ae8d69cff4/attempt-1
input_sha256: 6f6829406d692ffc63f74b72fd094f5bea7b61ea3b5217205e3b86ae8d69cff4
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 214a8043966ebc259cf1a95b57243355a78d755570c4344cb143f1ca81ff2906
output_sha256: d1284cd0664b928e180f4e30667065b5d6496997a862a7769b42e75134cda47f
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Resoluciones: (1) el targetNamespace es el actual de spec2viz con spec2viz
  reemplazado por specir; (2) la clave nueva es specir.catalog.annotations.v1; (3)
  migracion una sola vez al cargar: si no hay clave nueva y si vieja con JSON valido,
  se escribe la nueva y se borra la vieja; si ambas existen gana la nueva y la vieja
  se borra; si el JSON viejo es invalido no se toca y se registra en consola; (4)
  el comando de goldens se busca en el Makefile, pyproject o README de IR; (5) marcar
  el punto 8 del acta como hecho si esta en alcance; declarar el retiro no; (6) exporter
  es el atributo del elemento raiz definitions del BPMN; (7) esta tarea se despacha
  solo despues de cerrar la del punto 1; (8) el test va donde esten los tests actuales
  del catalogo (pytest sobre la pagina generada si no hay tests de JS).'
# ISO 8601 timestamp
created_at: '2026-11-23T18:04:19.984156+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T18:05:04.458570+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-180404/context-review/task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo/preflight/6f6829406d692ffc63f74b72fd094f5bea7b61ea3b5217205e3b86ae8d69cff4/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Resoluciones: (1) el targetNamespace es el actual de spec2viz con spec2viz reemplazado por specir; (2) la clave nueva es specir.catalog.annotations.v1; (3) migracion una sola vez al cargar: si no hay clave nueva y si vieja con JSON valido, se escribe la nueva y se borra la vieja; si ambas existen gana la nueva y la vieja se borra; si el JSON viejo es invalido no se toca y se registra en consola; (4) el comando de goldens se busca en el Makefile, pyproject o README de IR; (5) marcar el punto 8 del acta como hecho si esta en alcance; declarar el retiro no; (6) exporter es el atributo del elemento raiz definitions del BPMN; (7) esta tarea se despacha solo despues de cerrar la del punto 1; (8) el test va donde esten los tests actuales del catalogo (pytest sobre la pagina generada si no hay tests de JS).
