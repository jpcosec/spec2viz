FILE:desk/drawer/plans/specir/dag.yaml#node:IR06
id: IR06
title: IR06 Tipos de dominio transversales y cadena de prueba del blog
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Los tipos de dominio transversales de specIR y un store de prueba con la cadena
  de publicar un post del blog de ejemplo (React, Django REST Framework, PostgreSQL),
  recorrible por MCP.


  Alcance:

  Dentro: (1) clases Python de modelo, definidas en el paquete specIR como subclases
  del documento base de SLDB, para control de interfaz, acción, operación de API,
  handler, operación de dominio, política, estado, entidad de dominio y tabla; (2)
  tipos de relación como documentos RelationTypeDoc que specIR distribuye e instala
  en un store: triggers, invokes, handled_by, executes, governed_by, transitions,
  writes, persisted_in; (3) invariantes entre capas como documentos RuleDoc que specIR
  distribuye, por ejemplo que toda acción de interfaz invoque una operación de API
  existente; (4) un store de prueba poblado por MCP con la cadena de publicar un post.
  Frontera: las clases de modelo son código de specIR; los tipos de relación y las
  reglas son datos del store; el MCP escribe datos y no clases. Fuera: extractores
  automáticos, análisis de impacto, síntesis.'
acceptance: 'Las pruebas anteriores pasan y la cadena del blog queda como store de
  prueba reutilizable por las tareas posteriores.


  Validación:

  - Por MCP se recorre PublishButton, PublishAction, endpoint, handler, PublishPost
  y tabla, en ambos sentidos.

  - Una relación entre tipos no permitidos (por ejemplo un control de interfaz que
  escribe directo en una tabla) es rechazada por su RelationTypeDoc.

  - Quitar del store de prueba la operación de API que una acción invoca hace que
  la evaluación de reglas reporte el RuleDoc incumplido.

  - Dos vistas distintas (una de estados y una de componentes) muestran la misma entidad
  Post y el store contiene un solo documento para ella.

  - Cada nodo y relación lleva la procedencia de la taxonomía canónica decidida.

  - Las clases de modelo viven en el paquete specIR y ningún modelo de vocabulario
  visual de SLDB se redefine.'
output_scope:
- src/specir/models/__init__.py
- src/specir/models/domain.py
- src/specir/data/relation_types.yaml
- src/specir/data/rules.yaml
- src/specir/install.py
- tests/models/test_domain_models.py
- tests/models/test_blog_chain.py
- tests/fixtures/blog_chain.yaml
depends_on:
- IR04
- IR05
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR04
id: IR04
title: 'IR04 Escritura validada por MCP: proponer, validar, aplicar'
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Tools MCP de escritura con las que un agente propone, valida y aplica cambios
  al store, con el mecanismo decidido en la tarea de contrato de escritura.


  Alcance:

  Dentro, mutaciones del store que expone el MCP: crear, editar y borrar documentos
  de modelos ya registrados; afirmar y retirar aristas (RelationDoc); declarar y editar
  tipos de relación (RelationTypeDoc) y reglas (RuleDoc), que son documentos del store
  y por eso se escriben como datos. Toda escritura admite ejecución en seco. Fuera:
  crear o editar clases Python de modelos por MCP. Las clases de modelo se definen
  como código en el paquete specIR (o en el paquete del proyecto que las declare)
  y entran al store por el registro de modelos de SLDB; exponer su edición por MCP
  queda como decisión posterior, condicionada a la tarea de contrato de escritura.
  Fuera también: síntesis de código de aplicación.'
acceptance: 'Las pruebas anteriores pasan contra un store de prueba y un agente completa
  el ciclo proponer, validar y aplicar sobre un documento y sobre una arista.


  Validación:

  - Una ejecución en seco devuelve lo que se escribiría y no cambia ningún archivo
  del store.

  - Aplicar un cambio validado sobre un store que cambió después de la validación
  es rechazado con un error que lo dice.

  - Una arista que viola los tipos de origen o destino, la cardinalidad o la condición
  de su RelationTypeDoc es rechazada antes de escribir.

  - Un cambio que incumple un RuleDoc vigente es rechazado o reportado según la severidad
  de la regla, y la respuesta nombra la regla.

  - Ninguna tool de escritura recibe texto libre para interpretar: solo argumentos
  tipados.

  - Cada documento escrito lleva en su procedencia quién y por qué operación se escribió.

  - Una tool por encima del nivel de escritura permitido responde error sin evaluar
  nada.

  - No existe ninguna tool que cree o modifique módulos Python.'
