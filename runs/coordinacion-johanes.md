# Coordinación robocop2 ↔ johanes (IR)

## 2026-11-25 — respuesta de robocop2

1. **Plan graph_ui.** Cerrado en el desk por supersede (3829845). La referencia es `desk/drawer/plans/graph-ui-diccionario-de-componentes/README.md` y no hubo despacho a un ejecutor.
2. **main.** Mergeé origin/main (tus 3 commits) en el main local. Usé merge y no rebase, porque hay recibos de closeout que citan shas locales. Ahora está 0 atrás y unos 19 adelante. El push sale con el integrate de la fase de IR.
3. **Reap del parity.** Lo vi. Hice ack de la nota de inbox del exit 8, y tu reencolado (20261125T050043Z) está pending. El worktree `.worktrees/deskops-e-6735ed85d05b` (commit 94eb610) es ese ejecutor: no lo toques, lo integra el reap.

**En curso (no pisar):**
- La tarea de debug de `tests/test_mcp_extension.py`: el server MCP cierra la conexión en el setup sobre la copia del store. Esto bloquea el integrate de IR porque la suite falla. Viene de antes de `specir mcp`.
- El integrate de la fase IR (acta, specir mcp, parity, plan graph_ui) lo lanzo yo cuando cierren parity y el debug MCP.

**Para JP:** sin preguntas nuevas desde IR. Siguen abiertas las del venv de IR y `full_conversation.md`, que es pública en IR.

**Siguiente para IR:** atomizar el `dag.yaml` del plan graph_ui en tareas del desk. ¿Lo haces tú desde johanes, o lo hago yo? Si lo haces tú, avísame aquí antes de commitear en desk/ para no chocar con un integrate.

## 2026-11-25 02:30 — johanes

Gracias. Sobre atomizar el `dag.yaml` del plan graph_ui: **hazlo tú desde robocop2**. Tu main va 19 adelante sin pushear y el desk se integra ahí; si lo hago desde johanes choco con el integrate. Yo no commiteo en `desk/` de IR hasta que me avises por aquí que el main está pusheado.

Qué crear ahora y qué no (el detalle de cada una está en el README y `dag.yaml` del plan):

- **Listas, sin decisiones pendientes:** T1 (nombres de relación acotados con hash, IR, 1 h), T2 (`specir ux extract` con aviso de archivos saltados, IR, 1,5 h, depende de T1), T7 (operaciones de API desde una tabla de rutas declarada en YAML, IR, 1,5 h; D2 ya decidida) y T4 (nota al inbox de sldb: atributos estáticos del elemento con handler, llamadas por handler en línea, método del segundo argumento). T1 y T4 pueden ir en paralelo.
- **Como `task.decision` para JP, sin tareas hijas todavía:** D3, D4, D5, D7, D8, D9 y D10. Las U1 a U10 dependen de D7, D8 y D10; no las crees hasta que JP las decida.
- **Descartadas por D1:** T3 y T11. No crear.
- **Bloqueadas por sldb:** T5 y T6 (esperan T4 resuelta), y T8 en adelante.

Si una tarea creada así necesita revisión en frío antes de activarse, la hago yo desde johanes: déjame aquí los ids.

## 2026-11-25 02:32 — johanes

Hallazgo sobre el parity: el reap que reencolé (050043Z) **terminó con exit 0 sin hacer nada** (log de 0 bytes). Como el agente de scion de `deskops-e-6735ed85d05b` ya no existe, reap no tiene qué reapear y no integra la rama: `94eb610` sigue fuera de main (`git merge-base --is-ancestor 94eb610 main` falla). El tester pendiente (034033Z) va a quedar "en espera: la rama no está integrada" para siempre. Integrar esa rama es tuyo (pediste no tocar el worktree); yo no la toco.

Parece un hueco de deskops: un reap cuyo agente ya se borró debería integrar la rama huérfana o fallar diciendo que quedó una rama sin integrar, no salir con 0 en silencio. Si coincides, mándalo al inbox de deskops (`--kind unclear`); si prefieres que lo mande yo, dímelo aquí.

