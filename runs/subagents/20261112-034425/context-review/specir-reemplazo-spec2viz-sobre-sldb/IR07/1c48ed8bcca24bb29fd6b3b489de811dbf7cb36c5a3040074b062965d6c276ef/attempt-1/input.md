FILE:desk/drawer/plans/specir/dag.yaml#node:IR07
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

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR13
id: IR13
title: IR13 Migración de consumidores y gate final de retiro de spec2viz
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'Un comprobador del gate de retiro y un acta que demuestran, con evidencia,
  que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor
  importa ni invoca spec2viz.


  Alcance:

  Dentro: comprobador del gate de retiro, que lee la matriz de cobertura y verifica
  que cada fila tiene su condición cumplida con una prueba citada, y que recorre en
  solo lectura el universo auditado buscando dependencias de spec2viz. Universo auditado:
  exactamente los repos consumidores y los stores que lista el inventario de consumidores
  de docs/spec2viz/matriz-de-cobertura.md, más el propio repo de specIR; un repo o
  store que no esté en ese inventario no se audita, y añadir uno exige actualizar
  primero el inventario. Qué cuenta como dependencia: importaciones de spec2viz en
  código (import spec2viz o from spec2viz); dependencias declaradas en configuración
  ejecutable (pyproject.toml, requirements, archivos de CI, Makefile y scripts); puntos
  de entrada y llamadas al comando spec2viz en código, scripts o configuración ejecutable;
  llamadas a su API Python; y modelos spec2viz.sldb_models registrados en un índice
  de store. Qué no cuenta: menciones en texto, documentación, comentarios, changelogs
  o documentos del desk. Salida: por cada dependencia remanente, el repo o store,
  la ruta del archivo, la línea y la clase de dependencia; con al menos una, el gate
  falla con código de salida distinto de cero y el retiro no se puede declarar; pedidos
  de migración a los desks de graph_ui, deskops y de cada repo con stores afectados;
  acta de retiro con la evidencia por fila y por consumidor; actualización de la matriz
  de cobertura con esa evidencia.

  Fuera: implementar capacidades de spec2viz, que corresponden a las tareas de compiladores,
  renderers, IR13a, IR13b, IR13c e IR13d; editar archivos de otros repos; archivar
  o borrar el repo spec2viz, que es decisión de su dueño una vez cumplido el gate.'
acceptance: 'El comprobador termina con código de salida cero sobre todo el universo
  auditado, el acta de retiro está completa y declara el retiro, y spec2viz puede
  archivarse sin que ningún repo del workspace falle.


  Validación:

  - El comprobador falla sobre una matriz de entrada con una fila sin prueba citada
  y pasa cuando todas la tienen.

  - Sobre un repo de entrada con una importación de spec2viz en código, una dependencia
  en pyproject.toml y una llamada al comando spec2viz en un script, y un índice de
  store con un modelo spec2viz.sldb_models, el comprobador reporta las cuatro con
  repo, ruta, línea y clase de dependencia, termina con código de salida distinto
  de cero y no modifica ningún archivo.

  - Sobre un repo de entrada que solo menciona spec2viz en documentación, comentarios
  y un changelog, el comprobador no reporta ninguna dependencia.

  - El comprobador audita exactamente los repos y stores del inventario de la matriz
  de cobertura más el repo de specIR, y falla con un error que lo dice si se le pide
  auditar uno que no está en el inventario o si falta la ruta de uno que sí está.

  - Ejecutado sobre todos los repos y stores reales del inventario, el comprobador
  no reporta ninguna dependencia y termina con código de salida cero.

  - La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente
  declarado en la matriz de cobertura.

  - El acta de retiro lista, por cada consumidor del inventario, el mensaje enviado
  a su desk, la referencia del cambio que lo resolvió y la salida del comprobador;
  si quedó alguna dependencia, el acta dice que el retiro no está declarado.

  - Toda fila de la matriz de cobertura tiene su condición de retiro cumplida y su
  prueba citada.'
