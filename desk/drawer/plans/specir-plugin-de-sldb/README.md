# Plan: specIR como plugin sobre sldb

Escrito el 2026-11-25. Es el plan que ordena a los demás planes de este drawer. JP ese día:
"specIR va a pasar a ser un plugin sobre sldb", y el editor de grafo "va a pasar a ser un
componente más en surface". Nodos, dependencias y estimaciones en `dag.yaml`.

## Dónde queda specIR

| Pieza | Función |
|---|---|
| sldb | El sustrato: store, modelos, reglas, grafo, anclas, lectura de código, y la única puerta de entrada |
| deskops | Plugin sobre sldb: el trabajo (tareas, pills, decisiones, rituales, despacho) |
| **specIR** | Plugin sobre sldb: el modelo semántico de un sistema. Qué piezas hay, en qué capa, cómo se relacionan, con qué notación se ven, a qué afecta un cambio |
| surface | El contrato de cómo se hace un editor, y el compositor que arma pantallas |
| Editor de texto, editor de grafo | Componentes bajo ese contrato |

specIR aporta contenido y sldb hace el trabajo. specIR no dibuja ni tiene interfaz. Lo que
necesita de otro repo se pide por su inbox.

## Las cuatro reglas

Las mismas del plan `deskops/desk/drawer/plans/deskops-plugin-de-sldb/`, que hace lo mismo con
deskops:

1. Queda como código propio solo lo que nadie más puede hacer.
2. Lo que se puede declarar es dato del store, sembrado por el plugin.
3. Lo genérico es de sldb.
4. Lo que falta en sldb se pide por su inbox; no se construye aquí.

## Qué aporta el plugin

| Qué | Forma |
|---|---|
| Los tipos de nodo de un sistema, por capa | modelos registrados en el store |
| Relaciones entre capas e invariantes | datos sembrados |
| Notaciones: UML, BPMN, ORCA, IFML, capas | datos sembrados |
| El catálogo: qué diagramas hay y en qué categoría | datos sincronizados |
| Qué hecho de código es qué nodo | reglas de mapeo sobre los hechos que lee sldb |
| Impacto, capacidades, controles | herramientas montadas en el servidor de sldb |
| La composición de su pantalla (lista, editor de grafo, editor de texto) | dato; los componentes son de surface |
| Exportes de texto: PlantUML, Mermaid, D2, Vega, BPMN XML | código propio |

## Destino de cada módulo

Medido el 2026-11-25 sobre `main` `65c3e2d`: 7.857 líneas de Python en `src/specir/`.

| Grupo | Módulos | Líneas | Destino |
|---|---|---|---|
| Tipos de dominio | `models/` | 249 | queda propio |
| Mapeo de hechos a nodos | `extract/` | 897 | queda propio; crece con Python |
| Impacto | `impact.py` | 86 | queda propio; ya corre sobre el grafo de sldb |
| Exportes de texto | `visual/renderers/` (bpmn, mermaid, plantuml, d2, vega, view_mermaid, class_diagram, json_out), `lint_mermaid.py` | 2.227 | queda propio |
| Representación paralela a la de sldb | `visual/ir.py`, `projections.py`, `normalize.py`, `compilers/`, `schema.py`, `spec_models.py`, `notation_style.py`, `exceptions.py` | 1.072 | por revisar: los exportes deberían leer la vista que sldb ya resuelve |
| HTML de un diagrama | `visual/renderers/` (bpmn_viewer, graph_html, tree, antonia_html) | 1.007 | se borra cuando el editor de grafo exporte el modo lector |
| Página del catálogo | `visual/catalog/` | 1.054 | se borra cuando exista la composición en surface y su exportación |
| Instalación | `install.py` | 122 | genérico: declaración de plugin de sldb |
| CLI y servidor | `cli.py`, `mcp_extension.py`, `visual/commands.py`, `render_file.py`, `visual/__init__.py` | 793 | se reemplaza por un servidor fastmcp propio que declara cada herramienta una vez; queda para después |
| Registro del retiro de spec2viz | `visual/retirement.py` | 344 | legado: se borra |

Queda propio: 3.459 líneas. Sale o se adelgaza: 4.398.

## Fases

