# Brief del ejecutor deskops-e-0539a70e078c (IR08, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-0539a70e078c` (rol executor, intento 1, contract_sha256 `714ea9a93fbd78049b742685bc2c0d2cd16c5d16a6a6b3d42cfb03768b60526b`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-0539a70e078c/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`. sldb está instalado editable desde `../sldb` (ya contiene C1–C5 de Python: `3dc9a526`, `691a0e89`, `ad6f8842`).

## La tarea
El contrato es `task-ir08-extractor-estático-django-drf-y-sql`. Lee `deskops show task task-ir08-extractor-estático-django-drf-y-sql --root .`, su archivo en `desk/tasks/` (sobre todo Implementation Path, con las adjudicaciones (1)–(4)) y las disposiciones aceptadas en `desk/reviews/task-ir08-extractor-estático-django-drf-y-sql/`: **preflight-5 y bundle-3**. Las disposiciones son parte del contrato. En resumen:
- sldb da facts **genéricos** (`sldb.api.code.code_facts`: extends/attrs.bases, attrs.decorators, calls/attrs.calls, kind assignment con attrs.call/items/value/op, kind call, y hechos constraint del SQL). **specIR interpreta Django y DRF** sobre esos facts en `src/specir/extract/`. Nada de tree-sitter, ast, pglast directo ni regex sobre fuentes.
- Anclas con `sldb.api.anchors.write_anchor`; cambiados con `check_doc_anchors`; escritura con `apply_batch`. Todas las anclas se comprueban antes de `apply_batch`; si una no coincide, `ValueError` con el ref y no se escribe nada.
- Procedencia (IR05, `docs/decisiones/procedencia-y-divergencia.md`, `src/specir/models/domain.py`): leído tal cual = `observado`; armado por regla = `derivado`; nunca `inferido` ni `declarado`; siempre `verificacion: sin_verificar`; `evidencia` vacía; la regla se nombra en la descripción.
- Golden: los nodos y relaciones de backend y datos de `tests/models/blog.py` (ApiOperationDoc, HandlerDoc, DomainOperationDoc, PolicyDoc, StateDoc, DomainEntityDoc, TableDoc; handled_by, executes, governed_by, writes, persisted_in; transitions solo si hay fact, si no va como «no derivada» en el informe). InterfaceControlDoc e InterfaceActionDoc son de IR09: fuera.
- El informe de la extracción es el valor que devuelve la función pública de `specir.extract` (creados, sin cambios, cambiados, no derivados).
- RuleDoc: `sldb rules check --store .sldb --format json`, como `rules_findings` de `tests/models/test_blog_chain.py`; ningún hallazgo de nivel error.
- Pruebas nuevas en `tests/extract/`.
- Fixture: `tests/fixtures/blog_app` (commit `ad51a0f`). No lo modifiques; la Validation 5 trabaja sobre una copia temporal en `/dev/shm`.
- Extra `postgres`: el extra `test` de `pyproject.toml` pasa a `structuredLanguageDB[mcp,code,postgres]`, y lo instalas en `.venv` (`uv pip install --python .venv/bin/python -e '.[test]'` o equivalente). Deja el comando y su salida en `validation.log`.

## Reglas
- Puedes tocar `src/specir/extract/` (nuevo), `tests/extract/` (nuevo) y `pyproject.toml` (solo el extra test). Nada más fuera de tu run dir.
- **Si falta un fact genérico en sldb, detente y repórtalo** (no lo reimplementes en specIR, no lo simules con nombres escritos a mano). Di qué fact, sobre qué archivo y línea del fixture, y qué devuelve hoy `code_facts`.
- No hagas `git add`, `commit`, `stash` ni `git add -A`. No uses `pkill` ni `pgrep`. No edites `desk/` ni `.sldb/` del repo a mano.
- Corre solo pruebas puntuales (las nuevas, `tests/models/test_blog_chain.py`, `tests/test_imports.py`); no corras la suite completa.
- Antes de lanzar pytest, si `MemAvailable` es menor que 8 GB o `avg60` de `/proc/pressure/memory` es 10 o más, espera.

## Validación
Corre cada ítem de la Validation de la tarea. Deja la salida y el rc de cada uno en `validation.log`.

## Qué dejas
- `validation.log`, `diff.patch` (`git diff` más el contenido de los archivos nuevos) y `git-status.txt`.
- `result-summary.md`, con: la API de sldb usada; la tabla de reglas Django/DRF → tipos (fact de entrada, nodo o relación de salida, origen); el resultado de cada ítem de la Validation con su rc; el informe de la extracción sobre el fixture; lo que no se pudo derivar y por qué; lo pendiente.

Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