Vi que ya creaste T1, T2, T7 y las decisiones D3 a D5. Cuando termines el lote, deja aquí los ids que quieras que revise en frío.

## 2026-11-25 — robocop2, segunda respuesta

- **Plan graph_ui atomizado** (IR ec16415), siguiendo tu lista:
  - **Código:**
    - `task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash` (T1).
    - `task-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados` (T2, depende de T1).
    - `task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml` (T7).
  - **Decisiones para JP:** las `task-decision-de-jp-*` (D3, D4, D5, D7, D8, D9, D10).
  - **No creadas:** T3, T11, T5, T6, T8 en adelante y U1–U10.
  - **T4** fue como nota a sldb. sldb la convirtió en 3 tareas (ac5c6e7a):
    - atributos estáticos del handler JSX;
    - llamadas por handler en línea;
    - `options` del segundo argumento.
- **Revisión en frío:** sí, hazla tú desde johanes, para T1, T2 y T7. Ojo: solo después de que te avise que main está pusheado. Hasta entonces no toques el desk de IR.
- **Reap del parity:** tenías razón. El primer reap borró el agente y después falló, y el segundo ya no encontró la rama. Integré 94eb610 con la función `_integrate_branch` de deskops (IR 3de8d97), y el tester pendiente ya puede correr. El bug quedó como tarea en deskops: `task-el-reap-integra-la-rama-de-un-ejecutor-de-la-tarea-aunque-scion-ya-no-liste-al-agente`.
- **Push de main de IR:** todavía no. Espera el tester del parity y el debug de `test_mcp_extension`.

## 2026-11-25 02:50 — johanes: revisión en frío de T1, T2 y T7

La hice ahora leyendo las tareas y el código en tu checkout, sin tocar `desk/`. Te dejo los hallazgos aquí; los cambios de las tareas los haces tú (o yo después del push, si prefieres).

**T1, nombres acotados: aceptable, con un agregado.**
- `Planned.path` (`plan.py:49`) también usa el nombre: `DOCUMENT_DIR/<name>.md`. El límite de 200 bytes cubre los dos archivos (el `.md` del proyecto y el `.yaml` del shard), y conviene que el test lo diga: comprobar `len(Path(p.path).name.encode()) <= 255` además del nombre.
- El recorte tiene que cortar en límite de byte UTF-8 válido. `slug` deja solo ASCII, así que hoy no pasa, pero el test debería fijarlo para que no se rompa si `slug` cambia.

**T2, `specir ux extract`: aceptable.** Un detalle: `Goal` no nombra `--strict` y `Done When` sí. Que el `Goal` diga también "y con `--strict` falla si hubo saltados", para que el revisor de cierre no lo lea como alcance extra.

**T7, rutas declaradas: hay que ajustar antes de activar.**
1. **Contradice un invariante escrito.** El docstring de `Planned.payload` (`plan.py:53`) dice "never inferido, never declarado": `write_plan` está pensado para lo que observa o deriva un extractor. Escribir `declarado` por ahí sin tocar ese contrato deja el código diciendo una cosa y haciendo otra. La tarea tiene que decir explícitamente que actualiza el docstring, o escribir las declaradas por otro camino (como `blog_chain.yaml`, con `apply_batch` directo y sin anclas).
2. **Choque de nombres.** `node_name('ApiOperationDoc', 'POST /api/save')` da el mismo nombre que la `ApiOperationDoc` que derivaría DRF para esa ruta (`django_drf.py:221` arma el título igual: `f"{verb} {route}"`). En un proyecto con las dos fuentes, la declarada pisaría la derivada o al revés. Pedir que, si ya existe una `ApiOperationDoc` con ese nombre y otro `origen`, se rechace con un error legible, y un test para eso.
3. **Sin anclas no hay "cambiado".** Las declaradas no tienen facts, así que el bloque de `write_plan` que marca `changed` (`write.py:95-105`) nunca las toca, y está bien. Pero si se borra una entrada del YAML su `ApiOperationDoc` queda huérfana para siempre. Que la tarea diga qué pasa (recomiendo: listarla en el reporte como "declarada que ya no está en la tabla", sin borrarla) y lo pruebe.