output_scope:
- src/specir/mcp/write_tools.py
- src/specir/mcp/changes.py
- src/specir/mcp/mutability.py
- tests/mcp/test_write_tools.py
- tests/mcp/test_dry_run.py
- tests/mcp/test_mutability.py
depends_on:
- IR02
- IR03
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR05
id: IR05
title: 'IR05 Decisión: procedencia y divergencia entre código y modelo'
kind: decision
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Una taxonomía canónica de procedencia para specIR y una regla para la divergencia
  entre el modelo y el código del que se extrajo.


  Alcance:

  Dentro: elegir la taxonomía canónica entre (1) observado, inferido, validado (fundamentos_modelado_semantico_mcp.md,
  sección 7); (2) observado, derivado estáticamente, inferencia de LLM, verificado
  (Plan_IR.md, fase 5); (3) la autoridad de SLDB: source_raw, authored, theorem, generated,
  cache (sldb/src/sldb/models/provenance.py); definir las equivalencias; decidir si
  la relación entre un nodo extraído y su fuente se expresa con las anclas de código
  de SLDB; decidir qué prevalece cuando modelo y código discrepan y cómo se representa
  lo desconocido. Fuera: implementar extractores.'
acceptance: 'Los tres atoms existen y las tareas de tipos de dominio y de extractores
  pueden citar una sola taxonomía.


  Validación:

  - Existe un atom con la taxonomía canónica y la tabla de equivalencias con las otras
  dos listas.

  - Existe un atom que dice cómo se representa lo desconocido y cómo una inferencia
  pasa a validada, y por acción de quién.

  - Existe un atom sobre divergencia: qué ocurre con un nodo cuya fuente cambió.

  - Si la decisión exige algo que SLDB no tiene, la carencia está identificada con
  la fila correspondiente de la matriz de auditoría.'
output_scope:
- docs/decisiones/procedencia-y-divergencia.md
depends_on:
- IR01
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR07
id: IR07
title: 'IR07 Cobertura completa de spec2viz: matriz, fuente de verdad del diagrama
  y gate de retiro'
kind: docs
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Una matriz de cobertura de todas las capacidades de spec2viz, con modo y condición
  de retiro por fila; la decisión sobre el papel del YAML de spec frente al grafo;
  y un gate comprobable de migración y retiro. Es un plan de cobertura: no declara
  nada como ya migrado.


  Alcance:

  Dentro, una fila por cada capacidad de spec2viz, cada una con modo (migrar tal cual;
  reemplazar por otra arquitectura o experiencia con resultado equivalente; exponer
  desde specIR lo que ya vive en SLDB) y condición verificable de retiro:

  - Modelos de spec por tipo de diagrama: clase, secuencia, estado, componente, actividad,
  despliegue, matriz, reflexión; carga y validación de specs; export de JSON Schema
  de specs y de catálogos.

  - Representación intermedia y compiladores por tipo de diagrama.

  - Renderizadores: Mermaid, PlantUML, D2, BPMN y su visor, Vega, árbol, HTML de grafo,
  antonia-html y salida JSON.

  - Linter de Mermaid.

  - SpecSync: materializar un spec en el store como SpecDoc, SpecNodeDoc y RelationDoc,
  creando el RelationTypeDoc que falte y borrando lo que salió del spec.

  - from-graph: compilar el grafo de un store o un snapshot en un spec de componentes.

  - Generación de un spec de componentes desde el AST de Python.

  - Catálogos: build (HTML autocontenido), sync, validate y serve con autoguardado
  de anotaciones; registro vistas.yml y stores jerárquicos de diagramas.

  - NotationDoc, GlyphDoc, LinkDoc y PaletteDoc: list, validate, sync y view de notaciones;
  list, validate y sync de paletas, con la comprobación de contraste WCAG.

  - Emparejamiento de átomos con elementos de diagrama y cobertura por vista.

  - API Python pública y recursos empaquetados (plantillas HTML, bpmn-js, notaciones
  y paleta builtin).

  - Comando about y la habilidad de uso de spec2viz instalada para agentes.

  Dentro también: inventario de consumidores, con el archivo donde cada uno importa
  o invoca spec2viz: graph_ui (UIs/graph_ui/frontends/mindmap/sldb_adapter.py y su
  pyproject.toml), deskops (reglas de rutas en el módulo graph.desk_graph del paquete
  deskops, documentación de diagramas y la habilidad use-spec2viz) y los stores cuyo
  índice registra modelos spec2viz.sldb_models.

  Dentro también, la decisión antes separada: la fuente semántica es el grafo de SLDB;
  decidir si el YAML de spec queda como formato de autoría e intercambio de forma
  permanente o solo durante la paridad; cómo se dibuja algo que todavía no existe
  en el grafo (diseño previo a la implementación); y qué pasa con los specs YAML existentes
  en los repos que usan spec2viz.

  Fuera: migrar o implementar cualquier fila; extractores de otras tecnologías; análisis
  de impacto.'
