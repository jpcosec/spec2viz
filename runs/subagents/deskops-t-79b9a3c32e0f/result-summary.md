# Resultado del tester deskops-t-79b9a3c32e0f (intento 1)

- Tarea: `task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a`
- Rol: tester. Contrato: sha256 `39d7d97e36dab7cdddf9d623acf2b0f270796e43032f36936d07535324971908`
- Run dir: `runs/subagents/deskops-t-79b9a3c32e0f/`. La sesión es de Claude Code (no de pi), así que no hay session.jsonl ni sha256 que registrar.
- Trabajo verificado: el diff sin commitear de `tests/conftest.py` y `tests/test_mcp_extension.py`, sobre HEAD `728f68a`.
- Evidencia: `validation.log`, `suite-run1.log`, `suite-run2.log`, `strace-spec2viz-extract.log.gz` (las líneas de strace que tocan `spec2viz/.sldb`, más los `execve`), `board.txt`, `task.txt`, `graph.txt` y `git-status.txt`.

## Veredicto: FAIL (por un solo punto, la verificación 4a)

El diff cumple el Scope, las precisiones (a)–(d), preflight-3 y bundle-3, y toda la Validation escrita da verde. Pero el Done When pide «Ninguna prueba de IR lee … ../spec2viz/.sldb», y el brief pide comprobar justo eso. Con strace se ve que **durante `test_mcp_extension.py` sí se lee `../spec2viz/.sldb`**, solo en lectura y de forma transitiva:

- `deskops/.sldb/core/store_index.yaml` enlaza `spec2viz -> ../spec2viz/.sldb`.
- Por eso, al enlazar el store real de deskops, que sigue en FEDERATED, el servidor también alcanza el store real de spec2viz.

La causa queda fuera de los dos archivos de la tarea, y el ejecutor no la ve. Decide el coordinador: aceptar esta lectura residual o abrir una tarea aparte (en deskops o en la federación de sldb). No me corresponde arreglarlo.

## Verificaciones

| # | Verificación | Estado | Evidencia |
|---|---|---|---|
| 1a | grep `WORKSPACE / "spec2viz"\|\.\./spec2viz` en los 2 archivos | PASS | rc 1, sin coincidencias |
| 1b | `tests/test_mcp_extension.py -rs` | PASS | 5 passed, 0 skipped, rc 0, incluido `test_a_spec_of_the_linked_spec2viz_store_is_read_through_the_server` (218 s, bajo strace) |
| 1c | `tests/visual/test_visual_projections.py` | PASS | 9 passed, rc 0 |
| 1d | `tests/models/test_blog_chain.py` | PASS | 7 passed, 2 xfailed, rc 0 |
| 2 | Suite completa bajo flock | PASS (2.ª corrida) | Corrida 1: 1 failed, 746 passed, rc 1, **invalidada** (ver abajo). Corrida 2: 747 passed, 4 xfailed, rc 0, 299 s |
| 3 | `deskops graph missing --root .` | PASS | rc 0, «No missing graph references found.» |
| 4a | `../spec2viz/.sldb` no se lee | **FAIL** | strace: `sldb stores check` (pid 1433759) abre 1 vez `spec2viz/.sldb/core/store_index.yaml`; el proceso de `sldb mcp` (pid 1435554) hace 1233 `openat` sobre `../spec2viz/.sldb` y `.sldb_cache`, incluido `SpecDoc/class.sldb-models.yaml`. 0 escrituras. El digest y los mtimes del store real son iguales antes y después (`14d066f2…` / `941051c6…`) |
| 4b | El store temporal sale de la API pública y sin mocks | PASS | `build_spec_store`: `tmp_path_factory.mktemp("spec-store")`, copia de la fixture de IR, `init_store` y `SpecSync(store).sync(spec)`. Sin mocks |
| 4c | Precisiones (a)–(d) | PASS | (a) la helper y el fixture de sesión devuelven `<dir>/.sldb`, fuera de root. (b) `mount_copy(..., spec_store)`; `stores add <spec_store> --name spec2viz` con cwd=root, sin `.sldb` duplicado; único llamador, `store_copy`. (c) la prueba lee `spec_store/core/documents/SpecDoc/class.sldb-models.yaml`; `SPEC_STORE="spec2viz"`. (d) `spec_store_digest` = `tree_digest(spec_store)` + sha256 de cada `.md` bajo `spec_store.parent` (rglob), y entra en `copy_digest`, que da el «antes» (`copy_digest_before`) y el «después» |
| 4d | El payload esperado no relaja nada | PASS | Calculado por mi cuenta: el front matter sin `sldb` ⊆ `extract_document_payload` con valores iguales, y el payload agrega `title` y `description`, así que la aserción es más estricta. Las aserciones sobre la respuesta del servidor (found, store, address, path, version y payload) no cambian. Lo autorizan el Implementation Path y preflight-3 (5) |
| 4e | Fuera de desk/, .sldb/ y runs/ solo cambian 2 archivos | PASS | `git diff --stat`: los 2 archivos de tests más `.sldb/core/{models/RunDoc.yaml,store_index.yaml}` (registro de los RunDoc). Sin seguimiento fuera de esas rutas: `src/specir.egg-info` (mtime 02:20, anterior al ejecutor) y `__pycache__/`, artefactos de corrida, no cambios del ejecutor |

