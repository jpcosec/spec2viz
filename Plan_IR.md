Lo estructuraría como un DAG de capacidades, no como fases secuenciales. Las ramas de metamodelos, API/MCP y extracción pueden avanzar en paralelo.

El objetivo es construir un sistema de ingeniería de software asistida por agentes, basado en SLDB y spec2viz, que aproveche estándares OMG para conectar UX, backend, operaciones y datos mediante un grafo semántico tipado.

## 1. DAG de desarrollo

\#chatgpt-mermaid-\_r_2ur\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_2ur\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_2ur\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_2ur\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_2ur\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2ur\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_2ur\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_2ur\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_2ur\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_2ur\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_2ur\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_2ur\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2ur\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2ur\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_2ur\_ p{margin:0;}#chatgpt-mermaid-\_r_2ur\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2ur\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2ur\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2ur\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_2ur\_ .label text,#chatgpt-mermaid-\_r_2ur\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2ur\_ .node rect,#chatgpt-mermaid-\_r_2ur\_ .node circle,#chatgpt-mermaid-\_r_2ur\_ .node ellipse,#chatgpt-mermaid-\_r_2ur\_ .node polygon,#chatgpt-mermaid-\_r_2ur\_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_2ur\_ .rough-node .label text,#chatgpt-mermaid-\_r_2ur\_ .node .label text,#chatgpt-mermaid-\_r_2ur\_ .image-shape .label,#chatgpt-mermaid-\_r_2ur\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_2ur\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_2ur\_ .rough-node .label,#chatgpt-mermaid-\_r_2ur\_ .node .label,#chatgpt-mermaid-\_r_2ur\_ .image-shape .label,#chatgpt-mermaid-\_r_2ur\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_2ur\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_2ur\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2ur\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2ur\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_2ur\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_2ur\_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_2ur\_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_2ur\_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_2ur\_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-\_r_2ur\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_2ur\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2ur\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2ur\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_2ur\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_2ur\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_2ur\_ .icon-shape,#chatgpt-mermaid-\_r_2ur\_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_2ur\_ .icon-shape p,#chatgpt-mermaid-\_r_2ur\_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-\_r_2ur\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_2ur\_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_2ur\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_2ur\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_2ur\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_2ur\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_2ur\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_2ur\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_2ur\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2ur\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_2ur\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_2ur\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_2ur\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_2ur\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_2ur\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_2ur\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-\_r_2ur\_ .node rect,#chatgpt-mermaid-\_r_2ur\_ .node circle,#chatgpt-mermaid-\_r_2ur\_ .node ellipse,#chatgpt-mermaid-\_r_2ur\_ .node polygon,#chatgpt-mermaid-\_r_2ur\_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_2ur\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_2ur\_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_2ur\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_2ur\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_2ur\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}T00 · Auditoría de SLDB,spec2viz y graph_uiT01 · Gap analysis OMGT02 · Inventario de APIs SLDBT03 · Inventario de extractoresT04 · Contrato demetamodelosT05 · Modelo de proyeccionesT06 · Núcleo de operacionessemánticasT07 · MCP read-onlyT08 · MCP de mutacionesT09 · Validador deconformidadT10 · Resolver de proyeccionesT11 · Extractor Django / SQLT12 · Extractor React / UXT13 · Contratos transversalesT14 · Análisis de impactoT15 · Síntesis de cambiosT16 · Validación end-to-endT17 · Integración graph_ui

## 2. Tareas y entregables

Estimaciones preliminares en días efectivos de ingeniería, con agentes de código. Las tareas paralelas no deben sumarse como duración calendario.

## Backlog del DAG

18 tareas

Filtrar por ramaTodas las ramas

T00Auditoría de infraestructura

T01Gap analysis OMG

T02Inventario API SLDB

T03Inventario de extractores

T04Contrato de metamodelos

T05Modelo de proyecciones

T06Operaciones semánticas

T07MCP read-only

Descubrimiento de modelos, consultas, trazas y recursos MCP

&#x20;Depende de: T06

&#x20;2–4 días

T08MCP de mutaciones

T09Validador de conformidad

T10Resolver de proyecciones

T11Extractor Django / SQL

T12Extractor React / UX

T13Contratos transversales

Vinculación tipada entre UX, API, operaciones, dominio y datos

&#x20;Depende de: T08,T10,T11,T12

&#x20;4–7 días

