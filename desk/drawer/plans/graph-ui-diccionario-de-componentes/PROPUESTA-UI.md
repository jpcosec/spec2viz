# Propuesta: una UI nueva para specIR

Respuesta a D1 (JP, 2026-11-24): no apuntar a los experimentos de graph_ui; proponer una UI nueva,
inspirada en la superficie de sldb, que como mínimo haga lo que hacía la UI del spec2viz antiguo, sin
copiarla. La maqueta está en `maqueta-ui.html` (estática, sin servidor; se abre con doble clic).

## La idea en una frase

Una app chica, propia de specIR, con el lenguaje visual del SLDB Workbench ("papel con fierros
ocultables"), que muestra tres cosas del mismo store: los diagramas, la cadena entre capas y el
diccionario de controles. Y que es, ella misma, la primera interfaz que el diccionario describe.

## Por qué resuelve D1

- Se escribe en React con TSX, que es lo único que el extractor ve hoy. Medido sobre
  `sldb/surface/src` (87 componentes): 226 controles, 153 acciones, 226 `triggers`, ningún nombre
  demasiado largo y 175 entradas no derivadas. Sobre el htm de mindmap salían 0 controles.
- Deja de hacer falta el soporte de `htm` en sldb (la tarea T3 del plan) y graph_ui sale del
  camino crítico.
- Cada control nace con rol, nombre accesible y `data-testid`, así que el localizador del
  diccionario está completo desde el primer día.

## Qué se toma de la superficie de sldb y qué no

Se toma:

- Los tokens y la tipografía de `sldb/surface/DESIGN.md`: papel `#FAF9F6`, piedra `#F4F3EF`, tinta
  negra, serif para títulos y citas, monoespaciada para etiquetas, bordes de 2 px, sin colores de
  semáforo.
- Las dos lentes: **Lectura** (limpia) y **Fierros** (identificadores, hashes, anclas, la operación
  que trajo el dato).
- La forma de pantalla: lista a la izquierda, lienzo al centro, inspector a la derecha que aparece
  al seleccionar.
- Sus reglas: la UI no calcula, toda escritura es una operación con nombre, sin datos inventados
  (sin servidor queda vacía y lo dice).
- Su contrato de capas de código (`core` sin React, vistas sin `fetch` directo).

No se toma: el árbol espacial, la edición de prosa, la extracción con anclaje y el estudio de
modelos. Son de sldb y ya existen ahí.

La superficie ya tiene un inspector de diagramas (`Spec2VizInspectorView.tsx`, 411 líneas, con
`NotationSvgCanvas.tsx`, que dibuja lo que entrega `GET /notations/view`). Es la base del Catálogo;
cómo se comparte es la decisión D7.

## Las vistas

### 1. Catálogo (el mínimo: lo que hacía spec2viz)

| Lo que hacía la página de spec2viz | Aquí |
|---|---|
| Barra lateral con categorías plegables y filtro | Riel izquierdo con las vistas por categoría y un filtro |
| Cobertura de átomos por diagrama | Contador `n/m` junto a cada vista: nodos con átomo que los justifica |
| Diagrama con arrastre, zoom y reinicio | Lienzo con zoom y ajuste; el dibujo sale de la notación resuelta por sldb |
| Globo al pasar sobre un nodo (título, extracto, insignias) | Igual, con procedencia en vez de insignias de color |
| Panel de átomos con pestañas (átomos, referencias, relaciones) | Inspector en una sola columna: descripción, átomos citados, referencias, relaciones |
| Anotaciones por vista, con explorador, exportar, importar y borrar | Notas al margen del diagrama, guardadas en el store; lista de notas en el riel |
| Diagramas BPMN de specs de actividad | El visor BPMN que specIR ya trae |

Dos cambios deliberados respecto de spec2viz:

- Las anotaciones dejan de vivir en `localStorage`: son documentos del store, con autor y fecha.
  Exportar e importar ya no hacen falta.
- La página deja de ser un HTML generado con todo adentro. Es una app contra `sldb serve`; el
  `specir catalog build` actual sigue existiendo como exportación.

### 2. Capas (lo que spec2viz no tenía)

Cinco columnas, una por capa de specIR: Interfaz, API, Backend, Dominio, Datos. Cada nodo es una
tarjeta. Al seleccionar uno:

- se marca su cadena a través de las columnas y el resto se atenúa;
- abajo aparece la cadena escrita, salto por salto, con el tipo de relación y cuántos saltos están
  verificados;
- el inspector muestra lo que no se sabe del nodo (`desconocidos`, con su razón) y lo que alcanza
  si cambia (`specir_impact`).

Las brechas (una regla de specIR que no se cumple) se ven como tarjetas punteadas en la columna
donde falta algo. La procedencia se lee en el trazo y en una etiqueta, no en el color: `observado`,
`derivado`, `inferido`, `declarado`; borde punteado para lo que no está verificado.

Aquí va la única escritura propia de la primera versión, y es útil de verdad: **verificar como
humano**. specIR prohíbe que un agente marque algo como `verificado`; hace falta una persona, y hoy
no tiene dónde hacerlo.

### 3. Diccionario

Una fila por control: tipo, componente con archivo y línea, evento y acción, operación de API,
localizador y pruebas que lo tocan. Filtros: sin prueba, sin localizador, sin operación, por vista.
El inspector da la línea lista para pegar en una prueba (`page.get_by_role("button", name=…)`) y
salta a la cadena en Capas.

### 4. Brechas (después)

La lista de lo que hoy solo sale por consola: reglas que fallan (`specir_rules`), lo que la última
extracción no pudo derivar, agrupado por causa, y las anclas que dejaron de estar intactas.

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

- Aceptación sobre stores reales: la cadena del blog (`tests/fixtures`) para Capas, y el store de
  IR, que tiene specs de diagramas, para el Catálogo.
- Pruebas de componentes con vitest y dos o tres flujos con Playwright en Chrome real.
- La UI se describe a sí misma: `specir ux extract` sobre su código y `specir ux coverage` contra
  sus pruebas, con la regla de que ningún control queda sin localizador.

## Tareas que agrega al DAG

| Id | Tarea | Horas | Depende de |
|---|---|---|---|
| U1 | Esqueleto de la app (Vite, TSX, tokens, cascarón con pestañas y lentes, cliente de `sldb serve`) | 2 | D7 |
| U2 | Catálogo: riel con filtro y cobertura | 1,5 | U1 |
| U3 | Catálogo: lienzo con zoom e inspector del nodo | 2 | U1, D7 |
| U4 | Catálogo: BPMN para specs de actividad | 1,5 | U3 |
| U5 | Notas al margen guardadas en el store | 2 | U3 |
| U6 | Capas: columnas, selección y cadena | 2 | U1, D8 |
| U7 | Capas: verificar como humano | 1,5 | U6 |
| U8 | Diccionario: tabla, filtros e inspector | 2 | U1, T8 |
| U9 | Brechas | 1,5 | U6, D8 |
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
- **D9. Qué pasa con la página generada.** Mantener `specir catalog build` como exportación o
  retirarla cuando el Catálogo tenga paridad. Recomiendo mantenerla hasta que U1 a U5 estén
  aceptadas y decidir entonces.
