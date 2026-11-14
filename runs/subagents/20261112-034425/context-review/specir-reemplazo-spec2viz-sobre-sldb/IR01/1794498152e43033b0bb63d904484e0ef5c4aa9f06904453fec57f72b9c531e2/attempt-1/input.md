FILE:desk/drawer/plans/specir/dag.yaml#node:IR01
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
Revisa el nodo IR01 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

