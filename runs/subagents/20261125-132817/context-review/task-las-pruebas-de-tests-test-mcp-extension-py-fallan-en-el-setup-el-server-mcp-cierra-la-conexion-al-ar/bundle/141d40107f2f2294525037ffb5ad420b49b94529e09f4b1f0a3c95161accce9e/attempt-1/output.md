REFORMULACION
Nodo ejecutable, no agregado. Propósito: diagnosticar y corregir el fallo de setup de `tests/test_mcp_extension.py`, donde el servidor MCP cierra la conexión al arrancar sobre la copia del store. Resultado: causa identificada y corregida; pasan `tests/test_mcp_extension.py` y `tests/test_cli_mcp.py`. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`, usando el venv `/mnt/ssd/proyectos/SLDB_1/.venv`. Límites: no tocar `sldb`; si la causa está allí, detenerse y reportar con reproducción; no instalar specIR en el venv; mantener el alcance en `tests/conftest.py` o el código specIR que carga el servidor.

AMBIGUEDADES
1. “tests/conftest.py (fixtures de copia y served) o el codigo de specIR que el server carga.” Obliga a inventar si se autoriza modificar specIR si el parche de una línea en conftest no basta; el Implementation Path favorece conftest.
2. “con package_pythonpath de specir.install (absoluto).” No fija el import exacto ni cómo estará disponible `specir` durante pytest, sobre todo al afirmar también “specIR no esta instalado en el venv compartido”; obliga a inventar esa mecánica.
3. “PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest ... tests/...” No fija el directorio de ejecución; obliga a asumir si se corre desde IR o desde `SLDB_1`.

DRY-RUN
Lecturas: TaskDoc y rituales; `tests/conftest.py` (`store_copy`, `build_deskops_copy`, `served`); tests MCP y CLI; helper `package_pythonpath`; arranque `python -m sldb mcp`.
Cambios previstos: en `served()`, construir `env` con `PYTHONPATH` absoluto, combinando `package_pythonpath()` con el valor existente y filtrando vacíos.
Dependencias: helper importable, módulo `os`, copia del store, venv y ejecutable pytest.
Validaciones futuras: ejecutar el comando indicado; comprobar que no aparece `No module named 'specir'` ni “Connection closed”; confirmar que ambos archivos pasan.

FUTURO
Un nodo de ejecución aplicará el parche y correrá la validación. Closeout actualizará el Board, enlazará conocimiento/átomos si corresponde y preparará el commit. Un humano decidirá si se aprueba el cambio de conftest o si debe escalarse a `sldb` por inbox si la hipótesis falla.
