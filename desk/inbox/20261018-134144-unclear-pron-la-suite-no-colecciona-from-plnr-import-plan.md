---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-18T13:41:44'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T14:09:44'
---

# [pron] la suite no colecciona: from plnr import Plan

_Describe the incoming message with enough evidence to triage._

Para pron (no tiene desk de deskops, se deja aqui como rastro). Suite integrada SLDB_1 (tools/suite-check.sh, 2026-10-18): la suite de pron no colecciona en un venv limpio. Comando: cd pron && /tmp/suite-venv/bin/python -m pytest tests -q. Salida: 26 errors during collection, todos 'ImportError: cannot import name Plan from plnr (unknown location)'. Causa: src/pron/plnr/{plan_execution,plan_planning,theorem_load,pron_world,commit}.py hacen 'from plnr import ...' (paquete top-level) pero plnr vive en src/pron/plnr y no existe distribucion plnr (pip: No matching distribution found; tampoco esta en el entorno anaconda del dueño). Arreglo probable: 'from pron.plnr import ...' o declarar la dependencia. Log: /tmp/suite-check/suite-pron.log
