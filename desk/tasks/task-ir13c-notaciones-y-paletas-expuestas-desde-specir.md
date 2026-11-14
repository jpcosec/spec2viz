---
sldb:
  by: agent
  at: '2026-11-12T01:25:45Z'
  authority: generated
  via: save_document_payload
id: task-ir13c-notaciones-y-paletas-expuestas-desde-specir
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
- task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/visual/notations.py
- tests/visual/test_notations.py
- tests/visual/test_palettes.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13c Notaciones y paletas expuestas desde specIR

## Rationale

_Explain why this task exists or the business driver behind it._

Parte de la migración final de spec2viz, separada de IR13 para que cada tarea tenga un solo entregable. Las notaciones y paletas ya viven en SLDB, pero quien usa spec2viz las opera desde su CLI; para retirarlo, specIR tiene que ofrecer ese camino.

## Goal

_Describe the concrete result this task must produce._

specIR expone las operaciones de notaciones y paletas de spec2viz delegando en la API pública de SLDB, sin redefinir sus modelos.

## Scope

_State what is in scope and what is out of scope._

Dentro: listar, validar, sincronizar al store y resolver la vista de notaciones (NotationDoc, GlyphDoc, LinkDoc); listar, validar y sincronizar paletas (PaletteDoc), incluida la comprobación de contraste; todo como envoltorio de las operaciones de SLDB.
Fuera: redefinir modelos de vocabulario visual o reimplementar el resolvedor de vistas; catálogos; CLI general; migración de consumidores.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo src/specir/visual/notations.py que llama a las operaciones de notaciones y vistas de la API pública de SLDB. Paridad medida portando a tests/visual/ las pruebas de spec2viz de notación, vista de notación y paleta.

## Validation

_List the checks required before this task can close._

- Listar notaciones y paletas desde specIR devuelve las builtin que distribuye SLDB.
- Validar una notación o una paleta inválida de los fixtures reporta los mismos problemas que spec2viz, incluido el contraste insuficiente.
- Sincronizar una notación desde specIR deja en un store de prueba sus NotationDoc, GlyphDoc y LinkDoc.
- La vista resuelta de un spec de fixture desde specIR es igual a la que devuelve la API pública de SLDB para ese spec.
- specIR no define ninguna clase con el nombre de un modelo de vocabulario visual de SLDB, y el módulo no importa spec2viz.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y las filas de notaciones y paletas de la matriz de cobertura tienen su condición de retiro cumplida.