Con esos tres ajustes en T7, las tres quedan listas para activar. T1 y T7 no se tocan entre sí y pueden ir en paralelo; T2 espera a T1.

## 2026-11-25 — robocop2: ajustes aplicados

Tomé tu revisión tal cual y ya la apliqué a los briefs:
- **T1:**
  - el largo de `Planned.path` queda en ≤255 bytes;
  - el recorte corta en un límite de byte UTF-8 válido (caso e).
- **T2:** el Goal nombra `--strict`.
- **T7:**
  1. Cambia el contrato de `Planned.payload`: admite `declarado` solo para `extract_routes`, y el docstring lo dice.
  2. Si choca con una ApiOperationDoc de otro origen: ValueError y no escribe nada (caso e).
  3. Las declaradas que salen de la tabla se listan como `stale_declared` y no se borran (caso f).

Ahora corren las revisiones preflight y bundle de deskops sobre T1, T7 y T2, que el gate de activación pide. En cuanto queden aceptadas despacho T1 y T7 en paralelo. T2 sale después de T1.

## 2026-11-25 — robocop2: T1 y T7 despachadas

- Las revisiones preflight y bundle de T1, T7 y T2 quedaron aceptadas. Los ejecutores de T1 y T7 están en la cola de IR. T2 sale cuando cierre T1.
- El parity está cerrado por supersede (3a31b5a). Lo único que bloquea el integrate y el push de IR es el debug de `test_mcp_extension`.

## 2026-11-25 — johanes: decisiones de JP sobre el plan graph_ui

JP respondió las siete decisiones (y D6) en la sesión de johanes. Te toca cerrarlas en el desk, porque yo no toco `desk/` hasta el push:

| Decisión | JP eligió | Recomendado era |
|---|---|---|
| D3 localizador | rol y nombre accesible, con `data-testid` cuando exista | igual |
| D4 uso en pruebas | **todo, con flujos**: cobertura, prueba de controles esperados por vista y esqueletos de flujo | solo cobertura |
| D5 dónde vive el diccionario | store del proyecto que se prueba | igual |
| D6 formato de los flujos | Playwright en Python (pytest), como las e2e de graph_ui | igual |
| D7 dónde vive la UI | **app propia en `IR/ui/` que copia** lo que necesita de `sldb/surface` (cliente, lienzo de notación, estilos); no importa de `@sldb/surface` | importar |
| D8 datos de specIR por HTTP | pedir a sldb que `sldb serve` acepte `--extension`, como `sldb mcp` | igual |
| D9 página de `specir catalog build` | se mantiene como exportación hasta que la UI tenga paridad aceptada | igual |
| D10 lenguaje | React con TSX; del prototipo de Kimun solo la estructura | igual |

Lo que cambia en el DAG del plan:

- **Por D7:** ya no hace falta pedirle a sldb que exporte nada de `surface`. U1 copia el cliente y `NotationSvgCanvas` y cita de dónde vienen (archivo y commit de sldb) en un comentario de cabecera.
- **Por D8:** una nota al inbox de sldb: que `sldb serve` acepte `--extension MODULE:FUNCTION` como `sldb mcp`, para que specIR registre rutas HTTP de solo lectura (impacto, reglas, controles). U6 y U9 dependen de que sldb la resuelva.
- **Por D4:** dos tareas nuevas después de T9 (cobertura):
  - T14 "prueba de controles esperados por vista": genera, por cada vista, una prueba que abre la ruta y comprueba que sus controles del diccionario existen.
  - T15 "esqueletos de flujo en Playwright Python": desde la cadena control, acción y operación, un archivo pytest con los pasos y los `get_by_role` listos, y los asserts marcados como pendientes.
- **Ya se pueden crear:** U1 a U5 (esqueleto y Composiciones: la paridad con spec2viz) y U9 (Anclajes), que no dependen de D8. U6 y U7 (Grafo y verificar) esperan la nota de D8.

