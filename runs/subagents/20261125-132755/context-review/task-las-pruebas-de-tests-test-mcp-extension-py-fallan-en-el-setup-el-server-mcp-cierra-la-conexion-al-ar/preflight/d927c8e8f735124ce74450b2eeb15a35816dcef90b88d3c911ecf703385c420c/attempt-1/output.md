REFORMULACION

Propósito: diagnosticar y corregir el fallo de setup de `tests/test_mcp_extension.py`, donde el server MCP muere antes de `initialize()` sobre la copia del store. Resultado: la causa queda nombrada con el traceback del server y pasan `tests/test_mcp_extension.py` y `tests/test_cli_mcp.py`. Repo: `/mnt/ssd/proyectos/SLDB_1/IR` (suite de IR). Límites: tocar `tests/conftest.py` o el código de specIR que carga el server; no instalar specIR en el venv compartido; si la causa está en sldb, detener y reportar por inbox. Es una tarea ejecutable `task.debug`, no un agregado.

AMBIGUEDADES

1. “Causa confirmada por johanes” frente a “Se identifica por que el server muere”: no queda claro si el ejecutor debe reproducir/confirmar la causa o aplicar directamente el arreglo prescrito. Obliga a inventar si el diagnóstico es vinculante.
2. “package_pythonpath de specir.install”: no se indica import, firma ni ubicación exacta. Obliga a inventar `from specir.install import package_pythonpath` y su contrato.
3. “specIR no esta instalado” y “No module named 'specir'”: discrepancia de nombre. Obliga a inventar el nombre real del paquete/módulo.
4. “PYTHONPATH=src” en Validation frente a “PYTHONPATH absoluto”: no se fija el cwd ni cómo convive `src` relativo con el valor absoluto. Obliga a inventar directorio de ejecución y composición final.
5. “pedirlo por inbox a sldb”: no se define canal ni formato. Obliga a inventar el mecanismo de reporte.

DRY-RUN

Lecturas: TaskDoc, `tests/conftest.py` (`served`, `store_copy`, `build_deskops_copy`), `tests/test_mcp_extension.py`, `tests/test_cli_mcp.py`, `specir.install.package_pythonpath`. Cambios previstos: en `served()`, construir `env` anteponiendo el `package_pythonpath()` absoluto al `PYTHONPATH` existente. Sin ejecutar. Dependencias: `specir.install` importable, venv, `TMPDIR`. Validaciones futuras: ejecutar el comando pytest indicado, exigir 14 passed, capturar traceback del server y nombrar la causa; si el fallo está en sldb, detener y reportar.

FUTURO

Si la causa está en sldb, el equipo de sldb decide y corrige. El integrador/CI de IR valida la suite completa. El revisor acepta el resumen con traceback y evidencia de tests.
