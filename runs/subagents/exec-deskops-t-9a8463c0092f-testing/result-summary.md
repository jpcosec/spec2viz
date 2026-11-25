PASA

# specIR mcp — resultado del tester

- Tarea: `task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca`
- Commit del ejecutor: `564a82e3df55446accd998e28725410a814e611c` — *specir mcp: serve sldb MCP with specIR extension loaded*
- Archivos del commit: `src/specir/cli.py` (+12), `tests/test_cli_mcp.py` (nuevo, 38 líneas), `skills/use-specir/SKILL.md` (+1). No toca `sldb` ni `src/specir/mcp_extension.py`.
- Entorno: worktree limpio y desechable en `564a82e3` (detached HEAD, retirado al terminar), `TMPDIR=/tmp`, `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-9a8463c0092f-wt`. El `.venv` de `/mnt/ssd/proyectos/SLDB_1` no arranca en este contenedor (fue creado con Python 3.12 pero `/usr/bin/python3` es 3.11 y no lee su `site-packages`); usé Python 3.12.16 de `/dev/shm/deskops-test-venv` con `PYTHONPATH` al `src` del worktree, `sldb/src`, `deskops` y los `site-packages` 3.12 del `.venv`. Evidencia en `validation.log`.

## Pruebas

| Archivo | Resultado |
|---|---|
| `tests/test_cli_mcp.py` (nuevo, commit) | **3 passed**, rc 0 (1,21 s) |
| `tests/visual/test_cli.py` (regresión de `src/specir/cli.py`) | **40 passed**, rc 0 (56,49 s) |
| `tests/test_mcp_extension.py` (regresión pedida) | **11 errors**, todos en el fixture de sesión (`tests/conftest.py:153`, `sldb stores check`), no en el código del ejecutor. Ver salvedad. |

## Comprobaciones de la tarea

| Comprobación | Resultado |
|---|---|
| (a) El server construido con `specir.mcp_extension:register` tiene las cuatro tools `specir_*` | **PASS**. `test_the_server_with_the_extension_has_the_four_specir_tools` construye con `build_server(tmp_path, extensions=[load_extension(...)])` y exige `{specir_types, specir_nodes, specir_rules, specir_impact}`. |
| (b) `specir mcp --help` sale 0 y nombra `--store` | **PASS**. El test pasa; además verifiqué la salida: `--store PATH ... [required]`, `--level INTEGER Mutability level (default: read-only, sldb.mcp.mutability.READ)` y el docstring de una línea con las cuatro tools. |
| (c) Los argumentos llegan a `sldb.mcp.server.serve` | **PASS**. `test_arguments_reaching_serve` parchea `serve` y comprueba `extensions == ("specir.mcp_extension:register",)`, `level == READ` (default) y `actor is None`; con `--level 1 --actor me` llegan `1` y `"me"`. |
| `specir mcp --store <ruta>` montado en el grupo `main` y `--store` requerido | **PASS**. Comando click `mcp` sobre `main`; `--store` con `required=True`; `--level` y `--actor` según el encargo. |
| Línea de la skill | **PASS**. `skills/use-specir/SKILL.md:66` añade exactamente la línea pedida sobre `specir mcp --store <store del proyecto>`. |
| Alcance | **PASS**. Solo los tres archivos del commit; no hay cambios en sldb ni en `mcp_extension.py`. |

## Salvedad sobre `tests/test_mcp_extension.py`

El fixture `mount_copy` falla antes de ejecutar cualquier test con `sldb stores check --store .sldb` rc 1: el store real está en deriva de índice (`data_mutation`/`contract_moved`, 416 errores/21 alertas) y arrastra alertas `anchors/doc_lost` y `anchors/doc_changed` de `ReviewDoc` de otras tareas. No es causado por este commit:

- el commit no toca `.sldb`, `desk` ni la extracción;
- el mismo error de fixture se reproduce en el commit padre `2d7bd09` (sin los cambios del ejecutor); lo verifiqué con un test aislado (`1 error` en `tests/conftest.py:153`);
- el propio ejecutor documentó la misma limitación en `runs/subagents/exec-deskops-e-3d0893847263/validation.log`.

Por eso el veredicto es **PASA** para el trabajo del ejecutor: las tres comprobaciones del Done When y la prueba nueva pasan, y la regresión de CLI visual queda verde. Para que el comando de Validation completo dé rc 0 hace falta sanear el store/fixtures del host (`sldb stores update` / actualizar anclas de reviews ajenas), fuera del alcance de este commit.
