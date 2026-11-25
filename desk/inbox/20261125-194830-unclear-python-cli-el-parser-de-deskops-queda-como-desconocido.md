---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-25T19:48:30'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# python-cli: el parser de deskops queda como desconocido

_Describe the incoming message with enough evidence to triage._

specir extract python-cli sobre deskops: 102 modelos como DomainEntityDoc y 0 comandos. Desconocido (contado): deskops/cli/parser.py:_add_command_parser construye subparsers en una función y el registro (deskops/cli/registry.py) declara Command(...) dentro de funciones; los hechos no traen argumentos de llamadas de cuerpo. No cabe en ningún tipo nuevo; se espera el hecho (pedido enviado al inbox de sldb). Nota: 'IR' no está en el registro de repos, por eso va a este inbox y no con --to IR.
