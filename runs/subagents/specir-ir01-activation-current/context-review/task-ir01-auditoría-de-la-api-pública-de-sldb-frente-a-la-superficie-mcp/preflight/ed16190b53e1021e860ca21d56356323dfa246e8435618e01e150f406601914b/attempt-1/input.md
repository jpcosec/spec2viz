FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T04:14:02Z'
  authority: generated
  via: save_document_payload
id: task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:mcp
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- docs/auditoria/sldb-api-frente-a-mcp.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-specir-no-depende-de-pron-adopta-contratos-no-código
from_drawer: desk/drawer/tasks/task-ir01-auditor-a-de-la-api-p-blica-de-sldb-frente-a-la-superficie-mcp.md
---

# IR01 Auditoría de la API pública de SLDB frente a la superficie MCP

## Rationale

_Explain why this task exists or the business driver behind it._

Antes de diseñar la superficie MCP de specIR hay que saber qué ofrece ya la API pública de SLDB, para no reimplementar en specIR lo que es general y no depender de módulos internos de SLDB ni de pron.

## Goal

_Describe the concrete result this task must produce._

Una matriz que diga, capacidad por capacidad, qué necesita la superficie MCP de specIR y si la API pública de SLDB ya lo ofrece, hay que extenderlo en SLDB, o falta.

## Scope

_State what is in scope and what is out of scope._

El contrato final de escritura queda fuera solo como decisión de producto de IR02; las capacidades 6, 10 y 11 permanecen en esta auditoría como inventario de APIs existentes. Hay exactamente 11 filas, una por el listado numerado anterior. Un API relacionado que no pruebe la conducta requerida es requiere-extensión-en-SLDB; ninguna API relacionada es faltante; contrato de referencia indeterminado también es no disponible y se pregunta dentro de la única nota. Handoff no disponible tras envío repite exactamente sldb:<stem>, donde stem es el basename de path del resultado JSON sin .md; no usar tracked_name. Si falla, la celda contiene exactamente ERROR. El formato de éxito del Resumen es exactamente Nota enviada; ID: sldb:<stem>. Si no hay filas no disponibles, formato exacto No se envió nota: todas las capacidades están disponibles. Composición disponible requiere evidencia explícita en un docstring de sldb.api o en uno de los documentos SLDB enumerados; si se contradicen, registrar la discrepancia como no disponible y preguntar al desk. Los únicos símbolos/citas admisibles son rutas de archivo existentes y nombres de símbolos Python públicos, no etiquetas conceptuales. El informe no diseña la superficie MCP ni decide su contrato final.

## Implementation Path

_Outline the expected implementation route or affected surface._

Trabajar desde /home/jp/proyectos/SLDB_1/IR. El corpus de snapshot es exactamente: todos los archivos Python bajo ../sldb/src/sldb/api/; ../sldb/docs/README.md; ../sldb/docs/addressability_model.md; y ../sldb/docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md, selectors.md. Capturar git -C ../sldb rev-parse HEAD, branch --show-current y status --short --untracked-files=all limitado a esos pathspecs; otros archivos de ../sldb no afectan dirty ni hashes. Dirty incluye tracked/untracked dentro del corpus. Hashear SHA-256 solo los archivos de ese corpus modificados/untracked; excluir IR y ../pron. Si git falla, registrar el error y hashear todos los archivos del corpus. Escribir solo docs/auditoria/sldb-api-frente-a-mcp.md. Para fila 7, add_model(model_ref) registra una clase StructuredNLDoc con referencia module:ClassName; create_model crea desde campos; add_model_field, remove_model_field, edit_model_template, validate_model_draft y promote_model_draft editan/promueven. Fila 8 revisa contratos de check_store/check_edges sin ejecutarlos. Fila 10 verifica expected global StoreFingerprint.store_hash con rechazo atómico; expected_source_hash por documento no vale. Fila 4 distingue select_documents (predicados) y search (texto rankeado más where). Para evidencia de composición aceptar solo docstrings públicos de sldb.api o los documentos SLDB listados; la falta de explicación explícita se clasifica no disponible. Usar sldb://document/Model:name solo si addressability_model.md lo respalda. Leer ../pron/source/spec/14-superficie-mcp.md §1/§4 como único documento externo. Si hay no disponibles, message_body contiene solo estas filas con este formato exacto: encabezado ## Capacidad N: <nombre>; luego líneas Necesidad, Rutas/símbolos revisados, Brecha, Pregunta al desk, TaskDoc: task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp. No agregar introducción ni filas disponibles. Ejecutar una sola vez: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json. El resultado JSON incluye path; el ID es el stem del basename de path sin .md; usar ese mismo stem en todas las celdas como sldb:<stem> y en el Resumen exacto Nota enviada; ID: sldb:<stem>. Si send falla/no retorna path, celdas ERROR y Resumen exacto con campos Nota no enviada; tarea abierta; Comando: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json; Resultado: <stderr o JSON completo>; Fecha UTC: <ISO-8601>. No reintentar. Si no hay brechas, handoff literal — y Resumen exacto No se envió nota: todas las capacidades están disponibles. Las rutas ../sldb y ../pron se resuelven desde la raíz IR indicada.

## Validation

_List the checks required before this task can close._

- El informe contiene exactamente once capacidades y cada fila incluye capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha, acción y referencia de handoff.
- Cada fila usa uno de los estados cerrados y la acción correspondiente; disponible usa usar/componer y cada no disponible usa solicitar-extensión.
- Una fila disponible cita ruta existente bajo sldb/src/sldb/api/ y todos los símbolos públicos; la composición nombra cada operación.
- Cada fila no disponible enumera módulos existentes inspeccionados y explica la conducta que falta; no cita rutas o símbolos inventados.
- El informe lista el snapshot: commit/branch de sldb si existen, fecha UTC y git status; si los archivos de fuente están modificados, incluye hashes SHA-256 para fijar la revisión auditada.
- Si hay filas no disponibles, se envió un único mensaje cuyo título y cuerpo siguen Implementation Path, y el ID exacto aparece en Resumen y filas afectadas; si no hay filas no disponibles, Resumen declara que no se envió nota y cada handoff disponible contiene el carácter literal —.
- Si deskops message send falla o no retorna ID, Resumen registra el resultado y la tarea no se cierra como notificada.
- El informe lista fuentes revisadas y no abre módulos internos de SLDB ni importa/ejecuta pron; leer la spec pron como documento está permitido.

## Done When

_Name the observable condition that makes the task complete._

La matriz está escrita, cada fila tiene estado y cita, y los faltantes reales (si los hay) están notificados a SLDB.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

