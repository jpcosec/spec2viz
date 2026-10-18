---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-17T23:32:37'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Auditoría de empaquetado 2026-10-17: notations sin commitear, versión 0.1.0 vs CHANGELOG 0.2.0, sin tags

_Describe the incoming message with enough evidence to triage._

Auditoría read-only de empaquetado (2026-10-17). Hallazgos en spec2viz:
1. pyproject.toml:44 (package-data notations/*.yml), spec2viz/notation.py y spec2viz/notations/*.yml están sin commitear; una rueda construida desde HEAD 9cc97f7 sale sin notaciones aunque notation.py:264 las carga.
2. pyproject.toml:7 = 0.1.0 pero CHANGELOG.md:22 ya registra 0.2.0 y :3 tiene 'Unreleased'. 0 tags en el repo. Sin __version__.
3. La METADATA instalada (spec2viz-0.1.0.dist-info, editable en base) no incluye structuredLanguageDB aunque pyproject.toml:16 lo declara (>=0.1.6): la instalación es anterior al cambio. CHANGELOG.md:12 dice >=0.1.6 y :16 dice >=0.1.3.
4. spec2viz/sldb_models.py:17 importa sldb.models.structured_doc a nivel de módulo, fuera de la superficie sldb.api (archivo modificado sin commitear).
5. mmdc (spec2viz/linters/mermaid.py) es binario externo no documentado en metadata. renderers/antonia.py:14 carga Mermaid desde CDN.
6. spec2viz.egg-info (2026-10-13) anterior a notation*. Sin dist/build. Sin .github/workflows (solo Dependency Graph automático).
