# Brief del tester deskops-t-d471ebbc6f77 (IR13j, intento 1)

Eres el **tester independiente** de la tarea `task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s` del desk IR, con la identidad `deskops-t-d471ebbc6f77` (rol tester, intento 1, contract_sha256 `b577d7891a61c2f4c20a263acd532cce07d426ba22007c9b61d1b7c463ac0e63`). Lee primero tu rol en `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`. Devuelves evidencia y nada más: **no implementas, no arreglas, no cierras y no commiteas.** Verifica todo por tu cuenta.

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-d471ebbc6f77/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.
- No uses `pkill` ni `pgrep`, y no hagas `git add`, commit ni stash.

## Qué verificas
1. Lee la tarea, la nota de inbox que cita y las disposiciones aceptadas (preflight-1 y bundle-1). Corre **cada** comando de su Validation y anota en `validation.log` la salida y el rc de cada uno.
2. Comprueba con sldb, por tu cuenta, el mensaje real ante un `diagram_type` desconocido. Luego revisa el diff de `tests/visual/test_notations_parity.py`:
   - solo cambia el caso changes1;
   - el comparador es el mismo que el de los demás casos;
   - no queda ningún xfail;
   - ninguna otra expectativa se relajó (compara con `git show HEAD:tests/visual/test_notations_parity.py`).
3. Revisa el diff de la matriz y del acta:
   - SV-H01 queda cumplida solo si el xfail era su único faltante;
   - las filas que dependen de SV-H01 tienen el estado y el motivo correctos;
   - el resumen cuadra con tu propio recuento;
   - las filas no acreditadas del comprobador son exactamente las abiertas de la matriz;
   - el bloque nuevo sigue el formato de IR13h;
   - nada de lo escrito es falso.

   El ejecutor también tocó **G2** (la mención del xfail de SV-H01), fuera de la lista literal del Scope. Juzga si cabe en el Goal y si lo que escribió es cierto.
4. Fuera de `desk/`, `.sldb/` y `runs/` cambian solo los 3 archivos.
5. **Suite completa una vez, bajo el lock:** `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm timeout 9000 flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`. Antes, mira `free -g`: con menos de 8 GB disponibles, espera. Hay un **fallo externo conocido**: 2 pruebas de `tests/visual/test_sync_generation_parity.py`, por la regresión de B2 de sldb (`component_spec_from_python` lee un `.js` vendorizado). Ya tiene un espejo en IR. Si son exactamente esas, por esa causa, anótalas como ajenas. **Cualquier otro fallo cuenta.**

Al final compara con el informe del ejecutor, `runs/subagents/deskops-e-ab9406eaab99/result-summary.md`.

## Qué dejas
- `validation.log`.
- `board.txt`, con `deskops show board Board --root .`.
- `task.txt` y `git-status.txt`.
- `result-summary.md`, con PASS o FAIL por verificación, las discrepancias y un veredicto.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.
