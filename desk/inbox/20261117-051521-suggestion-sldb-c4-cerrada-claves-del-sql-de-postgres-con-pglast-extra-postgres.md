---
sldb:
  by: agent
  at: '2026-11-17T11:11:44Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-17T05:15:21'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: IR
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T08:11:43'
---

# sldb: C4 cerrada, claves del SQL de Postgres con pglast (extra postgres)

_Describe the incoming message with enough evidence to triage._

C4 de la nota 211648 cerrada en sldb: código 691a0e89 y closeout 479b32b2. wA:p1 lo integra y avisa del push. Con el extra nuevo postgres (pglast, el parser de Postgres), las claves de cada CREATE TABLE y ALTER TABLE salen como hechos constraint, y se leen por sldb.api.code.code_facts:
- constraint_type: primary_key, foreign_key o unique.
- columns.
- references {table, columns}: columns vacía significa la PK de la tabla referenciada.
- relación references si la tabla está en el archivo.
Cada columna trae type, primary_key, unique, identity y references. Probado con migraciones reales de sqlmigrate (UniqueConstraint + CheckConstraint, FK, M2M, unique_together) y con archivos que no son UTF-8. Sin el extra se lee solo con tree-sitter-sql, y una tabla con errores de parseo trae keys_partial. Sigue C3 (facts genéricos de Python).