acceptance: 'La matriz, la decisión y el gate de retiro están escritos y revisados,
  y de la matriz se pueden derivar las tareas de migración sin volver a inventariar
  spec2viz.


  Validación:

  - Todos los comandos y subgrupos que lista la ayuda del CLI de spec2viz aparecen
  en la matriz.

  - Todos los módulos de compiladores, renderizadores, linters y generadores del paquete
  spec2viz aparecen en la matriz.

  - Ninguna fila dice descartado, fuera de alcance o ya implementado sin una prueba
  citada.

  - Cada fila en modo reemplazar nombra el sustituto y la prueba que demostrará la
  equivalencia.

  - Cada fila en modo exponer desde SLDB cita la operación de la API pública de SLDB
  que la respalda.

  - Cada consumidor inventariado cita el archivo donde importa o invoca spec2viz.

  - Existe un atom con la decisión sobre el YAML de spec frente al grafo, con las
  alternativas descartadas, la regla para diseño previo a la implementación y el destino
  de los specs existentes.

  - El gate de retiro está escrito como lista comprobable: toda fila con su condición
  cumplida; la suite de spec2viz pasa contra specIR o tiene prueba equivalente declarada
  por fila reemplazada; ningún consumidor importa ni invoca spec2viz; ningún store
  registra modelos spec2viz.sldb_models.'
output_scope:
- docs/spec2viz/matriz-de-cobertura.md
- docs/spec2viz/gate-de-retiro.md
- docs/decisiones/fuente-de-verdad-del-diagrama.md
depends_on:
- IR03
- IR06
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR08
id: IR08
title: IR08 Extractor estático Django/DRF y SQL
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Un extractor estático que, a partir de una aplicación Django REST Framework
  y su esquema SQL, produce documentos y relaciones de los tipos de dominio de specIR,
  cada uno con su evidencia de origen.


  Alcance:

  Dentro: lectura estática (AST y metadatos, sin ejecutar la aplicación) de rutas
  y vistas, serializers y sus campos, modelos Django con sus relaciones, y tablas,
  columnas y claves del esquema SQL; producción de operaciones de API, handlers, entidades
  de dominio, tablas y las relaciones entre ellos; procedencia por nodo y relación
  con archivo, línea y hash del fragmento fuente, en la taxonomía decidida en la tarea
  de procedencia; idempotencia: extraer dos veces el mismo código no cambia el store.

  Fuera: frontend; análisis en tiempo de ejecución; reglas de negocio que no se deducen
  del código, que quedan como desconocidas o marcadas como inferidas; análisis de
  impacto; cualquier parche al código.'
acceptance: 'Las pruebas anteriores pasan sobre el fixture y el grafo de backend y
  datos del blog se obtiene sin poblarlo a mano.


  Validación:

  - Sobre el fixture de la aplicación del blog, el extractor produce los nodos de
  backend y datos de la cadena de publicar un post que la tarea de tipos de dominio
  pobló a mano, con los mismos tipos y relaciones.

  - Cada nodo y relación extraído lleva archivo, línea y hash del fragmento fuente,
  y su procedencia en la taxonomía canónica.

  - Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico (comparación
  del árbol del store).

  - Modificar un archivo fuente del fixture y volver a extraer señala los nodos anclados
  a ese archivo como cambiados, sin borrar hechos validados por una persona.

  - Ningún nodo inferido queda con procedencia de observado o validado.

  - Las relaciones extraídas pasan la validación de sus RelationTypeDoc y de los RuleDoc
  vigentes.

  - El módulo no importa pron ni spec2viz, ni módulos de SLDB fuera de sldb.api.'