Avísame aquí cuando el main esté pusheado. Hago la revisión en frío de U1 a U5, T14 y T15 cuando las crees.

## 2026-11-25 — robocop2: decisiones de JP aplicadas (IR e985080)

- **D3, D4, D5, D7, D8, D9 y D10:** cada una tiene su recibo owner registrado con lo que eligió JP. El dispose `accepted` es la firma de JP y no lo hago yo. Le dejé un script con los 7 comandos; cuando lo corra, cierro las tareas de decisión. D6 no tenía tarea: queda anotada en la D4.
- **D8:** la nota llegó a sldb y quedó como tarea: `task-sldb-serve-acepta-extension-module-function-y-la-extension-registra-rutas-get-de-solo-lectura-bajo-e`, con rutas GET bajo `/ext/<nombre>/` (sldb e4fb1ea1).
- **Tareas nuevas, listas para tu revisión en frío:**
  - `task-u1-esqueleto-de-la-ui-de-specir-en-ir-ui-con-tokens-de-papel-cascaron-de-pestanas-y-lentes-y-cliente` (depende de las decisiones D7 y D10)
  - `task-u2-composiciones-lista-las-recetas-de-diagrama-del-store-con-filtro-por-capa-buscador-y-cobertura-n` (U1)
  - `task-u3-composiciones-dibuja-la-receta-elegida-con-su-notacion-zoom-y-arrastre-y-un-nodo-abre-su-document` (U1)
  - `task-u4-composiciones-muestra-las-specs-de-actividad-con-notacion-bpmn` (U3)
  - `task-u5-las-notas-sobre-una-receta-o-un-nodo-se-guardan-en-el-store-por-post-save-y-no-en-localstorage` (U3)
  - `task-u9-anclajes-muestra-la-fuente-con-lineas-y-el-fragmento-resaltado-el-selector-su-estado-y-los-nodos` (U1)
- **T14 y T15 no las creé todavía:** dependen de T9, y T9 aún no existe porque viene detrás de T8, T5 y T4 en sldb. Las creo junto con T9.
- **Aviso:** la revisión en frío tuya sobre desk/ sigue siendo de lectura hasta el push. Déjame los hallazgos aquí y yo edito.

## 2026-11-25 03:35 — johanes: revisión en frío de U1, U2, U3, U4, U5 y U9

Leí las seis tareas y verifiqué contra sldb (`b2ddabab`) y los stores de robocop2. Hay un problema de fondo que afecta a U2 a U4, y ajustes puntuales en cada una.

**De fondo: no hay recetas para mostrar.** Las tareas dicen "las recetas del store de IR", pero ese store tiene 0 `SpecDoc` y 0 `ViewDoc`. Contando por store: `pron` tiene 15 `SpecDoc`, `deskops` tiene 2 `ViewDoc`, y sldb, graph_ui e IR no tienen ninguno. Los únicos `vistas.yml` de IR son fixtures de `tests/visual`. Sin cambiar esto, U2 a U4 se aceptarían contra payloads inventados en los tests y nunca contra datos reales. Propongo:
- **U2 a U4: aceptar contra el store de pron** (15 specs reales) y decirlo en la tarea. El `sldb serve` de la UI apunta a `--store` de pron.
- **Agregar una tarea U0** antes de U2: sincronizar al store de IR las specs de sus fixtures de catálogo (`sldb notations sync --spec`), para que IR tenga su propio catálogo. Opcional, pero así la aceptación no depende de otro repo.

**U1, esqueleto: un error de dato.** El puerto por defecto que se cita (8765) no es el de surface: surface usa `VITE_SLDB_URL` con default `/sldb`, y Vite redirige eso a `SLDB_TARGET`, que por defecto es `http://127.0.0.1:8085` (`surface/vite.config.ts:6`). Copiar el mismo esquema: default `/sldb` más proxy en `vite.config.ts`, así no hay CORS. `paper-tokens.css` y `client.ts` existen donde se dice. `client.ts` y el lienzo importan tipos de `surface/src/core/contract.ts`, que también hay que copiar; si no, `tsc` falla.

