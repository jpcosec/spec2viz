---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: scion
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T02:11:28'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# IR/.gitignore no ignora *.egg-info/ ni __pycache__/ (el hook de scion instala IR editable)

_Describe the incoming message with enough evidence to triage._

Desde el desk de scion (2026-11-16). La tarea task-hook-deskops-tools-venv-de-test-del-repo-de-la-tarea-pytest-pytest-xdist-y-extras-de-test-dentro-del hace que el hook pre-start de los ejecutores scion instale el repo de la tarea editable (uv pip install -e IR[test]). Eso crea src/specir.egg-info/ y deja __pycache__/ en IR, y IR/.gitignore solo ignora .sldb_cache/, .deskops.log y runs/subagents/*/session.jsonl. Hoy ya están sin trackear en el checkout de IR. Sugerencia: agregar *.egg-info/ y __pycache__/ a IR/.gitignore; sldb y deskops ya los ignoran.