output_scope:
- src/specir/extract/__init__.py
- src/specir/extract/provenance.py
- src/specir/extract/django_drf.py
- src/specir/extract/sql_schema.py
- tests/extract/test_django_drf.py
- tests/extract/test_sql_schema.py
- tests/extract/test_idempotencia.py
- tests/fixtures/blog_backend/manage.py
depends_on:
- IR05
- IR06
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR09
id: IR09
title: IR09 Extractor estático React/TSX y contratos de API
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Un extractor estático que, a partir de código React (JSX y TSX) y de los contratos
  de API disponibles, produce los elementos de interfaz del grafo de specIR y los
  vincula a las operaciones de backend, con evidencia de origen.


  Alcance:

  Dentro: lectura estática de componentes y sus propiedades, controles, acciones (handlers
  de eventos), estados locales declarados y llamadas HTTP; contratos de API disponibles
  (por ejemplo OpenAPI) para resolver a qué operación corresponde cada llamada; producción
  de controles, acciones, estados y las relaciones triggers e invokes hacia operaciones
  de API; evidencia de origen por nodo y relación con archivo, línea y hash; idempotencia.

  Fuera: observación del DOM o de eventos en ejecución; comportamiento dinámico que
  no se deduce del código, que no se afirma: se marca como inferido o se deja como
  desconocido; generación o modificación de código de interfaz.'
acceptance: 'Las pruebas anteriores pasan sobre el fixture y la mitad de interfaz
  de la cadena de publicar un post se obtiene sin poblarla a mano.


  Validación:

  - Sobre el fixture del blog, el extractor produce PublishButton, PublishAction y
  su relación con la operación de API de publicar, con los tipos de la tarea de tipos
  de dominio.

  - Cada nodo y relación extraído lleva archivo, línea y hash del fragmento fuente.

  - Una llamada HTTP cuya URL no se resuelve estáticamente produce una relación marcada
  como inferida o un hueco declarado, nunca una relación observada.

  - Una llamada a un endpoint que no existe en el grafo queda registrada como brecha,
  no se descarta ni se inventa la operación.

  - Ejecutar el extractor dos veces sobre el mismo código deja el store idéntico.

  - Las relaciones extraídas pasan la validación de sus RelationTypeDoc.'
output_scope:
- src/specir/extract/react_tsx.py
- src/specir/extract/api_contracts.py
- tests/extract/test_react_tsx.py
- tests/extract/test_api_contracts.py
- tests/fixtures/blog_frontend/package.json
depends_on:
- IR05
- IR06
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR10
id: IR10
title: IR10 Reglas semánticas y análisis de impacto
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Un conjunto de reglas RuleDoc que detectan brechas entre capas y una operación
  de análisis de impacto, expuesta por MCP, que devuelve los elementos afectados por
  un cambio con el camino que lo justifica.


  Alcance:

  Dentro: reglas RuleDoc, distribuidas por specIR como documentos, para cadenas rotas
  interfaz, API, operación, datos: acción sin operación de API, campo de interfaz
  ausente del serializer, operación sin handler, entidad sin persistencia, política
  sin representación en la interfaz; cada hallazgo con severidad, regla que lo produce
  y evidencia; operación de impacto: dado un nodo (campo, endpoint, regla, tabla),
  los nodos afectados en las demás capas con el camino de relaciones que lo explica
  y la procedencia de cada tramo; tool MCP de solo lectura para ambas.

  Fuera: proponer parches o cambios de código; aplicar correcciones al grafo; reglas
  que requieran ejecutar la aplicación.'
acceptance: 'Las pruebas anteriores pasan y un agente puede responder por MCP qué
  partes de la interfaz afecta un cambio en un campo, un endpoint o una regla del
  blog.


  Validación:

  - Por cada regla hay un store de prueba con la brecha sembrada y la evaluación la
  reporta con su severidad, la regla y los documentos implicados.

  - Sobre el grafo completo del blog sin brechas sembradas, las reglas no reportan
  hallazgos.

  - Dado el campo status de la tabla de posts, la operación de impacto devuelve PublishButton
  entre los afectados, con el camino completo de relaciones.

  - Cada tramo del camino devuelto lleva su procedencia, y un camino que pasa por
  una relación inferida se señala como tal.

  - Las tools de reglas e impacto no escriben en el store (comparación del árbol antes
  y después).

  - Ninguna respuesta incluye un parche ni una modificación propuesta.'
