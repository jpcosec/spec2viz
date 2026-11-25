# Plan: graph_ui como diccionario de componentes para probar UIs con specIR

Plan de la tarea `task-plan-probar-uis-con-graph-ui-como-diccionario-de-componentes-y-una-forma-comoda-de-usar-specir-ahi`.
Solo plan: no hay código. El DAG en forma de datos está en `dag.yaml`.

Medido el 2026-11-24 sobre graph_ui `36adfbb`, IR `f455b32` y sldb `61c5847f`.

## Decisiones tomadas

- **D1 (JP, 2026-11-24):** el objetivo no es mindmap ni las apps TSX de graph_ui, sino una UI nueva
  de specIR inspirada en la superficie de sldb, con paridad mínima con la UI del spec2viz antiguo.
  El 2026-11-25 JP fijó la forma: la estructura del prototipo web de Kimun con la estética del
  Workbench. La propuesta está en `PROPUESTA-UI.md` y la maqueta en `maqueta-ui.html`. Con esto T3 (soporte de
  `htm` en sldb) y T11 (registro de vistas de mindmap) salen del plan, y graph_ui queda como medición.
- **D2 (JP, 2026-11-24):** aprobada la tabla de rutas declarada en YAML para las operaciones de API
  de un backend que no es DRF.

## Lo que hay que saber antes de leer el resto

1. **El extractor de specIR hoy no ve la UI activa de graph_ui.** La UI activa es `frontends/mindmap`,
   escrita con plantillas `htm` en `.js` plano. Los facts de sldb no dan ahí ningún `component` ni
   `handlers`, así que specIR saca 0 controles. Lo que sí ve son las dos apps TSX
   (`apps/review-workbench`, `apps/knowledge-workbench`), y graph_ui declara retirada a
   `review-workbench`.
2. **Sobre las apps TSX el extractor falla al escribir.** Calcula el plan (133 controles, 88 acciones,
   133 `triggers`) pero `extract_frontend` aborta con `OSError: File name too long` y no escribe nada.
3. **No sale ningún `invokes`.** No hay operaciones de API en el store (el backend es `http.server`,
   no Django/DRF) y las llamadas HTTP pasan por `fetch` o por envoltorios propios.
4. **Al nodo de control le falta el localizador.** `InterfaceControlDoc` tiene `kind` y `component`,
   pero no cómo encontrar el control en la página, que es lo que una prueba necesita.

Por eso el diccionario no se puede "generar y usar" todavía: hay cuatro huecos que cerrar, dos de
ellos en sldb.

## 1. Inventario de graph_ui

| Carpeta | Estado | Cómo está escrita | Componentes que ve sldb | Backend |
|---|---|---|---|---|
| `frontends/mindmap` | activa | React 18 + `htm` en `.js`, sin bundler ni JSX (36 `.js`, 23 `.mjs`) | 0 (unos 60 componentes reales) | `serve.py`, `http.server`, puerto 8088 |
| `frontends/desk` | en uso (UI del desk) | DOM directo: `h(tag, attrs)` y `addEventListener` | 0 | `serve.py`, `http.server` |
| `frontends/workspace` | en uso, duplicada en mindmap | DOM directo: `innerHTML` y `addEventListener` | 0 | `serve.py`, `http.server`, puerto 8090 |
| `frontends/flow_editor` | retirada | `htm` y scripts clásicos | 0 | no tiene en este repo |
| `apps/review-workbench` | retirada | TSX real, Vite, shadcn (46 `.tsx`, 56 `.ts`) | 104 | proxy a 8088 y a `sldb serve` |
| `apps/knowledge-workbench` | sin declarar | TSX real, Vite, shadcn (25 `.tsx`, 11 `.ts`) | 79 | `/sldb` y un cliente mock |

Catálogos que ya existen:

- `frontends/mindmap/shell/registry.js:15` lista las 7 vistas (`{id, facet, label, component}`); la
  ruta es `/${facet}/${id}`. Es un catálogo de vistas, no de controles.
- `apps/*/src/components/ui/` tiene los 17 primitivos shadcn. No hay Storybook.
- `docs/representacion/propuesta-vocabulario-visual.md:84-150` propone `GestureDoc` (gesto a verbo),
  que es vecino del par control y acción; conviene no duplicarlo.

