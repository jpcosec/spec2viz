# Resultado del tester deskops-t-0e183e29ea34-a2

- Tarea: `task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real` (contract_sha256 `d52071c726040e712846438c4b7888ed40f933ee8aae1283bc9658a09b8b7714`), intento 2 (ciclo de corrección 1).
- Rol: tester. run_id `run-deskops-t-0e183e29ea34-a2`. session `scion://agent/deskops-t-0e183e29ea34-a2`. session_sha256: no disponible desde el tester (sesión claude/scion; el run.md lo deja vacío).
- Entrega revisada: el diff sin commitear de `deskops-e-94a0788c3f5a-a2` en `tests/conftest.py` y `tests/test_mcp_extension.py`, sobre HEAD `ad51a0f`.
- Evidencia: `validation.log`, `suite.txt`, `board.txt`, `task.txt`, `next.txt`, `graph.txt` y `git-status.txt`, en este directorio. No escribí en deskops ni en ningún store real. No hice add, commit ni stash.

## Veredicto por verificación

| # | Verificación | Resultado |
|---|---|---|
| V1 | grep `WORKSPACE / "deskops"\|\.\./deskops` | PASS: 2 coincidencias, ambas dentro de `build_deskops_copy`: `conftest.py:96 source = WORKSPACE / "deskops"` y el docstring de l. 93. |
| V2 | `pytest -q -rs -p no:cacheprovider tests/test_mcp_extension.py` | PASS: 7 passed, 0 skipped, rc 0. Bajo strace, también 7 passed y rc 0. |
| V3 | El alias `deskops` de la copia montada | PASS: `sldb stores list` da `deskops -> ../../deskops-copy0/deskops/.sldb` y `spec2viz -> ../../spec-store0/.sldb`, los dos bajo el basetemp de `/dev/shm`. La copia de deskops tiene `stores: []` y `links: []`. |
| V4 | strace: pasada la ventana de la copia, nadie abre nada bajo `SLDB_1/deskops/` | **PASS** (la verificación decisiva; detalle abajo). |
| V5 | Suite completa bajo flock | PASS con 2 fallos ajenos: 747 passed, 4 xfailed, 2 failed, rc 1. Los 2 fallos son exactamente las dos pruebas de `tests/visual/test_sync_generation_parity.py`. Su causa, que reproduje, es el finding `component-spec/syntax-error` sobre `visual/templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js`: la regresión conocida de sldb 600b51a9. No hay ningún otro fallo. |
| V6 | `deskops graph missing --root .` | PASS: rc 0. |
| R-a | La copia se hace una vez, en un fixture de sesión, sin caché ni archivos sin rastrear | PASS. `deskops_copy` y `federated` tienen `scope="session"`, y `git ls-files` aparece una sola vez en la traza. La copia no tiene `.sldb/.sldb_cache`. Su contenido coincide con `git ls-files ∪ .sldb` sin caché, con tres diferencias: la `.sldb_cache/` de la raíz y 39 `.pyc` que se generan en la copia durante la sesión, y 4 archivos rastreados que hoy no existen en el árbol de trabajo de deskops (`tests/fixtures/golden/...inbox*`, borrados sin commitear). El código salta esos 4. |
| R-b | Sin symlinks (precisión (b) corregida). Hay que notar que el brief todavía dice que «existen», pero eso es lo del intento 1 | PASS: hay 0 symlinks en `deskops-copy0`. sldb aceptó `stores remove` para sldb, pron y scion (rc 0), así que no se usó la opción 2. |
| R-b' | `stores declare --write` después de `stores remove` | PASS. Frente al deskops real, el `store.yaml` de la copia solo cambia `links: [sldb, pron, scion]` a `links: []`. Sin ese paso, la declaración conservaría los enlaces y un rebuild del índice los traería de vuelta. Es coherente con (b): no relaja nada y solo opera sobre la copia. |
| R-c | No queda ninguna ruta real fuera de `build_deskops_copy`; `federated` va por fixture; el digest se hace sobre la copia | PASS. `federated_digest` usa la lista `TRACKED` que se tomó al copiar y lee los archivos en la copia. `mount_copy` hace `stores add <copia> --name deskops`. |
| R-d | Las aserciones de `test_reading_through_every_tool_leaves_every_store_untouched` no se relajaron | PASS. Las líneas `assert` son idénticas a `git show HEAD:` (el diff da rc 0). Solo cambian la firma y el argumento `federated` de `copy_digest`. |
| R-e | `test_the_deskops_store_linked_is_the_session_copy` comprueba algo real | PASS. Lee el store_index de la copia montada y exige que el alias resuelva a `federated["deskops"]`, fuera del WORKSPACE. Con el `FEDERATED` de HEAD fallaría. |
| R-f | `test_no_store_linked_from_the_mounted_copy_leads_out_of_the_session_temp` comprueba algo real y fallaría con los symlinks del intento 1 | PASS. Recorre la federación de forma transitiva, con `resolve()`. Lo demostré con un layout en `/dev/shm` en el que `<base>/sldb` es un symlink al repo real: `linked_stores` resuelve a `/mnt/ssd/proyectos/SLDB_1/sldb/.sldb` y la aserción falla. |
| R-g | Sin mocks | PASS: no hay `mock`, `monkeypatch` ni `patch(`. |
| 4 | Fuera de `desk/`, `.sldb/` y `runs/` solo cambian los 2 archivos | PASS |