T14Análisis de impacto

T15Síntesis de cambios

T16Validación end-to-end

T17Integración graph_ui

&#x20;Copiar backlog completo

## 3. Hitos verificables

| Hito                     | Tareas necesarias       | Resultado                                   |
| ------------------------ | ----------------------- | ------------------------------------------- |
| M1 — Agente conectado    | T00, T02, T06, T07      | El agente explora SLDB mediante MCP         |
| M2 — Modelado formal     | T01, T04, T05, T09, T10 | Proyecciones conformes a metamodelos        |
| M3 — Agente modelador    | M1 + M2 + T08           | El agente modifica modelos y valida cambios |
| M4 — Sistema transversal | T03, T11, T12, T13      | Grafo UX ↔ API ↔ Django ↔ SQL               |
| M5 — Ingeniería asistida | T14, T15, T16           | Análisis de impacto y parches verificables  |
| M6 — Editor visual       | T17                     | Edición gráfica sobre el mismo modelo       |

Priorizaría M1 antes que todo lo demás. Permite poner inmediatamente al agente a trabajar sobre los repositorios y usarlo para acelerar el resto del DAG.

## 4. Decisiones que deben quedar explícitas

Hay tres decisiones técnicas que no conviene dejar implícitas:

- OMG como referencia, no dependencia: adoptar conceptos de MOF/UML/IFML, implementándolos mediante los contratos existentes de SLDB.
- Proyección versus identidad: no duplicar entidades por el hecho de representarlas en varios diagramas.
- MCP como consumidor principal: todas las operaciones deben ser invocables por agentes y también reutilizables por graph_ui.

El camino crítico para conseguir el primer sistema completo es aproximadamente:

`T00 → T01 → T04 → T09 → T08 → T13 → T15 → T16`

Aunque la rama MCP (`T02 → T06 → T07`) también debe estar terminada para alcanzar ese hito.





La organizaría como un proyecto MCP-first, aprovechando SLDB, spec2viz y graph_ui. El objetivo inicial no es generar aplicaciones completas, sino permitir que un agente comprenda y modifique sistemas existentes mediante sus modelos semánticos.

# Plan de desarrollo: Semantic Modeling MCP

**Objetivo:** construir una infraestructura de modelado semántico asistido por agentes que permita deconstruir, explorar, modificar y sintetizar sistemas de software, manteniendo consistencia entre UX, API, lógica de negocio y datos.

**Principio arquitectónico:** todo diagrama es una proyección de un grafo semántico tipado. Las relaciones entre elementos pueden atravesar esquemas y proyectos.

## 1. Arquitectura objetivo

```
flowchart TB
    Agent["Agente de código"]
    MCP["Semantic Modeling MCP"]
    Engine["Motor de operaciones semánticas"]

    Agent <--> MCP
    MCP <--> Engine

    Engine <--> SLDB["SLDB: grafo y modelos"]
    Engine <--> Extract["Extractores de código y APIs"]
    Engine <--> Specs["spec2viz: diagramas y notaciones"]

    Specs <--> UI["graph_ui"]
    SLDB <--> Storage["Documentos, código y fuentes"]
```

### Responsabilidades

| Componente      | Responsabilidad                                            |
| --------------- | ---------------------------------------------------------- |
| SLDB            | Identidad, almacenamiento, modelos, relaciones, integridad |
| spec2viz        | Esquemas de diagramas, notaciones y proyecciones           |
| graph_ui        | Exploración y edición visual                               |
| Motor semántico | Consultas, transformaciones, validaciones y mutaciones     |
| MCP             | Interfaz principal para agentes                            |
| Extractores     | Recuperación de estructuras desde sistemas existentes      |

El MCP no implementa la lógica semántica. La expone mediante herramientas tipadas.

---

## 2. Etapas de implementación

### Fase 0 — Auditoría y contratos existentes

**Esfuerzo: 2–3 días**

Revisar las implementaciones actuales antes de introducir nuevas abstracciones.

- Identificar operaciones SLDB reutilizables.
- Auditar `SpecDoc`, `SpecNodeDoc`, `RelationDoc` y `NotationDoc`.
- Revisar el contrato entre spec2viz y graph_ui.
- Identificar las operaciones de lectura y escritura que ya existen.
- Establecer equivalencias con MOF, Ecore y GLSP.

**Entregable:** matriz `existente / reutilizar / extender / implementar`.

