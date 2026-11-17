# Brief del ejecutor deskops-e-94a0788c3f5a-a2 (copia del store de deskops en las pruebas MCP; intento 2, ciclo de corrección 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-94a0788c3f5a-a2` (rol executor, intento 2, contract_sha256 `d52071c726040e712846438c4b7888ed40f933ee8aae1283bc9658a09b8b7714`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-94a0788c3f5a-a2/`.
- Usa `TMPDIR=/dev/shm` y el `.venv` de IR.

## La tarea
El contrato es `task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real`. Lee `deskops show task` y su archivo en `desk/tasks/`, con las precisiones (preflight-1) de la (a) a la (d), sus pills y las disposiciones aceptadas en `desk/reviews/task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real/` (preflight-5 y bundle-4, vigentes; preflight-3 y bundle-2 siguen valiendo en lo que no cambió). Esas disposiciones resuelven las dudas así:
- La caché es la constante `CACHE` (`.sldb_cache`). Los archivos sin rastrear no entran.
- `<deskops>` es `WORKSPACE / "deskops"`.
- La lista de `git ls-files` se toma una sola vez, al hacer la copia. Después todo se lee de la copia.
- «Rompe» quiere decir que `sldb stores add` o `check` sobre la copia falla, o que la sesión MCP no resuelve un store enlazado.
- El grep acepta coincidencias solo dentro de `build_deskops_copy`.

Lee primero `tests/conftest.py` y `tests/test_mcp_extension.py` completos. La tarea anterior, cerrada en b16aab7, introdujo `build_spec_store`, `spec_store` y `spec_store_digest`. Sigue ese patrón.

## Reglas
- Fuera de `desk/`, `.sldb/` y `runs/`, solo puedes tocar `tests/conftest.py` y `tests/test_mcp_extension.py`.
- `../deskops`, `../sldb`, `../pron` y `../scion` son de **solo lectura**. **No escribas nunca en el store real de deskops.**
- Sin mocks ni datos fabricados. Las aserciones de la prueba de untouched no se relajan.
- Si la copia rompe la resolución de los enlaces, detente y anótalo como bloqueo.
- No hagas `git add`, `commit`, `stash` ni `git add -A`. No uses `pkill` ni `pgrep`. No edites `desk/` ni `.sldb/` a mano.
- Corre solo pruebas puntuales; no corras la suite completa.

## Validación
Corre los comandos de la Validation, salvo la suite completa, que es del tester. Corre también uno por uno los archivos que usan los fixtures que cambies (`grep -lE 'FEDERATED|federated_digest|mount_copy|store_copy|deskops_copy' -r tests`). Deja la salida y el rc de cada uno en `validation.log`.

## Qué dejas
- `validation.log` y `diff.patch` (`git diff tests/conftest.py tests/test_mcp_extension.py`).
- `git-status.txt` y `diff-stat.txt`.
- `result-summary.md`, con:
  - los cambios y cómo cumplen (a)–(d);
  - los resultados;
  - lo pendiente o bloqueado.

Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.

## Ciclo de corrección 1: qué cambia
El intento 1 (`runs/subagents/deskops-e-473333353dce/`) dejó su diff **sin commitear** en `tests/conftest.py` y `tests/test_mcp_extension.py`. **Consérvalo y corrígelo; no empieces de cero.**

Su tester (`runs/subagents/deskops-t-af2c27434a91/result-summary.md`, léelo, sobre todo D2) dio FAIL por un motivo: la sesión MCP seguía leyendo el deskops real. Los symlinks `<tmp>/sldb` y `<tmp>/scion` apuntan a los repos reales, y sus `store_index` federan `../deskops/.sldb`, que se resolvía hacia el workspace.

La precisión (b) del contrato cambió. Léela entera:
- Los symlinks quedan prohibidos.
- Primero intentas quitar de la copia los enlaces a sldb, pron y scion con `sldb stores remove`, usando `--store` sobre la copia.
- Si sldb lo rechaza, porque un modelo de deskops depende de ese enlace (rc distinto de 0), copias ese store enlazado igual que el de deskops, en `<tmp>/<nombre>`. Sus enlaces de vuelta a `../deskops` resolverán así a la copia.
- Los enlaces de esas copias que apunten fuera de `<tmp>` se quitan. Si sldb rechaza quitarlos, te detienes y lo reportas.

La Validation suma un ítem: **strace -f** sobre `tests/test_mcp_extension.py` debe mostrar que, pasada la ventana de la copia, ningún proceso abre archivos bajo `SLDB_1/deskops/`. La ventana termina cuando `build_deskops_copy` devuelve. Córrelo tú y deja el resumen en `validation.log`.

Considera también agregar una prueba que fije esa garantía, por ejemplo que el store_index de cada store en la copia no resuelva fuera de `<tmp>`. El tester señaló que hoy ninguna prueba la cubre. Debe quedar dentro de los 2 archivos permitidos.
