---
id: atom-intermediate-representation-what
title: Intermediate Representation
five_wh_one_plus: what
tags:
- system:spec2viz
- topic:ir
provenance: spec2viz/ir.py
---

# Intermediate Representation

## Answer

La Representacion Intermedia (IR) es la coleccion de dataclasses puras de spec2viz/ir.py (SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR, ClassIR, MatrixIR) que representan un diagrama listo para dibujar, mas el EnforcementArtifact de reflection. Los compiladores la producen y los renderers la consumen.
