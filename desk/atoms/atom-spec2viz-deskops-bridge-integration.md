---
id: atom-spec2viz-deskops-bridge-integration
title: Deskops Bridge and Artifact Binding
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:deskops
- topic:integration
provenance: README.md
---

# Deskops Bridge and Artifact Binding

## Answer

El puente de integración `spec2viz.deskops` conecta el motor de diagramación con la capa de conocimiento de `deskops`. Permite resolver referencias a artefactos del espacio de trabajo (`desk/atoms/`, `desk/tasks/`, `desk/contexts/`) indicados en las propiedades `atoms:` o `references:` de los nodos de diagramas. Gracias a este puente, `spec2viz` puede validar la existencia de los átomos en la base de conocimiento y enriquecer los diagramas generados con enlaces de trazabilidad hacia las decisiones de arquitectura.
