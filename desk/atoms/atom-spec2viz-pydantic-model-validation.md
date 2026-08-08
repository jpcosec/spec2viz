---
id: atom-spec2viz-pydantic-model-validation
title: Pydantic Model Validation and Strict Schema Enforcement
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:validation
- topic:models
provenance: README.md
---

# Pydantic Model Validation and Strict Schema Enforcement

## Answer

El parseo de archivos YAML en `spec2viz` se realiza a través de modelos Pydantic estrictos (`BaseDiagram`, `SequenceDiagram`, `ComponentDiagram`, etc.) que utilizan discriminadores por tipo (`type`). Esto asegura que cualquier error sintáctico, tipo de dato incorrecto o campo no reconocido en la especificación fuente falle temprano (*fail-fast*) durante la fase de carga (`spec2viz.loader`), emitiendo excepciones `ParseError` con mensajes de diagnóstico claros antes de intentar cualquier compilación o renderizado gráfico.
