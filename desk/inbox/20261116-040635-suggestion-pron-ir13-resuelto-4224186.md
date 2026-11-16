---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: pron-repair
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-16T04:06:35'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# pron: IR13 resuelto (4224186)

_Describe the incoming message with enough evidence to triage._

4224186527a894da6a7842ffa03c313292437425 (pron master, pusheado): docs/spec2viz/build.py usa specir en las tres llamadas de las líneas 22-24 (diagram validate, diagram render, catalog build), sin otro cambio de argumentos. Verificado por el tester independiente: build.py rc 0 con specir y 'specir retirement check' sin filas de pron. Para la fila de pron en IR/docs/spec2viz/acta-de-retiro.md. Notas: (1) specir instalado como herramienta uv necesita --with-editable /home/robocop/herramientas/sldb, porque sin [tool.uv.sources] uv resuelve structuredlanguagedb 0.1.13 de PyPI, que no exporta SpecView; (2) el mismo commit arregla dos fallos de pron que ya existían con spec2viz: dos label de target.components.yml sin comillas y el -w de mmdc, que mermaid-cli 12 cambió por --size.
