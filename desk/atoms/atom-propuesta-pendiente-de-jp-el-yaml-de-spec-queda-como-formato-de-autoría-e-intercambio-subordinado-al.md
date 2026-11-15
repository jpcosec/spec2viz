---
sldb:
  by: agent
  at: '2026-11-15T21:33:03Z'
  authority: generated
  via: create_document
id: atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al
title: 'Propuesta pendiente de JP: el YAML de spec queda como formato de autoría e
  intercambio subordinado al grafo'
five_wh_one_plus: how
tags:
- system:specir
- system:spec2viz
- topic:migracion
- topic:fuente-de-verdad
provenance: docs/decisiones/fuente-de-verdad-del-diagrama.md
---

# Propuesta pendiente de JP: el YAML de spec queda como formato de autoría e intercambio subordinado al grafo

## Answer

ESTADO: PROPUESTA, PENDIENTE DE DECISIÓN DE JP (no aceptada; el modelo de atom no tiene campo de estado). Premisa: la fuente semántica es el grafo de SLDB y un diagrama es una vista. Recomendación: (1) el YAML de spec se conserva de forma permanente como formato de autoría e intercambio, subordinado al grafo: al sincronizarlo (SpecSync en sldb, D1) sus elementos pasan a SpecNodeDoc, y un elemento que representa una entidad existente se ancla a ella con vínculo explícito (atoms/refs, sldb.api.matching, D4); ante conflicto gana el grafo y la diferencia es un hallazgo. (2) Los diagramas de lo que ya existe se producen como proyección del grafo (ViewDoc evaluado o sldb notations from-graph, D2); un YAML sobre algo existente vale solo como vista curada con elementos anclados. (3) Diseño previo a la implementación: lo que aún no existe se autora en el YAML como elemento sin ancla, SpecSync lo materializa como SpecNodeDoc propio del spec y no como entidad; cuando la entidad aparece en el grafo se ancla por vínculo explícito; un chequeo determinista lista los elementos sin ancla como diseño pendiente de implementar y reporta posibles anclas por emparejamiento difuso sin anclarlas solo. (4) Specs YAML existentes (spec2viz, sldb, graph_ui, pron, deskops): se quedan donde están sin reescritura ni borrado desde specIR; durante la paridad son fixtures que deben validar con sldb.api.notations.load_spec con los mismos errores; tras el retiro cada repo decide por su desk, a pedido de IR13, pasar a proyección los que describen código existente cuando la prueba de equivalencia lo muestre y mantener como YAML los de diseño. Alternativas descartadas: YAML como fuente y store derivado (duplica entidades, contradice la premisa); YAML solo durante la paridad (sin forma de dibujar diseño previo, obliga a reescribir specs vigentes, pierde el diff revisable); autorar siempre en el store sin YAML (pierde revisión por diff y rompe vistas.yml; reconsiderable si el MCP cubre autoría de vistas con revisión equivalente). Detalle: docs/decisiones/fuente-de-verdad-del-diagrama.md.
