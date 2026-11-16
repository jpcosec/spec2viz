---
sldb:
  by: agent
  at: '2026-11-16T03:35:23Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-decisión-de-jp-g5-del-retiro-archivar-el-store-spec2viz-sldb-con-el-repo-o-reapuntar-sus-7-modelos-a.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb, workspace:desk
tags:
- workspace:desk
---

# spec2viz Board

## Purpose

_Explain what this board routes and why it exists._

Enruta el trabajo de spec2viz (specs de diagrama, notacion declarativa, sync al store sldb, catalogo) por los rituales execution, testing y closeout del ciclo de vida de deskops.

## Notes

_Add short operational notes about the current routed set._

Las tasks de 2026-05 (spike D2, goldens PlantUML, renderer antonIA) y las de 2026-10 (vocabulario visual, contrato con graph_ui, atributos de arista, empaquetado, trazabilidad, grafo Python) estan cerradas por closeout commit. No hay tasks abiertas. El catalogo vivo es graph_ui sobre el store sldb; el bundle HTML es el export estatico.

## Task Details

_Generated from the task references above._

- Decisión de JP (G5 del retiro): archivar el store spec2viz/.sldb con el repo o reapuntar sus 7 modelos a sldb [draft] - JP elige una de dos opciones y la decisión queda registrada en este desk y comunicada a IR: (A) archivar el store junto con el repo spec2viz cuando specir retirement check dé 0 (sin tocar el store ahora; IR quita el path spec2viz/.sldb del universo del comprobador y cambia la federación de sus pruebas por un fixture), o (B) mantener el store vivo después del retiro y reapuntar los 7 modelos a los públicos de sldb (sldb.models.notation.{spec_doc.SpecDoc, spec_node_doc.SpecNodeDoc, notation_doc.NotationDoc, glyph_doc.GlyphDoc, link_doc.LinkDoc, palette_doc.PaletteDoc, view_doc.ViewDoc}, fila SV-A17 de IR/docs/spec2viz/matriz-de-cobertura.md) con el CLI sldb, nunca a mano. Recomendación del coordinador: A, porque ningún consumidor fuera de las pruebas de IR lee este store y la decisión 6 del acta ya archiva el repo entero.
