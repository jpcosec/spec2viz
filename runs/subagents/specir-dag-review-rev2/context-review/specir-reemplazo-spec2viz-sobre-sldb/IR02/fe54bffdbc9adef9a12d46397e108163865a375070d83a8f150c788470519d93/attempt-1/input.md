FILE:desk/drawer/plans/specir/dag.yaml#node:IR02
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

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR01
id: IR01
title: IR01 Auditoría de la API pública de SLDB frente a la superficie MCP
kind: docs
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Una matriz que diga, capacidad por capacidad, qué necesita la superficie MCP
  de specIR y si la API pública de SLDB ya lo ofrece, hay que extenderlo en SLDB,
  o falta.


  Alcance:

  Dentro: una fila por capacidad de la superficie MCP: listar y describir modelos
  y tipos de relación; leer documento y campo; vecinos y recorrido del grafo; búsqueda
  por predicados; resolver una vista; escritura validada de documentos y aristas;
  reglas (RuleDoc) y transiciones; creación y edición de modelos; integridad; historia;
  identificador de estado del store utilizable como precondición de escritura; forma
  de deshacer una escritura. Fuera: escribir código, modificar SLDB, diseñar las tools.'
acceptance: 'La matriz está escrita, cada fila tiene estado y cita, y los faltantes
  reales (si los hay) están notificados a SLDB.


  Validación:

  - Cada fila de la matriz cita una ruta existente bajo sldb/src/sldb/api/ o declara
  explícitamente que la capacidad falta.

  - Ninguna fila se apoya en sldb.store, sldb.core ni en pron.

  - La matriz responde explícitamente si existe un identificador de estado del store
  y si existe una forma de deshacer una escritura.

  - Por cada fila marcada como faltante real existe una nota enviada al desk de SLDB;
  si no hay faltantes, el documento lo dice y no hay nota.'
output_scope:
- docs/auditoria/sldb-api-frente-a-mcp.md
depends_on: []
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
Revisa el nodo IR02 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

