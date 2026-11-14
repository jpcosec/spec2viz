
son gratis? tienen mcps?
Sí, todas las herramientas Eclipse que mencionamos son gratuitas y open source. Lo de los MCP es más limitado: no todas tienen integración directa con agentes de IA.

Comparación
Herramienta

Gratis / OSS

MCP

Eclipse Sirius Web

Sí, EPL 2.0

No encontré uno oficial

Eclipse Papyrus

Sí

No encontré uno oficial

Eclipse EMF

Sí

Hay proyectos comunitarios por investigar

Eclipse Acceleo

Sí

No encontré uno oficial

Eclipse OCL / QVT

Sí

No encontré uno oficial

Sirius Web, por ejemplo, se puede alojar en un servidor propio y utiliza React, Spring y GraphQL. No requiere contratar una plataforma comercial. 

eclipse-sirius.github.io
+2

Encontré uno especialmente relevante: GLSP MCP
Eclipse GLSP + MCP

En junio de 2026, EclipseSource presentó un servidor MCP para GLSP, desarrollado en colaboración con investigadores de TU Wien.

Permite que un agente:

Inspeccione nodos, relaciones y tipos disponibles.

Cree, modifique y elimine elementos.

Valide modelos y diagramas.

Ejecute auto-layout, navegación y operaciones de undo/redo.

GLSP Meets Model Context Protocol 

eclipsesource.com

También vale la pena revisar EMF Cloud Model Server. No es MCP nativo, pero expone modelos EMF mediante REST y JSON-RPC, lo que facilita construir un adaptador. 

EMF Cloud

Para tu ecosistema SLDB + spec2viz
Priorizaría GLSP MCP sobre Papyrus MCP.

GLSP es independiente del metamodelo concreto y permite editar diagramas conectados a modelos propios. Eso encaja mejor con tu grafo semántico que adoptar UML como modelo obligatorio.

La combinación que investigaría es:

SLDB → spec2viz → GLSP Server → GLSP MCP → agente

Así el agente podría editar estructuras semánticas mediante herramientas, en lugar de manipular directamente YAML o generar diagramas sin una validación de tipos.

podrias evaluar el esfuerzo que toma impemetar esas weas, copiarlas o usarlas?

Procesó durante 50s
Revisé la arquitectura de tus tres repositorios (SLDB, spec2viz, graph_ui) y la documentación actual de GLSP, Sirius Web y EMF.

Mi recomendación inicial es no adoptar EMF/Sirius completo. Aprovecharía ideas de OMG para la semántica y evaluaría GLSP como motor de edición visual y MCP.

La razón es que ya tienes varias piezas que esas herramientas normalmente obligan a construir.

1. Comparación de esfuerzo
Estimaciones para una persona con experiencia en Python, TypeScript y agentes de código, trabajando principalmente con apoyo de IA.

Días efectivos de ingeniería, no días calendario. Son estimaciones de planificación, no mediciones.

Alternativa

Prototipo

Integración sólida

Riesgo

Extender spec2viz + graph_ui

5–10 días

20–35 días

Bajo–medio

Integrar GLSP + MCP

8–15 días

25–45 días

Medio

Integrar Sirius Web + EMF

15–25 días

45–80 días

Alto

Copiar arquitectura OMG en Python

10–20 días

35–65 días

Medio–alto

Implementar editor/MCP propio completo

12–20 días

40–75 días

Medio–alto

Los rangos de integración sólida incluyen edición de nodos y relaciones, validación, sincronización con SLDB y pruebas básicas. No incluyen todavía ingeniería inversa automática completa de React/Django ni generación de aplicaciones de producción.

2. Qué reutilizaría realmente
Gallery · Eclipse Graphical Language Server Platform
Eclipse GLSP + MCP

Primera opción externa a evaluar

GLSP permite usar una base de datos o un modelo propio como fuente semántica. No exige EMF. Su servidor MCP para Node permite inspeccionar, modificar y validar diagramas, pero sigue siendo experimental. 

Eclipse Graphical Language Server Platform
+1

Lo que ganarías: motor de edición gráfica y protocolo para agentes sin desarrollar todo desde cero.

