---
sldb:
  by: agent
  at: '2026-11-12T01:25:18Z'
  authority: generated
  via: save_document_payload
id: task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:modelado
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar
- task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- src/specir/models/__init__.py
- src/specir/models/domain.py
- src/specir/data/relation_types.yaml
- src/specir/data/rules.yaml
- src/specir/install.py
- tests/models/test_domain_models.py
- tests/models/test_blog_chain.py
- tests/fixtures/blog_chain.yaml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-omg-es-referencia-conceptual-no-dependencia
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog.md
---

# IR06 Tipos de dominio transversales y cadena de prueba del blog

## Rationale

_Explain why this task exists or the business driver behind it._

La tesis de specIR es que un grafo tipado conecta interfaz, API, operación y datos sin duplicar objetos. Hay que demostrarla en un caso pequeño antes de construir extractores o análisis sobre ella.

## Goal

_Describe the concrete result this task must produce._

Los tipos de dominio transversales de specIR y un store de prueba con la cadena de publicar un post del blog de ejemplo (React, Django REST Framework, PostgreSQL), recorrible por MCP.

## Scope

_State what is in scope and what is out of scope._

Dentro: (1) clases Python de modelo, definidas en el paquete specIR como subclases del documento base de SLDB, para control de interfaz, acción, operación de API, handler, operación de dominio, política, estado, entidad de dominio y tabla; (2) tipos de relación como documentos RelationTypeDoc que specIR distribuye e instala en un store: triggers, invokes, handled_by, executes, governed_by, transitions, writes, persisted_in; (3) invariantes entre capas como documentos RuleDoc que specIR distribuye, por ejemplo que toda acción de interfaz invoque una operación de API existente; (4) un store de prueba poblado por MCP con la cadena de publicar un post. Frontera: las clases de modelo son código de specIR; los tipos de relación y las reglas son datos del store; el MCP escribe datos y no clases. Fuera: extractores automáticos, análisis de impacto, síntesis.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo de modelos dentro del paquete specIR, registrado en el store por el mecanismo de registro de modelos de SLDB, como hace deskops con los suyos; documentos builtin de RelationTypeDoc y RuleDoc instalados por un comando de specIR; población del store de prueba con las tools de escritura.

## Validation

_List the checks required before this task can close._

- Por MCP se recorre PublishButton, PublishAction, endpoint, handler, PublishPost y tabla, en ambos sentidos.
- Una relación entre tipos no permitidos (por ejemplo un control de interfaz que escribe directo en una tabla) es rechazada por su RelationTypeDoc.
- Quitar del store de prueba la operación de API que una acción invoca hace que la evaluación de reglas reporte el RuleDoc incumplido.
- Dos vistas distintas (una de estados y una de componentes) muestran la misma entidad Post y el store contiene un solo documento para ella.
- Cada nodo y relación lleva la procedencia de la taxonomía canónica decidida.
- Las clases de modelo viven en el paquete specIR y ningún modelo de vocabulario visual de SLDB se redefine.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y la cadena del blog queda como store de prueba reutilizable por las tareas posteriores.
