FILE:desk/drawer/plans/specir/dag.yaml#node:IR12
id: IR12
title: IR12 Renderers, linter y recursos estáticos de spec2viz
kind: code
owner_repo: specIR
node_role: delivery
parent_id: ROOT
scope: 'specIR produce todos los formatos de salida de spec2viz a partir de la representación
  intermedia, con paridad verificable, y distribuye los recursos que esos formatos
  necesitan.


  Alcance:

  Dentro: renderizadores Mermaid, PlantUML, D2, Vega, BPMN y su visor, árbol, HTML
  de grafo, antonia HTML y salida JSON; linter de Mermaid; export de JSON Schema de
  specs y de catálogos; recursos empaquetados: plantillas HTML, bpmn-js y los que
  requiera cada formato; comandos equivalentes a render, lint y schema. Cada pieza
  se migra tal cual o se reemplaza, según la matriz de cobertura.

  Fuera: compiladores; sincronización al store, catálogos y consumidores; retirar
  spec2viz.'
acceptance: 'Las pruebas de paridad de renderizadores, linter y schema pasan en specIR
  y sus filas de la matriz de cobertura tienen la condición de retiro cumplida.


  Validación:

  - Por cada renderizador, los fixtures de spec2viz producen en specIR una salida
  idéntica a su golden, o la diferencia está declarada en la matriz de cobertura con
  su prueba equivalente.

  - El linter de Mermaid reporta en specIR los mismos hallazgos que en spec2viz sobre
  los fixtures de lint.

  - El JSON Schema exportado por specIR para specs y catálogos es igual al de spec2viz,
  o la diferencia está declarada.

  - El HTML del visor BPMN y el HTML de grafo generados abren sin recursos externos
  faltantes (prueba de empaquetado).

  - Todos los valores del selector de renderizador de spec2viz existen en specIR.

  - El paquete no importa spec2viz.'
output_scope:
- src/specir/visual/renderers/__init__.py
- src/specir/visual/renderers/mermaid.py
- src/specir/visual/renderers/plantuml.py
- src/specir/visual/renderers/d2.py
- src/specir/visual/renderers/vega.py
- src/specir/visual/renderers/bpmn.py
- src/specir/visual/renderers/tree.py
- src/specir/visual/renderers/graph_html.py
- src/specir/visual/renderers/antonia_html.py
- src/specir/visual/renderers/json_out.py
- src/specir/visual/lint_mermaid.py
- src/specir/visual/schema.py
- src/specir/visual/templates/default.html
- tests/visual/test_renderers.py
- tests/visual/test_lint_mermaid.py
- tests/visual/test_schema.py
- tests/visual/test_resources.py
depends_on:
- IR11
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
Revisa el nodo IR12 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