Localizadores en el código (ocurrencias):

| Carpeta | `data-testid` | `aria-label` | `role=` |
|---|---|---|---|
| `frontends/mindmap` | 71 (solo en las vistas workspace y explorer) | 81 | 72 |
| `frontends/desk` | 39 | 11 | 1 |
| `frontends/workspace` | 0 | 1 | 6 |
| `apps/review-workbench` | 92 | 29 | 0 |
| `apps/knowledge-workbench` | 2 | 0 | 1 |

Lo que ya se prueba:

- `tests/e2e_*.py` (24 archivos): Playwright en Python contra `serve.py` y un store temporal real.
  Localizan por clase CSS y por nombre accesible en español (`locator(` 553 veces, `get_by_role` 67,
  `get_by_test_id` 38).
- `tests/*.test.mjs` (16 archivos): pruebas unitarias de la lógica `.mjs`, sin interfaz.
- `auto_user_test/` en la raíz **no tiene flujos**: son salidas viejas (capturas, HTML, `report.json`)
  de dos corridas de agosto contra `review-workbench`, y el flujo que las generó no está en el repo.
  El corredor sí existe: `apps/review-workbench/scripts/run-user-flow.mjs`, Playwright sobre un JSON
  `{name, baseUrl, steps:[{id, action, selector, value}]}`, con tres flujos en `user_flows/`.

Endpoints: todos con `if/elif` escritos a mano en `http.server`; no hay tabla de rutas ni OpenAPI.
mindmap usa un solo envoltorio, `request(path, init)` (`shell/api.js:4`); desk usa `getJSON` y
`postJSON`; workspace usa `fetchJson`.

## 2. Resultado real del extractor sobre graph_ui

Copia de los archivos versionados de `frontends/`, `apps/` y `src/` (326 archivos) en un directorio
temporal, con un store nuevo y specIR instalado.

| Paso | Resultado |
|---|---|
| `code_facts` sin `tree-sitter-typescript` | 206 archivos TS/JS en `skipped`, 0 facts de frontend, sin error |
| `code_facts` con la gramática | 935 facts de frontend: 399 funciones, 183 componentes, 130 tipos, 17 hooks |
| `extract` (backend) | 0 nodos creados, 0 no derivados |
| `interpret_frontend` (el plan, en memoria) | 133 `InterfaceControlDoc`, 88 `InterfaceActionDoc`, 133 `triggers`, 0 `invokes` |
| `extract_frontend` (escribir) | aborta: `OSError: [Errno 36] File name too long` |

Detalle del plan en memoria:

- Los 183 componentes son todos de `apps/`. 30 tienen handlers (135 en total): 22 en
  `review-workbench` (103 handlers) y 8 en `knowledge-workbench` (32).
- Controles por tipo: `Button` 30, `button` 25, `Input` 18, `div` 14, `ContextMenuItem` 8. Acciones
  por evento: click 45, change 17.
- 135 handlers dan 133 controles; no investigué los 2 que faltan.
- 109 entradas no derivadas: 84 por "el componente tiene más de un handler; no se sabe qué llamadas
  son suyas", 21 por "ninguna función con ese nombre" (hooks y funciones importadas), 4 por "más de
  una función".
- El nombre de la acción de un handler en línea es el de su primera llamada:
  `onClick={() => useSource(s)}` queda como acción `useSource`.
- 21 de las 133 relaciones tienen un nombre de más de 250 bytes (máximo 266). `edge_name`
  (`src/specir/extract/plan.py:65`) concatena los nombres de origen y destino, que ya llevan la ruta
  completa del componente.

Llamadas HTTP que los facts sí muestran en `frontends/` (nombre del envoltorio y si el primer
argumento es un literal que empieza con `/`):

| Frontend | Envoltorio | Con ruta literal | Sin ruta literal |
|---|---|---|---|
| mindmap | `request` | 11 | 8 |
| desk | `getJSON`, `postJSON` | 1 | 4 |
| workspace | `fetchJson` | 2 | 1 |
| flow_editor | `fetch` | 8 | 2 |

El método no está en ninguna: va en el segundo argumento (`{method:'POST'}`) y los facts solo dan el
primero.

## 3. Qué es el diccionario

Una entrada por control, leída del store, no un formato nuevo:

