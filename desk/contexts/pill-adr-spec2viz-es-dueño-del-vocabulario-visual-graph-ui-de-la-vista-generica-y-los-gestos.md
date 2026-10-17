---
# pill-xxx
id: pill-adr-spec2viz-es-dueño-del-vocabulario-visual-graph-ui-de-la-vista-generica-y-los-gestos
status: active
summary: spec2viz completo se muestra sobre graph_ui. Toda notacion (un NotationDoc
  por tipo de diagrama) y el catalogo (SpecDoc por categoria) viven en el store sldb
  y graph_ui los dibuja; el bundle HTML queda como export deprecado.
# e.g., language:python, library:pydantic
tags:
- system:spec2viz
- system:graph_ui
- topic:notation
- topic:sldb
---

# ADR: spec2viz es dueño del vocabulario visual; graph_ui de la vista generica y los gestos

## What

_Define the context or guardrail this pill carries._

spec2viz completo corre sobre graph_ui, no solo dos pilotos: cada tipo de diagrama (class, state, component, deployment, sequence, activity, component_view_matrix, reflection) tiene su NotationDoc builtin con GlyphDoc/LinkDoc; cada spec se sincroniza al store con su notacion y sus metadatos de catalogo (category, nav, summary de vistas.yml); 'spec2viz notation view' es el unico interprete del contrato y graph_ui lo sirve y dibuja. El catalogo es la lista de SpecDoc por categoria en graph_ui. El bundle HTML (catalog build) pasa a export estatico deprecado, no es el producto.

## Why

_Explain why this context matters for safe execution._

graph_ui ya lee el store de spec2viz (/api/graph devuelve SpecDoc, SpecNodeDoc y RelationDoc sin tocar nada) pero infiere el dibujo de la forma del payload con una tabla fija clase->color. Su manual docs/representacion pide un primer mapeo declarado y aplicabilidad; spec2viz ya es dueño de los modelos de referencia de cada notacion (Pydantic por tipo de diagrama), asi que es el lugar natural del vocabulario. Decision del usuario el 2026-10-17; contradice la D3 de graph_ui/docs/representacion/plan-de-cierre.md, que hay que actualizar.

## When

_Describe when an agent should apply this pill._

Al añadir o cambiar cualquier regla de como se dibuja un tipo de diagrama (flechas, anidamiento, compartimentos, terminales) o al integrar spec2viz con graph_ui.

## Where

_Name the files, surfaces, or scope this pill applies to._

spec2viz/sldb_models.py, spec2viz/notation.py, spec2viz/notations/*.yml, spec2viz/sldb_sync.py, spec2viz/cli.py; en graph_ui la vista generica (frontends/mindmap) y docs/representacion/plan-de-cierre.md (D3).

## How

_Describe the correct way to apply this guidance._

Toda regla de dibujo nueva va en un YAML de notacion (GlyphDoc/LinkDoc), nunca en un if por notacion dentro de un renderer ni en graph_ui. Un tipo de diagrama nuevo = modelo Pydantic + extraccion en sldb_sync + notacion YAML + test de vista; nada en graph_ui. Los campos ref son planos (model, where, relation) mas form opcional; LinkDoc lleva relation_type como referencia RelationTypeDoc:reltype-<rel>; '*' es el link comodin para relaciones libres. Las posiciones de vista no entran al YAML del spec ni al store de spec2viz.

## How Not

_Describe the shortcut or failure mode to avoid._

No meter React Flow, pron ni formas en spec2viz; no cablear colores o iconos por clase en codigo (anti-patron shared/classes.mjs); no hacer que spec2viz escriba de vuelta al YAML desde gestos; no usar claves on/off/yes/no en los YAML de notacion (YAML 1.1 los lee como booleanos).