**Criterio de aceptación:** ninguna capacidad nueva duplica una existente sin justificación.

### Fase 1 — MCP semántico mínimo

**Esfuerzo: 4–6 días**

Implementar un servidor MCP sobre las APIs Python existentes.

Herramientas iniciales:

```
models.list
models.describe

graph.query
graph.neighborhood
graph.trace

documents.inspect
relations.inspect

changes.propose
changes.validate
changes.apply
```

Requisitos:

- Referencias tipadas y estables.
- Consultas entre stores.
- Respuestas estructuradas y paginación.
- Errores interpretables por agentes.
- Cambios con validación y control de versión.
- Sin escrituras implícitas durante consultas.

**Entregable:** MCP funcional conectado a un store SLDB real.

**Criterio de aceptación:** un agente puede descubrir un modelo, recorrer sus relaciones, proponer una modificación y aplicarla tras validación explícita.

### Fase 2 — Metamodelos y conformidad

**Esfuerzo: 5–8 días**

Incorporar conceptos de OMG sin adoptar EMF como runtime.

Capacidades:

- Definición de tipos de nodos y relaciones.
- Restricciones de origen y destino.
- Cardinalidades.
- Herencia y composición.
- Identidad semántica independiente de apariciones.
- Validación de conformidad de un subgrafo.
- Esquemas versionados.

Distinguir formalmente:

1. Elemento semántico.
2. Aparición de ese elemento en una proyección.
3. Notación utilizada para representarlo.

**Entregable:** contrato de metamodelado y validador reutilizable.

**Criterio de aceptación:** dos diagramas pueden representar el mismo objeto sin duplicar su identidad semántica.

### Fase 3 — Proyecciones y transformaciones

**Esfuerzo: 5–8 días**

Extender spec2viz para construir diagramas mediante consultas al grafo.

Operaciones MCP:

```
projections.list
projections.describe
projections.generate
projections.validate

transformations.list
transformations.execute
```

Una proyección deberá declarar:

- Esquema de diagrama.
- Consulta o raíces del grafo.
- Relaciones que debe recorrer.
- Filtros.
- Notación.
- Referencias a los elementos originales.

Una transformación deberá declarar entradas, salidas, precondiciones y efectos.

**Entregable:** generación de diagramas de clases, estados y componentes desde un mismo modelo.

**Criterio de aceptación:** modificar un elemento semántico actualiza las proyecciones dependientes sin duplicar información.

### Fase 4 — Integración entre UX, API, backend y datos

**Esfuerzo: 7–12 días**

Implementar los esquemas y relaciones necesarios para describir una aplicación real.

**Caso de prueba:** blog mínimo con React, Django REST Framework y PostgreSQL.

Elementos que deben conectarse:

```
UXControl
  → UXAction
  → APIOperation
  → DjangoHandler
  → DomainOperation
  → DjangoModel
  → SQLTable
```

Además:

- Estados y transiciones.
- Permisos y políticas.
- Validación de formularios.
- Queries y transformaciones.
- Dependencias entre campos y componentes.
- Errores y resultados de operaciones.

Se utilizarán extractores existentes cuando sea posible y nuevos adaptadores para Django, OpenAPI y SQL.

**Entregable:** grafo transversal de la aplicación, con procedencia de cada elemento y relación.

**Criterio de aceptación:** el agente puede responder qué partes del frontend se ven afectadas por un cambio en un campo, endpoint o regla de negocio.

### Fase 5 — Ingeniería inversa UX

**Esfuerzo: 8–15 días**

Agregar extracción desde interfaces existentes.

Fuentes iniciales:

- Código React y JSX/TSX.
- Componentes y propiedades.
- Handlers y llamadas HTTP.
- DOM y eventos observables mediante Playwright.
- Contratos de API disponibles.

Distinguir:

- Elementos observados.
- Relaciones derivadas estáticamente.
- Inferencias propuestas por LLM.
- Relaciones verificadas.

Herramientas adicionales:

```
ux.extract
ux.inspect_interactions
ux.trace_to_backend
ux.detect_gaps
ux.propose_projection
```

**Entregable:** extractor que produce elementos UX vinculables al grafo de dominio y backend.

**Criterio de aceptación:** puede reconstruir el flujo de creación y publicación de un post desde la interfaz hasta su persistencia.

### Fase 6 — Síntesis y edición asistida

**Esfuerzo: 8–15 días**

