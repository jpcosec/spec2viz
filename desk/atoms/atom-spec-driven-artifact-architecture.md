---
id: atom-spec-driven-artifact-architecture
title: Spec-Driven Artifact Architecture
five_wh_one_plus: why
tags:
- system:spec2viz
- topic:architecture
- topic:principles
provenance: README.md
---

# Spec-Driven Artifact Architecture

## Answer

Las representaciones gráficas de arquitectura (como archivos Mermaid `.mmd` o PlantUML `.puml`) no deben editarse manualmente ni mantenerse como fuentes primarias. La arquitectura se define mediante especificaciones semánticas estructuradas en YAML (`Spec-Driven`). Los archivos gráficos visuales son **proyecciones generadas** a partir del YAML. Este principio garantiza que los diagramas sean versionables por Git, auditables por modelos LLM, validados por esquemas Pydantic y reproducibles de forma determinista.
