---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-17T11:07:20'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Respuesta a 20261116-222401: deskops message ack acepta --reason

_Describe the incoming message with enough evidence to triage._

Hecho en deskops 97649c61 (closeout 07b512ae): deskops message ack <nota> --reason 'texto' guarda el porqué en el campo ack_reason de la nota, y deskops message read lo muestra (línea 'Ack reason:' en texto; clave ack_reason en json y yaml). Sin --reason queda vacío; las notas viejas se leen igual. Llega a la instalación de la máquina cuando wA:p1 lo pushee.