output_scope:
- src/specir/data/layer_rules.yaml
- src/specir/impact.py
- src/specir/mcp/impact_tools.py
- tests/rules/test_layer_rules.py
- tests/test_impact.py
depends_on:
- IR06
- IR08
- IR09
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR11
id: IR11
title: IR11 Compiladores y proyecciones de spec2viz
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'specIR compila todos los tipos de diagrama que compila spec2viz y produce
  diagramas tanto desde un spec autorado como desde una proyección del grafo, según
  el contrato decidido en la tarea de cobertura.


  Alcance:

  Dentro: modelos de spec, carga y validación para clase, secuencia, estado, componente,
  actividad, despliegue, matriz y reflexión; representación intermedia y un compilador
  por tipo; materialización de proyecciones: de un ViewDoc evaluado sobre el grafo
  y de un SpecDoc con sus SpecNodeDoc a la misma representación intermedia. Cada pieza
  se migra tal cual o se reemplaza, según el modo que le asigne la matriz de cobertura;
  los modelos de vocabulario visual se usan desde SLDB y no se redefinen.

  Fuera: renderizado a formatos de salida, linter y recursos empaquetados; sincronización
  al store, catálogos y consumidores; retirar spec2viz.'
acceptance: 'Las pruebas de paridad de compiladores pasan en specIR y las filas de
  compiladores y proyecciones de la matriz de cobertura tienen su condición de retiro
  cumplida.


  Validación:

  - Los ocho tipos de diagrama compilan en specIR, y cada fixture de compilador de
  spec2viz produce en specIR una representación intermedia estructuralmente equivalente
  a la de spec2viz según la normalización definida en el camino de implementación,
  o la diferencia está declarada en la fila correspondiente de la matriz de cobertura
  con su prueba equivalente.

  - La función de normalización tiene su propia prueba: dos representaciones que difieren
  solo en el orden de nodos o en metadata de procedencia resultan iguales, y dos que
  difieren en un campo, un nodo o una arista resultan distintas.

  - Los specs YAML existentes validan en specIR con los mismos errores tipados que
  en spec2viz, salvo que la decisión de la tarea de cobertura diga otra cosa.

  - Un diagrama de componentes y uno de estados generados desde proyecciones del grafo
  del blog muestran la entidad Post y el store sigue teniendo un solo documento para
  ella.

  - Compilar desde un spec autorado y desde la proyección equivalente del grafo da
  representaciones intermedias estructuralmente equivalentes según la misma normalización.

  - specIR no define ninguna clase con el nombre de un modelo de vocabulario visual
  de SLDB.

  - Ningún módulo bajo src/specir/ importa spec2viz (prueba de imports); spec2viz
  solo aparece importado en pruebas de paridad bajo tests/.'
output_scope:
- src/specir/visual/__init__.py
- src/specir/visual/spec_models.py
- src/specir/visual/loader.py
- src/specir/visual/validator.py
- src/specir/visual/ir.py
- src/specir/visual/compilers.py
- src/specir/visual/projections.py
- tests/visual/test_spec_models.py
- tests/visual/test_compilers.py
- tests/visual/test_projections.py
depends_on:
- IR07
- IR06
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:ROOT
id: ROOT
title: 'specIR: MCP sobre SLDB y reemplazo funcional de spec2viz'
owner_repo: specIR
children:
- IR01
- IR02
- IR03
- IR04
- IR05
- IR06
- IR07
- IR08
- IR09
- IR10
- IR11
- IR12
- IR13
- IR13a
- IR13b
- IR13c
- IR13d
scope: Nuevo paquete periférico sobre la API pública de SLDB. El MCP entrega primero
  capacidades de lectura/escritura y análisis; la capa visual absorbe de forma gradual
  spec2viz. pron no será dependencia de ejecución; sus contratos necesarios se incorporan
  como MCPs en SLDB. spec2viz solo se retira cuando la matriz completa y el gate de
  retiro lo demuestren.
acceptance: Los 17 nodos de entrega cierran con evidencia y el gate externo G_SLDB_PRON_MCP
  queda satisfecho. El nodo IR13 final confirma toda la matriz de cobertura y los
  consumidores migrados antes de proponer retirar spec2viz.

FILE:instruccion
Revisa el nodo IR06 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