Sirius Web 2025.4
Eclipse Sirius Web

No lo adoptaría inicialmente

Tiene metamodelos, vistas configurables, colaboración y GraphQL. Pero su arquitectura principal depende de Java, Spring y EMF. Introducirlo supondría mantener una segunda infraestructura de modelos. 

eclipse-sirius.github.io

Lo que ganarías: un entorno de modelado mucho más completo, a costa de una integración considerable.

3. Qué trabajo falta realmente en tus repositorios
Esta es la parte más importante de la evaluación.

Capacidad

Situación actual

Esfuerzo estimado

Grafo semántico y relaciones

SLDB ya lo proporciona

0–2 días

Especificaciones tipadas

spec2viz ya las valida

2–4 días para extensiones

Notaciones declarativas

Implementadas

1–3 días para ampliar

Proyecciones desde consultas al grafo

Parcial: existen from-graph y notation view

4–8 días

Identidad semántica compartida entre vistas

Hay refs, pero falta formalizar apariciones

3–6 días

Edición semántica desde diagramas

graph_ui ya edita documentos; falta completar el contrato de edición de diagramas

5–10 días

MCP de modelado

Por implementar o integrar

3–7 días

Compatibilidad Ecore / UML

Por implementar

7–15 días para un subconjunto

Estos esfuerzos tienen solapamientos: no deben sumarse mecánicamente.

Además, hay algo que juega a tu favor: graph_ui ya usa React Flow, tiene edición de documentos y modelos, y separa fuentes, vistas y shell. No estás partiendo de un canvas vacío.

4. Tres estrategias concretas
A. Mantener tu stack

Recomendada
SLDB + spec2viz + graph_ui + MCP propio

Formalizar proyecciones, añadir operaciones de edición tipadas y exponerlas como herramientas MCP.

Ventajas

Sin migración, sin dependencia de Java y con total control de la semántica.

Desventajas

Tienes que desarrollar y mantener parte del protocolo y las operaciones del editor.

B. SLDB + GLSP

Conservar SLDB, reemplazar o complementar el editor

Implementar SourceModelStorage, GModelFactory y handlers de edición que operen sobre SLDB. Son los principales puntos de extensión previstos por GLSP. 
Eclipse Graphical Language Server Platform

Ventajas

Reutilizas operaciones de edición, sincronización visual y MCP experimental.

Desventajas

Nuevo runtime TypeScript/Node y una integración sustancial con graph_ui.

C. SLDB + EMF + Sirius

Interoperabilidad OMG más profunda

Mapear modelos Pydantic a Ecore, sincronizar instancias y relaciones, y definir viewpoints Sirius.

Ventajas

Ecosistema maduro para metamodelos, constraints, transformaciones y representaciones.

Desventajas

Duplicidad de modelos, sincronización compleja y mayor superficie tecnológica.

5. Plan que ejecutaría
1

Prueba de identidad y proyecciones

3–5 días

Una misma entidad Post aparece en diagramas de clases, estados y UX, conservando identidad semántica. Cambiarla afecta correctamente a las tres vistas.

2

Operaciones de edición y MCP

4–8 días adicionales

Herramientas inspect, query, propose_patch, validate y apply_patch, utilizando SLDB como fuente de verdad.

3

Prueba de integración GLSP

4–7 días adicionales

Conectar un diagrama de juguete de SLDB con GLSP y probar edición bidireccional y MCP. Comparar con graph_ui antes de decidir si conviene adoptarlo.

4

Esquemas UX + backend + SQL

8–15 días adicionales

Vincular acciones de un formulario con una API Django y su persistencia SQL. Detectar dependencias y cambios inconsistentes entre las capas.

El objetivo de estas cuatro etapas sería un prototipo de extremo a extremo en aproximadamente 19–35 días efectivos, con alcance deliberadamente limitado. La extracción automática desde aplicaciones arbitrarias y la síntesis robusta de código serían etapas posteriores.

6. Mi decisión
Prioridad recomendada

SLDB + spec2viz + graph_ui

90/100

GLSP como complemento

74/100

Sirius Web + EMF

29/100

