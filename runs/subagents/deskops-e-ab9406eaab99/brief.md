# Brief del ejecutor deskops-e-ab9406eaab99 (IR13j, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-ab9406eaab99` (rol executor, intento 1, contract_sha256 `b577d7891a61c2f4c20a263acd532cce07d426ba22007c9b61d1b7c463ac0e63`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-ab9406eaab99/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.

## La tarea
El contrato es `task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s`. Lee `deskops show task`, su archivo en `desk/tasks/`, la nota de inbox que cita y las disposiciones aceptadas en `desk/reviews/task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s/`: preflight-1 y bundle-1. Esas disposiciones fijan:
- **Faltantes:** lo que falta lo dice la columna Falta de la sección Acreditación (IR13). Las filas que dependen de SV-H01 son las que la nombran en esa columna.
- **El caso:** es `changes1` de `test_invalid_notations_are_rejected`, en `tests/visual/test_notations_parity.py:230`, con el mismo comparador que los demás casos.
- **Redacción y cifras:** la redacción sigue el estilo de las corridas de IR13g e IR13h. Las cifras salen de la corrida y de recontar la tabla.

## Reglas
- Solo puedes tocar `tests/visual/test_notations_parity.py`, `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`.
- Antes de fijar el texto, comprueba el mensaje real con sldb, y no cambies ninguna otra expectativa de la prueba. Si SV-H01 tiene otro faltante además del xfail, sigue abierta con ese motivo.
- Si algo falla, detente y repórtalo.
- No hagas `git add`, `commit`, `stash` ni `git add -A`. No uses `pkill` ni `pgrep`. No edites `desk/` ni `.sldb/` a mano.
- Corre solo pruebas puntuales; no corras la suite completa.

## Validación
Corre cada comando de la Validation y del Implementation Path. Deja la salida y el rc de cada uno en `validation.log`.

## Qué dejas
- `validation.log` y `diff.patch` (`git diff` de los 3 archivos).
- `git-status.txt`.
- `result-summary.md`, con:
  - el mensaje real de sldb;
  - el cambio en la prueba;
  - el estado nuevo de SV-H01 y de las filas que dependen de ella, cada una con su motivo;
  - el resumen;
  - la corrida del comprobador;
  - lo pendiente.

Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
