## REFORMULACION
Nodo ejecutable (`task.code`), no agregado. **Propósito:** que la copia aislada que arma `mount_copy` incluya los RunDoc de `runs/subagents/*/run.md`, para que `sldb stores update` no los reporte como faltantes y las pruebas MCP pasen. **Resultado:** `tests/conftest.py` copia esos RunDoc a la misma ruta relativa; `tests/test_mcp_extension.py` da 5 passed y la suite completa rc 0. **Repo:** IR. **Límites:** solo `tests/conftest.py` (`mount_copy`, constante de patrón y docstring del módulo); no tocar `.sldb`, `desk` ni `runs`; no cambiar `original_digest`, `copy_digest`, `FEDERATED` ni otros tests/src.

## AMBIGUEDADES
1. «git diff --stat muestra solo tests/conftest.py fuera de desk/, .sldb/ y runs/» frente a «Fuera: tocar .sldb, desk o runs del repo». Obliga a inventar si la validación debe rechazar cualquier cambio dentro de `desk/`, `.sldb/` o `runs/`, o solo verificar que fuera de ahí no haya cambios distintos de `tests/conftest.py`.
2. «Dentro: tests/conftest.py, solo mount_copy y sus constantes» frente a «actualizar el docstring del módulo». Obliga a decidir si el docstring es una excepción permitida o si “solo” lo excluye; la instrucción siguiente parece ordenarlo, pero el alcance no lo formula como excepción.

## DRY-RUN
**Lecturas:** `tests/conftest.py`; listado de `runs/subagents/*/run.md`; estado/diff para confirmar superficie. **Cambios previstos:** declarar `RUN_DOCS = 'runs/subagents/*/run.md'` junto a `COPIED`; tras el bucle de `COPIED`, recorrer `sorted(REPO.glob(RUN_DOCS))`, crear el directorio padre y `shutil.copy2` a `root / path.relative_to(REPO)`; actualizar el docstring para mencionar los RunDoc. **Dependencias:** `REPO`, `COPIED`, `shutil` y `Path` ya existen; sin dependencias nuevas. **Validaciones futuras:** pytest de `tests/test_mcp_extension.py` (5 passed, rc 0); `git diff --stat`; suite completa bajo `flock` con `SPECIR_MMDC` y `TMPDIR`; `deskops graph missing --root .` rc 0. Sin ejecutar.

## FUTURO
El nodo de ejecución implementará el cambio y devolverá las salidas de pytest, diff y suite completa. El board o un humano decide el cierre y el commit. La disponibilidad de los RunDoc existentes y del comando `deskops` corresponde al entorno, no a este nodo.