Puntuación orientativa propia: reutilización, esfuerzo, compatibilidad y control arquitectónico; no es un benchmark.
No copiaría GLSP ni Sirius completos. Sus motores de edición y toda la infraestructura de colaboración tienen un costo de mantenimiento que probablemente no se justifica para tu objetivo.

Haría una implementación pequeña sobre SLDB y spec2viz, tomando de OMG sus conceptos de metamodelado, conformidad y proyección. Luego evaluaría si GLSP aporta suficiente valor para sustituir parte de graph_ui.

Las referencias técnicas que usaría para esa decisión son la arquitectura de modelos de GLSP y su contrato MCP.

La primera inversión no debería ser construir otra UI: debería ser demostrar que diferentes diagramas pueden editar el mismo objeto semántico sin duplicarlo ni perder consistencia. Ese resultado te sirve independientemente de la tecnología visual que elijas.

Mira, creo que lo que vale la pena copiar es 1- modelo 2- api 3 - ui (hasta por ahi)
Sí. De hecho, copiaría la arquitectura de contratos, no las implementaciones completas de Eclipse.

La dividiría en tres capas, manteniendo SLDB como infraestructura semántica.

1. Modelo, API y UI
Capa

Referencia a copiar

Implementación propia

Modelo

OMG MOF / EMF Ecore

Modelos Pydantic + grafo SLDB

API

EMF Model Server + GLSP Protocol

API de consulta, edición y validación

UI

Sirius Viewpoints + GLSP

spec2viz + graph_ui

2. Arquitectura objetivo
3. UI
2. API
1. MODELO
spec2viz: notaciones
graph_ui: editor
Queries y proyecciones
Comandos y transacciones
Validación y cambios
SLDB: grafo tipado
Metamodelos Pydantic
Agentes MCP
3. Qué copiaría concretamente
Modelo — EMF/Ecore
Metamodelos explícitos: tipos, propiedades, relaciones y herencia.

Conformidad entre instancias y metamodelos.

Identidad semántica independiente de las vistas.

Restricciones e invariantes.

Referencias entre modelos.

Aquí evaluaría importar/exportar Ecore, sin adoptar su runtime Java.

API — EMF Model Server / GLSP
Consultas de elementos y subgrafos.

Operaciones tipadas de edición.

Validación previa a aplicar cambios.

Transacciones, undo/redo y notificaciones.

Suscripciones para mantener sincronizadas las proyecciones.

Esta sería probablemente la capa con más trabajo nuevo.

UI — Sirius / GLSP
Viewpoints declarativos.

Selección de elementos mediante consultas.

Notaciones independientes del modelo.

Edición visual traducida a operaciones semánticas.

Múltiples representaciones del mismo nodo.

Aquí spec2viz ya cubre una parte significativa.

4. Orden de implementación
Fase

Entregable

Estimación

1

Contrato de metamodelos y referencias

4–7 días

2

API de consultas y mutaciones semánticas

6–10 días

3

Proyecciones declarativas y edición visual

7–12 días

4

MCP reutilizando la API

3–5 días

Total orientativo: 20–34 días efectivos, suponiendo reutilización del código actual y sin incorporar un editor gráfico completamente nuevo.

5. Una decisión que considero importante
No haría que spec2viz implemente todas estas responsabilidades.

Mantendría:

SLDB: persistencia, identidad, grafo y contratos de modelos.

Una API semántica compartida: consultas, proyecciones, validaciones y mutaciones.

spec2viz: esquemas de diagramas y notaciones.

graph_ui: edición y visualización.

Así también un agente MCP o un generador de código utilizaría las mismas operaciones que la UI.

El objetivo sería que una modificación hecha mediante un diagrama, una API o un agente produzca exactamente la misma mutación semántica validada.

Eso es lo que vale la pena rescatar de la arquitectura de EMF/Sirius/GLSP.

ahora, entiendes que lo prioritario es el MCP de esto o no?
Sí. El MCP es la prioridad número uno, porque el consumidor principal del sistema será un agente de código, no un usuario editando diagramas manualmente.

El objetivo es que el agente pueda inspeccionar, comprender, modificar y validar un sistema a través de su grafo semántico, sin depender de interpretar archivos sueltos.

