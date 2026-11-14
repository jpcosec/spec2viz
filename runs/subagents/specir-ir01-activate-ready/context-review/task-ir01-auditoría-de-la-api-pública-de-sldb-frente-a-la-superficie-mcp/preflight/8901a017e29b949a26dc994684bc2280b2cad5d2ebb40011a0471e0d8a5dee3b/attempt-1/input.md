FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T04:06:08Z'
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

La referencia normativa de kb_undo es la sección 4 del archivo ../pron/source/spec/14-superficie-mcp.md, que ya está en Implementation Path; no hay otro documento de referencia. Si el comportamiento requerido queda indeterminado, clasificar requiere-extensión-en-SLDB cuando exista una operación pública relacionada y faltante cuando no exista ninguna; ambos estados generan una pregunta explícita en la nota única dirigida al desk de SLDB. Los símbolos de modelo se buscan como nombres Python exactos sldb.api.create_model, sldb.api.add_model, sldb.api.validate_model_draft y sldb.api.promote_model_draft; si alguno no se exporta o no existe, registrarlo como no disponible, no inferirlo por nombre. Una composición cuenta como documentada solo cuando un docstring o documento de las fuentes declaradas describe esas operaciones juntas para satisfacer la conducta; no derivar suficiencia solo de que existan funciones compatibles. Todas las filas no disponibles repiten exactamente el mismo valor sldb:<note-id>. Si el mensaje falla o no retorna ID, handoff es ERROR literal en todas las filas no disponibles y Resumen declara exactamente: Nota no enviada; tarea abierta, con comando, resultado y fecha UTC. Si no hay filas no disponibles, Resumen declara exactamente: No se envió nota: todas las capacidades están disponibles. El guion EM DASH literal — es el único valor handoff para filas disponibles.

## Implementation Path

_Outline the expected implementation route or affected surface._

Trabajar desde /home/jp/proyectos/SLDB_1/IR; todas las rutas parten de esa raíz y se inspecciona el working tree presente. Antes de leer, capturar git -C ../sldb rev-parse HEAD, branch --show-current y status --short --untracked-files=all; dirty incluye tracked y untracked dentro del corpus. Registrar SHA-256 de cada archivo inspeccionado modificado/untracked. Si git falla, registrar el resultado y calcular hashes de todos los archivos inspeccionados. Escribir solo docs/auditoria/sldb-api-frente-a-mcp.md, crear su carpeta si falta. Inspeccionar recursivamente todos los archivos Python bajo ../sldb/src/sldb/api/, ../sldb/docs/README.md, addressability_model.md y ../sldb/docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md y selectors.md. El único documento externo es ../pron/source/spec/14-superficie-mcp.md; ahí está la sección 4 con kb_undo. Para fila 7 buscar los símbolos Python exactos sldb.api.create_model, add_model, validate_model_draft y promote_model_draft y verificar que sus docstrings describan las conductas; la ausencia de un símbolo se registra. Para fila 8 comprobar si los símbolos públicos sldb.api.check_store y sldb.api.check_edges producen diagnósticos de solo lectura; no ejecutar los checks. Para fila 10 comprobar si la raíz StoreFingerprint.store_hash se acepta y compara dentro de la misma operación de escritura con rechazo atómico de mismatch; una comparación del caller o source_hash por doc no satisface el requerimiento. Para fila 11 contrastar solo el contrato escrito en la sección 4 del documento pron citado; lo indeterminado se pregunta al desk de SLDB. Composición solo se acepta con docstring o documento que describa expresamente las operaciones juntas; no inferirla de firmas compatibles. Si cualquier fila no está disponible, mandar un mensaje a sldb con título [specIR] Brechas API pública SLDB para MCP, una sección por fila con necesidad, símbolos/rutas revisados, conducta faltante, pregunta y TaskDoc IR01. Un solo mensaje; repetir el mismo ID sldb:<id> en Resumen y todas las filas no disponibles. Si send falla/no da ID, usar handoff ERROR y Resumen exacto Nota no enviada; tarea abierta, comando, resultado y fecha UTC; no reintentar ni cerrar. Si todas están disponibles, handoff literal — y Resumen exacto No se envió nota: todas las capacidades están disponibles. No leer módulos internos de SLDB ni importar/ejecutar pron.

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