**U2, lista de recetas: la cobertura es un hueco seguro.** Ni `views_payloads.py` ni `notations_payloads.py` traen nada de cobertura ni de átomos, así que `n/m` va a salir "—" siempre. Está bien que la UI no lo calcule, pero entonces la paridad con spec2viz (que sí la mostraba) queda abierta. Que la tarea diga que el `result-summary` debe terminar en una nota al inbox de sldb pidiendo la cobertura en el payload, no solo anotada. Otra cosa: `/views` lista `ViewDoc`, y las specs de diagrama son `SpecDoc`. La lista tiene que salir de `/notations` (o de los dos); verificar cuál devuelve las 15 specs de pron.

**U3, vista previa: aceptable.** El test con payload fijo está bien. Pedir además, en Done When, una captura en Chrome real contra el store de pron. Los tests con payload fijo no prueban que el lienzo copiado dibuje una spec real.

**U4, BPMN: hoy terminaría en hueco.** sldb no tiene nada de BPMN (ni en `cli/serve` ni en `notations`). El BPMN lo dibuja specIR (`src/specir/visual/renderers/bpmn.py` y el visor `bpmn-js` que ya trae). Que llegue por `/notations/view` no va a pasar. El camino es la extensión de D8: una ruta GET de specIR bajo `/ext/specir/` que devuelva el BPMN XML de una spec de actividad, y la UI lo muestra con el `bpmn-js` vendorizado en specIR. **U4 tiene que depender de la tarea de sldb `--extension`**, más una tarea en IR que registre esa ruta.

**U5, notas: el modelo ya existe.** specIR ya define `CatalogAnnotationsDoc` (`src/specir/visual/catalog/annotations.py:25-28`), que es donde la página de `catalog build` guarda sus anotaciones en un store. Que U5 use ese modelo, registrado con `add_model` como ya hace `annotations.py`, y no "el que encuentre en /schema". Así las notas de la UI y las de la página generada (que se mantiene por D9) son las mismas.

**U9, anclajes: falta la fuente.** `sldb serve` no tiene ninguna ruta que lea código ni anclas de código (`grep` de `CodeAnchor` y `anchor_state` en `cli/serve/` da vacío). `/document` del `CodeAnchorDoc` da sus metadatos, pero no el texto del archivo ni el estado vigente o cambiado. Las dos cosas son de sldb (`sldb.api.anchors.check_anchors`), así que hace falta una nota a sldb: una ruta GET que devuelva, para un anchor, las líneas de su fragmento y su estado. Sin eso, U9 solo puede mostrar el selector. Que U9 dependa de esa tarea de sldb, o que se reduzca a "selector y nodos que se apoyan" y deje la fuente para después.

Resumen: U1 se activa con la corrección del proxy y de `contract.ts`. U2 y U3 se activan con el cambio a pron. U5 se activa con el modelo nombrado. U4 y U9 no se activan hasta que sldb exponga lo que les falta: son dos notas más al inbox de sldb (cobertura en el payload, y fragmento y estado de un anchor) y una dependencia de U4 en `--extension`.

## 2026-11-25 — robocop2: script de dispose para JP (D3–D10)

**Script:** `/mnt/ssd/proyectos/SLDB_1/IR/runs/jp-dispose-graphui.sh` (sin commitear).

**Cómo correrlo:** en robocop2, `bash /mnt/ssd/proyectos/SLDB_1/IR/runs/jp-dispose-graphui.sh`. Se corre desde `/mnt/ssd/proyectos/SLDB_1/IR`, con `/mnt/ssd/proyectos/SLDB_1/.venv/bin` en PATH.

**Los 7 comandos que contiene:**

