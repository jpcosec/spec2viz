# Propuesta: una UI nueva para specIR

> **Estado al 2026-11-25:** esta propuesta queda como referencia de forma y estética. Su
> arquitectura (una app propia de specIR) está en revisión: el render principal de los diagramas
> es la vista de notación de graph_ui, y JP decidió esperar a su panel embebible. Ver el README
> de esta carpeta y `../paridad-por-capacidades/`.

Respuesta a D1 (JP, 2026-11-24): no apuntar a los experimentos de graph_ui; proponer una UI nueva,
inspirada en la superficie de sldb, que como mínimo haga lo que hacía la UI del spec2viz antiguo, sin
copiarla. La maqueta está en `maqueta-ui.html` (estática, sin servidor; se abre con doble clic).

## Decisión de forma (JP, 2026-11-25)

La estructura es la del prototipo web de Kimun (`jpcosec/kimun`, rama `prototype/kimun-web`,
carpeta `prototypes/kimun-web`), con la estética que ya tenemos: la del SLDB Workbench. La maqueta
es la versión 2 y reemplaza a la primera (Catálogo, Capas, Diccionario), que queda en el historial.

## La idea en una frase

El prototipo de Kimun, vestido de papel y con el contenido de specIR: un explorador a la izquierda,
tres pestañas (Grafo, Anclajes, Composiciones) y un panel de documento a la derecha.

## Qué se toma de cada lado

Del prototipo de Kimun, la estructura:

- Explorador con buscador (`Ctrl K`) y los documentos agrupados.
- **Grafo**: lienzo con tarjetas, botón de vecindad, zoom, y abajo la tira de conexiones del nodo.
- Panel derecho del nodo con pestañas Documento, Markdown e Historial.
- **Anchorings**: la fuente con números de línea y el fragmento resaltado; a la derecha el
  selector, la captura, su estado y qué lo usa.
- **Composiciones**: recetas, los bloques de cada receta con su estado, y la vista previa con
  "ver anclaje" en cada bloque.

Del SLDB Workbench, la estética y las reglas:

- Tokens de `sldb/surface/DESIGN.md`: papel `#FAF9F6`, piedra `#F4F3EF`, tinta negra, serif en
  títulos, monoespaciada en etiquetas, bordes de 2 px. Sin el morado ni los colores por tipo del
  prototipo: el tipo va escrito y la selección es tinta.
- Las lentes Lectura y Fierros.
- La UI no calcula, toda escritura es una operación con nombre, sin datos inventados.

## Cómo calza specIR en esa estructura

| Kimun | specIR |
|---|---|
| Explorador por carpetas | Explorador por capa: Interfaz, API, Backend, Dominio, Datos |
| Grafo de documentos y enlaces | Grafo del sistema: los nodos de specIR ordenados por capa, con sus relaciones |
| Vecindad | La cadena del nodo elegido (`specir_impact`); el resto se atenúa |
| Tipos por color | Procedencia por trazo y etiqueta: `declarado`, `observado`, `derivado`, `inferido`; punteado si no está verificado o si es una brecha |
| Panel Documento | El documento del nodo: descripción, lo que no se sabe, lo que alcanza si cambia |
| Guardar versión | Verificar como humano (specIR se lo prohíbe a los agentes y hoy no hay dónde hacerlo) |
| Anchorings sobre Markdown | Anclajes sobre código: el fact de sldb en que se apoya cada nodo, con estado vigente o cambiado |
| Composiciones que usan el anclaje | Nodos y relaciones que se apoyan en ese fragmento |
| Recetas | Los diagramas del catálogo (lo que hacía spec2viz) y el diccionario de controles |
| Bloques de la receta | Qué nodos y relaciones entran, con cuántos quedaron sin resolver |
| Vista previa | El diagrama dibujado con su notación, o la tabla del diccionario |

Dos cosas salen mejor que en la primera propuesta:

- El **diccionario** deja de ser una vista aparte: es una receta más. Sus huecos (sin operación,
  sin localizador, sin prueba) se leen como bloques sin resolver.
- Los **diagramas** de spec2viz también son recetas. La paridad con el catálogo viejo queda dentro
  de Composiciones: lista con cobertura de átomos, vista previa con zoom, nodo que abre su
  documento, BPMN y notas guardadas en el store en vez de `localStorage`.

Lo que hacía la página de spec2viz y dónde queda:

| spec2viz | Aquí |
|---|---|
| Barra lateral con categorías y filtro | Lista de recetas con filtro por capa y buscador |
| Cobertura de átomos por diagrama | El `n/m` de cada receta |
| Diagrama con arrastre, zoom y reinicio | Vista previa de la receta |
| Globo y panel de átomos del nodo | Panel de documento del nodo |
| Anotaciones con explorador, exportar e importar | Notas del store sobre la receta o el nodo |
| BPMN de specs de actividad | Receta con notación BPMN |