output_scope:
- src/specir/visual/retirement.py
- src/specir/cli.py
- tests/visual/test_retirement_gate.py
- docs/spec2viz/acta-de-retiro.md
- docs/spec2viz/matriz-de-cobertura.md
depends_on:
- IR13A
- IR13B
- IR13C
- IR13D
- IR07
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR13A
id: IR13A
title: IR13a Sincronización de specs al store y generación de specs
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'specIR materializa un spec en el store y genera specs de componentes desde
  un grafo y desde código Python, con el mismo resultado que spec2viz.


  Alcance:

  Dentro: sincronización de un spec al store como SpecDoc, SpecNodeDoc y RelationDoc,
  con creación del RelationTypeDoc que falte y borrado de los documentos que salieron
  del spec; compilación de un grafo de store o de un snapshot a un spec de componentes;
  generación de un spec de componentes desde el AST de Python. Cada pieza se migra
  tal cual o se reemplaza, según el modo que le asigne la matriz de cobertura.

  Fuera: catálogos; notaciones y paletas; CLI; migración de consumidores; retirar
  spec2viz.'
acceptance: 'Las pruebas anteriores pasan y las filas de sincronización, importación
  de grafo y generación de la matriz de cobertura tienen su condición de retiro cumplida.


  Validación:

  - Sincronizar un spec con specIR deja en un store de prueba los mismos SpecDoc,
  SpecNodeDoc y RelationDoc que spec2viz sobre los fixtures de sincronización.

  - Volver a sincronizar tras quitar un elemento del spec borra su SpecNodeDoc y sus
  RelationDoc.

  - Una relación de tipo no builtin crea su RelationTypeDoc y el índice de aristas
  valida después de sincronizar.

  - La compilación desde grafo produce, sobre el fixture de snapshot de spec2viz,
  un spec de componentes que valida y es equivalente al de spec2viz, o su reemplazo
  por proyección tiene la prueba equivalente declarada en la matriz.

  - La generación desde AST produce, sobre un paquete Python de fixture, un spec de
  componentes equivalente al de spec2viz.

  - El paquete no importa spec2viz.'
output_scope:
- src/specir/visual/sync.py
- src/specir/visual/graph_import.py
- src/specir/visual/generate_python.py
- tests/visual/test_sync.py
- tests/visual/test_graph_import.py
- tests/visual/test_generate_python.py
depends_on:
- IR07
- IR11
requires: []

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR13C
id: IR13C
title: IR13c Notaciones y paletas expuestas desde specIR
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'specIR expone las operaciones de notaciones y paletas de spec2viz delegando
  en la API pública de SLDB, sin redefinir sus modelos.


  Alcance:

  Dentro: listar, validar, sincronizar al store y resolver la vista de notaciones
  (NotationDoc, GlyphDoc, LinkDoc); listar, validar y sincronizar paletas (PaletteDoc),
  incluida la comprobación de contraste; todo como envoltorio de las operaciones de
  SLDB.

  Fuera: redefinir modelos de vocabulario visual o reimplementar el resolvedor de
  vistas; catálogos; CLI general; migración de consumidores.'
acceptance: 'Las pruebas anteriores pasan y las filas de notaciones y paletas de la
  matriz de cobertura tienen su condición de retiro cumplida.


  Validación:

  - Listar notaciones y paletas desde specIR devuelve las builtin que distribuye SLDB.

  - Validar una notación o una paleta inválida de los fixtures reporta los mismos
  problemas que spec2viz, incluido el contraste insuficiente.

  - Sincronizar una notación desde specIR deja en un store de prueba sus NotationDoc,
  GlyphDoc y LinkDoc.

  - La vista resuelta de un spec de fixture desde specIR es igual a la que devuelve
  la API pública de SLDB para ese spec.

  - specIR no define ninguna clase con el nombre de un modelo de vocabulario visual
  de SLDB, y el módulo no importa spec2viz.'
output_scope:
- src/specir/visual/notations.py
- tests/visual/test_notations.py
- tests/visual/test_palettes.py
depends_on:
- IR07
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
Revisa el nodo IR07 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

