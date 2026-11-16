# Resultado del tester deskops-t-8825fdd278af-a2 (intento 2)

- Tarea: `task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents`
- Rol: tester, intento 2. contract_sha256 `43f09b39721ee252d24d047ada67c4c5092d7696f6f3d65db2e1c0e7a8024f64`
- run_id: `deskops-t-8825fdd278af-a2`
- session: `/home/robocop/.claude/projects/-mnt-ssd-proyectos-SLDB-1/6bf27ce7-7b51-4d7e-8c88-6d1a08f50157.jsonl`. El sha256 al escribir este resumen era `b0c4321a65d672248dfe5d0ab17e63032850fd2b8a4f4273b6725784328c038e`; la sesión sigue abierta y el archivo seguirá creciendo.
- Evidencia: `validation.log`, `board.txt`, `task.txt`, `next.txt`, `graph.txt` y `git-status.txt` en este run dir.
- No hice commit, add ni stash, y no modifiqué código ni desk/.

## Veredicto: **PASS**

| # | Verificación | Resultado | Evidencia |
|---|---|---|---|
| 1 | `tests/test_mcp_extension.py` | **PASS**: 5 passed, rc 0, 65,8 s | validation.log §1. Al correr había 7 RunDocs en `.sldb/core/documents/RunDoc/` y 7 `runs/subagents/*/run.md`; la prueba se hizo con más RunDocs registrados que los 2 que exige la tarea. |
| 2 | Suite completa bajo el lock (`-n 4`) | **PASS**: 734 passed, 4 xfailed, rc 0, 253,8 s | validation.log §2b. Con el lock tomado había 18 GB disponibles. |
| 3 | `deskops graph missing --root .` | **PASS**: rc 0, "No missing graph references found." | validation.log §3 y graph.txt |
| 4 | Diff contra el contrato | **PASS** | validation.log §4 |
| 5 | Fuera de desk/.sldb/runs, esta tarea solo cambia `tests/conftest.py` | **PASS** | validation.log §5 |

### Detalle de la verificación 2
El primer intento salió con **rc=124 y no cuenta como corrida**. El `timeout 3000` vence tanto en la espera como en la ejecución, y se agotó mientras `flock` esperaba `/dev/shm/sldb1-tests.lock`. Lo retenía otra suite (pid 181097, más de 55 min con el lock) y había otros 2 procesos en cola. pytest no llegó a arrancar.

El reintento usó `timeout 9000`. Obtuvo el lock a las 10:47:09 y terminó a las 10:51:23 con rc 0. Todo queda registrado en el log.

### Detalle de la verificación 4
- El diff es idéntico a `runs/subagents/deskops-e-f98a77856867/diff.patch`: `diff` da rc 0. El cambio no se tocó desde que lo entregó el ejecutor.
- Copia solo `runs/subagents/*/run.md`: `sorted(REPO.glob(RUN_DOCS))`, y cada archivo va a `root / run_doc.relative_to(REPO)` con `mkdir(parents=True, exist_ok=True)` y `shutil.copy2`. Es la misma ruta relativa, y ni `session.jsonl` ni el resto de `runs/` se copian.
- La constante `RUN_DOCS = "runs/subagents/*/run.md"` está declarada junto a `COPIED`, con un comentario `#:` de una línea que explica el porqué.
- El docstring del módulo menciona ahora `runs/subagents/*/run.md`.
- Ninguna línea +/- toca `original_digest`, `copy_digest` ni `FEDERATED` (el grep da rc 1).
- No hay mocks: el grep de `mock|monkeypatch|MagicMock|patch(` sobre `tests/conftest.py` da rc 1.

### Detalle de la verificación 5
`git status` muestra, fuera de desk/, .sldb/ y runs/ (y sin contar `__pycache__` ni egg-info), estos cambios:
- `tests/conftest.py`, que es el de esta tarea;
- `src/specir/visual/notation_style.py`, `docs/spec2viz/acta-de-retiro.md` y `docs/spec2viz/matriz-de-cobertura.md`, que figuran en `runs/subagents/deskops-e-31500ac1cfa1/diff-stat.txt` de IR13e;
- `tests/visual/test_notations_parity.py` y `tests/visual/fixtures/spec2viz-notations/` (sin rastrear), de IR13e según el brief y la review bundle-1.

`runs/subagents/deskops-e-31500ac1cfa1/diff.patch` no existe, así que la atribución a IR13e se apoya en su diff-stat y en la disposición de bundle-1. El diff de esta tarea (verificación 4) no toca ninguno de esos archivos.

`tests/visual/test_catalog.py` ya no tiene cambios sin commitear.

## Discrepancias con el ejecutor (deskops-e-f98a77856867)
- Suite completa: el ejecutor reportó 733 passed y 5 xfailed; yo obtuve 734 passed y 4 xfailed. La diferencia es el xfail de `test_label_key_of_sldb_splits_underscores_like_norm_key`, que se quitó en `d25a1b6`/`4dc8946` después de su corrida. Es la causa del FAIL del intento 1 y no tiene que ver con esta tarea.
- RunDocs: el ejecutor tenía 3 `run.md` y ahora hay 7. El fixture los copia todos y `test_mcp_extension` sigue pasando.
- No hay discrepancias en el diff ni en el alcance.

## Guardrails probados
- Sin mocks ni datos fabricados: el fixture copia los run.md reales del repo.
- El alcance se limita a `tests/conftest.py`.
- No cambian los digests ni la federación.

## Tests obsoletos o faltantes
No encontré ninguno. No hay una prueba negativa dedicada que demuestre que sin el cambio falla, pero la tarea no la pide; el fallo original está documentado en `runs/subagents/deskops-t-5a39cc2dfbf8/result-summary.md`.

## Pendiente antes del closeout
Nada de esta tarea. El closeout debe commitear solo `tests/conftest.py` (más desk/.sldb/runs) y dejar fuera los archivos de IR13e.