Orden correcto de implementación
Prioridad

Componente

Responsabilidad

1

MCP semántico

Herramientas para explorar, consultar y modificar modelos

2

Modelo

Extender los contratos de SLDB con semántica OMG donde aporte

3

API

Exponer operaciones tipadas, compartidas con el MCP

4

UI

Proyectar y editar modelos visualmente mediante spec2viz

El MCP debería ofrecer inicialmente estas capacidades:

discover_schemas()
inspect_element(id)
query_graph(query)
inspect_relations(id)
propose_change(intent)
validate_change(patch)
apply_change(patch)
Y después herramientas especializadas:

deconstruct_ui(source)
trace_interaction(element_id)
analyze_impact(element_id)
generate_projection(schema, context)
Una distinción importante: no construiría primero una API REST completa para envolverla después con MCP. Implementaría un núcleo de operaciones tipadas en Python, accesible directamente mediante MCP y reutilizable posteriormente por la API y la UI.

El primer hito sería conectar un agente a SLDB y conseguir que pueda recorrer y modificar correctamente esta cadena:

SaveButton → UXAction → APIOperation → DjangoHandler → SQLTable

Con validación de tipos, relaciones y consistencia entre capas.

Ese es el producto mínimo que necesitas para desbloquear el vibecoding. Los diagramas serían un mecanismo de inspección y edición adicional, no el centro de la arquitectura.

Me podriai hacer, a la luz de eso una "planificacion" de esta wea?
La organizaría como un proyecto MCP-first, aprovechando SLDB, spec2viz y graph_ui. El objetivo inicial no es generar aplicaciones completas, sino permitir que un agente comprenda y modifique sistemas existentes mediante sus modelos semánticos.

Plan de desarrollo: Semantic Modeling MCP
Objetivo: construir una infraestructura de modelado semántico asistido por agentes que permita deconstruir, explorar, modificar y sintetizar sistemas de software, manteniendo consistencia entre UX, API, lógica de negocio y datos.

Principio arquitectónico: todo diagrama es una proyección de un grafo semántico tipado. Las relaciones entre elementos pueden atravesar esquemas y proyectos.

1. Arquitectura objetivo
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
Responsabilidades
Componente	Responsabilidad
SLDB	Identidad, almacenamiento, modelos, relaciones, integridad
spec2viz	Esquemas de diagramas, notaciones y proyecciones
graph_ui	Exploración y edición visual
Motor semántico	Consultas, transformaciones, validaciones y mutaciones
MCP	Interfaz principal para agentes
Extractores	Recuperación de estructuras desde sistemas existentes
El MCP no implementa la lógica semántica. La expone mediante herramientas tipadas.

2. Etapas de implementación
Fase 0 — Auditoría y contratos existentes
Esfuerzo: 2–3 días

Revisar las implementaciones actuales antes de introducir nuevas abstracciones.

Identificar operaciones SLDB reutilizables.

Auditar SpecDoc, SpecNodeDoc, RelationDoc y NotationDoc.

Revisar el contrato entre spec2viz y graph_ui.

Identificar las operaciones de lectura y escritura que ya existen.

Establecer equivalencias con MOF, Ecore y GLSP.

Entregable: matriz existente / reutilizar / extender / implementar.

Criterio de aceptación: ninguna capacidad nueva duplica una existente sin justificación.

Fase 1 — MCP semántico mínimo
Esfuerzo: 4–6 días

Implementar un servidor MCP sobre las APIs Python existentes.

Herramientas iniciales:

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
Requisitos:

Referencias tipadas y estables.

Consultas entre stores.

Respuestas estructuradas y paginación.

Errores interpretables por agentes.

Cambios con validación y control de versión.

Sin escrituras implícitas durante consultas.

Entregable: MCP funcional conectado a un store SLDB real.

Criterio de aceptación: un agente puede descubrir un modelo, recorrer sus relaciones, proponer una modificación y aplicarla tras validación explícita.

Fase 2 — Metamodelos y conformidad
Esfuerzo: 5–8 días

Incorporar conceptos de OMG sin adoptar EMF como runtime.

Capacidades:

Definición de tipos de nodos y relaciones.