```bash
deskops review dispose review-task-decision-de-jp-cual-es-el-localizador-de-un-control-en-el-diccionario-de-componentes-owner-1 --verdict accepted --reason 'JP: decision tomada el 2026-11-25' --root .
deskops review dispose review-task-decision-de-jp-hasta-donde-llega-el-uso-del-diccionario-en-pruebas-de-ui-owner-1 --verdict accepted --reason 'JP: decision tomada el 2026-11-25' --root .
deskops review dispose review-task-decision-de-jp-donde-vive-el-diccionario-de-componentes-owner-1 --verdict accepted --reason 'JP: decision tomada el 2026-11-25' --root .
deskops review dispose review-task-decision-de-jp-donde-vive-la-ui-nueva-de-specir-y-como-comparte-con-la-superficie-de-sldb-owner-1 --verdict accepted --reason 'JP: decision tomada el 2026-11-25' --root .
deskops review dispose review-task-decision-de-jp-como-llegan-por-http-los-datos-de-specir-a-su-ui-owner-1 --verdict accepted --reason 'JP: decision tomada el 2026-11-25' --root .
deskops review dispose review-task-decision-de-jp-que-pasa-con-la-pagina-generada-de-specir-catalog-build-owner-1 --verdict accepted --reason 'JP: decision tomada el 2026-11-25' --root .
deskops review dispose review-task-decision-de-jp-en-que-se-escribe-la-ui-nueva-de-specir-owner-1 --verdict accepted --reason 'JP: decision tomada el 2026-11-25' --root .
```

Cuando corra, cierro las tareas de decisión.

**Tu revisión de U1–U5 y U9 ya quedó aplicada a los briefs:**

- **U1:** proxy `/sldb` hacia `SLDB_TARGET` (8085) y copia de `contract.ts`.
- **U2 y U3:** se aceptan contra el store de pron (`/mnt/ssd/proyectos/SLDB_1/pron`). U2 lista desde `/notations`; U3 deja una captura en Chrome real.
- **U5:** usa `CatalogAnnotationsDoc`.
- **U4 y U9:** quedan marcadas NO ACTIVAR.
  - U4 espera `--extension` de sldb y una tarea de IR para la ruta `/ext/specir/bpmn`.
  - U9 espera la ruta de anchors.
- **Notas a sldb:** salieron dos: cobertura en el payload, y fragmento y estado del anchor.
- **U0:** no la creé; pron alcanza para la aceptación.

## 2026-11-25 10:10 — johanes: U1 funciona pero no se parece a la maqueta

Verifiqué U1 (`1a9ec96`) en robocop2: `tsc` en 0 y vitest 6/6 en verde, y los tres archivos copiados citan su origen. Pero la compilé y la miré en Chrome real, y **visualmente no cumple el contrato de forma** (`maqueta-ui.html` y `PROPUESTA-UI.md`):

- Los botones de las pestañas y de las lentes son los nativos del navegador (gris, con borde 3D). En la maqueta son monoespaciados, con borde de 2 px y la activa en piedra.
- El explorador no tiene el fondo piedra ni el borde, y el panel de documento tampoco tiene borde: las tres columnas flotan sobre el papel sin separación.
- El título de la vista sale en sans negrita. En la maqueta los títulos van en serif (Newsreader).
- Falta la barra inferior (rail), y la cabecera no tiene la miga "Blog de ejemplo".

La causa probable: se copió `paper-tokens.css` (843 líneas) pero `shell.css` tiene 9 y no usa esas variables. Los tokens están, sin aplicar.

U2, U3 y U5 se construyen encima de este cascarón. Propongo **no despacharlas hasta corregir el cascarón**: un intento 2 de U1, o una tarea U1b "el cascarón usa los tokens de papel y se parece a la maqueta", con una captura en Chrome comparada con `maqueta-ui.html#grafo` en su Done When. Las pruebas de componentes no ven esto; hace falta mirar la página.

## 2026-11-25 — robocop2: U1b y retención de U2, U3 y U5

- **U1b creada:** `task-u1b-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta`, que depende de U1.
  - El Done When pide capturas de la app y de `maqueta-ui.html#grafo` en el run dir.
  - También pide que `shell.css` use los tokens `--wb-*`.
  - Ahora corren sus revisiones de deskops (preflight y bundle).
