# IR13g: resultado del tester deskops-t-e9062210030f (intento 1)

- Tarea: `task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee`.
- Rol: tester. Contrato sha256: `0fea76a0464bf82489830560da4b0b667a7da1c5dc27dae0a11f0feaa8d9cc93`. Es el mismo que el de preflight-2 y bundle-1, y los dos están aceptados.
- Run: `run-deskops-t-e9062210030f`.
  - Sesión: `scion://agent/deskops-t-e9062210030f`.
  - El session_sha256 no se puede calcular desde aquí, porque es una sesión de scion sin archivo local.
- No implementé nada, ni hice commit, `git add` o stash.
- Evidencia en este directorio:
  - `validation.log`, `retirement-check.txt` y `retirement-check-post-deskops.txt`;
  - `suite-1.log` y `suite-2.log`;
  - `board.txt`, `task.txt`, `next.txt`, `graph.txt` y `git-status.txt`.

## 1. Comandos de Validation e Implementation Path

| Verificación | Resultado | Estado |
|---|---|---|
| `git -C ../UIs/graph_ui merge-base --is-ancestor 79d63ee HEAD` | rc 0. HEAD `824c135`; `c9b09f7` también es ancestro (rc 0) | PASS |
| `git -C ../UIs/graph_ui grep -nE 'from spec2viz\|import spec2viz\|spec2viz>=' HEAD` | rc 0 con 43 coincidencias: 5 en `desk/` y 38 en `runs/`. Excluyendo `desk/` y `runs/`, rc 1 (ninguna). `pyproject.toml` y `.github/` no mencionan spec2viz | PASS |
| `pytest -q -rxX tests/visual/test_notations_parity.py` | rc 0: 88 passed y 1 xfailed. El único xfail es `test_invalid_notations_are_rejected[changes1-not a spec2viz diagram type]` (mindmap, SV-H01) | PASS |
| Las 13 pruebas de SV-H03 (`-k`: 10 de notation_view, 2 de view_contract_resolved y test_resolve_documents_is_public_and_filters_relations) | rc 0: 19 passed, 0 xfail | PASS |
| `timeout 300 .venv/bin/specir retirement check` con las 5 rutas | rc 1. 85 dependencias: IR 43, deskops 22, spec2viz/.sldb 19, sldb 1, graph_ui 0 y pron 0. 9 filas no acreditadas | PASS (rc 1 esperado; sin dependencias de graph_ui) |
| Filas no acreditadas frente a las abiertas en Acreditación (IR13) | Coinciden exactamente: SV-A17, H01, K09, K16, K18, K21, K23, K26 y K29 | PASS |
| `pytest tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py` | rc 0: 11 passed y 1 xfailed (el estricto del universo real) | PASS |
| `deskops graph missing --root .` | rc 0: «No missing graph references found.» | PASS |
| `git diff --stat` fuera de `desk/`, `.sldb/` y `runs/` | Cambian los 2 documentos y `tests/conftest.py` y `tests/test_mcp_extension.py`. Esos dos son ajenos: su diff es idéntico al de `runs/subagents/deskops-e-068628774e48/diff.patch` (sin diferencias) | PASS |

## 2. Diff de los documentos frente al Scope

| Punto | Resultado | Estado |
|---|---|---|
| SV-H03 pasa a cumplida | Antes, su única Falta era «Solo G4: graph_ui aún importa…». Sus pruebas pasan sin xfail (19 de 19) | PASS |
| SV-K22 pasa a cumplida | Antes, su Falta era «Depende de SV-H03 (…; falta solo G4 de graph_ui)» | PASS |
| SV-K18 sigue abierta | Su Falta queda «Depende de SV-K21 (SV-K19, SV-K20 y SV-K22 ya cumplidas)», coherente con SV-K21 abierta | PASS |
| Resumen | Mi recuento de la tabla Acreditación da 105 filas: 96 cumplidas y 9 abiertas. La matriz dice «96 cumplidas, 9 abiertas (tras IR13g)» y G1 del acta, «96 cumplidas y 9 abiertas» | PASS |
| Tabla principal | Las filas de SV-H03, K18 y K22 llevan la nota «IR13g: …». El inventario de consumidores no se tocó | PASS |
| Acta, fila de graph_ui | Resuelto con `79d63ee`, closeout `c9b09f7` y la nota `20261116-131509` (existe en `desk/inbox/`). Trae el pendiente de `ci.yml`: `--src` en las líneas 47 y 112, verificado en el HEAD de graph_ui | PASS |
| Acta, G4 y Lo que falta | G4 ya no nombra a graph_ui como pendiente: da el reparto deskops 22, sldb 1, IR 43 y spec2viz/.sldb 19, y graph_ui y pron como resueltos. En Lo que falta, el punto 1 no nombra a graph_ui y el punto 3 quita SV-H03 y SV-K22 | PASS |
| Acta, bloque nuevo de la corrida | Sigue el formato de IR13f: rc, dependencias, filas, task id, comando y `timeout 300`, HEADs y reparto por repo. Las 85 líneas de la salida del acta son idénticas a las de mi corrida (`diff` vacío) | PASS |
| SHAs anotados | Comprobados: sldb `b0e4f649`, graph_ui `824c135` (39 rutas sin commitear), deskops `aa25fdb0`, pron `39ea972` y spec2viz `91ba1d0`. El de IR, `3ec37f2`, es impreciso (ver discrepancias) | PASS con observación |