Permitir al agente modificar una aplicación a partir de cambios semánticos.

Funciones:

- Proponer operaciones y componentes faltantes.
- Producir contratos de API.
- Proponer reglas de negocio.
- Generar parches de código.
- Actualizar modelos y proyecciones.
- Ejecutar validaciones y tests.

La generación deberá conservar las referencias a los nodos semánticos que motivaron cada cambio.

**Entregable:** flujo completo `inspeccionar → proponer → validar → modificar → verificar`.

**Criterio de aceptación:** agregar una capacidad como `SchedulePost` permite identificar las capas afectadas y producir cambios coherentes y revisables.

---

## 3. Dependencias

```
flowchart TD
    A["F0 Auditoría"] --> B["F1 MCP mínimo"]
    A --> C["F2 Metamodelos"]
    B --> D["F3 Proyecciones"]
    C --> D
    D --> E["F4 Integración full-stack"]
    B --> E
    E --> F["F5 Ingeniería inversa"]
    E --> G["F6 Síntesis"]
    F --> G
```

Las fases 1 y 2 pueden desarrollarse en paralelo. La fase 5 puede adelantarse parcialmente si los extractores existentes ya entregan información suficiente.

## 4. Estimación global

| Hito                       | Esfuerzo acumulado aproximado |
| -------------------------- | ----------------------------- |
| MCP operativo              | 6–9 días                      |
| Metamodelos y proyecciones | 16–25 días                    |
| Integración full-stack     | 23–37 días                    |
| Ingeniería inversa UX      | 31–52 días                    |
| Síntesis asistida          | 39–67 días                    |

Estimaciones para una persona experimentada utilizando agentes de código. No incluyen endurecimiento para producción, seguridad multiusuario ni compatibilidad completa con OMG.

## 5. Alcance y límites

**Dentro del primer MVP:**

- MCP funcional.
- Conformidad de modelos.
- Consultas y relaciones entre esquemas.
- Proyecciones declarativas.
- Ejemplo React + Django + PostgreSQL.
- Validación de impacto entre capas.

**Fuera del primer MVP:**

- Editor visual nuevo.
- Implementación completa de UML/MOF.
- Migración a EMF o Sirius.
- Generación automática de aplicaciones arbitrarias.
- Ingeniería inversa universal de cualquier sitio web.
- Colaboración multiusuario en tiempo real.

## 6. Riesgos prioritarios

| Riesgo                                | Mitigación                                                 |
| ------------------------------------- | ---------------------------------------------------------- |
| Duplicación semántica entre diagramas | Identidad canónica y apariciones explícitas                |
| Inferencias incorrectas del agente    | Procedencia, estado de verificación y validación           |
| Cambios destructivos                  | Propuestas, previsualización y aplicación controlada       |
| Complejidad de metamodelos OMG        | Implementar subconjuntos según necesidades verificadas     |
| Dependencia excesiva del renderer     | Separar operaciones semánticas de visualización            |
| Divergencia entre código y modelo     | Extractores incrementales y comprobaciones de consistencia |

## 7. Definición de éxito

El sistema se considera funcional cuando un agente conectado al MCP puede:

1. Descubrir los conceptos y operaciones de una aplicación.
2. Recorrer sus dependencias entre UX, API, backend y SQL.
3. Visualizar esas dependencias mediante diferentes esquemas de diagramas.
4. Detectar contradicciones entre las capas.
5. Proponer modificaciones semánticas.
6. Generar o actualizar implementaciones asociadas.
7. Validar que los cambios respetan los contratos del sistema.

**Principio final:** el agente trabaja sobre modelos semánticos verificables; el código y los diagramas son representaciones relacionadas de esos modelos, sin exigir que todos los artefactos sean generados exclusivamente desde ellos.

### Prioridad de ejecución

Yo fijaría el primer hito real al terminar la fase 3, aproximadamente 16–25 días efectivos: MCP, metamodelos y proyecciones funcionando sobre SLDB.

Después, el blog Django sería la prueba de que esa infraestructura puede conectar capas heterogéneas sin inventar una segunda ontología ni duplicar objetos.

No tocaría significativamente graph_ui hasta demostrar eso.

Resultado final esperado: un agente que pueda inspeccionar una aplicación existente, reconstruir sus dependencias semánticas, discutir cambios a nivel de modelo y llevarlos al código sin perder trazabilidad entre las capas.





