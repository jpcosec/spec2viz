---
sldb:
  by: agent
  at: '2026-11-12T01:31:27Z'
  authority: generated
  via: save_document_payload
id: task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
pills:
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- docs/spec2viz/matriz-de-cobertura.md
- docs/spec2viz/gate-de-retiro.md
- docs/decisiones/fuente-de-verdad-del-diagrama.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
from_drawer: desk/drawer/tasks/task-ir07-matriz-de-cobertura-de-spec2viz-para-su-retiro.md
---

# IR07 Cobertura completa de spec2viz: matriz, fuente de verdad del diagrama y gate de retiro

## Rationale

_Explain why this task exists or the business driver behind it._

specIR debe cubrir todas las funcionalidades de spec2viz para poder retirarlo. Sin una lista completa con el modo de cobertura de cada cosa, el retiro no es verificable. Además conviven dos modelos de diagrama: en spec2viz el YAML del spec es la fuente y el store es derivado; en specIR la fuente semántica es el grafo de SLDB y el diagrama es una vista. Esa tensión se resuelve aquí porque condiciona el modo de cada fila.

## Goal

_Describe the concrete result this task must produce._

Una matriz de cobertura de todas las capacidades de spec2viz, con modo y condición de retiro por fila; la decisión sobre el papel del YAML de spec frente al grafo; y un gate comprobable de migración y retiro. Es un plan de cobertura: no declara nada como ya migrado.

## Scope

_State what is in scope and what is out of scope._

Dentro, una fila por cada capacidad de spec2viz, cada una con modo (migrar tal cual; reemplazar por otra arquitectura o experiencia con resultado equivalente; exponer desde specIR lo que ya vive en SLDB) y condición verificable de retiro:
- Modelos de spec por tipo de diagrama: clase, secuencia, estado, componente, actividad, despliegue, matriz, reflexión; carga y validación de specs; export de JSON Schema de specs y de catálogos.
- Representación intermedia y compiladores por tipo de diagrama.
- Renderizadores: Mermaid, PlantUML, D2, BPMN y su visor, Vega, árbol, HTML de grafo, antonia-html y salida JSON.
- Linter de Mermaid.
- SpecSync: materializar un spec en el store como SpecDoc, SpecNodeDoc y RelationDoc, creando el RelationTypeDoc que falte y borrando lo que salió del spec.
- from-graph: compilar el grafo de un store o un snapshot en un spec de componentes.
- Generación de un spec de componentes desde el AST de Python.
- Catálogos: build (HTML autocontenido), sync, validate y serve con autoguardado de anotaciones; registro vistas.yml y stores jerárquicos de diagramas.
- NotationDoc, GlyphDoc, LinkDoc y PaletteDoc: list, validate, sync y view de notaciones; list, validate y sync de paletas, con la comprobación de contraste WCAG.
- Emparejamiento de átomos con elementos de diagrama y cobertura por vista.
- API Python pública y recursos empaquetados (plantillas HTML, bpmn-js, notaciones y paleta builtin).
- Comando about y la habilidad de uso de spec2viz instalada para agentes.
Dentro también: inventario de consumidores, con el archivo donde cada uno importa o invoca spec2viz: graph_ui (UIs/graph_ui/frontends/mindmap/sldb_adapter.py y su pyproject.toml), deskops (reglas de rutas en el módulo graph.desk_graph del paquete deskops, documentación de diagramas y la habilidad use-spec2viz) y los stores cuyo índice registra modelos spec2viz.sldb_models.
Dentro también, la decisión antes separada: la fuente semántica es el grafo de SLDB; decidir si el YAML de spec queda como formato de autoría e intercambio de forma permanente o solo durante la paridad; cómo se dibuja algo que todavía no existe en el grafo (diseño previo a la implementación); y qué pasa con los specs YAML existentes en los repos que usan spec2viz.
Fuera: migrar o implementar cualquier fila; extractores de otras tecnologías; análisis de impacto.

## Implementation Path

_Outline the expected implementation route or affected surface._

Fuentes: spec2viz/spec2viz/cli.py y los módulos del paquete; spec2viz/tests/ como definición de paridad; el plan absorber-spec2viz-y-modelos-ui de SLDB para lo que ya vive en SLDB. La matriz se escribe en el repo de specIR. Cada fila o grupo de filas se convierte después en una tarea de migración propia; esta tarea no migra nada. Propiedad de archivos compartidos: esta tarea crea docs/spec2viz/matriz-de-cobertura.md con todas las filas, su modo y su condición de retiro, sin evidencia de cumplimiento; la tarea final IR13 la actualiza después, añadiendo por fila la prueba que acredita la cobertura, una vez cerradas IR13a, IR13b, IR13c e IR13d.

## Validation

_List the checks required before this task can close._

- Todos los comandos y subgrupos que lista la ayuda del CLI de spec2viz aparecen en la matriz.
- Todos los módulos de compiladores, renderizadores, linters y generadores del paquete spec2viz aparecen en la matriz.
- Ninguna fila dice descartado, fuera de alcance o ya implementado sin una prueba citada.
- Cada fila en modo reemplazar nombra el sustituto y la prueba que demostrará la equivalencia.
- Cada fila en modo exponer desde SLDB cita la operación de la API pública de SLDB que la respalda.
- Cada consumidor inventariado cita el archivo donde importa o invoca spec2viz.
- Existe un atom con la decisión sobre el YAML de spec frente al grafo, con las alternativas descartadas, la regla para diseño previo a la implementación y el destino de los specs existentes.
- El gate de retiro está escrito como lista comprobable: toda fila con su condición cumplida; la suite de spec2viz pasa contra specIR o tiene prueba equivalente declarada por fila reemplazada; ningún consumidor importa ni invoca spec2viz; ningún store registra modelos spec2viz.sldb_models.

## Done When

_Name the observable condition that makes the task complete._

La matriz, la decisión y el gate de retiro están escritos y revisados, y de la matriz se pueden derivar las tareas de migración sin volver a inventariar spec2viz.
