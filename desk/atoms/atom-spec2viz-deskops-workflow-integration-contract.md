---
id: atom-spec2viz-deskops-workflow-integration-contract
title: Spec2viz Deskops Workflow Integration Contract
five_wh_one_plus: how
tags:
- system:spec2viz
- system:deskops
- topic:integration
- topic:adr
provenance: spec2viz/deskops.py
---

# Spec2viz Deskops Workflow Integration Contract

## Answer

El contrato de integración de flujo de trabajo entre `spec2viz` y `deskops` define cómo se compilan los registros de arquitectura (`vistas.yml`) en paquetes HTML interactivos:

1. **Parseo de Átomos 5WH1+ (`parse_atoms`):** `spec2viz/deskops.py` escanea `desk/atoms/*.md`, extrae el frontmatter YAML y clasifica el contenido en las 7 dimensiones 5WH1+ (`what`, `why`, `how`, `how_not`, `when`, `where`, `for_whom`) indexándolas por título normalizado en `window.ATOMS_DB`.
2. **Orquestación de Vistas (`render_deskops`):** `spec2viz` procesa el archivo de registro `vistas.yml`, carga los diagramas proyectados (`.mmd`, `.svg`, `.html`) y genera la navegación de categorías (`{{NAV}}`) y secciones (`{{SECTIONS}}`).
3. **Inyección y Vinculación Dinámica (HOW):** En la plantilla `template.html`, se inyecta `window.ATOMS_DB` en el cliente. El navegador registra manejadores de eventos (hover y click) sobre los nodos de los diagramas, permitiendo desplegar tarjetas flotantes de previsualización 5WH1+ (*hover popovers*) y resaltado visual (*marking/highlighting*) de nodos y enlaces conectados.
