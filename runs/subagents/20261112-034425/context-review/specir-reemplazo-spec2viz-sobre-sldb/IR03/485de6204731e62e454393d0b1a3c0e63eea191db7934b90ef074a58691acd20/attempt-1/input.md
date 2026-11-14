FILE:desk/drawer/plans/specir/dag.yaml#node:IR03
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
Revisa el nodo IR03 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