## 3. Superficie tocada
Fuera de `desk/`, `.sldb/` y `runs/`, la tarea solo cambia `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`. Los cambios de `tests/conftest.py` y `tests/test_mcp_extension.py` son ajenos y previos, y su diff es idéntico al patch de deskops-e-068628774e48. **PASS**

## 4. Suite completa bajo el lock
- **Intento 1** (17:34–17:42; free: 14 GB disponibles). Resultado: `1 failed, 746 passed, 4 xfailed`, rc 1.
  - Falló `tests/test_mcp_extension.py::test_reading_through_every_tool_leaves_every_store_untouched`, con «reading wrote to» sobre el store real de deskops (`deskops/.sldb`, `desk/`, `runs/`).
  - Causa: en esa ventana deskops hizo 5 commits (`421d6a27`, `74ffdb63`, `e4a98712`, `87d0a7d6` y `afc89576`, de 17:37:45 a 17:40:31). Los mtimes de `Board.yaml` (17:40:22) y `store.yaml` (17:40:57) caen dentro.
  - Reencolé una vez, como pide el brief.
- **Intento 2** (17:42:56–17:57:33): mismo resultado, `1 failed, 746 passed, 4 xfailed`, rc 1, y la misma prueba.
  - Las rutas que «cambiaron» son exactamente las del closeout de deskops `task-las-skills-y-el-script-de-diagramas-de-deskops-dejan-de-invocar-spec2viz-y-usan-specir-ir13`: el TaskDocsDoc, su modelo, `store_index.yaml` y la tarea.
  - Sus commits (`ce66f69e`, `2421ca29` y `ee9bc3cd`) son de 17:54–17:55, dentro de la ventana.
- **Conclusión:** las dos veces el fallo viene de escrituras de otro agente en el store real de deskops. La tarea no lo causa, porque solo toca dos `.md` de docs.
  - El resto de la suite pasa: 746 passed, y los 4 xfail son los conocidos.
  - **No hay una corrida de la suite completamente verde.** Ya hice el único reencolado que pedía el brief, así que no lancé un tercer intento.
  - **Estado: PASS condicionado.** El único fallo es ajeno y está verificado con commits y mtimes; queda que el coordinador lo acepte o pida otra corrida en un momento sin actividad de deskops.

## Discrepancias y observaciones
1. **(Menor) HEAD de IR en el bloque de IR13g.** El acta y la matriz anotan IR `3ec37f2`, pero el `retirement-check.txt` final del ejecutor es de las 17:28:37, posterior al commit `0431626` (17:27:53).
   - `0431626` solo toca `desk/`, `.sldb/` y `runs/` (IR08/IR09) y no cambia la salida del comprobador, porque las 43 dependencias de IR están en `tests/`.
   - Si se quiere exactitud, el HEAD de la corrida es `0431626`.
   - No cambia ninguna cifra.
2. **(Informativo, posterior a la tarea) deskops ya no tiene dependencias.** Tras sus commits de las 17:37–17:55 (HEAD `ee9bc3cd`), una corrida nueva da rc 1, **63 dependencias** (IR 43, spec2viz/.sldb 19, sldb 1, deskops 0) y las mismas 9 filas (`retirement-check-post-deskops.txt`).
   - El bloque de IR13g sigue siendo cierto, porque fija deskops en `aa25fdb0`.
   - La fila de deskops y G4 del acta quedarán desactualizadas cuando deskops avise. Es tarea aparte, fuera de este Scope.
