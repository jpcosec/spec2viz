# Brief del ejecutor deskops-e-67da42f92e6d (IR08, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-67da42f92e6d` (rol executor, intento 1, contract_sha256 `97b9091cc39fcdd4967919cefd2e8c515c6f0eb4d23f7afd15cad71d2529600b`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-67da42f92e6d/`.
- Usa `TMPDIR=/dev/shm` y el `.venv` de IR.

## La tarea
El contrato es `task-ir08-extractor-estático-django-drf-y-sql`. Lee `deskops show task` y su archivo en `desk/tasks/` completo, con sus atoms y pills ligados y las disposiciones aceptadas en `desk/reviews/task-ir08-extractor-estático-django-drf-y-sql/` (preflight-2 y bundle-2). Las dependencias están cerradas y son lectura obligatoria:
- **IR05**: la taxonomía de procedencia y la divergencia entre código y modelo.
- **IR06**: los tipos de dominio y la cadena del blog poblada a mano en `tests/fixtures/blog_chain.yaml`, `tests/models/blog.py` y `tests/models/test_blog_chain.py`.
- **B2 de sldb**: el SQL de Postgres en `../sldb` 50e4aaab (`src/sldb/code/lang_sql.py`, `sql_readers.py` y sus pruebas en `tests/api/test_anchors.py` y `tests/selfdoc/test_treesitter_symbols.py`) y el reader de Python/Django que ya tenía `sldb.code`. Consúmelos **solo por la API pública** (`sldb.api`); los módulos internos se leen para entender, no se importan.

## Superficie (lo que fija este brief dentro del contrato)
- Módulo: `src/specir/extract/`, que el Implementation Path llama `specir.extract`.
- Pruebas: `tests/extract/`.
- Fixture: el contrato pide «una aplicación Django REST Framework real y pequeña, la del blog de ejemplo, versionada en el repo de specIR». Hoy **no existe** en IR, así que la creas en `tests/fixtures/blog_app/`. Debe ser una app DRF mínima y real (modelos, serializers, vistas y urls) que cubra la mitad de backend y datos de la cadena de publicar un post de `blog_chain.yaml`.
- SQL de Postgres del fixture: el DDL **no se escribe a mano**. Lo genera el `manage.py sqlmigrate` real de Django con el backend de PostgreSQL, en un venv desechable bajo `/dev/shm` (por ejemplo, `uv venv /dev/shm/ir08-django && uv pip install --python /dev/shm/ir08-django django djangorestframework psycopg`). Sus `.sql` se versionan en el fixture con una línea que diga cómo se generaron. sqlmigrate no necesita un servidor Postgres. **No agregues Django a las dependencias de IR**: el extractor es estático, sldb lee el código fuente.
- Si sldb.api no expone un fact que necesitas, **detente** y anótalo. No lo reimplementes: se pide por el desk de sldb.

## Reglas
- Fuera de `desk/`, `.sldb/` y `runs/`, solo puedes tocar `src/specir/extract/`, `tests/extract/` y `tests/fixtures/blog_app/`.
- `../sldb` es de **solo lectura**.
- Sin mocks ni datos fabricados. Sin tree-sitter, ast ni parsers propios en specIR.
- No hagas `git add`, `commit`, `stash` ni `git add -A`. No uses `pkill` ni `pgrep`. No edites `desk/` ni `.sldb/` a mano.
- Corre solo pruebas puntuales; no corras la suite completa. Borra el venv de `/dev/shm` al terminar.

## Validación
Implementa una prueba por cada ítem de la Validation y córrelas. Corre también `tests/models/test_blog_chain.py`, `tests/test_imports.py` y `deskops graph missing --root .`. Deja la salida y el rc de cada uno en `validation.log`.

## Qué dejas
- `validation.log` y `diff.patch` (`git diff` más el contenido de los archivos nuevos, o `git status --short` con su lista).
- `git-status.txt`.
- `result-summary.md`, con:
  - los archivos;
  - cómo cumple cada ítem de la Validation;
  - qué API de sldb usaste;
  - cómo generaste el SQL;
  - lo pendiente o bloqueado.

Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
