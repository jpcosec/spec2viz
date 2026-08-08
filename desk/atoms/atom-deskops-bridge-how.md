---
id: atom-deskops-bridge-how
title: Deskops Integration Bridge Architecture
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:deskops
- topic:architecture
- topic:integration
provenance: spec2viz/deskops.py
---

# Deskops Integration Bridge Architecture - HOW

## Answer

El mecanismo de integración entre `spec2viz` y `deskops` opera a través de los siguientes pasos técnicos en `spec2viz/deskops.py`:

1. **Extracción y Parseo de Átomos (`parse_atoms`):**
   - Escanea el directorio de conocimiento `desk/atoms/*.md`.
   - Utiliza una expresión regular (`^---\s*$`) para separar el frontmatter YAML del cuerpo del Markdown.
   - Extrae la clave `title` (normalizada a minúsculas) y la dimensión 5WH1+ (`five_wh_one_plus`: `what`, `why`, `how`, `how_not`, `when`, `where`, `for_whom`).
   - Indexa en una estructura jerárquica JSON: `window.ATOMS_DB[title_norm]["atoms"][question] = { "id": fm.id, "body": body }`.

2. **Resolución de Vistas y Plantilla (`render_deskops`):**
   - Carga el registro `vistas.yml` y agrupa las vistas por la propiedad `category`.
   - Para cada vista, lee la fuente especificada (`.mmd`, `.svg`, o `.html`) desde `base_dir`.
   - Construye la barra de navegación lateral (`{{NAV}}`) y la estructura de secciones (`{{SECTIONS}}`).

3. **Inyección en Tiempo de Compilación:**
   - Reemplaza los marcadores `{{NAV}}` y `{{SECTIONS}}` en `template.html`.
   - Inyecta `window.ATOMS_DB = JSON.stringify(atoms_db)` en el script final del documento HTML.

4. **Vinculación Interactiva en el Navegador:**
   - En el cliente web, al hacer clic en un nodo de diagrama Mermaid o SVG, se normaliza el título del nodo y se busca en `window.ATOMS_DB`.
   - Se despliega el panel interactivo (*Atom Drawer*) permitiendo navegar por las pestañas 5WH1+ registradas para ese componente de arquitectura.