Restricciones de origen y destino.

Cardinalidades.

Herencia y composición.

Identidad semántica independiente de apariciones.

Validación de conformidad de un subgrafo.

Esquemas versionados.

Distinguir formalmente:

Elemento semántico.

Aparición de ese elemento en una proyección.

Notación utilizada para representarlo.

Entregable: contrato de metamodelado y validador reutilizable.

Criterio de aceptación: dos diagramas pueden representar el mismo objeto sin duplicar su identidad semántica.

Fase 3 — Proyecciones y transformaciones
Esfuerzo: 5–8 días

Extender spec2viz para construir diagramas mediante consultas al grafo.

Operaciones MCP:

projections.list
projections.describe
projections.generate
projections.validate

transformations.list
transformations.execute
Una proyección deberá declarar:

Esquema de diagrama.

Consulta o raíces del grafo.

Relaciones que debe recorrer.

Filtros.

Notación.

Referencias a los elementos originales.

Una transformación deberá declarar entradas, salidas, precondiciones y efectos.

Entregable: generación de diagramas de clases, estados y componentes desde un mismo modelo.

Criterio de aceptación: modificar un elemento semántico actualiza las proyecciones dependientes sin duplicar información.

Fase 4 — Integración entre UX, API, backend y datos
Esfuerzo: 7–12 días

Implementar los esquemas y relaciones necesarios para describir una aplicación real.

Caso de prueba: blog mínimo con React, Django REST Framework y PostgreSQL.

Elementos que deben conectarse:

UXControl
  → UXAction
  → APIOperation
  → DjangoHandler
  → DomainOperation
  → DjangoModel
  → SQLTable
Además:

Estados y transiciones.

Permisos y políticas.

Validación de formularios.

Queries y transformaciones.

Dependencias entre campos y componentes.

Errores y resultados de operaciones.

Se utilizarán extractores existentes cuando sea posible y nuevos adaptadores para Django, OpenAPI y SQL.

Entregable: grafo transversal de la aplicación, con procedencia de cada elemento y relación.

Criterio de aceptación: el agente puede responder qué partes del frontend se ven afectadas por un cambio en un campo, endpoint o regla de negocio.

Fase 5 — Ingeniería inversa UX
Esfuerzo: 8–15 días

Agregar extracción desde interfaces existentes.

Fuentes iniciales:

Código React y JSX/TSX.

Componentes y propiedades.

Handlers y llamadas HTTP.

DOM y eventos observables mediante Playwright.

Contratos de API disponibles.

Distinguir:

Elementos observados.

Relaciones derivadas estáticamente.

Inferencias propuestas por LLM.

Relaciones verificadas.

Herramientas adicionales:

ux.extract
ux.inspect_interactions
ux.trace_to_backend
ux.detect_gaps
ux.propose_projection
Entregable: extractor que produce elementos UX vinculables al grafo de dominio y backend.

Criterio de aceptación: puede reconstruir el flujo de creación y publicación de un post desde la interfaz hasta su persistencia.

Fase 6 — Síntesis y edición asistida
Esfuerzo: 8–15 días

Permitir al agente modificar una aplicación a partir de cambios semánticos.

Funciones:

Proponer operaciones y componentes faltantes.

Producir contratos de API.

Proponer reglas de negocio.

Generar parches de código.

Actualizar modelos y proyecciones.

Ejecutar validaciones y tests.

La generación deberá conservar las referencias a los nodos semánticos que motivaron cada cambio.

Entregable: flujo completo inspeccionar → proponer → validar → modificar → verificar.

Criterio de aceptación: agregar una capacidad como SchedulePost permite identificar las capas afectadas y producir cambios coherentes y revisables.

3. Dependencias
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
Las fases 1 y 2 pueden desarrollarse en paralelo. La fase 5 puede adelantarse parcialmente si los extractores existentes ya entregan información suficiente.

4. Estimación global
Hito	Esfuerzo acumulado aproximado
MCP operativo	6–9 días
Metamodelos y proyecciones	16–25 días
Integración full-stack	23–37 días
Ingeniería inversa UX	31–52 días
Síntesis asistida	39–67 días
Estimaciones para una persona experimentada utilizando agentes de código. No incluyen endurecimiento para producción, seguridad multiusuario ni compatibilidad completa con OMG.

