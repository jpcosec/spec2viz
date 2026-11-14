FILE:desk/drawer/plans/specir/dag.yaml#node:IR04
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

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR02
id: IR02
title: 'IR02 Decisión: contrato de escritura y nivel de mutabilidad del MCP'
kind: decision
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Un registro de decisión en docs/decisiones/contrato-de-escritura-mcp.md con
  cuatro decisiones tomadas por el dueño del proyecto (qué es una propuesta de cambio,
  qué precondición protege la aplicación, dónde se declara el nivel de escritura permitido,
  y si existe deshacer), y un atom durable por cada decisión que la deja disponible
  para las demás tareas.


  Alcance:

  Dentro: (a) propuesta de cambio como lote prevalidado sin persistir o como documento
  persistente; (b) precondición que impide aplicar sobre un store que cambió desde
  la validación; (c) dónde se declara el nivel de escritura permitido (contenido,
  reglas y tipos de relación, modelos): al arrancar el servidor, en un documento del
  store, o por actor; (d) si hay una operación de deshacer o basta la historia en
  git. Fuera: implementar; decidir permisos multiusuario.'
acceptance: 'El registro de decisión está completo con la elección del dueño, los
  cuatro atoms existen y apuntan a él, y la tarea de escritura por MCP puede citar
  un mecanismo concreto para cada principio.


  Validación:

  - docs/decisiones/contrato-de-escritura-mcp.md existe y tiene una sección por cada
  una de las cuatro decisiones, cada una con alternativas, alternativa elegida, motivo,
  fecha y quién decidió.

  - Cada sección nombra la operación de la API pública de SLDB que sostiene la alternativa
  elegida según la matriz de auditoría, o la carencia notificada a SLDB.

  - Existe un atom por cada decisión, su campo provenance apunta al registro y su
  texto coincide con la alternativa elegida en el registro.

  - El registro lista los ids de los cuatro atoms y las referencias de la tarea los
  incluyen.

  - Ninguna decisión introduce un camino de escritura al store que no pase por la
  API pública de SLDB.

  - El atom de principios de seguridad de la superficie MCP cita los mecanismos decididos
  y ya no los declara pendientes.'
output_scope:
- docs/decisiones/contrato-de-escritura-mcp.md
depends_on:
- IR01
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR03
id: IR03
title: IR03 Servidor MCP de solo lectura sobre un store SLDB real
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Un servidor MCP de solo lectura, en el paquete specIR, con el que un agente
  descubre modelos, lee documentos, recorre relaciones y resuelve vistas de un store
  SLDB.


  Alcance:

  Dentro: servidor MCP por stdio sobre la API pública de SLDB con tools para listar
  y describir modelos y tipos de relación, leer un documento o un campo, vecinos y
  recorrido por relación, búsqueda por predicados, resolver una vista (ViewDoc o SpecDoc)
  a JSON, e integridad del store. Fuera: cualquier escritura, tipos de dominio nuevos,
  extractores, renderizado de diagramas.'
acceptance: 'Las pruebas anteriores pasan sobre la copia aislada del store real de
  este repo y un agente conectado al servidor recorre ese store sin escribir en él.


  Validación:

  - Las pruebas corren con un cliente MCP real contra el servidor real lanzado por
  stdio sobre la copia aislada del store de este repo; cada tool devuelve JSON estructurado
  y, por cada documento, su dirección estable.

  - Los documentos que devuelven las tools existen en el store original con el mismo
  id y contenido (comparación contra los archivos de desk/ del repo).

  - Todo conjunto llega paginado, con su total y una marca cuando quedó cortado; se
  prueba sobre el modelo con más documentos del store.

  - El SpecDoc real class.sldb-models del store de spec2viz resuelve desde la federación
  de la copia, y las tools de lectura y de resolución de vistas lo devuelven con el
  mismo contenido que tiene en ../spec2viz/.sldb; si el store o el documento faltan,
  la prueba falla nombrando cuál falta.

  - Montar la copia y ejecutar todas las tools de lectura no modifica ningún archivo
  de la copia ni de los stores federados de deskops y de spec2viz (comparación del
  árbol antes y después).

  - El store original del repo no cambia durante las pruebas (comparación del árbol
  de .sldb/ y desk/ antes y después).

  - Una consulta sobre algo que el store no declara devuelve conjunto vacío con explicación,
  no un error opaco.

  - Una prueba de imports comprueba que el paquete no importa pron, spec2viz, ni módulos
  de SLDB fuera de sldb.api.

  - Ninguna prueba crea documentos de contenido inventado ni sustituye la API de SLDB,
  el servidor o el cliente por un doble.'
output_scope:
- pyproject.toml
- src/specir/__init__.py
- src/specir/mcp/__init__.py
- src/specir/mcp/server.py
- src/specir/mcp/read_tools.py
- src/specir/mcp/addresses.py
- src/specir/mcp/paging.py
- tests/conftest.py
- tests/mcp/test_read_tools.py
- tests/mcp/test_no_writes.py
- tests/test_imports.py
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
- IR13A
- IR13B
- IR13C
- IR13D
scope: Nuevo paquete periférico sobre la API pública de SLDB. El MCP entrega primero
  capacidades de lectura/escritura y análisis; la capa visual absorbe de forma gradual
  spec2viz. pron no será dependencia de ejecución; sus contratos necesarios se incorporan
  como MCPs en SLDB. spec2viz solo se retira cuando la matriz completa y el gate de
  retiro lo demuestren.
acceptance: Los 17 nodos de entrega cierran con evidencia; el gate final de IR13 confirma
  toda la matriz de cobertura y los consumidores migrados antes de proponer retirar
  spec2viz.

FILE:instruccion
Revisa el nodo IR04 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

