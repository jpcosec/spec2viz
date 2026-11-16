# IR13h — resultado del ejecutor deskops-e-5d20e77cfc47 (intento 1)

Solo se tocaron `docs/spec2viz/acta-de-retiro.md` y `docs/spec2viz/matriz-de-cobertura.md` (sin commit). Evidencia: `validation.log`, `check.out`/`check.err` (salida completa del comprobador), `diff.patch` y `git-status.txt`.

## Cambios en el acta
- **Fila de deskops** (Consumidores): la celda Dependencias sigue la forma de pron/graph_ui (22 históricas, corrida del 2026-11-15, «0 desde la del 2026-11-16 de IR13h», HEAD `12c5c2ce`, origin/main `ee9bc3cd`). «Cambio que lo resolvió» pasa a **resuelto**, con los tres pares en origin: `421d6a27`/closeout `74ffdb63` (enlace al store de spec2viz), `42b752ea`/`b716bf85` (regla de `desk_graph.py:75`), `ce66f69e`/`2421ca29` (skills y `render_diagram.py`), y cómo se comprobó desde IR.
- **G4** (tabla del gate): 63 dependencias según la corrida de IR13h: sldb 1 (`gen_golden.py:5`), IR 43 (oráculos de paridad) y `spec2viz/.sldb` 19 (G5). graph_ui, pron y deskops figuran como resueltos.
- **Lo que falta, punto 1**: queda sldb; lo demás de G4 es de IR (punto 6) y G5 (punto 2). deskops figura como resuelto.
- **Bloque nuevo de la corrida** (con el formato del de IR13g), fechado el 2026-11-16 a las 19:33 -03:00.
- Además, para que el acta no se contradiga con la corrida nueva: la frase inicial pasa de 85 a 63 dependencias (IR13h), y el bloque «Salida del comprobador» se reemplaza por las 63 líneas de la corrida nueva. Se quitan las 22 líneas de deskops y el resto queda idéntico.

## Cambios en la matriz
- Solo la línea «Estado IR13» de G4: 63 dependencias (sldb 1, IR 43, `spec2viz/.sldb` 19). graph_ui, deskops y pron salen con 0. Las filas y el resumen no cambian.

## Corrida del comprobador
`timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb`, hecha el 2026-11-16 a las 19:33 -03:00: **rc 1**, 63 dependencias, 9 filas no acreditadas.
- Dependencias por repo: IR 43, sldb 1, spec2viz/.sldb 19; deskops 0, graph_ui 0, pron 0.
- Filas no acreditadas: SV-A17, H01, K09, K16, K18, K21, K23, K26, K29. Son las mismas 9 que figuran como `abierta` en «Acreditación (IR13)» de la matriz.
- HEADs: IR `4f1e108`, sldb `12e9b191`, graph_ui `824c135` (39 rutas sin commitear), deskops `12c5c2ce` (origin/main `ee9bc3cd`, después de `git fetch`), pron `39ea972`, spec2viz `91ba1d0`.

## Verificaciones (todas en validation.log)
- `merge-base --is-ancestor` contra `origin/main` de deskops: 2421ca29, 74ffdb63, b716bf85 (y 421d6a27, 42b752ea, ce66f69e) dan rc 0.
- `grep -n spec2viz ../deskops/.sldb/core/store_index.yaml` da una sola coincidencia: la línea 308, `- system.spec2viz`. Es una etiqueta semántica del modelo `ViewDoc` de sldb (`sldb.models.notation_models:ViewDoc`), **no un enlace de store**. Los `stores:` federados son solo sldb, pron y scion. Lo interpreté como «sin enlace de store a spec2viz». Si el coordinador lo lee distinto, la fila no debería quedar como resuelta.
- `git diff --stat` fuera de desk/, .sldb/ y runs/ muestra solo los dos documentos.
- `pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py`: 11 passed, 1 xfailed (el xfail estricto del universo real), rc 0.
- `deskops graph missing --root .`: «No missing graph references found», rc 0.

## Pendiente (fuera de alcance)
- En deskops quedan menciones en prosa a spec2viz (la remisión de `.opencode/skills/use-spec2viz/SKILL.md`, `references/vocabulary.md`). No cuentan para el comprobador.
- El HEAD local de deskops (`12c5c2ce`) va por delante de origin/main (`ee9bc3cd`); el comprobador lee su árbol de trabajo.
- La fila G5 y el punto 2 de Lo que falta siguen diciendo que `task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a` está bloqueada. En IR ya está cerrada (`b16aab7`, closeout `4f1e108`). Hay que actualizarlo en otra tarea.
- La fila de IR en Consumidores sigue mencionando la federación de `spec2viz/.sldb` en `tests/conftest.py`. Lo cambió `b16aab7` y no se tocó aquí.
- Commit y cierre de la tarea: los hace el coordinador.
