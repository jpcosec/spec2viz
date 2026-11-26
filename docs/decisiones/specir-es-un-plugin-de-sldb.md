# specIR es un plugin sobre sldb

> **Estado: DECIDIDO por JP el 2026-11-25.** Sin ejecutar. El trabajo está en
> `desk/drawer/plans/specir-plugin-de-sldb/`.

## Contexto

specIR nació como paquete aparte con CLI, servidor MCP, instalador, renderers de HTML y una página
de catálogo propios: 7.857 líneas de Python el 2026-11-25. Más de la mitad repite lo que sldb y los
editores ya hacen (resolver una vista, dibujarla, servirla, instalar modelos en un store).

Ese mismo día quedó fijado el reparto del workspace: sldb es el sustrato, deskops es un plugin
sobre sldb que lleva el trabajo, y las interfaces son editores bajo el contrato de `sldb/surface`
(ADR de sldb `surface-is-an-editor-contract.md`).

## Decisión

- **specIR es un plugin sobre sldb.** Aporta el modelo semántico de un sistema: qué piezas hay, en
  qué capa, cómo se relacionan, con qué notación se ven y a qué afecta un cambio.
- **Describe cualquier sistema**, no solo aplicaciones web ni solo los repos de este workspace. Lo
  que hoy no describe es porque falta el mapeo, no porque el modelo lo impida.
- **Cuatro reglas**, las mismas del plan de deskops como plugin:
  1. Queda como código propio solo lo que nadie más puede hacer.
  2. Lo que se puede declarar es dato del store, sembrado por el plugin.
  3. Lo genérico es de sldb.
  4. Lo que falta en otro repo se pide por su inbox; no se construye aquí ni se le escribe una
     tarea en su Board.
- **specIR no lee código.** Lo lee sldb con tree-sitter y entrega hechos. specIR decide qué hecho
  es qué nodo.
- **specIR no dibuja ni tiene interfaz.** Su pantalla (el catálogo) es una composición declarada
  como dato, que aporta el plugin; los componentes que la arman son de surface.
- **Cómo sirve specIR sus herramientas y cómo conversa con sldb lo fija la especificación de
  plugins de sldb**, igual que para cualquier plugin (JP, 2026-11-26). specIR no lo decide por su
  cuenta y espera esa especificación. Con esto queda sin efecto lo anotado el 2026-11-25
  (servidor fastmcp propio, aparte, que llama a sldb por el CLI).
- **Se quedan como código propio** los tipos de dominio, el mapeo de hechos a nodos, el impacto y
  los exportes de texto (PlantUML, Mermaid, D2, Vega, BPMN XML).
- **Se borran** el HTML de un diagrama (lo reemplaza el modo lector del editor de grafo), la página
  del catálogo (la reemplaza la composición), la representación paralela a la vista resuelta de
  sldb y el registro del retiro de spec2viz.

## Consecuencias

- De 7.857 líneas quedan propias unas 3.459.
- Las fases de contrato, contenido y descripción de sistemas no dependen de nadie. Servir y retirar
  esperan a sldb, a surface y al editor de grafo.
- Tres pedidos salen por inbox: cómo instala un plugin sus modelos y semillas (sldb), una
  composición de pantalla declarada como dato (surface) y exportar el modo lector de una
  composición entera (editor de grafo).

## Sin verificar

- Cuánto de la representación paralela (`visual/ir.py` y vecinos) usan hoy los exportes de texto.
- Que el compositor de surface acepte una composición aportada por un plugin: surface todavía no
  tiene compositor.