| Fase | Qué | Depende de otros |
|---|---|---|
| F1 Contrato | La decisión registrada y las capacidades como nodos con su prueba | no |
| F2 Contenido | Notaciones de UML y clases de spec recibidas de sldb; notación de capas; BPMN; pantalla y navegación en el modelo, e IFML; ORCA después | no, salvo ver BPMN y capas con carriles |
| F3 Describir sistemas | Mapeo de una librería de Python con CLI; relación de dependencia e invariantes; diccionario de controles sobre `sldb/surface` | sldb: argumentos literales de las llamadas de Python |
| F4 Servir | El impacto llega a decisiones, pills y tareas; servidor fastmcp propio; composición de la pantalla como dato | sldb y surface; el servidor queda para después |
| F5 Retirar | Legado, representación paralela, HTML de un diagrama, página del catálogo | el editor de grafo y surface |

F1, F2 y F3 se pueden hacer ya. F4 y F5 esperan a otros repos.

## El servidor de specIR

JP (2026-11-25): es mejor que specIR declare su propio MCP con fastmcp, aparte, y no que sea una
extensión del servidor de sldb.

- De esa declaración salen su MCP, su CLI y el code mode, igual que se decidió para sldb.
- Eventualmente se fusiona con el de sldb.
- Mientras tanto, las herramientas de specIR llaman a sldb por su CLI, no como librería en el
  mismo proceso.
- **Queda para después**: el CLI de sldb se está modificando, así que no se empieza hasta que
  asiente.

Consecuencia: el pedido a sldb de "una forma única de declarar un plugin" pierde buena parte de su
motivo, porque el servidor es la declaración. Sembrar modelos y datos en un store sigue siendo
instalación y sigue sin resolverse.

## Lo que specIR pide a otros

| A quién | Qué | Estado |
|---|---|---|
| sldb | Cómo instala un plugin sus modelos y semillas en un store | pedido por inbox el 2026-11-25 |
| sldb | Aplicar reglas y relaciones de un store enlazado, para no copiar semillas | pedido por deskops (C1) |
| sldb | Un CLI estable al que las herramientas de specIR puedan llamar | en curso en sldb |
| sldb | Argumentos literales en las llamadas de Python | tarea creada |
| sldb | Qué documentos aplican a un archivo o símbolo | tarea creada |
| sldb | Notación que declara su estándar; documento sin glifo como hueco; predicado sobre tags | tareas creadas |
| surface | Composición de pantalla declarada como dato por un plugin | pedido por inbox el 2026-11-25 |
| editor de grafo | Dibujar `ViewDoc`; carriles por partición; SVG y HTML del modo lector de un diagrama | las dos primeras cerradas; del modo lector falta G-B2 |
| surface | Exportar el modo lector de una composición entera (graph_ui entrega su parte por diagrama) | acordado en la sala del 2026-11-25; la nota quedó en el inbox de graph_ui |
| sldb | Atributos estáticos del elemento con handler JSX, para el localizador del diccionario de controles | tarea suya en borrador |
| deskops | Guardar el dónde como punteros | tarea creada |

## Decisiones de JP que fijan este plan

Tomadas el 2026-11-25 y registradas en `docs/decisiones/specir-es-un-plugin-de-sldb.md`:

- specIR es un plugin sobre sldb y no tiene interfaz propia.
- specIR describe cualquier sistema, no solo aplicaciones web ni solo los repos del workspace.
- El plugin aporta como dato la composición de su pantalla.
- La lista de ocho capacidades de `docs/decisiones/paridad-por-capacidades.md` se acepta.
- El modelo se amplía con pantalla y navegación; lo de ORCA va después.
- El diccionario de controles se prueba sobre `sldb/surface`, sin esperar la migración de graph_ui.
- Los exportes de texto se quedan. El HTML de un diagrama y la página del catálogo son funciones
  distintas: el primero lo reemplaza el modo lector del editor de grafo; la segunda es una
  composición de surface sobre el catálogo de specIR.
- Lo que specIR necesita de otro repo va a su inbox, nunca como tarea en su Board.

## Planes hermanos

- `paridad-por-capacidades/`: el trabajo de F1 y F2.
- `graph-ui-diccionario-de-componentes/`: el diccionario de controles de F3.
- `deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/`: por qué el qué y el dónde de un
  sistema son de specIR.
- `sldb/desk/drawer/plans/superficie-como-contrato-de-editores/`: surface y sus componentes.
