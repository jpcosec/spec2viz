---
id: atom-spec2viz-sldb-boundary-contract
title: Spec2viz SLDB Boundary Contract
five_wh_one_plus: how
tags:
- system:spec2viz
- system:sldb
- topic:boundary
- topic:adr
provenance: README.md
---

# Spec2viz SLDB Boundary Contract

## Answer

El contrato de frontera entre `spec2viz` y `sldb` establece una separación clara de responsabilidades arquitectónicas:

1. **Dominio de SLDB:** `sldb` posee la infraestructura de documentos Markdown estructurados, modelos `StructuredNLDoc`, marcado reversible (`⸢rev•field⸥`), almacenamiento `.sldb` e índices de búsqueda física y semántica.
2. **Dominio de Spec2viz:** `spec2viz` posee las especificaciones estructuradas de diagramas (`BaseDiagram`), representaciones intermedias (`IR`) y proyectores visuales (`Mermaid`, `PlantUML`, `D2`, `Vega`).
3. **Mecanismo de Integración (HOW):** `spec2viz` consume los almacenes de `sldb` en modo lectura para validar trazabilidad de átomos (`desk/atoms/`) y referencias a documentos. `spec2viz` nunca muta directamente los payloads de documentos Markdown de `sldb`; en su lugar, delega las operaciones sobre campos y modelos a `sldb docs` y `sldb fields`.