| Campo | De dónde sale | Estado hoy |
|---|---|---|
| componente y archivo:línea | `InterfaceControlDoc.component` y su ancla | existe |
| tipo de control | `InterfaceControlDoc.kind` | existe |
| evento y acción | `triggers` hacia `InterfaceActionDoc` | existe |
| operación de API | `invokes` hacia `ApiOperationDoc` | el tipo existe; en graph_ui sale vacío |
| vista o ruta donde aparece | el registro de vistas de mindmap | falta |
| localizador (`data-testid`, rol, nombre accesible) | atributos estáticos del elemento | falta en los facts y en el modelo |
| procedencia | `origen`, `verificacion` | existe |

El diccionario es entonces una proyección: `InterfaceControlDoc` más sus dos saltos, agrupada por
componente y por vista. Vive en el store del proyecto que se prueba (ver D5).

## 4. Cómo se genera

Con el extractor de frontend de specIR sobre graph_ui, una vez cerrados estos huecos:

| Hueco | De quién es | Tarea |
|---|---|---|
| Nombres de relación de más de 255 bytes | specIR | T1 |
| No hay comando: solo `specir.extract.extract_frontend` en Python | specIR | T2 |
| La gramática ausente se salta en silencio | specIR avisa; la lista `skipped` ya la da sldb | T2 |
| Componentes y handlers en plantillas `htm` | sldb (specIR lee facts, no código) | T3 |
| Atributos estáticos del elemento con handler | sldb | T4 |
| Qué llamadas son de cada handler en línea | sldb | T4 |
| Método de la llamada en el segundo argumento | sldb | T4 |
| Campo de localizador en `InterfaceControlDoc` | specIR | T5 |
| Envoltorios HTTP propios (`request`, `getJSON`) | specIR, como configuración de la regla | T6 |
| Operaciones de API de un backend que no es DRF | specIR | T7, según D2 |

`frontends/desk` y `frontends/workspace` (DOM directo) quedan fuera de este plan: no tienen
componentes que nombrar y pedirían otra regla distinta.

## 5. Cómo se usa para probar UIs

Tres usos, del más barato al más caro. El primero no ejecuta nada y es el que propongo hacer.

1. **Cobertura** (T9). Cruza los localizadores del diccionario con los que usan `tests/e2e_*.py` y
   lista los controles que ninguna prueba toca, por vista. Sirve desde el primer día y no cambia
   las pruebas de graph_ui.
2. **Controles esperados** (después, según D4). Por cada vista, una prueba generada que abre la ruta
   y comprueba que los controles del diccionario existen. Detecta controles que desaparecen.
3. **Esqueletos de flujo** (después, según D4). De la cadena control, acción y operación, un flujo en
   el formato JSON de `run-user-flow.mjs`, para que una persona o un agente lo complete.

Además, sin trabajo nuevo: cuando un ancla de un componente deja de estar `intact`, `specir_impact`
ya dice qué controles y operaciones toca; con el cruce de T9 dice también qué pruebas revisar.

## 6. Ergonomía

Un grupo nuevo en el comando, propio de specIR (no envuelve nada de sldb):

```bash
specir ux extract <raíz> [--store <ruta>] [--paths frontends/mindmap] [--json]
specir ux dictionary [--store <ruta>] [--component X] [--view Y] [--format md|json]
specir ux coverage --tests <carpeta> [--store <ruta>] [--format md|json]
```

- `extract` corre el backend y el frontend, imprime creados, cambiados y no derivados agrupados por
  causa, y termina con error si sldb saltó archivos por falta de gramática.
- `dictionary` no escribe: proyecta el store.
- `coverage` no ejecuta pruebas: lee sus localizadores.

Y una tool MCP de solo lectura, `specir_controls`, con los mismos filtros que `dictionary`, para que
un agente que escribe una prueba pregunte "qué controles tiene esta vista y cómo se localizan".

## 7. DAG de tareas

Cada tarea cabe en menos de 2 horas con sus pruebas. Las de sldb y graph_ui son notas a su inbox; el
trabajo lo hace su desk.

