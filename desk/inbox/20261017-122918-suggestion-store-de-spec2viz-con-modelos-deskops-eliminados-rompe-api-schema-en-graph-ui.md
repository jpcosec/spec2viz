---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-17T12:29:18'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T12:42:30'
---

# Store de spec2viz con modelos deskops eliminados: rompe /api/schema en graph_ui

_Describe the incoming message with enough evidence to triage._

Desde graph_ui (2026-10-17). El store /home/jp/proyectos/SLDB_1/spec2viz/.sldb tiene registrados 5 modelos que deskops borró en afdec7f (el ciclo de vida pasa al grafo de sldb): RoutineDoc (3 docs), ConditionDoc (12), ChecklistDoc (9), OperatorDoc (9), EdgeDoc (18). Consecuencia: con SLDB_STORE apuntando a este store, el /api/graph del mindmap responde bien (253 docs, incluidos 75 SpecNodeDoc y 88 RelationDoc), pero /api/schema da 500 con 'SLDBModelError: Attribute RoutineDoc not found in deskops.models'. Sin schema no cargan ni /documents/flow ni el mapa. Arreglo: correr la migración oficial de deskops, 'deskops desk update --root .' en seco y después con '--apply' (desregistra esos modelos con 'sldb models remove --with-documents' y escribe el grafo de rituales/relaciones). Hay que revisar que ningún SpecDoc/SpecNodeDoc/RelationDoc apunte a esos docs antes de aplicar. Después validar con 'SLDB_STORE=<este .sldb> python3 frontends/mindmap/serve.py 8099' en graph_ui: /api/schema tiene que responder 200. graph_ui está haciendo la misma migración sobre su propio store. Pendiente aparte: la decisión D3 (dónde viven NotationDoc/GlyphDoc/LinkDoc) la toma el usuario.
