PASA

# Resultado del tester (task-specir-extract… D1 de IR08)

- task: `task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester`
- commit del ejecutor: `184152898d77efe7062fef47e81624f1b7f2edf1` — *specir.extract: source_hash via sldb.api code_facts, no source reads*
- archivos del commit: `src/specir/extract/write.py`, `tests/extract/test_blog_extraction.py`
- run: `exec-deskops-t-66e1914de785-testing`

## Verificación

| Comprobación | Resultado |
|---|---|
| `git show 1841528 --name-only` | Solo `src/specir/extract/write.py` y `tests/extract/test_blog_extraction.py`, dentro del Scope. |
| `grep -rnE 'read_bytes|read_text|open\(' src/specir/extract --include='*.py'` | rc 1, sin coincidencias. `write.py` ya no importa `hashlib`; usa `sldb.api.code.code_facts`. |
| `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/extract/test_blog_extraction.py` | **16 passed** en 71.43 s (incluye la prueba nueva `test_the_extractor_reads_no_source_file`). |
| `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/models/test_blog_chain.py` | **7 passed, 2 xfailed** en 13.79 s (los xfail son preexistentes de IR04/sldb). |
| `deskops graph missing --root .` | rc 0, «No missing graph references found». |
| Eficacia de la prueba nueva | En un worktree desechable se restauró la línea antigua `hashlib.sha256(...read_bytes())`: la prueba nueva falla con 21 lecturas del fixture (`AssertionError: assert ['/tmp/pytest.../blog/models.py', ...] == []`). Por tanto vigila la regresión D1 de verdad. |

Todo se ejecutó en un worktree limpio en `1841528` (`/tmp/ir-test-1841528`, con `PYTHONPATH` a su `src`), no sobre el árbol de trabajo sucio, para no mezclar cambios ajenos en curso.

## Nota sobre el árbol de trabajo actual

En `/workspace/IR` hay cambios no commiteados ajenos a esta tarea (`src/specir/mcp_extension.py`, `tests/test_mcp_extension.py` y documentación de desk). Con ellos, `tests/models/test_blog_chain.py::test_an_agent_does_not_verify_through_the_mcp` falla porque el test antiguo espera `is_error` y la implementación en curso devuelve un rechazo `domain`. En el commit `1841528` esa prueba pasa; no es un defecto del trabajo del ejecutor.

## Entorno

`IR/.venv/bin/python` apuntaba a `/home/robocop/...`, inexistente en el contenedor. Repunté el symlink local (`.venv` está gitignored) al Python 3.13 de uv disponible en `/home/scion/...`, manteniendo el `site-packages` del venv; con eso `specir`, `sldb` y `pytest` importan correctamente. No se tocó código versionado.

## Veredicto

**PASA.** El extractor obtiene el `source_hash` comparado vía `sldb.api.code.code_facts`, mantiene el `ValueError` con el `ref` y la regla de no escribir si un ancla falla, y ya no abre ni lee fuentes. La prueba de tests/extract cubre la regresión y las validaciones quedan en verde.