## V4 en detalle (strace -f -tt)

- Traza: `execve` más las syscalls de archivos (open*, stat*, access, readlink, chdir, getdents64) de `pytest tests/test_mcp_extension.py` con `--basetemp` en `/dev/shm`. Tuvo 1.015.955 líneas y la borré después de analizarla; el resumen está en `validation.log`.
- La ventana de la copia termina con el último syscall del `stores declare --write` final (pid 916362), a las 22:06:32.122915. El siguiente proceso es el `stores add ... --name deskops` de `mount_copy`.
- Hay 129.024 accesos que nombran `SLDB_1/deskops`. Todos vienen del pytest principal (es decir, de copytree/copy2) y de `git ls-files`, entre las 22:06:05.545 y las 22:06:20.510. Terminan antes del primer `stores remove`.
- **Después de la ventana hay 0 accesos**, y eso incluye a `sldb mcp`, `stores add/update/check` y `edges rebuild`.
- El único `chdir` al deskops real es el de `git ls-files`. No hay ninguna ruta relativa `../{deskops,sldb,pron,scion}`.
- `SLDB_1/{sldb,pron,scion}/.sldb` y `herramientas/deskops/.sldb` tienen 0 accesos en toda la corrida. Fuera de IR, después de la ventana solo se leen `SLDB_1/sldb/src` y `pyproject.toml`, que son el código del paquete sldb instalado editable y no su store.
- Conclusión: después de la copia no se lee el deskops real. Una escritura en deskops durante la corrida ya no puede mover el digest ni lo que lee la sesión MCP. El D2 del intento 1 queda resuelto.

## Comparación con el informe del ejecutor

Coincide en todo lo verificable: el grep, los 7 passed, los alias, los 3 `remove` aceptados, el diff de `store.yaml` y el strace con 129.007 accesos antes del corte y 0 después; mi cifra (129.024) cuenta más tipos de syscall. No hay discrepancias de fondo. Una aclaración menor: la línea de `source` es la 96 y la del docstring la 93, no la 92 y la 89 que da el ejecutor. Su observación de que la opción 2 de (b) no está cubierta por pruebas es correcta: el camino existe, pero no se ejercita.

### Observación 2 (`stores check` sobre la copia aislada da 2 store/missing)

La reproduje. Da rc 1 por `RunDoc:run-deskops-e-d5d217748798` y `run-deskops-t-350841cd869d`. Sus `run.md` existen en deskops, pero no están rastreados (no aparecen en `git ls-files` y tampoco están ignorados). La copia los excluye por (a) y por la disposición bundle-2 (1).

**No afecta al contrato.** Ninguna Validation exige que la copia de deskops pase su propio `check`. El `stores check` de `mount_copy`, sobre la copia montada de IR, sale con rc 0, y las 7 pruebas pasan. Es una inconsistencia transitoria que hereda la instantánea mientras deskops tiene RunDocs sin commitear. Solo importaría si en el futuro alguna prueba leyera esos RunDocs concretos a través de la federación.

## Pruebas obsoletas o ausentes

- La opción 2 de (b) (copiar el store enlazado cuando sldb rechaza el `remove`) no tiene cobertura: hoy no se ejercita. No bloquea, porque el contrato solo la exige como alternativa.
- Sigue fuera de alcance la carrera sobre el store propio de IR, `IR/.sldb` e `IR/desk` (D1 del intento 1).

## Veredicto

**PASS.** Se cumplen las precisiones (a)–(d) y toda la Validation: V1, V2, V3, V4 y V6 dan PASS, y V5 da verde salvo los 2 fallos externos conocidos de `test_sync_generation_parity.py`, cuya causa verifiqué. Con strace queda demostrado que, terminada la copia, ningún proceso abre nada del deskops real ni de los stores de sldb, pron o scion. No hay mocks ni aserciones relajadas, y fuera de `desk/`, `.sldb/` y `runs/` solo cambian los 2 archivos. Antes del closeout no hace falta nada más.
