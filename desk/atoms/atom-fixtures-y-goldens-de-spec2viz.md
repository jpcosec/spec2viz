---
id: atom-fixtures-y-goldens-de-spec2viz
title: Fixtures y goldens de spec2viz
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:testing
provenance: desk/contexts/pill-test-fixture-spec2viz-fixtures-and-golden-outputs.md
---

# Fixtures y goldens de spec2viz

## Answer

Los goldens (examples/*.puml, docs/architecture/spec2viz/*.mmd, fixtures de tests) son expectativas ejecutables, no capturas incidentales. Ante un cambio que los toque se regenera el artefacto afectado con el pipeline actual (spec2viz diagram render), se compara con el golden y se explica si cada diff es intencional; en tareas por lotes se verifica que todos los artefactos esperados se regeneren y que ningun golden ajeno cambie. No se sobreescriben goldens en masa para poner los tests en verde ni se mezclan cambios de esquema de fixtures con cambios de renderer salvo que la tarea los acople.
