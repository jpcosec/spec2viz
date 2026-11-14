FILE:desk/drawer/plans/specir/dag.yaml#node:IR13
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

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR13B
id: IR13B
title: IR13b Catálogos, anotaciones y emparejamiento de átomos
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'specIR construye, sincroniza, valida y sirve catálogos de diagramas, con anotaciones
  y con los átomos emparejados a cada elemento, cubriendo lo que hace spec2viz.


  Alcance:

  Dentro: registro de vistas (vistas.yml) y stores jerárquicos de diagramas; construcción
  del catálogo HTML autocontenido; sincronización del catálogo al store; validación
  del registro; servidor local con autoguardado de anotaciones; emparejamiento de
  átomos con elementos de diagrama (explícito y difuso) y cobertura por vista. Cada
  pieza se migra tal cual o se reemplaza, según la matriz de cobertura.

  Fuera: sincronización de un spec individual; notaciones y paletas; CLI; migración
  de consumidores.'
acceptance: 'Las pruebas anteriores pasan y las filas de catálogo y de emparejamiento
  de átomos de la matriz de cobertura tienen su condición de retiro cumplida.


  Validación:

  - La validación de un registro de vistas reporta en specIR los mismos errores tipados
  que spec2viz sobre los fixtures de catálogo.

  - La sincronización del catálogo deja en un store de prueba el mismo contenido que
  spec2viz, y no escribe nada si alguna vista falla.

  - El catálogo construido contiene las mismas vistas, categorías y navegación que
  el de spec2viz sobre el fixture, y abre sin recursos externos faltantes.

  - Una anotación hecha en el servidor local queda guardada y reaparece al recargar.

  - El emparejamiento de átomos reporta los mismos átomos por elemento y la misma
  cobertura por vista que spec2viz sobre los fixtures de átomos; un id de átomo desconocido
  es advertencia, o error en modo estricto.

  - El paquete no importa spec2viz.'
output_scope:
- src/specir/visual/catalog.py
- src/specir/visual/catalog_serve.py
- src/specir/visual/atoms.py
- tests/visual/test_catalog.py
- tests/visual/test_catalog_serve.py
- tests/visual/test_atoms_matching.py
depends_on:
- IR13A
- IR12
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

FILE:desk/drawer/plans/specir/dag.yaml#edge:IR13D
id: IR13D
title: IR13d CLI, API Python y habilidad de agente de la capa visual
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'specIR ofrece un comando, una API Python pública y una habilidad de agente
  que cubren cada entrada pública de spec2viz.


  Alcance:

  Dentro: comando de specIR con equivalentes de todos los comandos y subgrupos de
  spec2viz (diagram, notation, palette, catalog, y los alias de primer nivel render,
  validate, lint, schema y build, y about); API Python pública equivalente a la que
  exporta el paquete spec2viz; habilidad de agente que reemplaza a la de uso de spec2viz;
  tabla de correspondencia comando por comando.

  Fuera: implementar las capacidades, que vienen de las tareas de compiladores, renderers,
  IR13a, IR13b e IR13c; instalar la habilidad en otros repos; migrar consumidores.'
acceptance: 'Las pruebas anteriores pasan y las filas de CLI, API Python y habilidad
  de la matriz de cobertura tienen su condición de retiro cumplida.


  Validación:

  - Cada comando y subgrupo que lista la ayuda de spec2viz tiene una fila en la tabla
  de correspondencia con su equivalente en specIR, y una prueba invoca cada equivalente.

  - Las pruebas de API de spec2viz portadas pasan contra la API pública de specIR.

  - La habilidad de agente nombra solo comandos que existen en el comando de specIR
  (comprobado por una prueba que los extrae y los invoca con ayuda).

  - El paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado.'
output_scope:
- src/specir/cli.py
- src/specir/visual/__init__.py
- skills/use-specir/SKILL.md
- docs/spec2viz/correspondencia-cli.md
- tests/visual/test_cli.py
- tests/visual/test_api.py
- tests/visual/test_packaging.py
depends_on:
- IR13A
- IR13B
- IR13C
- IR12
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
Revisa el nodo IR13 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

