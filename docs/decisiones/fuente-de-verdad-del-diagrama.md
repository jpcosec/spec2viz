# Fuente de verdad del diagrama: el grafo de SLDB y el papel del YAML de spec

**Estado: aceptada por JP el 2026-11-15** (transmitida por el supervisor con autorización explícita). El
YAML del spec queda como formato de autoría e intercambio subordinado al grafo, en los términos de la
sección «Decisión» de abajo. El atom que la registra en el desk es
`atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`;
la propuesta de IR07 (`atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`)
se fusionó en él con `deskops atoms merge` y queda como redirección. El modelo de atom de deskops no tiene
campo de estado, así que el estado va en el título y en la respuesta. Con esto el ítem G7 del gate de
retiro (`docs/spec2viz/matriz-de-cobertura.md`) queda cumplido.

## Contexto

Conviven dos modelos de diagrama:

- **spec2viz**: el YAML del spec es la fuente; el store es derivado (`spec2viz diagram sync` materializa
  el spec como SpecDoc, SpecNodeDoc y RelationDoc).
- **specIR**: la fuente semántica es el grafo de SLDB (entidades extraídas o autoradas, sus aristas); un
  diagrama es una **vista** (aparición de entidades bajo una notación), no una segunda copia de las
  entidades (atom `atom-entidad-aparición-proyección-y-notación-son-cosas-distintas`).

Dado que la fuente semántica es el grafo (premisa fijada por la tarea IR07), queda por decidir el papel
del YAML de spec, cómo se dibuja lo que aún no existe en el grafo y qué pasa con los specs existentes.

## Decisión

1. **El YAML de spec se conserva de forma permanente como formato de autoría e intercambio, subordinado
   al grafo.** Es la forma revisable en un diff de autorar una vista o un diseño. No es fuente de las
   entidades: al sincronizarlo (SpecSync, D1: `sldb notations sync --spec`) sus elementos pasan a
   SpecNodeDoc del store, y un elemento que representa una entidad existente se ancla a ella con un
   vínculo explícito (`atoms:`/`refs:` por elemento, resuelto por `sldb.api.matching`, D4). Ante un
   conflicto entre el YAML y el grafo, gana el grafo y la diferencia se reporta como hallazgo; el YAML no
   sobrescribe documentos de entidad.
2. **Los diagramas de lo que ya existe se producen como proyección del grafo** (ViewDoc evaluado por
   `sldb.api.notations.evaluate_projection_view`, o un spec de componentes generado con
   `sldb notations from-graph`, D2), no se escriben a mano. Un YAML autorado para algo que ya está en el
   grafo es válido solo como vista curada (selección, orden, agrupación, notación), y sus elementos van
   anclados.
3. **Regla para diseño previo a la implementación.** Lo que aún no existe en el grafo se autora en el YAML
   del spec como elemento **sin ancla**. SpecSync lo materializa como SpecNodeDoc propio del spec (no como
   entidad del dominio). Cuando la implementación aparece en el grafo (un extractor o una autoría crea la
   entidad), el elemento se ancla por vínculo explícito y el diagrama pasa a validarse contra el grafo.
   Un chequeo determinista lista los elementos sin ancla de cada spec como «diseño pendiente de
   implementar»; no es error, es estado visible. Un elemento sin ancla cuyo nombre empareja con una
   entidad existente (emparejamiento difuso de D4) se reporta como «posible ancla» para que alguien lo
   confirme; nunca se ancla solo.
4. **Destino de los specs YAML existentes.** Se quedan donde están, sin reescritura masiva ni borrado
   desde specIR:
   - Durante la paridad son fixtures: los de `spec2viz/tests/fixtures/`, `spec2viz/examples/` y
     `spec2viz/docs/architecture/spec2viz/` se portan como fixtures de las pruebas de paridad (IR11,
     IR12, D3) y deben validar con `sldb.api.notations.load_spec` con los mismos errores tipados.
   - Tras el retiro, cada repo (sldb, graph_ui, pron, deskops; inventario en la matriz) decide por su
     desk, a pedido de IR13: los specs que describen código ya presente en el grafo pueden pasar a
     proyección cuando la prueba de equivalencia lo muestre; los de diseño se mantienen como YAML,
     validados con sldb y sincronizados con `sldb notations sync --spec`.
   - La ruta `docs/architecture/spec2viz` que reconoce el grafo del desk de deskops
     (`deskops/deskops/graph/desk_graph.py:75`) se renombra o generaliza por pedido al desk de deskops;
     specIR no la toca.

## Alternativas descartadas

- **El YAML como fuente y el store como derivado (el modelo de spec2viz tal cual).** Duplica entidades:
  la misma clase o componente existe como entidad del grafo y como nodo del spec, y nada obliga a que
  coincidan. Contradice la premisa de que la fuente semántica es el grafo.
- **El YAML solo durante la paridad y después solo proyecciones.** Deja sin forma de dibujar un diseño
  antes de implementarlo, y obliga a reescribir o borrar specs vigentes en cinco repos sin beneficio
  verificable. También pierde el formato de intercambio revisable en diffs.
- **Autorar siempre en el store (CLI o MCP de sldb) sin YAML.** Viable para agentes, pero quita la
  revisión por diff de un archivo y rompe los flujos de catálogo (`vistas.yml`) y los specs existentes. Se
  puede reconsiderar si el MCP llega a cubrir la autoría de vistas con revisión equivalente.

## Efecto sobre la matriz

Las filas marcadas con † en `docs/spec2viz/matriz-de-cobertura.md` dependen de esta decisión: el
inventario de specs existentes y la regla de rutas de deskops. El resto de las filas no cambia de modo
con ninguna de las alternativas.
