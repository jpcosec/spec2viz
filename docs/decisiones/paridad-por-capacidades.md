# specIR cumple capacidades, no reproduce el código de spec2viz

> **Estado: DECIDIDO por JP el 2026-11-25.** Los goldens ya se borraron (`1fd427c`); el resto está
> sin ejecutar. Reemplaza la regla "la paridad con spec2viz se demuestra con sus pruebas".

## Contexto

specIR reemplazó a spec2viz el 2026-11-23 con una regla: la paridad se demuestra con sus pruebas.
El resultado fue paridad de código. Se portaron unas 6.000 líneas tal cual, con 12 renderers, y
las pruebas comparaban byte a byte contra salidas guardadas de spec2viz `2de1056`.

Esa mitad visual corría en paralelo a sldb y a graph_ui, que ya resuelven y dibujan lo mismo. Una
medición del 2026-11-25 lo confirmó: las 38 specs válidas del corpus de spec2viz, de sus 8 tipos de
diagrama, se dibujan en la vista de notación de graph_ui sin errores ni avisos.

## Decisión

- **Paridad por capacidades.** JP: "necesito que pueda hacer lo mismo, no que tenga la misma
  lógica". Cada capacidad se acredita con una prueba de aceptación de lo que hace, nunca con una
  salida idéntica.
- **Los goldens de spec2viz se borran**, y con ellos las pruebas que los leen. JP: "mantenerlos
  solo genera ruido".
- **specIR declara y extrae; no dibuja.** Un diagrama es un `SpecDoc` o un `ViewDoc` del store con
  su notación. Lo dibuja y lo edita graph_ui. HTML y SVG quedan solo para incrustar en línea.
- **specIR no tiene interfaz propia.** Lo que haya que ver de specIR se ve en los editores de
  texto y de grafo (ADR de sldb `surface-is-an-editor-contract.md`).
- **specIR es dueño del contenido de las notaciones** (UML, BPMN, ORCA, IFML, capas) y de las
  clases de spec; sldb conserva el mecanismo (ADR de sldb
  `mechanism-in-sldb-content-in-specir.md`).

## Las capacidades

| # | Capacidad | Dónde se cumple | Estado al 2026-11-25 |
|---|---|---|---|
| 1 | Ver cualquiera de los 8 tipos de diagrama del store, con su notación | editor de grafo | cumplida en dibujo |
| 2 | Navegar el catálogo por categoría | editor de grafo | cumplida si el catálogo se sincroniza |
| 3 | Abrir un nodo y ver su documento, sus átomos y sus referencias | editor de texto | falta |
| 4 | Anotar un diagrama o un nodo, guardado en el store | los dos editores | falta |
| 5 | Editar desde el diagrama | editor de grafo | falta |
| 6 | Incrustar un diagrama como SVG o HTML estático | editor de grafo | en curso |
| 7 | Validar una spec y sincronizarla al store | sldb | cumplida |
| 8 | Exportar a PlantUML, Mermaid, D2 o BPMN XML | specIR | cumplida |

JP no objetó la lista; tampoco la aceptó de forma expresa.

## Consecuencias

- Las tareas U2, U3, U4, U5 y U9 de la app `IR/ui/` quedan sin efecto, igual que las decisiones
  D1, D7 y D10 del plan del diccionario de componentes.
- `CatalogAnnotationsDoc` y la página HTML del catálogo se retiran cuando se cumplan las
  capacidades 1 a 4 y 6.
- `mcp_extension` de specIR pasa a montarse como servidor en el de sldb cuando su API esté sobre
  fastmcp (ADR de sldb `one-command-taxonomy-served-by-fastmcp.md`).
- Al mapear ORCA e IFML aparecen huecos del modelo de dominio de specIR que ninguna notación tapa:
  atributos de entidad y relaciones entre entidades (ORCA); contenedor de vista, flujo de
  navegación y paso de parámetros (IFML).
