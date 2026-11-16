# Resultado del tester deskops-t-8825fdd278af (intento 1)

- Tarea: `task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents`
- Rol: tester (`role-deskops-tester`); contract_sha256 `43f09b39721ee252d24d047ada67c4c5092d7696f6f3d65db2e1c0e7a8024f64`
- Run id: `run-deskops-t-8825fdd278af`; session: `scion://agent/deskops-t-8825fdd278af`; session_sha256: no disponible (sesión scion, sin archivo local)
- Ejecutor verificado: `deskops-e-f98a77856867`
- Evidencia: `validation.log` en este directorio (cada comando, su salida y su rc)

## Veredicto: **FAIL**, por la verificación 2. El cambio de la tarea es correcto; la suite falla por una causa ajena a él

El diff de `tests/conftest.py` cumple el contrato y `tests/test_mcp_extension.py` pasa. Aun así, la suite completa sale con **rc 1**: hay un XPASS(strict) en `tests/visual/test_catalog.py`, causado por un commit de sldb que se hizo después de la corrida del ejecutor. Como Done When pide «la suite completa de IR sale con rc 0», hoy no se cumple.

## Verificaciones

| # | Verificación | Resultado | Evidencia |
|---|---|---|---|
| 1 | `pytest tests/test_mcp_extension.py` | **PASS** | `5 passed in 67.75s`, rc=0, con 4 RunDocs en `runs/subagents/*/run.md` (incluido el de este tester) |
| 2 | Suite completa bajo `flock` con `-n 4` | **FAIL** | `1 failed, 733 passed, 4 xfailed in 226.43s`, rc=1. `free -g`: 18 GB disponibles al empezar. Empezó a las 09:30:56Z y terminó a las 10:16:39Z (esperó el lock) |
| 3 | `deskops graph missing --root .` | **PASS** | "No missing graph references found.", rc=0 |
| 4 | Diff contra el contrato | **PASS** | Ver abajo |
| 5 | Fuera de desk/.sldb/runs esta tarea solo cambia `tests/conftest.py` | **PASS** | Ver abajo |

### 4. El diff contra el contrato
- Copia solo `runs/subagents/*/run.md`: usa `sorted(REPO.glob(RUN_DOCS))` y `shutil.copy2` a `root / run_doc.relative_to(REPO)`, con `mkdir(parents=True, exist_ok=True)` para el padre. No copia nada más de `runs/` (ni `session.jsonl`, ni otros archivos).
- Constante `RUN_DOCS = "runs/subagents/*/run.md"`, declarada junto a `COPIED` con un comentario de una línea que explica el motivo.
- El docstring del módulo menciona los `run.md` en su ruta relativa.
- `original_digest`, `copy_digest` (línea 96, todavía sobre `COPIED` + federados) y `FEDERATED` no cambian: el diff tiene solo 3 hunks (docstring, constante y bucle).
- No hay mocks: `grep mock tests/conftest.py` no encuentra nada, y la copia es de archivos reales.
- `runs/subagents/deskops-e-f98a77856867/diff.patch` es idéntico a `git diff tests/conftest.py` (lo comprobé con `diff`, que dio IDENTICAL).

### 5. Alcance
- `runs/subagents/deskops-e-31500ac1cfa1/diff-stat.txt` y `git-status.txt` (IR13e, de antes de esta tarea) ya listaban `src/specir/visual/notation_style.py`, `docs/spec2viz/acta-de-retiro.md`, `docs/spec2viz/matriz-de-cobertura.md`, `tests/visual/test_notations_parity.py` y `tests/visual/fixtures/spec2viz-notations/`. En ese momento `tests/conftest.py` **no** aparecía.
- En el `git status` actual, el único archivo nuevo fuera de desk/, .sldb/ y runs/ respecto de ese estado es `tests/conftest.py`, además de los `__pycache__/` que generan las pruebas. Esta tarea no tocó los archivos de IR13e; no los evalué.

## El fallo de la verificación 2
- Prueba: `tests/visual/test_catalog.py::test_label_key_of_sldb_splits_underscores_like_norm_key`, marcada `xfail(strict=True)` porque «sldb's label_key keeps '_'».
- Causa: el commit de sldb `06dbcf02` (2026-11-16 06:38:02 -0300, es decir 09:38Z) dice «matching: label_key trata el guion bajo como separador, igual que normKey del catálogo». El fallo esperado ya no ocurre, así que el xfail estricto se vuelve FAILED. IR usa sldb como instalación editable desde `../sldb`.
- No depende de esta tarea: la prueba falla igual corrida sola (`1 failed in 0.60s`, rc=1). `test_catalog.py` no usa `mount_copy`, `store_copy` ni los fixtures federados (el grep no encuentra nada), y no tiene cambios locales (su último commit es `2d28453`).
- Por qué el ejecutor vio verde: su `validation.log` es de las 06:27 -0300 (09:27Z), antes del commit de sldb. Por eso dio `733 passed, 5 xfailed`; ahora son 4 xfailed y 1 failed.

## Discrepancias con el ejecutor
- La suite completa: el ejecutor reporta rc 0 (733 passed, 5 xfailed), y yo obtengo rc 1 hoy. No es un error del ejecutor; cambió el estado de sldb entre las dos corridas.
- El ejecutor contó 3 RunDocs; yo conté 4, porque se sumó el `run.md` de este tester. Con 4 la prueba también pasa.
- Sobre todo lo demás (diff, alcance, graph missing) no hay discrepancias.

## Pruebas obsoletas o que faltan
- Queda obsoleta `test_label_key_of_sldb_splits_underscores_like_norm_key`: su `xfail(strict=True)` codifica un comportamiento de sldb que ya se corrigió. Quitar el marcador no está en el alcance de esta tarea ni me corresponde como tester.
- No falta ninguna prueba para el cambio: `test_mcp_extension.py` ejerce `mount_copy` con RunDocs en el store.

## Qué falta antes del closeout
- Quitar el `xfail` de `tests/visual/test_catalog.py:522` en una tarea aparte (o ampliar el alcance de esta, si el coordinador lo decide) y volver a correr la suite completa hasta que dé rc 0. Hecho eso, el cambio de `tests/conftest.py` se puede cerrar tal como está.