5. Alcance y límites
Dentro del primer MVP:

MCP funcional.

Conformidad de modelos.

Consultas y relaciones entre esquemas.

Proyecciones declarativas.

Ejemplo React + Django + PostgreSQL.

Validación de impacto entre capas.

Fuera del primer MVP:

Editor visual nuevo.

Implementación completa de UML/MOF.

Migración a EMF o Sirius.

Generación automática de aplicaciones arbitrarias.

Ingeniería inversa universal de cualquier sitio web.

Colaboración multiusuario en tiempo real.

6. Riesgos prioritarios
Riesgo	Mitigación
Duplicación semántica entre diagramas	Identidad canónica y apariciones explícitas
Inferencias incorrectas del agente	Procedencia, estado de verificación y validación
Cambios destructivos	Propuestas, previsualización y aplicación controlada
Complejidad de metamodelos OMG	Implementar subconjuntos según necesidades verificadas
Dependencia excesiva del renderer	Separar operaciones semánticas de visualización
Divergencia entre código y modelo	Extractores incrementales y comprobaciones de consistencia
7. Definición de éxito
El sistema se considera funcional cuando un agente conectado al MCP puede:

Descubrir los conceptos y operaciones de una aplicación.

Recorrer sus dependencias entre UX, API, backend y SQL.

Visualizar esas dependencias mediante diferentes esquemas de diagramas.

Detectar contradicciones entre las capas.

Proponer modificaciones semánticas.

Generar o actualizar implementaciones asociadas.

Validar que los cambios respetan los contratos del sistema.

Principio final: el agente trabaja sobre modelos semánticos verificables; el código y los diagramas son representaciones relacionadas de esos modelos, sin exigir que todos los artefactos sean generados exclusivamente desde ellos.

Prioridad de ejecución
Yo fijaría el primer hito real al terminar la fase 3, aproximadamente 16–25 días efectivos: MCP, metamodelos y proyecciones funcionando sobre SLDB.

Después, el blog Django sería la prueba de que esa infraestructura puede conectar capas heterogéneas sin inventar una segunda ontología ni duplicar objetos.

No tocaría significativamente graph_ui hasta demostrar eso.

En tu opinion, si le pasai esa wea a alguien entiende de que mierda le estay hablando? No mencionas ni omg ni para que estabamos haciendo esto
No. Tenís razón. Ese documento es una lista de tareas técnicas sin contexto. Alguien que no haya participado en esta conversación no entendería qué problema estamos resolviendo, por qué estamos usando OMG, qué queremos reutilizar ni cuál es el resultado esperado.

Además, perdí el objetivo original: desbloquear el diseño y desarrollo de interfaces complejas mediante agentes de código.

La planificación debería comenzar con algo como esto:

1. Motivación y problema
Actualmente, los agentes de código pueden generar componentes, APIs y modelos de datos, pero tienen dificultades para razonar sobre aplicaciones completas.

En particular, les cuesta mantener la coherencia entre:

Lo que un usuario puede hacer en la interfaz.

Las operaciones que implementa el backend.

Los datos disponibles y sus relaciones.

Las reglas de negocio, estados y restricciones.

Las distintas representaciones de estos elementos.

El resultado es que el vibecoding funciona razonablemente bien para componentes aislados, pero se deteriora cuando las interacciones atraviesan múltiples capas.

El objetivo del proyecto es proporcionar a los agentes una representación semántica navegable y modificable de una aplicación completa.

2. Hipótesis de solución
Utilizar un grafo semántico tipado como representación intermedia compartida.

Cada aspecto del sistema se describe mediante un esquema formal: interfaces, clases, estados, operaciones, servicios, datos y procesos.

Los diagramas son proyecciones de ese grafo, no fuentes de verdad independientes.

Esto permite que un agente recorra una relación como:

Botón → Acción UX → Operación API → Método Django → Modelo → Tabla SQL

Pero también que recorra el sistema en sentido contrario, detecte inconsistencias y proponga modificaciones.

