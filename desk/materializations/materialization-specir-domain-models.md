---
sldb:
  by: agent
  at: '2026-11-15T15:34:25Z'
  authority: generated
  via: create_document
id: materialization-specir-domain-models
title: specIR domain models
source_atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
- atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla
- atom-lo-desconocido-se-nombra-y-solo-un-humano-fuera-del-mcp-o-un-chequeo-determinista-verifica
- atom-omg-es-referencia-conceptual-no-dependencia
target_kind: python_module
target_identity: src/specir/models/domain.py
validation:
- TMPDIR=/dev/shm pytest -q tests
tags:
- system:specir
- topic:modelado
- topic:materialization
---

# specIR domain models

## Intent

The nine cross-layer domain types of specIR as StructuredNLDoc subclasses in the specIR package, each carrying the IR05 provenance (origen, verificacion, verificado_por, evidencia, desconocidos) and authority authored; no visual model of SLDB is redefined.
