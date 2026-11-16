# Resultado del tester deskops-t-79b9a3c32e0f-a2 (intento 2)

- Tarea: `task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a`
- Rol: tester. Contrato: sha256 `39d7d97e36dab7cdddf9d623acf2b0f270796e43032f36936d07535324971908`
- Run id: `run-deskops-t-79b9a3c32e0f-a2`. Sesión: `scion://agent/deskops-t-79b9a3c32e0f-a2`. Es una sesión de Claude Code, no de pi, así que no hay un archivo de sesión ni un sha256 que registrar.
- Trabajo verificado: el diff sin commitear de `tests/conftest.py` y `tests/test_mcp_extension.py`. Es **byte a byte igual** a `runs/subagents/deskops-e-068628774e48/diff.patch` (`cmp` rc 0).
- Evidencia: `validation.log`, `graph.txt`, `board.txt`, `task.txt`, `next.txt` y `git-status.txt`.

## Veredicto: PASS

## Verificaciones

| # | Verificación | Estado | Evidencia (validation.log) |
|---|---|---|---|
| 0 | El diff coincide con el del ejecutor | PASS | `cmp` rc 0 |
| 1a | grep `WORKSPACE / "spec2viz"\|\.\./spec2viz` en los 2 archivos | PASS | rc 1, sin coincidencias. La única ruta del workspace que queda es `FEDERATED = {"deskops": …}` |
| 1b | `tests/test_mcp_extension.py -rs` | PASS | 5 passed, 0 skipped, rc 0, 142 s, bajo strace. Se recolectan 5 pruebas y pasan las 5, incluida `test_a_spec_of_the_linked_spec2viz_store_is_read_through_the_server` |
| 1c | `tests/visual/test_visual_projections.py` | PASS | 9 passed, rc 0 |
| 1d | `tests/models/test_blog_chain.py` | PASS | 7 passed, 2 xfailed, rc 0 |
| 2 | Suite completa una vez, bajo flock (`-n 4`, timeout 9000) | PASS | 747 passed, 4 xfailed, **0 skipped, 0 failed**, rc 0, 372 s. Antes había 14 GB disponibles. El HEAD de deskops fue el mismo antes y después (`7801327f`), así que no hubo escritor concurrente y no hizo falta reencolar |
| 3 | `deskops graph missing --root .` | PASS | rc 0, «No missing graph references found.» |
| 4a | `../spec2viz/.sldb` no se lee | **PASS** | strace -f sobre toda la corrida de `test_mcp_extension.py` (open, openat, openat2, stat, newfstatat, statx, access, faccessat2, readlink y getdents64; 324 697 líneas): **0** syscalls con `spec2viz/.sldb` y **0** con `SLDB_1/spec2viz` o `../spec2viz`. Hubo 16 406 syscalls sobre el store temporal `spec-store`. El digest de `../spec2viz/.sldb` (`941051c6…`), su mtime máximo y su atime máximo son iguales antes y después |
| 4a' | `../deskops/.sldb` ya no enlaza spec2viz | PASS | `store.yaml` `links:` solo tiene sldb, pron y scion. `grep 'spec2viz/\.sldb\|\.\./spec2viz'` en `store.yaml` y `core/store_index.yaml` da rc 1. La única aparición de `spec2viz` en store_index es la etiqueta semántica `system.spec2viz` del modelo ViewDoc (línea 308), que no es un enlace. Commit `421d6a27` |
| 4b | El store temporal sale de la API pública y sin mocks | PASS | `build_spec_store` copia la fixture de IR `tests/visual/fixtures/spec2viz/docs/architecture/spec2viz/class-sldb-models.yml` a `tmp_path_factory.mktemp("spec-store")` y llama a `sldb.api.init_store(project)` y a `SpecSync(project/.sldb).sync(spec)`. No hay mocks ni documentos escritos a mano |
| 4c | Precisiones (a)–(d) | PASS | **(a)** `build_spec_store(tmp_path_factory) -> Path` devuelve `<dir>/.sldb` y la llama el fixture de sesión `spec_store`. Su directorio está fuera de `root`. **(b)** `mount_copy(tmp_path_factory, name, spec_store)` corre `sldb stores add <spec_store> --name spec2viz --store .sldb` con cwd=root y sin un `.sldb` duplicado. Su único llamador es `store_copy`, según `grep 'mount_copy('`. **(c)** La prueba pide `spec_store` y lee `spec_store/core/documents/SpecDoc/class.sldb-models.yaml`. `SPEC_STORE = "spec2viz"`. **(d)** `spec_store_digest` = `tree_digest(spec_store)` + el sha256 de cada `.md` bajo `spec_store.parent` (rglob, sin la caché), fusionados en el mismo dict. Entra en `copy_digest`, que da el «antes» (`copy_digest_before`, tomado antes de `mcp`) y el «después» de `test_reading_through_every_tool_leaves_every_store_untouched`. `federated_digest` sigue cubriendo solo FEDERATED (deskops). `original_digest` no cambia |
| 4d | El cambio de la fuente del payload no relaja nada | PASS | Lo comprobé por mi cuenta: construí el store igual que la fixture y comparé, con un script independiente (`python -I`). Las claves del front matter son category, diagram_type, id, nav, nodes, notation, sha256, sldb, spec_path, summary y version. Las del payload son esas mismas, sin `sldb`, más `title` y `description`. Ninguna clave del front matter, salvo `sldb`, cambia de valor. La aserción por clave cubre ahora un superconjunto, así que es más estricta. Las aserciones sobre la respuesta del servidor (found, store, address, path, version y el payload clave por clave) siguen iguales; se añaden `expected["id"] == SPEC` y que exista el archivo indexado. Lo autorizan el Implementation Path («se ajusta la prueba para leer los datos del store temporal») y preflight-3 (5): cambia de dónde salen los datos esperados, no lo que se exige al servidor. Los datos esperados vienen de la API pública sobre el store temporal, mientras que la respuesta llega por el servidor MCP sobre la copia montada que federa ese store. La prueba sigue comprobando lo que debe: que una spec de un store enlazado se lee a través del servidor con su identidad, versión y payload |
| 4e | Fuera de desk/, .sldb/ y runs/ solo cambian 2 archivos | PASS | `git status --short` fuera de esas rutas: solo `M tests/conftest.py` y `M tests/test_mcp_extension.py`. Lo demás son los `.sldb/core/{models/ReviewDoc.yaml,models/RunDoc.yaml,store_index.yaml}` y los recibos y RunDocs que deja el registro |