3. Por qué OMG
El Object Management Group lleva décadas estandarizando precisamente las estructuras necesarias para modelar sistemas complejos.

No queremos implementar UML completo ni sustituir nuestros sistemas por herramientas Eclipse.

Queremos aprovechar los contratos y abstracciones ya desarrollados en el ecosistema OMG:

Estándar

Qué aporta

MOF / EMOF

Metamodelos, tipos e instancias

UML

Estructuras, operaciones, estados y comportamientos

IFML

Interacciones y flujos de interfaces

OCL

Restricciones e invariantes

QVT

Transformaciones entre modelos

DI / UMLDI

Separación entre elementos semánticos y representaciones gráficas

Y estudiar tres implementaciones de referencia:

EMF/Ecore: arquitectura de metamodelos.

EMF Model Server / GLSP: APIs para consultar y modificar modelos.

Sirius / GLSP: proyecciones y edición visual.

La intención es copiar las abstracciones y contratos que sean útiles, no mantener sus runtimes completos.

4. Qué hemos construido y qué falta
Ya existen tres proyectos que constituyen la base tecnológica:

SLDB proporciona la persistencia y navegación del grafo semántico, los modelos Pydantic y las relaciones tipadas.

spec2viz permite definir diagramas semánticos, validarlos y representarlos utilizando notaciones declarativas.

graph_ui permite explorar y editar visualmente estructuras almacenadas en SLDB.

Lo que falta es completar su interoperabilidad como sistema de modelado, especialmente:

Conformidad formal con metamodelos.

Proyecciones sobre elementos con identidad semántica compartida.

Operaciones de consulta, modificación y validación reutilizables.

Extracción de modelos desde código existente.

Síntesis de cambios de software desde modelos.

5. Por qué el MCP es prioritario
El consumidor principal no será un usuario dibujando diagramas: será un agente de código.

El MCP debe permitirle descubrir los esquemas disponibles, navegar relaciones, comprender comportamientos, identificar inconsistencias y proponer modificaciones verificables.

La UI gráfica es complementaria: sirve para inspeccionar, discutir y corregir los modelos.

Por eso el orden de desarrollo debe ser:

MCP → contratos semánticos OMG compatibles → operaciones y transformaciones → proyecciones → integración UX/backend → síntesis.

Esto debería ser la introducción de un documento bastante más completo, seguido de la arquitectura, las decisiones técnicas, los hitos y los criterios de aceptación.

También corregiría otra cosa de la planificación anterior: no daría por hecho qué falta implementar sin auditar primero el estado real de SLDB y spec2viz. La planificación debe distinguir claramente capacidades existentes, brechas comprobadas y propuestas arquitectónicas.

El entregable que corresponde es una especificación de proyecto y plan de ejecución, no simplemente un roadmap de tareas.

ok, ahora, como si tuvieras que hacer un dag con la tareas, como se veria?
Lo estructuraría como un DAG de capacidades, no como fases secuenciales. Las ramas de metamodelos, API/MCP y extracción pueden avanzar en paralelo.

El objetivo es construir un sistema de ingeniería de software asistida por agentes, basado en SLDB y spec2viz, que aproveche estándares OMG para conectar UX, backend, operaciones y datos mediante un grafo semántico tipado.

1. DAG de desarrollo
T00 · Auditoría de SLDB,spec2viz y graph_ui
T01 · Gap analysis OMG
T02 · Inventario de APIs SLDB
T03 · Inventario de extractores
T04 · Contrato demetamodelos
T05 · Modelo de proyecciones
T06 · Núcleo de operacionessemánticas
T07 · MCP read-only
T08 · MCP de mutaciones
T09 · Validador deconformidad
T10 · Resolver de proyecciones
T11 · Extractor Django / SQL
T12 · Extractor React / UX
T13 · Contratos transversales
T14 · Análisis de impacto
T15 · Síntesis de cambios
T16 · Validación end-to-end
T17 · Integración graph_ui
2. Tareas y entregables
Estimaciones preliminares en días efectivos de ingeniería, con agentes de código. Las tareas paralelas no deben sumarse como duración calendario.

Backlog del DAG
18 tareas
Filtrar por rama
all