3. **Pendiente que ya señaló el ejecutor.** La línea de G4 en el checklist de gates de la matriz todavía nombra a graph_ui y pron. El Scope solo pedía G1 y G2, así que no es un incumplimiento.

## Contraste con el ejecutor (deskops-e-be491a5e3b00)
- Coincide en todo lo que verifiqué:
  - rc y cifras: 85, 9 y 96/9, y el reparto por repo;
  - las 9 filas, 88 passed y 1 xfailed, y los 19 casos de SV-H03 sin xfail;
  - HEADs de sldb, graph_ui, deskops, pron y spec2viz, y las 39 rutas sin commitear de graph_ui;
  - las líneas de `ci.yml` 47 y 112;
  - las pruebas de matriz y gate (11 passed y 1 xfailed) y graph missing rc 0.
- Solo difiere en el matiz del HEAD de IR (observación 1).

## Corrida 3 (pedida por el coordinador)

La lancé con el mismo comando y bajo el lock. Antes de lanzarla había 9 GB disponibles.

- **Ventana.** Lancé el comando a las 18:01:15 y terminó a las 18:38:59; casi todo ese tiempo fue espera del lock. Pytest tardó 461 s, así que corrió aproximadamente de 18:31:18 a 18:38:59.
- **`git -C ../deskops log -1` antes:** `ee9bc3cd`, de las 17:55:18.
- **`git -C ../deskops log -1` después:** `7801327f`, de las 18:24:21. Entre medio entraron 3 commits (`f3282fd2`, `8583ea84` y `7801327f`, de 18:23 a 18:24), todos antes de que arrancara pytest.
- **Resultado: `1 failed, 746 passed, 4 xfailed`, rc 1. No es verde.**
- **Prueba fallida:** la misma de las corridas 1 y 2, `tests/test_mcp_extension.py::test_reading_through_every_tool_leaves_every_store_untouched` («reading wrote to»).
- **Qué cambió.** Las 10 rutas que la prueba detectó son escrituras **sin commitear** de deskops entre 18:32:42 y 18:35:14, dentro de la ventana de pytest. Corresponden a una tarea nueva, `task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb`, con su preflight-1 y su bundle-1. Además cambiaron `Board.yaml`, `Board.md`, los modelos TaskCodeDoc, BoardDoc y ReviewDoc, `store.yaml` y `store_index.yaml`.
  - deskops siguió activo aunque había cerrado sus tareas de IR13.
  - Sus escrituras todavía no tienen commit, así que `git log -1` no las refleja; sí aparecen en `git -C ../deskops status`, en los mtimes y en `run-deskops-e-d62639bcf100`.
- **Conclusión.** La causa es la misma que en las corridas 1 y 2: un agente de deskops escribe en su store real mientras corre la prueba. Fuera de esa prueba, todo pasa en las tres corridas: 746 passed y los mismos 4 xfail.
- **Sigue sin haber una corrida verde.** Para conseguirla hay que correr la suite con deskops en reposo, es decir, con su agente activo (`deskops-e-d62639bcf100`) parado o terminado. La alternativa es que la prueba digiera una copia en lugar del store real, pero eso es otra tarea, porque además `tests/test_mcp_extension.py` tiene cambios ajenos sin commitear.
- Evidencia: `suite-3.log`, `suite-3-times.txt`, `suite-3-deskops.txt`, `suite-3-changed.txt` y `validation.log` (sección «Corrida 3»).

## Veredicto
**PASS.**
- Todas las verificaciones de contenido y de Validation pasan, y ninguna afirmación de los documentos es falsa.
- La única nota es la imprecisión menor del HEAD de IR, que no cambia ninguna cifra.
- La suite completa no tiene ninguna corrida verde: las tres dan 746 passed, 1 failed y 4 xfailed. El fallo es siempre la misma prueba de digest «untouched», por escrituras concurrentes de deskops en su store real. Lo verifiqué con commits y mtimes en las corridas 1 y 2, y con mtimes y `git status` en la 3. No lo causa la tarea.
- Antes del closeout no hace falta nada de la tarea. Opcionalmente, el coordinador puede corregir `3ec37f2` a `0431626` o repetir la suite en un momento sin actividad de deskops.
