# IR13i — tester deskops-t-270be4709340 (intento 1)

- task: `task-ir13i-corregir-en-el-acta-el-estado-de-g5-y-la-fila-de-ir-tras-cerrar-la-federación-de-las-pruebas-m`
- role: tester; run_id `run-deskops-t-270be4709340`; contract_sha256 `cc20a0132dcfe7218c4a89a32d741ada2cf2d92407ac132f8fc89f2799a225f7`
- session: `scion://agent/deskops-t-270be4709340`; session_sha256: no disponible (sesión scion, sin archivo local)
- IR HEAD `d6a804f`. Disposiciones leídas: preflight-1 y bundle-1 (ambas accepted).
- Evidencia: `validation.log`, `suite.log` (+ `suite-start.txt`), `board.txt`, `task.txt`, `next.txt`, `graph.txt`, `git-status.txt`.

## Verificaciones

| # | Verificación | Resultado |
|---|---|---|
| 1 | `git merge-base --is-ancestor 4f1e108 HEAD` (y `b16aab7`) | PASS, rc 0 ambos |
| 1 | `421d6a27`, `74ffdb63` en deskops origin/main | PASS, rc 0; anteriores a b16aab7 (17:37 vs 19:15), así que «después de que deskops quitara su enlace» es cierto |
| 1 | Grep de ruta al store real (`WORKSPACE / "spec2viz"` / `../spec2viz`) en `git show HEAD:tests/conftest.py` y `HEAD:tests/test_mcp_extension.py` | PASS, rc 1 en los dos. `grep -nE spec2viz` solo muestra el nombre del enlace del store temporal, la ruta de fixtures de IR y el nombre de una prueba |
| 1 | `git diff --stat` fuera de desk/.sldb/runs = solo el acta | PASS con salvedad: aparecen además `tests/conftest.py` y `tests/test_mcp_extension.py`, cambios ajenos anunciados. Su diff es **idéntico** (sin líneas `index`) al de `runs/subagents/deskops-e-473333353dce/diff.patch`. `tests/fixtures/blog_app/` sin seguimiento (IR08). Nada más fuera de desk/.sldb/runs. Nota: preflight-1 suponía árbol limpio porque la tarea de la copia del store estaría cerrada; no lo está (sigue abierta, preflight-4 sin commitear) |
| 1 | `grep -n 'bloqueada' docs/spec2viz/acta-de-retiro.md` | PASS, rc 1 (sin coincidencias; tampoco «bloquead*») |
| 1 | `pytest tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py` | PASS, 11 passed, 1 xfailed, rc 0 |
| 1 | `deskops graph missing --root .` | PASS, rc 0 |
| 2 | Fila G5: federación resuelta con b16aab7/4f1e108; queda quitar el store del universo y archivarlo | PASS |
| 2 | Punto 2 (G5) de Lo que falta: mismo cambio | PASS |
| 2 | Fila de IR en Consumidores sin menciones a la federación, conserva oráculos y `test_matriz_cobertura_spec2viz.py:31` | PASS (también quita «y cambiar la federación por un fixture» del plan propio: correcto, ya hecho) |
| 2 | Punto 6 de Lo que falta (fuera de la lista literal del Scope) | PASS: cabe en el Goal (antes afirmaba que faltaba quitar la federación, ya no cierto) y lo que dice es cierto (b16aab7 la quitó; verificado arriba). Recomiendo aceptarlo |
| 2 | Nada falso | PASS: grep `federa\|conftest` en el acta solo deja menciones verdaderas (deskops federa sldb/pron/scion, comprobado: `../deskops/.sldb/core/store_index.yaml` solo nombra `system.spec2viz` en la línea 308; el `.sldb` de IR federa stores, sección de rendimiento, no tocada). No se tocaron matriz, recuento ni corridas |
| 2 | Diff del acta = `diff.patch` del ejecutor | PASS, idéntico |
| 3 | Fuera de desk/.sldb/runs solo cambia el acta (aparte de los ajenos) | PASS |
| 4 | Suite completa bajo lock (`-n 4`, mmdc real), 21:23–21:32 | **FAIL (ajeno a la tarea)**: 2 failed, 746 passed, 4 xfailed, rc 1 |

## Fallos de la suite (no los causa IR13i)

- `tests/visual/test_sync_generation_parity.py::test_a_component_spec_from_specir_python_ast_validates`
- `tests/visual/test_sync_generation_parity.py::test_python_ast_generation_of_specir_matches_spec2viz_up_to_the_declared_differences`

Ambos: `assert findings == []` con un hallazgo `component-spec/syntax-error` sobre
`visual/templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js`. Se reproduce aislado y de forma determinista
(`validation.log`): `component_spec_from_python` del sldb editable (`/mnt/ssd/proyectos/SLDB_1/sldb`, HEAD `502ef641`)
ahora recorre también ese `.js` vendorizado. Origen probable: sldb `600b51a9` (2026-11-16 18:25, «sldb.code lee el
frontend: TS, TSX, JS y JSX…», toca `sldb/code/files.py` y `scan.py`). Las suites de testers anteriores del mismo día
(hasta 18:38) tenían esos dos tests en verde. IR13i solo cambia un `.md`, y estos tests no usan las fixtures MCP de los
cambios ajenos de conftest. No es el fallo de concurrencia de `test_reading_through_every_tool_leaves_every_store_untouched`
(ese pasó), así que no reencolé.

## Comparación con el informe del ejecutor

Coincide en todo: rc de cada comando, diff del acta, cambios ajenos y salvedad del criterio `git diff --stat`, punto 6.
Diferencias: el ejecutor no corrió la suite completa; la mía muestra los 2 fallos de arriba, ajenos.

## Veredicto

**PASS** para IR13i: todas las verificaciones de la tarea pasan y el contenido del acta es cierto y está dentro del Goal
(punto 6 incluido). La suite completa no está verde por una regresión externa de sldb (600b51a9 lee el `.js` minificado
vendorizado en `component_spec_from_python`). Necesita una tarea o nota a sldb (o una exclusión de `vendor/` en IR) antes
de dar por buena la suite de IR; no bloquea el closeout de un cambio solo documental, pero lo decide el coordinador.
Pendiente de coordinador: integrar o retirar los cambios ajenos de conftest/test_mcp_extension para que el criterio
literal de `git diff --stat` se cumpla.
