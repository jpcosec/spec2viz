## REFORMULACION
**Propósito:** que las pruebas de IR localicen el workspace de SLDB_1 mediante `SPECIR_WORKSPACE` cuando corren fuera del árbol del repo, manteniendo `REPO.parent` como fallback. **Resultado:** en `tests/conftest.py`, extraer la resolución a `workspace_root()` y derivar `WORKSPACE`; revisar usos de `WORKSPACE`; añadir `tests/test_workspace_env.py` que pruebe presencia y ausencia de la variable. **Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`. **Límites:** solo `tests/conftest.py` y un test chico; resto de fixtures fuera; no incluir Task-Id en el commit de código. Nodo ejecutable, no agregado.

## AMBIGUEDADES
1. “Revisar que todo uso de WORKSPACE (l.~96 deskops, otros hermanos) pase por esa constante”: no enumera “otros hermanos” ni indica qué hacer si alguno no pasa por `WORKSPACE`; obligaría a inventar el inventario y si se refactoriza.
2. “con monkeypatch de la variable y reimportando o leyendo la funcion que la resuelve”: deja abiertas dos mecánicas y no aclara cómo probar el fallback sin depender del `REPO.parent` real; obligaría a inventar el diseño del test.
3. “los tests que usan el store de deskops encuentran el workspace desde una copia fuera de SLDB_1”: el comando de validación no crea ni usa esa copia; obligaría a inventar cómo simularla o aceptar solo la variable.
4. “Fuera: el resto de fixtures” frente a “otros hermanos”: no queda claro si revisar usos en fixtures hermanas es solo lectura o cambio; obligaría a decidir alcance.

## DRY-RUN
Sin ejecutar: leer `tests/conftest.py` (línea 29 y usos de `WORKSPACE`), `desk/config.json` y `tests/test_mcp_extension.py`. Cambios previstos: `workspace_root()` con `os.environ.get('SPECIR_WORKSPACE')` o `REPO.parent`; `WORKSPACE=workspace_root()`; sustituir usos directos si los hay; crear test que monkeypatchee la variable y, para el fallback, aísle `REPO.parent`. Dependencias: pytest y entorno. Validación futura: `TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=$PWD/src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_workspace_env.py tests/test_mcp_extension.py`.

## FUTURO
El ejecutor implementa y ejecuta la validación; el closeout añade trailers; un humano decide si ampliar el refactor a fixtures no listadas; el integrate confirma la copia limpia.
