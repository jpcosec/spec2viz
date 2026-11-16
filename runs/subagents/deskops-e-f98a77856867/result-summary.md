# Resultado del ejecutor deskops-e-f98a77856867 (intento 1)

Tarea: `task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents` (contract_sha256 `43f09b39…8024f64`).

## Cambio (solo `tests/conftest.py`)
- Nueva constante `RUN_DOCS = "runs/subagents/*/run.md"` junto a `COPIED`, con comentario de una línea: el store registra RunDocs que viven fuera de `.sldb/` y `desk/`.
- `mount_copy`: después del bucle sobre `COPIED`, recorre `sorted(REPO.glob(RUN_DOCS))` y copia cada `run.md` con `shutil.copy2` a `root / path.relative_to(REPO)`, creando antes el directorio padre. No copia nada más de `runs/`.
- Se actualizó el docstring del módulo para mencionar los `run.md`.
- No cambian `original_digest`, `copy_digest` ni `FEDERATED`. El parche está en `diff.patch`.

## Validación (detalle en `validation.log`)
1. `tests/test_mcp_extension.py`: **5 passed, rc 0**. Había 3 RunDocs en `runs/subagents/*/run.md`: deskops-e-31500ac1cfa1, deskops-e-f98a77856867 y deskops-t-5a39cc2dfbf8.
2. Suite completa bajo `flock /dev/shm/sldb1-tests.lock` con `-n 4`: **733 passed, 5 xfailed, rc 0** (244 s). Al empezar, `free -g` daba 18 GB disponibles.
3. `deskops graph missing --root .`: "No missing graph references found.", **rc 0**.
4. Fuera de desk/, .sldb/ y runs/, `git diff --stat` muestra `tests/conftest.py` y además los archivos de IR13e (`src/specir/visual/notation_style.py`, `docs/spec2viz/*`), que ya estaban modificados antes y no se tocaron. El estado completo está en `git-status.txt`.

No hice commit, add ni stash, y no toqué desk/, .sldb/ ni runs/ fuera de este run dir.
