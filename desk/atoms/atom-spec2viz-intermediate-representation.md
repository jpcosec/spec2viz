---
id: atom-spec2viz-intermediate-representation
title: Intermediate Representation (IR) Decoupling
five_wh_one_plus: why
tags:
- system:spec2viz
- topic:architecture
- topic:ir
provenance: README.md
---

# Intermediate Representation (IR) Decoupling

## Answer

`spec2viz` utiliza una Representación Intermedia (IR) desacoplada basada en dataclasses de Python para separar completamente los compiladores de especificaciones fuente de los renderizadores de salida. Sin una IR, añadir un nuevo tipo de diagrama o un nuevo backend de renderizado requeriría implementar $M \times N$ conversiones directas. La IR reduce la complejidad a $M + N$, permitiendo que los compiladores traduzcan el esquema Pydantic en una estructura gráfica agnóstica (`SequenceIR`, `ComponentIR`, `StateIR`), y que cualquier renderizador (PlantUML, Mermaid, D2) la proyecte sin conocer los detalles del YAML original.
