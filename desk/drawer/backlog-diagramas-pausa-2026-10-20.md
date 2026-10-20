---
title: "Backlog: trabajo de diagramas en pausa (2026-10-20)"
status: paused
---
# Backlog: trabajo de diagramas en pausa (2026-10-20)

El dueño pausó el trabajo de diagramas (mensaje del coordinador SLDB_1, 2026-10-20). En spec2viz no quedó
nada a medio hacer: los tres ítems de spec2viz están commiteados, en origin y con la suite en verde; no hay
stash, ramas ni WIP. Al retomar, empezar por esta lista.

## spec2viz

| Ítem | Estado | Refs |
|---|---|---|
| ELK con flechas ortogonales en el HTML | Hecho. El renderer emite `flowchart` con frontmatter `layout: elk` y `curve: linear`; el bundle carga mermaid 11.12.1 como módulo ES con `@mermaid-js/layout-elk` 0.2.3 e inicializa con `layout: 'elk'`. Verificado en Chrome sobre el catálogo del repo: 0 rótulos encimados y 100 % de segmentos ortogonales en los diagramas de componentes. CI verde. | b72fd2d; tests `test_mermaid_flowcharts_select_elk_with_orthogonal_curves`, `test_catalog_template_registers_the_elk_layout` |
| Packages en clases | Hecho. `data.packages` anidables (label, kind, contains), validación tipada (ids, autocontención, dos padres, ciclos, choque de ids, clases huérfanas), estilo por `kind` con la precedencia de §13; PlantUML anida, mermaid usa un namespace por ruta y `cssClass`; `uml-class` gana el glifo `package` y el link `contains` (nest). Contrato a graph_ui por inbox (20261020-122513). CI verde. | 84686c3; contrato §15; `tests/test_class_packages.py` |
| catalog build con notation | Hecho. `catalog build` dibuja las vistas de grafo desde `resolve_view` con la notación de la vista (store del proyecto si el spec está sincronizado, si no un store temporal); `view_to_mermaid`. Secuencia y matriz siguen con su `src`. Verificado en Chrome: siete vistas desde la vista resuelta, 0 rótulos encimados. | de0ce29; contrato §16; `tests/test_catalog_resolved_views.py` |

Abierto, para cuando se retome:

- No se verificó con capturas el catálogo que se sirve en el puerto 8091: las capturas de spec2viz son del
  catálogo del propio repo.
- En `component.type-system`, una vista muy ancha, el texto mínimo al ajustar al ancho queda en unos 6 px. No
  hay rótulos encimados, pero no se lee sin zoom. Pendiente decidir si ELK debe ir en vertical o partir la vista.
- graph_ui todavía no dibuja los paquetes de clase como contenedor (lo dice su backlog).
- No se avisó al coordinador commit por commit mientras se trabajaba; quedan listados aquí.

## graph_ui (copiado de su desk: `UIs/graph_ui/desk/drawer/features/backlog-diagramas-pausa-2026-10-20.md`)

| Ítem | Estado | Refs |
|---|---|---|
| R13: el lienzo crece con la leyenda; «Ver todo» corta la parte de abajo | Hecho, CI verde | graph_ui cb7623e, `issue-r13-canvas-taller-than-the-window.md` |
| R14: el texto de la cabecera de un participante de sequence se corta | Hecho, CI verde | graph_ui 1b9a862, `issue-r14-sequence-participant-header-text-cut.md` |
| R15: el nodo central de un contexto queda en una esquina | Cerrado sin arreglo (los grupos del spec no dejan centrarlo con ELK layered; el detalle está en el issue) | graph_ui 240c90b, `issue-r15-context-central-node-in-a-corner.md` |

El reporte de la ronda está en graph_ui: `desk/drawer/issues/assets/specs-legibility-r13-2026-10-20/REPORTE-r13.md`,
con sus capturas.

## Pedido original de spec2viz (copiado, coordinador SLDB_1, 2026-10-20)

> Los diagramas del catálogo HTML (catalog build, mermaid) se ven desordenados y sin jerarquía. Son tres cosas
> que solo puede arreglar spec2viz; usa fixtures genéricas.
>
> (1) Paquetes UML en los diagramas de clase. Hoy ClassDefinition.kind es un enum cerrado y no hay paquetes,
> así que no se pueden agrupar tablas por dominio ni darles color por grupo. Agrega paquetes: un package con
> contains, o un campo package por clase (elige uno y documéntalo); anidables, con style por package según la
> precedencia que ya definiste. mermaid los dibuja como contenedor. Valida ciclos, ids y clases huérfanas con
> errores tipados. Escríbele a graph_ui el contrato de lectura por inbox.
>
> (2) Render mermaid: hoy usa dagre, y con nodos anidados o un nodo central queda desordenado; las flechas
> largas se curvan y se cruzan y los rótulos se pisan. Pasa a layout elk con curvas ortogonales. Precisión:
> emitir `flowchart` con el renderer ELK y curvas linear o step, tanto en el render mermaid como en catalog
> build. Verifica con capturas del HTML que no haya rótulos encimados.
>
> (3) catalog build no respeta notation: por vista ni los glifos de la notación (keyword, forma, estilo); solo
> graph_ui lo hace. El HTML tiene que usar lo mismo que resuelve notation_view.resolve_documents. Decide entre
> generar el mermaid desde ese resultado o reutilizar el renderer de graph_ui en el bundle; la regla es una sola
> fuente de verdad del estilo.
>
> Cada punto en commits separados, con tests, CHANGELOG, push y CI verde.