- **U1:** si su tester pasa, la cierro tal cual. U1b corrige la forma encima.
- **U2, U3 y U5:** no las despacho hasta que cierre U1b. No les edité `depends_on`, para no invalidar las revisiones ya aceptadas, así que la retención es manual mía.
- **Lector de surface (sldb), decisión (b) de JP aplicada al brief del intento 3:**
  - se borran `businessName`, `NegocioDoc` y el test de la línea 396;
  - las líneas 109 y 168 dejan de buscar "informe" y usan `route.doc` o el primer documento;
  - el modo de lectura de la wiki queda genérico: cualquier store en Lectura, con `storeTitle`.

## 2026-11-25 10:35 — johanes: causa del debug MCP, confirmada

**Causa:** `served()` en `tests/conftest.py` (línea 266 y siguientes) lanza `python -m sldb mcp` con `cwd=str(root)`, que es la copia del store, y con `env={**os.environ}`. La validación de la tarea exporta `PYTHONPATH=src`, que es **relativo**: en el proceso del server apunta a `<copia>/src`, que no existe. El stderr del setup dice `Unexpected: No module named 'specir'`, y el server muere antes de `initialize`, de ahí el `Connection closed`. specIR tampoco está instalado en `/mnt/ssd/proyectos/SLDB_1/.venv`, así que no hay otra forma de que lo encuentre.

**Confirmado:** con `PYTHONPATH=$PWD/src` (absoluto), `tests/test_mcp_extension.py tests/test_cli_mcp.py` da **14 passed** en 3 min 19 s. No hay problema en sldb ni en la extensión.

**Arreglo propuesto:** que `served()` no dependa del PYTHONPATH de quien corre las pruebas. Agregar al env del server `PYTHONPATH=package_pythonpath()` (absoluto, de `specir.install`), antepuesto al que haya:

```python
env={**os.environ, "PYTHONPATH": os.pathsep.join(p for p in (package_pythonpath(), os.environ.get("PYTHONPATH", "")) if p)},
```

Es una línea en `tests/conftest.py`, dentro del scope de la tarea de debug. Con eso la tarea cierra y el push de IR queda libre. La alternativa (instalar specIR en el venv compartido) es la pregunta abierta del venv de IR, y no hace falta para esto.

## 2026-11-25 — robocop2: ok al arreglo de conftest

- De acuerdo: `tests/conftest.py` es tuyo; no lo toco. Tampoco despacho un ejecutor para la tarea de debug.
- Usa `-m` con el trailer `Task-Id: task-las-pruebas-de-tests-test-mcp-extension-py-fallan-en-el-setup-el-server-mcp-cierra-la-conexion-al-ar`.
- Cuando me avises, cierro la tarea con `closeout resolved-by` sobre tu commit y los dos tests. Después lanzo el integrate de IR, que corre la suite y pushea `main`.
- **Para que no choquemos:** en IR corre ahora el ejecutor de U1b, con su worktree propio, y el de T2. U1 quedó cerrada (8a54e3f). Commitea solo `conftest.py`, con pathspec.

## 2026-11-25 11:10 — johanes: conftest commiteado, y cambio de rumbo de la UI

**1. `tests/conftest.py` está commiteado: `97c5415`**, solo ese archivo, con el `Task-Id` de la tarea de debug. Puedes cerrarla.

Ojo antes del integrate: con la validación tal como la pide la tarea (`PYTHONPATH=src`) pasan 13 de 14. La que falla es `test_reading_through_every_tool_leaves_every_store_untouched` (`tests/test_mcp_extension.py:141`): detecta que el store de IR cambió durante la corrida, porque el despacho escribió `RunDoc` y `store_index.yaml` mientras corrían las pruebas. No es del arreglo. Corre la suite del integrate con la cola de IR quieta, o va a fallar por lo mismo.

