---
id: task-ir11-compiladores-y-proyecciones-de-spec2viz
status: deferred
summary: 'Candidata diferida: cubrir en specIR los modelos de spec, los compiladores
  de todos los tipos de diagrama y la materialización de proyecciones ViewDoc y SpecDoc.'
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ''
history: []
references: []
depends_on:
- task-ir07-matriz-de-cobertura-de-spec2viz-para-su-retiro
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
---

# IR11 Compiladores y proyecciones de spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

Candidata diferida. Los compiladores son el centro de spec2viz: convierten un spec en una representación lista para dibujar. Sin cubrirlos, ninguna otra parte de la capa visual puede migrar, y es donde se aplica la decisión sobre el YAML de spec frente al grafo.

## Goal

_Describe the concrete result this task must produce._

specIR compila todos los tipos de diagrama que compila spec2viz y produce diagramas tanto desde un spec autorado como desde una proyección del grafo, según el contrato decidido en la candidata de cobertura.

## Scope

_State what is in scope and what is out of scope._

Dentro: modelos de spec, carga y validación para clase, secuencia, estado, componente, actividad, despliegue, matriz y reflexión; representación intermedia y un compilador por tipo; materialización de proyecciones: de un ViewDoc evaluado sobre el grafo y de un SpecDoc con sus SpecNodeDoc a la misma representación intermedia. Cada pieza se migra tal cual o se reemplaza, según el modo que le asigne la matriz de cobertura; los modelos de vocabulario visual se usan desde SLDB y no se redefinen.
Fuera: renderizado a formatos de salida, linter y recursos empaquetados; sincronización al store, catálogos y consumidores; retirar spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Tipo sugerido: task.code (el tipo se asigna al autorar la tarea activa con deskops add task --task-type; en una candidata diferida task_type queda vacío). Módulos de compilación en el paquete specIR; paridad medida con los fixtures y pruebas de compiladores de spec2viz (spec2viz/tests/) ejecutados contra specIR; resolución de vistas por la API pública de SLDB.

## Validation

_List the checks required before this task can close._

- Los ocho tipos de diagrama compilan en specIR, y cada fixture de compilador de spec2viz produce en specIR la misma representación intermedia, o la diferencia está declarada en la fila correspondiente de la matriz de cobertura con su prueba equivalente.
- Los specs YAML existentes validan en specIR con los mismos errores tipados que en spec2viz, salvo que la decisión de la candidata de cobertura diga otra cosa.
- Un diagrama de componentes y uno de estados generados desde proyecciones del grafo del blog muestran la entidad Post y el store sigue teniendo un solo documento para ella.
- Compilar desde un spec autorado y desde la proyección equivalente del grafo da la misma representación intermedia.
- specIR no define ninguna clase con el nombre de un modelo de vocabulario visual de SLDB.
- El paquete no importa spec2viz.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas de paridad de compiladores pasan en specIR y las filas de compiladores y proyecciones de la matriz de cobertura tienen su condición de retiro cumplida.
