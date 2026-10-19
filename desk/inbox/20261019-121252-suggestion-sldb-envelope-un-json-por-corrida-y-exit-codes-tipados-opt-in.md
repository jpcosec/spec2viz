---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-19T12:12:52'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-19T12:36:11'
---

# sldb --envelope: un JSON por corrida y exit codes tipados, opt-in

_Describe the incoming message with enough evidence to triage._

sldb main (2065f0c5) agrega 'sldb --envelope <comando> ...': un solo valor JSON en stdout, {ok, command, store, revision, data, warnings} o {ok: false, error: {type: 'ns/name', message}, exit}, y exit codes tipados: 0 ok, 1 missing, 2 ambiguous, 3 rejected, 4 busy, 5 store/runtime, 6 usage, 70 unexpected. Contrato en sldb docs/cli-envelope.md.

No cambia nada para ti hoy: sin --envelope la CLI imprime y sale como antes. deskops parsea 'models list', 'stores list' y 'stores check' con --format json (bootstrap.py y workspace.py); con --envelope esa misma salida queda en data.

Propuesta: que migres tus llamadas a la CLI de sldb a --envelope cuando te convenga, y que me avises. Cuando los consumidores estén migrados, el envelope pasa a ser el comportamiento por defecto en una versión que lo diga en el CHANGELOG. Si algún tipo de error o código no te sirve para distinguir lo que necesitas, dímelo antes de esa versión.
