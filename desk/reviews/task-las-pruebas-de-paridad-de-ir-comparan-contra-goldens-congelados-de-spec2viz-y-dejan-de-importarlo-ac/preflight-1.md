---
sldb:
  by: agent
  at: '2026-11-21T06:20:48Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac@sha256:6a415aa3c8d3e1b0707b180346de58ab4b20cf36ab79e1d4b463634e1be70644
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-061925/context-review/task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac/preflight/5d30c9b39c608c877f13eaddc1ba0bdac002409465164516b8abe0974b6c57f4/attempt-1
input_sha256: 5d30c9b39c608c877f13eaddc1ba0bdac002409465164516b8abe0974b6c57f4
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ae61f26380fa539131e623a0d9fb6aa631c2bf6b2d84078a851f0a00a3764ff1
output_sha256: 641ad76bb60e6a6eaf587b209e1f4d85421fcb0dbb7d702ed450eda404002a55
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador. P1 y B3) El script de grabación va
  en el run dir del ejecutor (runs/subagents/exec-<tu agente>/record_goldens.py, el
  mismo directorio de result-summary.md). Se commitea junto con los goldens, para
  que se pueda volver a grabar. P2) ''Sin spec2viz importable'' se comprueba así:
  el checkout /mnt/ssd/proyectos/SLDB_1/spec2viz está instalado en el venv como editable
  (spec2viz.cli resuelve a .../spec2viz/spec2viz/cli.py). Para la segunda corrida,
  un conftest no sirve. Se corre con un sitecustomize temporal en un directorio fuera
  del repo, que inserte en sys.meta_path un finder que levante ImportError para ''spec2viz''
  y sus submódulos: PYTHONPATH=<ese dir> python -m pytest ... La salida va al run
  dir. Además, grep -rn ''spec2viz'' en los archivos tocados no muestra imports. P3
  y B1) Un caso está cubierto si el golden existente tiene la misma entrada (mismo
  archivo de spec o registro y mismo renderer o comando) y guarda la salida que la
  prueba en vivo compara. Si es así, la prueba en vivo se borra; si hay duda, se graba
  un golden nuevo, no se borra. P4) El worktree es el que dispatch le da al ejecutor
  (su prompt lo dice). El trailer es ''Task-Id: task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac''
  en el cuerpo. P5 y B4) El código de spec2viz no cambió desde 2de1056: git diff --name-only
  2de1056 HEAD -- spec2viz está vacío y HEAD es 91ba1d0. Los goldens nuevos se nombran
  spec2viz-2de1056-<tema>.json, igual que los existentes, y el script anota que se
  grabaron desde HEAD 91ba1d0 con código idéntico a 2de1056. P6) El marcador existe:
  pyproject.toml línea 43 (''parity: compares specIR with spec2viz as the oracle;
  skipped when spec2viz is not installed''). El inventario se hace con pytest -m parity
  -q -rA tests/visual tests/test_matriz_cobertura_spec2viz.py con spec2viz instalado,
  y su salida va al run dir como base (B2: el número de casos que pasan; sin spec2viz
  tiene que dar el mismo número de passed, sin skipped de paridad). B5) Para test_matriz_cobertura_spec2viz.py
  se usa un golden: tests/visual/goldens/spec2viz-2de1056-cli.json con los comandos
  de spec2viz.cli que la prueba lee hoy. B6) ''La matriz'' fuera de alcance es el
  documento docs/spec2viz/matriz-de-cobertura.md. Su test, tests/test_matriz_cobertura_spec2viz.py,
  sí está dentro y se modifica.'
# ISO 8601 timestamp
created_at: '2026-11-21T06:19:35.981880+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T06:20:46.318591+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-061925/context-review/task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac/preflight/5d30c9b39c608c877f13eaddc1ba0bdac002409465164516b8abe0974b6c57f4/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. P1 y B3) El script de grabación va en el run dir del ejecutor (runs/subagents/exec-<tu agente>/record_goldens.py, el mismo directorio de result-summary.md). Se commitea junto con los goldens, para que se pueda volver a grabar. P2) 'Sin spec2viz importable' se comprueba así: el checkout /mnt/ssd/proyectos/SLDB_1/spec2viz está instalado en el venv como editable (spec2viz.cli resuelve a .../spec2viz/spec2viz/cli.py). Para la segunda corrida, un conftest no sirve. Se corre con un sitecustomize temporal en un directorio fuera del repo, que inserte en sys.meta_path un finder que levante ImportError para 'spec2viz' y sus submódulos: PYTHONPATH=<ese dir> python -m pytest ... La salida va al run dir. Además, grep -rn 'spec2viz' en los archivos tocados no muestra imports. P3 y B1) Un caso está cubierto si el golden existente tiene la misma entrada (mismo archivo de spec o registro y mismo renderer o comando) y guarda la salida que la prueba en vivo compara. Si es así, la prueba en vivo se borra; si hay duda, se graba un golden nuevo, no se borra. P4) El worktree es el que dispatch le da al ejecutor (su prompt lo dice). El trailer es 'Task-Id: task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac' en el cuerpo. P5 y B4) El código de spec2viz no cambió desde 2de1056: git diff --name-only 2de1056 HEAD -- spec2viz está vacío y HEAD es 91ba1d0. Los goldens nuevos se nombran spec2viz-2de1056-<tema>.json, igual que los existentes, y el script anota que se grabaron desde HEAD 91ba1d0 con código idéntico a 2de1056. P6) El marcador existe: pyproject.toml línea 43 ('parity: compares specIR with spec2viz as the oracle; skipped when spec2viz is not installed'). El inventario se hace con pytest -m parity -q -rA tests/visual tests/test_matriz_cobertura_spec2viz.py con spec2viz instalado, y su salida va al run dir como base (B2: el número de casos que pasan; sin spec2viz tiene que dar el mismo número de passed, sin skipped de paridad). B5) Para test_matriz_cobertura_spec2viz.py se usa un golden: tests/visual/goldens/spec2viz-2de1056-cli.json con los comandos de spec2viz.cli que la prueba lee hoy. B6) 'La matriz' fuera de alcance es el documento docs/spec2viz/matriz-de-cobertura.md. Su test, tests/test_matriz_cobertura_spec2viz.py, sí está dentro y se modifica.
