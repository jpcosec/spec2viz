# Brief del ejecutor deskops-e-068628774e48 (federación de las pruebas MCP, G5 opción A; intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-068628774e48` (rol executor, intento 1, contract_sha256 `39d7d97e36dab7cdddf9d623acf2b0f270796e43032f36936d07535324971908`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

## Dónde

- Raíz de trabajo: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de cualquier comando, porque tu pane arrancó en el directorio padre.
- Run dir (tu evidencia): `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-068628774e48/`.
- Usa siempre `TMPDIR=/dev/shm` y el `.venv` de IR.

## La tarea

Lee completa la tarea `task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a`: `deskops show task <id> --root .` y su archivo `desk/tasks/task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a.md`. Ese archivo es el contrato, con su Scope, el Implementation Path y sus «Precisiones (bundle-1)» de la a a la d, la Validation y el Done When. Este brief no lo reemplaza. Lee también los pills ligados y las disposiciones aceptadas en `desk/reviews/task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a/`: preflight-3 y bundle-3.

### Resolución de las ambigüedades de bundle-3 (disposición aceptada)
1. `spec_store` es la ruta del `.sldb` del store temporal, según la precisión (a). Su proyecto es `spec_store.parent`. El enlace se hace con `sldb stores add <spec_store> --name spec2viz --store .sldb`, con cwd en la copia montada. No dupliques `.sldb`.
2. Dónde se combina el digest del store de specs (extender `copy_digest` o crear una función nueva) queda a tu elección. La precisión (d) fija qué se digiere, cuándo y en qué pruebas. Informa lo que elegiste y por qué.

## Reglas

- Fuera de `desk/`, `.sldb/` y `runs/`, solo puedes tocar estos archivos: `tests/conftest.py` y `tests/test_mcp_extension.py`.
- `../spec2viz` y `../sldb` son de **solo lectura**. Usa la API pública de sldb. Nada de mocks ni de datos fabricados.
- Si `SpecSync` no construye el store fuera de un repo git, o si falta una API pública, **detente** y anótalo. No improvises.
- No edites a mano nada bajo `desk/` ni `.sldb/`. No hagas `git add`, `commit`, `stash`, `git add -A` ni `--autostash`. No uses `pkill` ni `pgrep`.
- Corre solo pruebas puntuales, archivo por archivo y sin lock. **No corras la suite completa**: la corre el tester independiente.

## Validación que debes correr (desde IR)

```bash
grep -nE 'WORKSPACE / "spec2viz"|\.\./spec2viz' tests/conftest.py tests/test_mcp_extension.py
TMPDIR=/dev/shm .venv/bin/python -m pytest -q -rs -p no:cacheprovider tests/test_mcp_extension.py
TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py
git diff --stat
deskops graph missing --root .
```

Corre también, uno por uno, los demás archivos de prueba que usan los fixtures que cambiaste. Búscalos con `grep -lE 'mount_copy|store_copy|spec_store|federated_digest|original_digest' -r tests`.

## Qué dejas en el run dir

- `validation.log`: cada comando con su salida y su rc.
- `diff.patch`: `git diff tests/conftest.py tests/test_mcp_extension.py > diff.patch`.
- `git-status.txt` y `diff-stat.txt`.
- `result-summary.md`, con:
  - los archivos tocados;
  - qué hace cada cambio y cómo cumple las precisiones (a)–(d);
  - la elección del digest;
  - los resultados;
  - lo pendiente o bloqueado.

Cuando termines, responde en una línea: `EJECUTOR TERMINADO: <ruta de result-summary.md>` o `EJECUTOR BLOQUEADO: <motivo>`.