| Id | Tarea | Repo | Horas | Depende de |
|---|---|---|---|---|
| T1 | Nombres de relación acotados (resumen con hash cuando pasan de un largo), con prueba de una ruta profunda | IR | 1 | |
| T2 | `specir ux extract`, con aviso de archivos saltados | IR | 1,5 | T1 |
| T3 | Nota a sldb: facts de `component` y `handlers` en plantillas `htm` | sldb (nota) | 0,3 | D1 |
| T4 | Nota a sldb: atributos estáticos del elemento, llamadas por handler y método del segundo argumento | sldb (nota) | 0,3 | |
| T5 | Localizador en `InterfaceControlDoc` y el extractor lo llena | IR | 1,5 | T4 hecho en sldb, D3 |
| T6 | Envoltorios HTTP configurables en la regla de `invokes` | IR | 1,5 | T4 hecho en sldb |
| T7 | Operaciones de API de graph_ui en el store | IR | 1,5 | D2 |
| T8 | `specir ux dictionary` (md y json) | IR | 1,5 | T2, T5 |
| T9 | `specir ux coverage` contra `tests/e2e_*.py` | IR | 2 | T8 |
| T10 | Tool MCP `specir_controls` | IR | 1 | T5 |
| T11 | Vista de cada control, leída del registro de vistas de mindmap | IR | 1,5 | T3 hecho en sldb, T8 |
| T12 | Sección del diccionario en `skills/use-specir/SKILL.md` | IR | 0,5 | T8, T9 |
| T13 | Nota a graph_ui: instalar specIR en su store y correr la cobertura en su CI | graph_ui (nota) | 0,3 | T9, D5 |

Orden: T1 y T4 primero y en paralelo (no se tocan). T1, T2 y T7 dan ya un diccionario de las apps
TSX sin localizador, que sirve para probar el camino completo. T3 y T4 son la ruta crítica: sin ellas
no hay diccionario de mindmap ni localizadores.

Total en IR: unas 13,5 horas. Lo de sldb no está estimado aquí.

## 8. Decisiones abiertas para JP

Cada una se crea como `task.decision` al promover este plan.

- **D1. Qué interfaz es el objetivo.** (a) mindmap, la activa, que exige soporte de `htm` en sldb;
  (b) las apps TSX, que funcionan con T1 pero están retiradas o sin declarar. Recomiendo (a) como
  objetivo y usar las apps TSX solo como banco de prueba mientras llega T3.
- **D2. De dónde salen las operaciones de API de un backend que no es DRF.** (a) una tabla de rutas
  declarada en YAML, que entra como `declarado`; (b) una regla nueva que lea el `if/elif` de
  `http.server`. Recomiendo (a): la regla de (b) serviría solo para graph_ui.
- **D3. Cuál es el localizador.** (a) rol y nombre accesible, con `data-testid` cuando exista;
  (b) pedir a graph_ui `data-testid` en todos los controles. Recomiendo (a): mindmap ya tiene 81
  `aria-label` y sus pruebas localizan así.
- **D4. Hasta dónde llega el uso en pruebas.** Solo cobertura (T9), o también controles esperados y
  esqueletos de flujo. Recomiendo parar en cobertura y decidir el resto con el informe en la mano.
- **D5. Dónde vive el diccionario.** (a) en el store de graph_ui, con specIR instalado ahí; (b) en
  un store aparte de IR. Recomiendo (a): las anclas quedan junto al código que describen.
- **D6. Qué se hace con `auto_user_test/`.** Son salidas viejas de la app retirada. Borrarlas o
  dejarlas es de graph_ui; lo que importa aquí es si el formato JSON de `run-user-flow.mjs` se
  reutiliza para mindmap (solo aplica si D4 llega a esqueletos de flujo).

## 9. Cómo reproducir la medición

```bash
W=$(mktemp -d)
cd UIs/graph_ui && git ls-files frontends apps src | rsync -a --files-from=- . $W/graph_ui/
pip install --target $W/pydeps "tree-sitter-typescript>=0.23"
export PYTHONPATH=<IR>/src:$W/pydeps
sldb stores init --path $W/graph_ui
python -m specir.install --store $W/graph_ui/.sldb
python -c "from specir.extract import extract, extract_frontend as f; r='$W/graph_ui'; print(extract(r)); print(f(r))"
```

La última línea termina en el `OSError` del punto 2. El plan en memoria sale de
`specir.extract.react_tsx.interpret_frontend(Facts(code_facts(raíz)["facts"]), [])`.
