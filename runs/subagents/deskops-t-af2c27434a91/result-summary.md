# Resultado del tester deskops-t-af2c27434a91

- Tarea: `task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real` (contract_sha256 `081661cf8fd8d00b4acb5c9efa6bc71363ea8be581f28c26d99686c3076dc362`), intento 1.
- Rol: tester. run_id `run-deskops-t-af2c27434a91`. session `scion://agent/deskops-t-af2c27434a91`, session_sha256: no disponible desde el tester (sesión scion/claude, el run.md lo deja vacío).
- Entrega revisada: diff sin commitear del ejecutor `deskops-e-473333353dce` en `tests/conftest.py` y `tests/test_mcp_extension.py` sobre HEAD `bf0e503`.
- Evidencia: `validation.log`, `board.txt`, `task.txt`, `next.txt`, `graph.txt`, `git-status.txt` en este directorio.

## Veredicto por verificación

| # | Verificación | Resultado |
|---|---|---|
| V1 | grep de rutas reales: una sola coincidencia, `tests/conftest.py:60 source = WORKSPACE / "deskops"`, dentro de `build_deskops_copy` | PASS |
| V2 | `pytest -q -rs tests/test_mcp_extension.py` rc 0, sin skipped | PASS (corrida 2: 6 passed, rc 0; corrida 3 bajo strace: 6 passed, rc 0). La corrida 1 falló por una escritura ajena en IR, ver D1 |
| V3 | El alias `deskops` de la copia montada apunta a un directorio temporal | PASS: `deskops -> ../../deskops-copy0/deskops/.sldb`, que resuelve a `/dev/shm/pytest-of-robocop/pytest-1010/deskops-copy0/deskops/.sldb` (store_index y `sldb stores list`) |
| V4 | Suite completa bajo flock, rc 0 | NO CORRIDA: veredicto decidido por D2, cancelada por el coordinador (en cola del lock de 20:35:30 a 21:06:10, pytest nunca llegó a arrancar; kill del flock propio) |
| V5 | `deskops graph missing --root .` rc 0 | PASS |
| R-a | Copia única en fixture de sesión, sin caché ni archivos sin rastrear | PASS: `deskops_copy` y `federated` tienen `scope="session"`. La copia no tiene `.sldb_cache`. Contra `git ls-files` ∪ `.sldb` sin caché, no falta nada y no sobra ningún archivo sin rastrear. Solo sobran 39 `__pycache__/*.pyc` que la propia prueba escribe dentro de la copia (20:28:39, al importar los modelos de deskops). Están en el .gitignore de deskops y no se digieren |
| R-b | Symlinks sldb, pron y scion | PASS: los tres existen en `<tmp>/deskops-copy0` y apuntan a `/mnt/ssd/proyectos/SLDB_1/{sldb,pron,scion}` |
| R-c | Ninguna ruta real de deskops fuera de `build_deskops_copy`; `federated` por fixture; digest sobre la copia con la lista de ls-files tomada una vez | PASS en el código |
| R-d | Aserciones de `test_reading_through_every_tool_leaves_every_store_untouched` sin relajar | PASS: las 3 `assert` son idénticas a `git show HEAD:tests/test_mcp_extension.py`. Solo cambian la firma y el argumento `federated` de `copy_digest` |
| R-e | `test_the_deskops_store_linked_is_the_session_copy` comprueba algo real | PASS: lee el store_index real de la copia montada y exige que el alias `deskops` resuelva al `federated["deskops"]` y fuera del WORKSPACE. Con el `FEDERATED` de HEAD fallaría |
| R-f | Sin mocks | PASS: ni `mock`, ni `monkeypatch`, ni `patch(` |
| 3 | La cura: ni el digest ni la sesión MCP abren archivos bajo `SLDB_1/deskops/` fuera de la copia | **FAIL (parcial)**: el digest cumple. La sesión MCP no, ver D2 |
| 4 | Fuera de desk/, .sldb/ y runs/ solo cambian los 2 archivos | PASS |

## Discrepancias