T00

Auditoría de infraestructura


T01

Gap analysis OMG


T02

Inventario API SLDB


T03

Inventario de extractores


T04

Contrato de metamodelos


T05

Modelo de proyecciones


T06

Operaciones semánticas


T07

MCP read-only

Descubrimiento de modelos, consultas, trazas y recursos MCP

 Depende de: T06

 2–4 días


T08

MCP de mutaciones


T09

Validador de conformidad


T10

Resolver de proyecciones


T11

Extractor Django / SQL


T12

Extractor React / UX


T13

Contratos transversales

Vinculación tipada entre UX, API, operaciones, dominio y datos

 Depende de: T08,T10,T11,T12

 4–7 días


T14

Análisis de impacto


T15

Síntesis de cambios


T16

Validación end-to-end


T17

Integración graph_ui

3. Hitos verificables
Hito

Tareas necesarias

Resultado

M1 — Agente conectado

T00, T02, T06, T07

El agente explora SLDB mediante MCP

M2 — Modelado formal

T01, T04, T05, T09, T10

Proyecciones conformes a metamodelos

M3 — Agente modelador

M1 + M2 + T08

El agente modifica modelos y valida cambios

M4 — Sistema transversal

T03, T11, T12, T13

Grafo UX ↔ API ↔ Django ↔ SQL

M5 — Ingeniería asistida

T14, T15, T16

Análisis de impacto y parches verificables

M6 — Editor visual

T17

Edición gráfica sobre el mismo modelo

Priorizaría M1 antes que todo lo demás. Permite poner inmediatamente al agente a trabajar sobre los repositorios y usarlo para acelerar el resto del DAG.

4. Decisiones que deben quedar explícitas
Hay tres decisiones técnicas que no conviene dejar implícitas:

OMG como referencia, no dependencia: adoptar conceptos de MOF/UML/IFML, implementándolos mediante los contratos existentes de SLDB.

Proyección versus identidad: no duplicar entidades por el hecho de representarlas en varios diagramas.

MCP como consumidor principal: todas las operaciones deben ser invocables por agentes y también reutilizables por graph_ui.

El camino crítico para conseguir el primer sistema completo es aproximadamente:

T00 → T01 → T04 → T09 → T08 → T13 → T15 → T16

Aunque la rama MCP (T02 → T06 → T07) también debe estar terminada para alcanzar ese hito.

Resultado final esperado: un agente que pueda inspeccionar una aplicación existente, reconstruir sus dependencias semánticas, discutir cambios a nivel de modelo y llevarlos al código sin perder trazabilidad entre las capas.

podriai hacer un documento pa explicar los fundamentos de esta wea?

Procesó durante 1m 15s
Preparé un documento de fundamentos técnicos y conceptuales, independiente del DAG de tareas.

Fundamentos de una infraestructura de modelado semántico para agentes de código

Markdown · 10 secciones · Incluye diagramas Mermaid

Descargar documento Markdown

Qué contiene
Motivación: por qué el vibecoding falla al diseñar sistemas con interacciones complejas.

Fundamentos: grafos semánticos tipados, identidad, instancias, relaciones y proyecciones.

Modelo conceptual: dominio, datos, operaciones, estados y contexto.

Ejemplo concreto: blog React + Django + PostgreSQL.

Estándares OMG: MOF, UML, IFML, OCL, QVT y sus aplicaciones.

Arquitectura: responsabilidades de SLDB, spec2viz y graph_ui.

MCP-first: por qué el agente es el consumidor principal y qué herramientas necesita.

Ingeniería inversa y síntesis: cómo recuperar modelos desde código y producir modificaciones.

Criterios de éxito: qué debe demostrar el primer prototipo.

Decisiones arquitectónicas: principios y límites del proyecto.

La tesis central del documento es:

El grafo semántico no es un dibujo de la aplicación: es una representación operable de sus entidades, comportamientos, datos, estados, contextos y relaciones.

Los diagramas son proyecciones de ese modelo; el MCP permite a los agentes operar sobre él y las transformaciones vinculan el modelo con el código.


fundamentos_modelado_semantico_mcp.md
Documento




⋮⋮⋮⋮
