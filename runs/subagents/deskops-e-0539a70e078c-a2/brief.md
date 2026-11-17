# Brief del ejecutor deskops-e-0539a70e078c-a2 (IR08, ciclo de corrección 1/2)

Eres el **ejecutor** de la tarea `task-ir08-extractor-estático-django-drf-y-sql` del desk IR, intento 2 (`deskops-e-0539a70e078c-a2`, contract_sha256 `714ea9a93fbd78049b742685bc2c0d2cd16c5d16a6a6b3d42cfb03768b60526b`). Corriges solo los dos defectos de abajo y te detienes. **No cierras, no commiteas, no avanzas el desk, no lanzas agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR` (`cd` ahí). Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-0539a70e078c-a2/`.
- `TMPDIR=/dev/shm`. Si `.venv/bin/python` no arranca en tu contenedor, usa un venv de trabajo en `/dev/shm` que reuse los site-packages de `.venv` (pglast 8.8 ya está instalado ahí; sldb editable desde `../sldb`) y bórralo al terminar.
- El código del intento 1 está en el árbol sin commitear (`src/specir/extract/`, `tests/extract/`, `pyproject.toml`). Lee el contrato (`deskops show task …`, su archivo, preflight-5 y bundle-3 en `desk/reviews/…`), el informe del intento 1 (`runs/subagents/deskops-e-0539a70e078c/result-summary.md`) y el del tester (`runs/subagents/deskops-t-05230b7b7270/result-summary.md`, con sus sondas en `probes/`).

## Defectos a corregir (decisión del coordinador)
1. **OBS-1, omisión silenciosa de políticas** (`src/specir/extract/django_drf.py`, `PREDICATE_PREFIXES`). Se mantiene la convención de prefijos de predicado (`can_`, `is_`, `has_`, `may_`) para crear PolicyDoc y governed_by, pero:
   - la regla la nombra en la descripción de lo que crea (es una convención de specIR, no un fact);
   - toda función **del código analizado** (un fact function de módulo del árbol, no importada de terceros) que la operación llama y que no pasa el filtro va a `not_derived` con su motivo (por ejemplo «llamada a función del proyecto sin señal de política: ensure_publishable»). Nunca se omite en silencio.
   - Prueba nueva con una copia en `/dev/shm` del fixture donde `can_publish` se llama `ensure_publishable`: 0 PolicyDoc, 0 governed_by y la función listada en `not_derived`.
2. **OBS-2, relación obsoleta sin señalar** (`src/specir/extract/write.py`, `write_plan`). Al re-extraer, todo documento o relación ya existente en el store, escrito por el extractor y anclado a un archivo cuyo `source_hash` cambió, que el plan nuevo ya no produce, se lista en `changed`, sin borrarse ni modificarse. Prueba nueva con el caso m8 del tester: en una copia, quitar `self.save(...)` de `Post.publish`; la relación `writes` sigue en el store y sale en `changed`.

## Reglas
- Toca solo `src/specir/extract/` y `tests/extract/`. Nada de tree-sitter, ast, pglast, regex sobre fuentes. No modifiques `tests/fixtures/blog_app`.
- No hagas `git add`, commit ni stash; no uses `pkill` ni `pgrep`; no edites `desk/` ni `.sldb/`.
- Solo pruebas puntuales: `tests/extract`, `tests/models/test_blog_chain.py`, `tests/test_imports.py`. Antes de pytest, si `MemAvailable` es menor que 8 GB o `avg60` de `/proc/pressure/memory` es 10 o más, espera.
- Si algo del contrato no se puede cumplir sin un fact que sldb no da, detente y repórtalo.

## Qué dejas
`validation.log` (cada ítem de la Validation con su rc, más las dos pruebas nuevas), `diff.patch` (diff completo frente a HEAD, archivos nuevos incluidos), `git-status.txt` y `result-summary.md` (qué cambió por cada defecto, salida de las pruebas, informe de la extracción sobre el fixture).

Al terminar responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