**D2 (la que decide el veredicto): la sesión MCP sigue leyendo el store real de deskops, por federación transitiva.** Strace (`-f`) sobre `tests/test_mcp_extension.py` (resumen en `validation.log`):
- pytest (pid principal) solo toca `SLDB_1/deskops/` entre 20:30:39 y 20:30:55, y lo mismo `git ls-files`: es la ventana de la copia. Después, el digest solo lee la copia. **Esa parte de la cura funciona**: una escritura en el deskops real ya no puede mover `copy_digest` ni tumbar la aserción `changed`, que era el síntoma del Rationale.
- El servidor `sldb mcp` (pid 400960) abre de solo lectura 1761 archivos distintos de `/mnt/ssd/proyectos/SLDB_1/deskops/` durante toda la sesión, de 20:31:33 a 20:34:09: 1973 `openat`, todos con `O_RDONLY`, y 16455 `stat`. Lee `.sldb/core/documents/*` y `.sldb_cache/edges/*`. `sldb stores check` de `mount_copy` (pid 399388) abre también el `store_index.yaml` real. No hay ninguna escritura.
- El camino: `<tmp>/sldb` y `<tmp>/scion` son symlinks a los repos reales, y sus `store_index` federan `../deskops/.sldb`, que sldb resuelve desde la ruta real hacia `/mnt/ssd/proyectos/SLDB_1/deskops/.sldb`. `pron` federa `../../../herramientas/deskops/.sldb`, otra instalación fuera de la copia.
- Consecuencia: el Done When pide literalmente que las pruebas MCP "no leen ni digieren el store real de deskops", y el punto 3 del brief, que la sesión MCP no abra archivos bajo `SLDB_1/deskops/`. **Leen.** Queda el riesgo de que una escritura concurrente de deskops (un archivo a medio escribir o una caché de edges que cambia) haga fallar una `mcp.call` como `check_integrity` o `select_documents include_linked`. Ese fallo ya no estaría en el digest, pero tumbaría la prueba igual. No lo demostré empíricamente, porque no se puede escribir en deskops.
- Causa: viene del contrato, no de un desvío del ejecutor. La precisión (b) manda symlinks a los repos reales, y el ejecutor la cumple al pie de la letra. Una salida posible, que es decisión de contrato: que `<tmp>/sldb` y `<tmp>/scion` sean copias o directorios cuyo `.sldb` resuelva `../deskops` a `<tmp>/deskops`, en vez de symlinks; o aceptar explícitamente la lectura transitiva y ajustar el Done When.

**D1 (fuera de alcance): carrera sobre el store propio de IR.** La corrida 1 de V2 falló en la tercera aserción (`moved`, sobre `IR/.sldb` e `IR/desk`): otro desk dejó a las 20:27:07 una InboxNote en IR (`desk/inbox/20261116-202707-suggestion-sldb-code-lee-sql-...md`, su yaml, `models/InboxNoteDoc.yaml` y `store_index.yaml`) en mitad de la corrida. No tiene relación con deskops. Es la misma clase de carrera que la observación 1 del ejecutor, y esta tarea no la cubre. Afecta igual a la suite completa si alguien escribe en IR mientras corre.

## Observación 2 del ejecutor (`stores check` sobre la copia aislada: 2 store/missing)

La reproduje: `sldb stores check` sobre `pytest-1010/deskops-copy0/deskops` sale con rc 1 por `RunDoc:run-deskops-e-a6a9943b2333` y `run-deskops-t-23c03e37fed7`, "tracked at runs/subagents/{exec,test}-…/run.md, not on disk". Al hacerse la copia, deskops ya tenía los yaml de esos RunDocs en `.sldb`, pero aún no había commiteado sus `run.md`. Minutos después ya estaban rastreados (closeout `36c44b92` de deskops). **No afecta al contrato:** las disposiciones aceptadas excluyen los archivos sin rastrear (bundle-2, punto 1), y el flujo de la prueba (`stores add/update/edges rebuild/check` sobre la copia montada de IR) sale con rc 0. Es una inconsistencia transitoria que hereda la instantánea. Solo importaría si se quisiera que la copia pase su propio `check`.

## Pruebas obsoletas o ausentes

- No hay ninguna prueba que fije que la sesión MCP no lee el deskops real. `test_the_deskops_store_linked_is_the_session_copy` solo mira el alias directo y no la federación transitiva. Por eso D2 pasa inadvertido.

## Veredicto

**FAIL.** El código cumple las precisiones (a)–(d) y la Validation que pude correr: V1, V2, V3 y V5 en PASS, y la cura del digest funciona. Pero no se cumple el Done When ("no leen ni digieren el store real de deskops"), ni el punto 3 del brief: la sesión MCP sigue leyendo 1761 archivos del deskops real, de solo lectura, a través de la federación transitiva de los symlinks sldb y scion (D2). La causa está en la precisión (b) del contrato, así que el arreglo exige decidir el contrato antes de reintentar. V4 no se corrió.