### La prueba de la spec sigue probando lo que debe
El `content_hash` del SpecDoc real (`d0a8bcef…`) difiere del temporal (`c64366dd…`), y la prueba exige `document["version"] == entry["content_hash"]` del temporal. Por eso, aunque el servidor también abre el SpecDoc real por la federación transitiva, la respuesta que valida sale del store temporal. La colisión del alias `spec2viz` (temporal en la copia, real vía deskops) se resuelve a favor del temporal.

### Corrida 1 de la suite: invalidada por un escritor externo
El único fallo fue `test_reading_through_every_tool_leaves_every_store_untouched`. Los 4 archivos cambiados son todos del store **real de deskops**:
- `desk/tasks/task-los-selectores-de-deskops-aceptan-…md` y su TaskCodeDoc;
- `models/TaskCodeDoc.yaml`;
- `store_index.yaml`.

El commit `4b4ebaa1` de deskops («closeout: task-los-selectores-de-deskops-…») cayó a las 12:13:45, en mitad de la corrida (que terminó a las 12:15:46). Los mtimes de deskops son 12:13:40 y 12:13:41. Fue un closeout concurrente en otro repo, no una escritura del servidor MCP. Reencolé la suite y la corrida 2 dio verde. Nota: esta fragilidad viene de antes. La prueba digiere el store real de deskops, así que cualquier escritura de otro agente en deskops durante la suite la tumba.

### Impacto del archivo de spec2viz (simulado sin tocar el real)
Copié `deskops/.sldb` y `desk/` a `/dev/shm`, con enlaces simbólicos a los hermanos sldb, pron y scion pero sin spec2viz. Un store nuevo que enlaza esa copia de deskops da PASS en `sldb stores add`, `update` y `check` (rc 0). El control con spec2viz también da rc 0. El enlace transitivo colgante no rompe `stores check`. No simulé la sesión MCP completa con spec2viz ausente, porque FEDERATED apunta a una ruta fija.

## Discrepancias con el ejecutor
1. El ejecutor da por cumplido que no se lee el store real; no lo midió. Con strace, el store real sí se lee de forma transitiva por la federación de deskops (verificación 4a).
2. El resto coincide: los greps, las 5/9/7+2x pruebas, graph missing, el ajuste del payload (`KeyError: 'sldb'` con el front matter crudo; ahora se suman title y description) y el diseño del digest.
3. Observación menor que el ejecutor ya menciona: `tests/visual/test_visual_projections.py` define su propio fixture `spec_store`, de alcance módulo, que tapa al de sesión y devuelve el **proyecto**, no el `.sldb`. No hay conflicto hoy, pero tienen el mismo nombre y semánticas distintas.

## Para el cierre
- Decisión del coordinador sobre 4a: aceptar la lectura transitiva y de solo lectura de `../spec2viz/.sldb` a través de deskops, o abrir una tarea para que deskops deje de enlazar spec2viz (o para que el archivo de G5 lo quite).
- Ninguna prueba faltante u obsoleta en el alcance de la tarea.
