# Brief del tester deskops-t-05230b7b7270-a2 (IR08, intento 2, tras el ciclo de corrección 1)

Eres el **tester independiente** de la tarea `task-ir08-extractor-estático-django-drf-y-sql` del desk IR, con la identidad `deskops-t-05230b7b7270-a2` (rol tester, intento 2, contract_sha256 `714ea9a93fbd78049b742685bc2c0d2cd16c5d16a6a6b3d42cfb03768b60526b`). Lee primero tu rol en `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`. Devuelves evidencia y nada más: **no implementas, no arreglas, no cierras y no commiteas.** Verifica todo por tu cuenta; no te fíes del informe del ejecutor.

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-05230b7b7270-a2/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`. El `.venv` ya tiene sldb editable desde `../sldb` con pglast 8.8 (extra postgres), instalado desde el host por el coordinador. Si `.venv/bin/python` no arranca dentro de tu contenedor, dilo y usa un venv de trabajo en `/dev/shm` que reuse los site-packages de `.venv`; bórralo al terminar.
- No uses `pkill` ni `pgrep`, y no hagas `git add`, commit ni stash. No edites nada fuera de tu run dir.

## Qué verificas
1. Lee la tarea (`deskops show task task-ir08-extractor-estático-django-drf-y-sql --root .` y su archivo), y las disposiciones aceptadas en `desk/reviews/task-ir08-extractor-estático-django-drf-y-sql/`: **preflight-5 y bundle-3** (son parte del contrato). Corre **cada** ítem de la Validation y anota en `validation.log` la salida y el rc de cada uno.
2. **Sin lectura de código en specIR.** Revisa `src/specir/extract/` entero: nada de tree-sitter, ast, pglast, regex o lectura de los fuentes del fixture (open/read_text sobre .py o .sql); solo `sldb.api` y `sldb.api.anchors`. Corre el grep de la Validation y busca además lecturas de archivo indirectas.
3. **Sin datos fabricados.** Juzga cada regla de la tabla del ejecutor: ¿sale de un fact real de `code_facts` o de nombres escritos a mano para el fixture? Mira en particular:
   - la regla de PolicyDoc por prefijo `can_/is_/has_/may_` (¿cabe en el contrato o es heurística de nombre no acordada?);
   - el fallback `<app>_<modelo>` de persisted_in sin `Meta.db_table`;
   - que la ruta `POST /posts/{id}/publish` salga de `router.register` + `action(detail, methods)` y no de un literal.
   Haz una **prueba de mutación** en una copia en `/dev/shm` del fixture: renombra el modelo, la tabla, el prefijo del router y el método del action, y comprueba que lo extraído cambia en consecuencia.
4. **Procedencia.** Todo nodo y relación: `observado` o `derivado`, `sin_verificar`, `evidencia` vacía, la regla nombrada; anclas con archivo, línea y `source_hash` iguales a los de `code_facts` (compáralos tú).
5. **Idempotencia y cambios.** Repite la doble extracción y el caso de archivo modificado por tu cuenta (en `/dev/shm`), incluido un documento con `verificacion: verificado` que no debe borrarse ni sobrescribirse.
6. **Golden.** Compara con `tests/models/blog.py`: mismos tipos y relaciones de backend y datos. Revisa si `not_derived` (transitions, CRUD heredado) está bien justificado.
7. Fuera de `desk/`, `.sldb/` y `runs/` cambian solo `pyproject.toml` (solo el extra test), `src/specir/extract/` y `tests/extract/`. Ignora `.scion/settings.yaml` (lo crea scion).
8. **Suite completa una vez, bajo el lock:** `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm timeout 9000 flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`. Antes, si `MemAvailable` es menor que 8 GB o `avg60` de `/proc/pressure/memory` es 10 o más, espera. `../sldb` ya incluye el arreglo de la regresión de B2 (a7a05203), así que las 2 pruebas de `tests/visual/test_sync_generation_parity.py` deberían pasar; si fallan, anota la causa exacta. Un fallo de mmdc/Chromium por memoria se reejecuta en serie antes de contarlo. **Cualquier otro fallo cuenta.**

Al final compara con los informes del ejecutor: intento 1 `runs/subagents/deskops-e-0539a70e078c/result-summary.md` y corrección `runs/subagents/deskops-e-0539a70e078c-a2/result-summary.md`.

## Qué dejas
`validation.log`, `suite.log`, los scripts de tus sondas y `result-summary.md` con una tabla por verificación (PASS/FAIL y evidencia) y un veredicto **PASS** o **FAIL** con cada defecto concreto (archivo, línea, qué falla).

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta>`.

## Además, por el ciclo de corrección 1
- El tester anterior (`runs/subagents/deskops-t-05230b7b7270/result-summary.md`) dio FAIL solo por 7 errores de setup de `tests/test_mcp_extension.py`, causados por la deriva del store `.sldb` de IR (ReviewDoc `contract_sha256`). El coordinador la corrigió en `db7a61b` con `sldb models update ReviewDoc`: comprueba `sldb stores check --store .sldb` (PASS) y que esos 7 errores desaparezcan en tu suite.
- OBS-1 corregido: repite la mutación `can_publish` → `ensure_publishable` y comprueba que la función sale en `not_derived` con su motivo, y que ninguna función de terceros aparece ahí.
- OBS-2 corregido: repite el caso m8 (quitar `self.save(...)`) y comprueba que la relación `writes` sigue en el store sin cambios y sale en `changed`. Prueba también que un documento con `verificacion: verificado` siga intacto.
- **El intento 1 informó 13 creados sobre el fixture y la corrección informa 15.** Explica la diferencia con el detalle de cada documento creado: ¿son anclas, nodos o relaciones nuevos, y son correctos según el contrato y el golden?
