---
# pill-xxx
id: pill-adr-spec2viz-es-dueño-del-vocabulario-visual-graph-ui-de-la-vista-generica-y-los-gestos
status: active
summary: La notacion (NotationDoc, GlyphDoc, LinkDoc) se declara en spec2viz y vive
  en el store sldb; graph_ui la interpreta en vivo. El bundle HTML pasa a ser export
  estatico.
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

Reparto entre spec2viz y graph_ui para que los specs corran sobre graph_ui: spec2viz define los modelos Pydantic NotationDoc (nivel, tipo de diagrama, layout), GlyphDoc (modelo + predicado where -> forma, rotulo, compartimentos) y LinkDoc (relacion -> trazo line|nest|lane|cell|axis, linea, terminales) en spec2viz.sldb_models, los valida y los escribe al store con 'spec2viz diagram sync' y 'spec2viz notation sync'. graph_ui es dueño de la vista generica que lee SpecDoc.notation -> NotationDoc -> glyphs/links y dibuja, y de GestureDoc y la edicion de vuelta. Pilotos: UML de clases y statechart.

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

Toda regla de dibujo nueva va en un YAML de notacion (GlyphDoc/LinkDoc), nunca en un if por notacion dentro de un renderer ni en graph_ui. Los campos ref son planos (model, where, relation) mas un 'form' opcional con la forma pron; LinkDoc lleva relation_type como referencia RelationTypeDoc:reltype-<rel> para que el indice de aristas vea que relacion nombra; el modelo se valida en sync porque el indice no resuelve refs a modelos. Las posiciones de vista no entran al YAML del spec ni al store de spec2viz.

## How Not

_Describe the shortcut or failure mode to avoid._

No meter React Flow, pron ni formas en spec2viz; no cablear colores o iconos por clase en codigo (anti-patron shared/classes.mjs); no hacer que spec2viz escriba de vuelta al YAML desde gestos; no usar claves on/off/yes/no en los YAML de notacion (YAML 1.1 los lee como booleanos).
