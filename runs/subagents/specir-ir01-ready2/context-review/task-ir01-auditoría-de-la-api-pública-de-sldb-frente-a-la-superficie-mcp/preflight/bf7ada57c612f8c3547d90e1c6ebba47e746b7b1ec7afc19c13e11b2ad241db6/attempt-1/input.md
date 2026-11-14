FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T04:10:15Z'
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

Auditar exactamente 11 filas para el cliente MCP de specIR, con el agente MCP como actor: (1) catálogo de modelos y tipos de relación con campos/tipos; (2) leer payload/campo por identidad estable Model:name; (3) vecinos y recorrido dirigido de aristas con profundidad; (4) buscar documentos por filtros soportados por sldb.api.where/search y anotar si además exige texto; (5) ejecutar una ViewDoc existente y devolver su resultado; (6) crear/editar/borrar documentos ordinarios, RelationDoc, RelationTypeDoc y RuleDoc, con validación del modelo/reglas; (7) crear modelos, editar esquema por draft/validación/promoción y registrar clases Python existentes; (8) obtener diagnósticos públicos de integridad del store y del índice de aristas; (9) consultar journal e historial de documentos/procedencia; (10) leer StoreFingerprint.store_hash y usar esa huella de todo el store como precondición atómica de escritura, rechazando mismatch; (11) revertir escritura confirmada según el contrato kb_undo de la sección 4 de pron. Esas once filas agrupan las suboperaciones enumeradas; no añadir filas. Conducta normativa de undo: solo lo que describe pron/source/spec/14-superficie-mcp.md §4 y su regla §1 de que escrituras por forma dejan MoveDoc; no inferir semántica adicional. Si el contrato no permite decidir equivalencia, preguntar al desk SLDB y clasificar requiere-extensión-en-SLDB si hay operación relacionada o faltante si no existe ninguna. No considerar disponible la precondición global si solo existe source_hash por documento o si el caller compara antes de escribir sin rechazo atómico. Identidad Model:name es el nombre estable registrado por SLDB; usar sldb://document/Model:name solo si docs lo respaldan. Filtros limitados a predicados documentados por sldb.api.where. Estado disponible solo si la conducta exacta está en API pública directamente o por composición descrita explícitamente en docstrings/documentos; no inferir suficiencia de firmas compatibles. Estados exactos: disponible, requiere-extensión-en-SLDB, faltante. Acciones: usar/componer para disponible, solicitar-extensión para no disponibles. Handoff es el carácter EM DASH literal — para disponible; el mismo valor sldb:<note-id> repetido en todas las filas no disponibles tras una nota única; si falla el envío, ERROR literal en todas las filas no disponibles. El Resumen del informe usa exactamente No se envió nota: todas las capacidades están disponibles. si no hay brechas; si falla usa Nota no enviada; tarea abierta, con comando, resultado y fecha UTC; si se envía usa ID sldb:<id>. El informe y la nota no deciden el contrato final de escritura. Fuera: diseñar tools, escribir código, editar otros repos e importar/ejecutar pron o leer módulos internos de SLDB.

## Implementation Path

_Outline the expected implementation route or affected surface._

Trabajar desde /home/jp/proyectos/SLDB_1/IR. El remitente de --root . es IR; --to sldb identifica al destinatario. Capturar git -C ../sldb rev-parse HEAD, branch --show-current y status --short --untracked-files=all. Dirty incluye tracked y untracked dentro del corpus. Registrar SHA-256 solo de archivos Python API y documentos SLDB inspeccionados que estén modificados/untracked; excluir TaskDocs, archivos de IR y spec pron. Si git falla, registrar el error y hashear todos los archivos SLDB inspeccionados. Escribir solo docs/auditoria/sldb-api-frente-a-mcp.md. Inspeccionar recursivamente todos los archivos Python de ../sldb/src/sldb/api/; ../sldb/docs/README.md; ../sldb/docs/addressability_model.md; ../sldb/docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md y selectors.md. El único doc externo es ../pron/source/spec/14-superficie-mcp.md (§1 y §4). Fila 7 busca símbolos Python exactos sldb.api.create_model, add_model, validate_model_draft y promote_model_draft; fila 8 revisa contratos de sldb.api.check_store y check_edges sin ejecutarlos; fila 10 comprueba si StoreFingerprint.store_hash se acepta y compara dentro de una escritura con rechazo atómico (source_hash por documento no basta). Composición cuenta solo si un docstring/documento declara que esas operaciones juntas cubren la conducta. URI sldb://document/Model:name solo si lo respaldan los documentos SLDB enumerados, en particular addressability_model.md; si no, omitir URI y citar la identidad Model:name respaldada. Si equivalencia queda indeterminada, no preguntar antes ni mandar otra nota: clasificar la fila no disponible y preguntar en la única nota. Si hay no disponibles, construir message_body con solo esas filas, cada sección con número/necesidad, rutas y símbolos revisados, conducta faltante, pregunta al desk y el ID textual task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp. Ejecutar exactamente una vez: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json. Repetir el mismo ID de la respuesta JSON como sldb:<id> en las filas afectadas. Resumen de éxito exacto: Nota enviada; ID: sldb:<id>. Sin brechas, handoff literal — y Resumen exacto: No se envió nota: todas las capacidades están disponibles. Si falla/no trae ID, handoff ERROR y Resumen con estos campos: Nota no enviada; tarea abierta; Comando: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json; Resultado: <stderr o JSON>; Fecha UTC: <ISO-8601>. No reintentar ni cerrar como notificada. No leer módulos internos de SLDB ni importar/ejecutar pron.

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

