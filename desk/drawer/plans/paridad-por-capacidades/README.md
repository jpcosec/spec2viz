# Plan: paridad de specIR por capacidades

Escrito el 2026-11-25. Es el contrato de specIR después de la corrección de rumbo de ese día.
Tareas, dependencias y decisiones en `dag.yaml`. El borrador de notación está en `specir-layers.yml`.

## Qué cambió

specIR reemplazó a spec2viz con la regla "la paridad se demuestra con sus pruebas". El resultado
fue paridad de código: unas 6.000 líneas portadas tal cual, con pruebas que comparan byte a byte
contra goldens de spec2viz `2de1056`.

JP lo corrigió el 2026-11-25:

- "Necesito que pueda hacer lo mismo, no que tenga la misma lógica."
- "El render principal de los diagramas es en los fierros de graph_ui"; HTML o SVG, solo en línea.
- "Pitéate todos los goldens de spec2viz... tenemos que cumplir con features, no código.
  Mantenerlos solo genera ruido."

## Qué es specIR ahora

- **Declara, no dibuja.** Un diagrama es un `SpecDoc` o `ViewDoc` del store con su notación; lo
  dibuja la vista de notación de graph_ui con lo que resuelve sldb.
- **Extrae del código** los nodos y relaciones entre capas (interfaz, API, backend, dominio, datos).
- **Los renderers de texto** (PlantUML, Mermaid, D2, Vega, BPMN XML) y la página del catálogo
  quedan como exportaciones.

El plan de qué tiene que entregar graph_ui está en
`UIs/graph_ui/desk/drawer/plans/fierros-hacia-afuera/`. Lo que hay que pedirle a sldb, en
`sldb/desk/drawer/plans/pedidos-de-specir-y-graph-ui/`.

## Las capacidades

Borrador, a aceptar por JP. En el store van como `AtomDoc` (una por capacidad), con un
`MaterializationContractDoc` hacia su prueba de aceptación, una `RuleDoc` que exige esa evidencia
y una `ViewDoc` que las lista. Sin modelos nuevos.

| # | Capacidad | Dónde se cumple | Estado |
|---|---|---|---|
| 1 | Ver cualquiera de los 8 tipos de diagrama del store, con su notación | graph_ui | cumplida en dibujo: 38 specs del corpus, sin avisos |
| 2 | Navegar el catálogo por categoría | graph_ui | cumplida si el catálogo se sincroniza con `vistas.yml` |
| 3 | Abrir un nodo y ver su documento, sus átomos y sus referencias | graph_ui | falta el panel de átomos |
| 4 | Anotar un diagrama o un nodo, guardado en el store | graph_ui | falta |
| 5 | Editar desde el diagrama | graph_ui | no existe; JP decidió que entra ahora |
| 6 | Incrustar un diagrama como SVG o HTML estático | graph_ui | en borrador (G-B) |
| 7 | Validar una spec y sincronizarla al store | sldb | cumplida |
| 8 | Exportar a PlantUML, Mermaid, D2 o BPMN XML | specIR | cumplida |

La matriz de 105 filas (`docs/spec2viz/matriz-de-cobertura.md`) y el acta de retiro quedan como
registro histórico.

## Trabajo de IR

| Tarea | Estado |
|---|---|
| Borrar los goldens de spec2viz y las pruebas que los leen; reescribir el guardrail de paridad | tarea en borrador. Destraba el integrate: 8 de sus fallos son de estas pruebas |
| Sembrar la notación de los tipos de specIR desde `specir.install` | sin tarea; el borrador está validado |
| Capacidades como datos del store, con su regla y su vista | sin tarea; espera que JP acepte la lista |
| Notaciones de ORCA e IFML sobre los tipos de specIR | sin tarea |
| `specir mcp` delega en `mcp_extension`; `cli.py` deja de importar `sldb.mcp` | tarea en borrador |
| Las pruebas encuentran el workspace por `SPECIR_WORKSPACE` | tarea en borrador |

### La notación de los tipos de specIR

`specir-layers.yml`: 11 glifos (uno por tipo de dominio) y 11 links (los 10 tipos de relación de
specIR más `references`). `sldb notations validate` lo acepta. Probado de punta a punta en el
servidor: con el blog de ejemplo extraído a un store, `POST /api/views/evaluate` de graph_ui
devuelve los nodos con su glifo y las aristas, sin error de notación.

Límites conocidos:

- **No se puede ver todavía.** La vista de notación de graph_ui solo lista `SpecDoc`. Depende de la
  tarea G-C de graph_ui.
- **No hay carriles por capa.** El layout `lanes` de graph_ui es el de secuencia, y los carriles de
  actividad salen de `data.partition`. El borrador usa grafo de izquierda a derecha.

### Estándares

Un estándar es una notación (`NotationDoc`, `GlyphDoc`, `LinkDoc`), no un modelo nuevo ni código.

- **UML** ya existe: 6 de las 8 notaciones builtin de sldb.
- **ORCA** (objetos, relaciones, CTAs, atributos) e **IFML** son dos notaciones más sobre los tipos
  de specIR. Al mapearlas aparecen huecos del modelo de specIR, que ninguna notación tapa:
  - ORCA: no hay atributos de entidad como nodos ni relaciones entre entidades.
  - IFML: no hay contenedor de vista (pantalla), flujo de navegación ni paso de parámetros.
- Para revisar un estándar faltan tres cosas en sldb (pedidos 9, 10 y 11 del plan de sldb).

## Decisiones

Tomadas por JP el 2026-11-25:

- Paridad por capacidades, no por código. Los goldens se borran.
- El guardrail `pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas` se reescribe.
- El mapeo de un estándar es dato del store.
- `full_conversation.md` se queda en el repo público.
- specIR se instala editable en el venv compartido de robocop2 (hecho).

Abiertas:

- **Aceptar la lista de capacidades.**
- **Dónde caen el panel de átomos, las anotaciones y el diccionario de controles**: en graph_ui o
  en specIR. Es parte de la frontera que JP quiere delimitar.

## Pendientes sueltos

| Pendiente | Dueño |
|---|---|
| El integrate de IR falla y `main` va adelante de GitHub sin pushear (71 commits el 2026-11-25). Causas: store de deskops ausente en la copia del integrate (18 errores), `cli.py` importa `sldb.mcp` (2 fallos), pruebas de goldens (8 fallos). Los 67 errores de `No module named 'specir'` deberían haberse ido con la instalación editable; sin verificar | despacho de robocop2 |
| Una prueba MCP falla si el despacho escribe en el store de IR mientras corre (`tests/test_mcp_extension.py:141`) | despacho de robocop2 |
| pron: qué se hace con él | JP; ver el plan de sldb |
| Las sesiones de Claude de robocop2 pierden el login; falta un token de larga duración (`claude setup-token`, lo corre JP) | JP |
| Las decisiones D3 a D10 quedaron firmadas como `disposed_by: IR`, no a nombre de JP | deskops |
| `IR/runs/coordinacion-johanes.md` en robocop2 es la bitácora de este día; no está commiteada | despacho de robocop2 |