## Discrepancias
- **Con el ejecutor:** ninguna en cuanto a resultados. Mis cifras coinciden: 5, 9 y 7+2x pruebas, graph missing rc 0, `KeyError: 'sldb'` con el front matter crudo, el superconjunto title/description y el diseño del digest. El ejecutor no midió la lectura de `../spec2viz/.sldb`; ahora está medida y da 0.
- **Con el tester del intento 1:** su único FAIL (4a: 1233 `openat` de `sldb mcp` sobre `../spec2viz/.sldb`, por el enlace de deskops) **ya no se reproduce**: 0 aperturas, tras `421d6a27` de deskops. El resto coincide. Su suite necesitó 2 corridas por un closeout concurrente en deskops; la mía pasó a la primera, sin escritores.
- Queda la observación menor del intento 1, que no bloquea: `tests/visual/test_visual_projections.py` define su propio fixture `spec_store`, de alcance módulo, que tapa al de sesión y devuelve el proyecto, no el `.sldb`. Hoy no hay conflicto, pero tienen el mismo nombre y semánticas distintas.

## Para el cierre
- No faltan pruebas ni hay pruebas obsoletas en el alcance de la tarea.
- Sigue abierta la fragilidad conocida, con su propia tarea: `test_reading_through_every_tool_leaves_every_store_untouched` digiere el store real de deskops. En esta corrida no se manifestó.
- No hice commits ni cambié el desk ni el código.
