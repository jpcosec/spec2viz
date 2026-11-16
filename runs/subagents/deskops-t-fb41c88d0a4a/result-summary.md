# IR13h — resultado del tester deskops-t-fb41c88d0a4a (intento 1)

- Tarea: `task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4`
- Rol: tester. Run id: `run-deskops-t-fb41c88d0a4a`. Contrato: sha256 `28509da07e3fb092fe84c5d16be68442226270fc226e177e71f8a2c37ace80a1` (preflight-2 y bundle-1 aceptadas).
- Sesión: `scion://agent/deskops-t-fb41c88d0a4a` (session_sha256 no disponible: sesión scion, sin archivo local).
- Evidencia: `validation.log`, `suite-1.log`, `board.txt`, `task.txt`, `next.txt`, `graph.txt`, `git-status.txt`.
- No implementé, no arreglé, no commiteé ni cerré nada.

## Verificaciones

| # | Verificación | Resultado |
|---|---|---|
| 1a | `git -C ../deskops fetch -q origin`; merge-base --is-ancestor de 2421ca29, 74ffdb63, b716bf85 (y 421d6a27, 42b752ea, ce66f69e, ee9bc3cd) contra origin/main | PASS, todos rc 0; origin/main = `ee9bc3cd` |
| 1b | `grep -n spec2viz ../deskops/.sldb/core/store_index.yaml` | PASS: única coincidencia línea 308 `- system.spec2viz`, etiqueta semántica del modelo `ViewDoc` de sldb. `stores:` de store_index y `links:` de store.yaml: solo sldb, pron, scion. En origin/main `.sldb/store.yaml` no tiene enlace a spec2viz |
| 1c | `specir retirement check` con las 5 rutas | PASS: rc 1 (esperado), 63 dependencias (sldb 1, IR 43, spec2viz/.sldb 19; deskops/graph_ui/pron 0), 9 filas no acreditadas = las 9 `abierta` de «Acreditación (IR13)» (A17, H01, K09, K16, K18, K21, K23, K26, K29) |
| 1d | pytest matriz + gate | PASS: 11 passed, 1 xfailed, rc 0 |
| 1e | `deskops graph missing --root .` | PASS: rc 0 |
| 2a | Fila deskops del acta: resuelto, 3 pares en origin, celda Dependencias con forma pron/graph_ui | PASS |
| 2b | G4 del acta, G4 de la matriz y Lo que falta punto 1 no nombran graph_ui/deskops/pron como pendientes | PASS |
| 2c | Bloque nuevo de la corrida con el formato del de IR13g | PASS (misma estructura: rc, recuentos, filas, tarea, HEADs, por repo, explicación de la variación) |
| 2d | Bloque «Salida del comprobador» = mi corrida línea a línea | PASS: `diff` de las 63 líneas rc 0 |
| 2e | Cifras y SHAs: IR `4f1e108`, sldb `12e9b191`, graph_ui `824c135` (39 rutas sin commitear), deskops HEAD `12c5c2ce` (9 por delante de origin/main `ee9bc3cd`), pron `39ea972`, spec2viz `91ba1d0` | PASS, coinciden todos |
| 2f | El acta no afirma nada falso | PASS en lo que cambia el diff; **discrepancia preexistente fuera del Scope** (abajo) |
| 3 | Fuera de desk/, .sldb/ y runs/ solo cambian los dos documentos | PASS (`git diff --stat` y untracked) |
| 4 | Suite completa bajo flock (free: 16 GB disponibles) | PASS: 747 passed, 4 xfailed, rc 0 (318 s; esperó el lock desde 19:38, terminó 20:05). Sin reencolar |

## Discrepancias

1. **Texto falso preexistente, fuera del Scope de IR13h:** la fila G5 del gate (acta línea 93) y el punto 2 de «Lo que falta» (líneas 203-207) dicen que `task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a` está «bloqueada» porque `deskops/.sldb` enlaza spec2viz. Ya no es cierto: esa tarea está cerrada en IR (`b16aab7`, closeout `4f1e108` = HEAD) y deskops quitó el enlace (`421d6a27`, que la propia fila nueva de deskops cita). También la fila IR de Consumidores (línea 106) sigue citando la federación de `spec2viz/.sldb` en `tests/conftest.py`, que cambió `b16aab7`. El Scope de IR13h no incluye esas filas; el ejecutor lo reportó igual. Requiere una tarea de seguimiento.
2. Observación menor: `../deskops/README.md:141-143` (origin/main) aún muestra `spec2viz validate/render` en prosa; no cuenta para el comprobador, y el acta solo afirma «quedan menciones en prosa», sin decir que sean exhaustivas.

## Comparación con el ejecutor (`runs/subagents/deskops-e-5d20e77cfc47/result-summary.md`)
Coincide en todo: comandos, rc, 63/9, SHAs, interpretación de la línea 308 y los pendientes fuera de alcance (G5/Lo que falta punto 2 desactualizados, fila IR, menciones en prosa, HEAD de deskops por delante de origin).

## Veredicto
**PASS**. El contrato de IR13h se cumple. Antes de declarar nada sobre G5, conviene una tarea de seguimiento para corregir la fila G5, el punto 2 de Lo que falta y la fila IR de Consumidores (discrepancia 1).
