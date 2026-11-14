FILE:desk/drawer/plans/specir/dag.yaml#node:IR08
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

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR06
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
Revisa el nodo IR08 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

