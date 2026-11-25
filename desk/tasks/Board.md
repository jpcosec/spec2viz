---
sldb:
  by: agent
  at: '2026-11-25T13:47:55Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-las-pruebas-de-tests-test-mcp-extension-py-fallan-en-el-setup-el-server-mcp-cierra-la-conexion-al-ar.md
- desk/tasks/task-u2-composiciones-lista-las-recetas-de-diagrama-del-store-con-filtro-por-capa-buscador-y-cobertura-n.md
- desk/tasks/task-u3-composiciones-dibuja-la-receta-elegida-con-su-notacion-zoom-y-arrastre-y-un-nodo-abre-su-document.md
- desk/tasks/task-u4-composiciones-muestra-las-specs-de-actividad-con-notacion-bpmn.md
- desk/tasks/task-u5-las-notas-sobre-una-receta-o-un-nodo-se-guardan-en-el-store-por-post-save-y-no-en-localstorage.md
- desk/tasks/task-u9-anclajes-muestra-la-fuente-con-lineas-y-el-fragmento-resaltado-el-selector-su-estado-y-los-nodos.md
- desk/tasks/task-u1b-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb
tags: []
---

# IR Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for IR.

## Notes

_Add short operational notes about the current routed set._

Estado al 2026-11-21 (09:40 UTC): IR13, gate de retiro de spec2viz. specir retirement check (con --path de deskops, UIs/graph_ui, pron, sldb y spec2viz/.sldb) da 0 dependencias en sldb, deskops, pron, graph_ui e IR. Quedan 19 en el store spec2viz/.sldb (G5) y la fila SV-A17, que depende de él. Cerradas hoy: filas de validate (3d0a436, closeout 9c343b9) y oráculos de paridad congelados en goldens (c47111d, closeout 3bbc758); el script de grabación quedó en /mnt/ssd/proyectos/SLDB_1/reports/spec2viz-goldens/. Espera a JP la task.decision 'JP decide: declarar el retiro de spec2viz, sacar spec2viz/.sldb del universo del comprobador y archivar el repo' (acta, puntos 2 y 8, más la declaración).

## Task Details

_Generated from the task references above._

- Las pruebas de tests/test_mcp_extension.py fallan en el setup: el server MCP cierra la conexion al arrancar sobre la copia del store [draft] - Se identifica por que el server muere al arrancar sobre la copia del store de la sesion (fixtures store_copy y build_deskops_copy de tests/conftest.py) y se corrige la causa, de modo que tests/test_mcp_extension.py pase.
- U2: Composiciones lista las recetas de diagrama del store con filtro por capa, buscador y cobertura n/m [draft] - En la pestana Composiciones, la lista de recetas (las specs de diagrama: SpecDoc que sldb serve lista en /notations; /views solo si tambien trae specs) con filtro por capa, buscador por titulo (parcial, sin distinguir mayusculas) y la cobertura de cada una cuando sldb la de (hoy '—'). Aceptacion contra el store de pron, que tiene 15 SpecDoc; el store de IR no tiene.
- U3: Composiciones dibuja la receta elegida con su notacion, zoom y arrastre, y un nodo abre su documento [draft] - Vista previa de la receta elegida dibujada con /notations/view, con zoom, arrastre y reinicio, y clic en un nodo que abre su documento en el panel derecho.
- U4: Composiciones muestra las specs de actividad con notacion BPMN [draft] - Que una receta cuya spec es de actividad se dibuje con notacion BPMN, como hacia spec2viz.
- U5: las notas sobre una receta o un nodo se guardan en el store por POST /save y no en localStorage [draft] - Notas sobre la receta o el nodo, guardadas en el store de sldb (como las anotaciones de spec2viz, pero en el store), con lista, alta y edicion.
- U9: Anclajes muestra la fuente con lineas y el fragmento resaltado, el selector, su estado y los nodos que se apoyan [draft] - La pestana Anclajes: para un CodeAnchorDoc, la fuente con numeros de linea y el fragmento resaltado; a la derecha el selector, el estado (vigente o cambiado) y los nodos y relaciones de specIR que se apoyan en el.
- U1b: el cascaron de la UI de specIR usa los tokens de papel y se parece a la maqueta [active] - Que el cascaron de IR/ui se vea como desk/drawer/plans/graph-ui-diccionario-de-componentes/maqueta-ui.html#grafo: pestanas y lentes monoespaciadas con borde de 2 px y la activa en piedra; explorador con fondo piedra y borde; panel de documento con borde; titulos en serif (Newsreader); rail inferior; miga con el nombre del store en la cabecera.