## Una diferencia de implementación con el prototipo

El prototipo de Kimun está escrito en JavaScript plano sobre el DOM (`addEventListener`,
`createElement`), con ProseMirror para el editor. El extractor de specIR no ve controles en ese
estilo: sobre el DOM directo de graph_ui salieron 0. Si esta UI va a ser la primera que el
diccionario describe, tiene que escribirse en React con TSX, tomando del prototipo la estructura y
no el código. Es la decisión D10.

## De dónde salen los datos

| Dato | Fuente | Estado |
|---|---|---|
| Documentos, relaciones, vistas | `sldb serve`: `/graph`, `/document`, `/views` | existe |
| Dibujo de un diagrama | `sldb serve`: `/notations/view` | existe |
| Camino entre dos nodos | `sldb serve`: rutas de `graph` (`path`, `neighborhood`) | existe; falta comprobar que alcanza para la cadena |
| Impacto, reglas, capas de un tipo | hoy solo por MCP (`specir_impact`, `specir_rules`, `specir_types`) | falta por HTTP |
| Diccionario y cobertura | no existe todavía (T8 y T9 del plan) | falta |
| Guardar una nota o una verificación | `sldb serve`: `POST /save` con `expected` | existe |

`sldb mcp` acepta `--extension MODULE:FUNCTION` y `sldb serve` no. Para que la UI no calcule, lo de
specIR tiene que llegar por HTTP: es la decisión D8.

## Cómo se prueba

- Aceptación sobre stores reales: la cadena del blog (`tests/fixtures`) para Grafo y Anclajes, y el
  store de IR, que tiene specs de diagramas, para Composiciones.
- Pruebas de componentes con vitest y dos o tres flujos con Playwright en Chrome real.
- La UI se describe a sí misma: `specir ux extract` sobre su código y `specir ux coverage` contra
  sus pruebas, con la regla de que ningún control queda sin localizador.

## Tareas que agrega al DAG

| Id | Tarea | Horas | Depende de |
|---|---|---|---|
| U1 | Esqueleto de la app (Vite, TSX, tokens, cascarón con pestañas y lentes, cliente de `sldb serve`) | 2 | D7 |
| U2 | Composiciones: lista de recetas de diagrama con cobertura | 1,5 | U1 |
| U3 | Composiciones: vista previa del diagrama con zoom y panel de documento del nodo | 2 | U1, D7 |
| U4 | Composiciones: BPMN para specs de actividad | 1,5 | U3 |
| U5 | Notas guardadas en el store | 2 | U3 |
| U6 | Grafo por capas, cadena del nodo y tira de conexiones | 2 | U1, D8 |
| U7 | Verificar como humano | 1,5 | U6 |
| U8 | Receta del diccionario: bloques y tabla | 2 | U1, T8 |
| U9 | Anclajes: fuente, selector, estado y nodos que se apoyan | 1,5 | U1 |
| U10 | La UI en su propio diccionario, con cobertura en sus pruebas | 1 | U8, T9 |

U1 a U5 son el mínimo pedido (paridad con spec2viz): unas 9 horas. El total es de 17 horas.

## Decisiones nuevas para JP

- **D7. Dónde vive y cómo comparte con la superficie.** (a) App propia en `IR/ui/`, que importa de
  `@sldb/surface` el cliente, el lienzo de notación y los estilos (hay que pedirle a sldb que los
  exporte); (b) vistas nuevas dentro de `sldb/surface`; (c) app propia que copia lo que necesita.
  Recomiendo (a): la superficie se declara general ("nada depende de un dominio") y las capas de
  specIR son un dominio; copiar el lienzo lo dejaría en dos lugares.
- **D8. Cómo llegan por HTTP los datos de specIR.** (a) Pedir a sldb que `sldb serve` acepte
  `--extension`, como ya hace `sldb mcp`; (b) un servidor propio de specIR. Recomiendo (a): es el
  mismo contrato que ya usa el MCP y no agrega un segundo proceso.
- **D10. En qué se escribe.** (a) React con TSX, tomando del prototipo de Kimun solo la estructura;
  (b) reutilizar el código del prototipo, en JavaScript sobre el DOM. Recomiendo (a): con (b) el
  extractor no ve ningún control y la UI no podría describirse a sí misma.
- **D9. Qué pasa con la página generada.** Mantener `specir catalog build` como exportación o
  retirarla cuando Composiciones tenga paridad. Recomiendo mantenerla hasta que U1 a U5 estén
  aceptadas y decidir entonces.