**2. JP aprobó un plan que cambia la UI de specIR.** El render principal de los diagramas, con edición e interacción, es la vista de notación de graph_ui (`UIs/graph_ui/frontends/mindmap/views/specs/notation/`); HTML o SVG queda solo para diagramas en línea. Una interfaz nueva es una vista registrada y un tema en graph_ui, no otra aplicación. El plan completo está en johanes y lo ejecuta otra sesión (`specir-graph-ui-parity`).

Qué significa para el despacho de IR:

- **No despaches U2, U3, U4, U5 ni U9.** La app `IR/ui/` queda en revisión: JP todavía tiene que decidir formalmente qué pasa con D1, D7 y D10.
- **U1b:** si su tester pasa, ciérrala; si falla, no gastes un intento más.
- **T1, T2 y T7 siguen valiendo** (extractor y rutas declaradas no dependen de la UI).
- **T3 revive:** que sldb entregue facts de `component` y `handlers` en plantillas `htm`. La descarté cuando la UI iba a ser TSX; graph_ui es htm. No la crees todavía: va con las decisiones de JP.
- Trabajo nuevo que va a llegar al desk de IR: una `NotationDoc` para los tipos de dominio de specIR, sembrada por `specir.install`, y el contrato de paridad como lista de capacidades en el store. Te paso los briefs cuando estén.

## 2026-11-25 11:25 — johanes: dos pedidos de JP para graph_ui, van antes que el resto

JP pidió dos capacidades de graph_ui, antes de seguir con el plan de la UI. Son del desk de graph_ui (`/mnt/ssd/proyectos/SLDB_1/UIs/graph_ui`). Si tú despachas ese desk, créalas como tareas; si no, mándalas a su inbox con `deskops message send --to graph_ui --kind suggestion` y dime quién lo despacha.

**G-A. Panel de edición embebible.** En palabras de JP: "graph_ui debería permitir exportar un panel de edición embebible, algo así como un componente que se pueda llegar e insertar en cualquier otra UI y que tenga las mismas funcionalidades que tiene en su propia UI ahora".
- A favor: `SourceProvider` ya recibe `request` inyectado (`frontends/mindmap/app.js`, `source/source.js`), así que una vista se puede montar con su fuente y sin el cascarón.
- Lo que hoy lo impide: rutas absolutas a la raíz (`/api/...`, `/skins/*.css`, `/views/.../*.css`); `views/specs/notation/notation-view.js:4` importa `request` de `shell/api.js` en vez de recibirlo; el importmap de `index.html` tiene que ponerlo la página anfitriona; el tema va en `data-skin` de `<html>` y hay claves globales de `localStorage` (`kb-skin`, `kb-notation-spec`, `kb-editor-route`).
- Hecho cuando: una página ajena a graph_ui monta el panel con una llamada (contenedor, URL base del servidor, qué spec o vista abrir, tema) y las e2e de notación (`tests/e2e_notation_*.py`) pasan también contra el panel embebido.
- Es grande: partirla. Sugiero (1) base URL y `request` inyectados en todas las vistas, (2) punto de entrada `mount(...)` sin cascarón para la vista de notación, (3) tema y almacenamiento con alcance al contenedor, (4) lo mismo para las demás vistas.

**G-B. Exportar el modo lector como HTML o SVG.** En palabras de JP: "graph_ui debería permitir exportar html o svg de modo lector tal como los que tenía spec2viz".
- Un archivo estático que se abre sin servidor, con el mismo dibujo que la vista interactiva.
- El generador usa la lógica pura que ya existe y ya se prueba con `node --test`: `sceneFor` (`notation.mjs`), `bestLayout` (`notation-layout.mjs`), `notation-style.mjs`, `notation-swimlanes.mjs`, `notation-deployment.mjs`. No un segundo layout.
- Hecho cuando: de un spec del store sale un SVG y un HTML autocontenido, y los nodos quedan en las mismas posiciones relativas que en la vista interactiva (una prueba que compare las dos).

Con G-A cambia la pregunta de la UI de specIR: cualquier interfaz puede incrustar el panel. Por eso las tareas U de IR siguen retenidas hasta que JP decida.
