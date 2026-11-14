FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T04:04:09Z'
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

Matriz para el cliente MCP de specIR; el actor de cada fila es el agente MCP. Son once filas numeradas, una por cada punto de esta lista; suboperaciones relacionadas se detallan dentro de su fila y no crean filas adicionales. (1) catálogo de modelos y tipos de relación con nombres/campos/tipos; (2) leer payload/campo por identidad estable Model:name; (3) vecinos y recorrido dirigido por aristas con profundidad; (4) buscar documentos por filtros de campo soportados por sldb.api.where/search, sin exigir una sintaxis nueva; (5) ejecutar una ViewDoc existente; (6) crear/editar/borrar documentos ordinarios, RelationDoc, RelationTypeDoc y RuleDoc con validación del modelo y reglas; (7) crear un modelo desde declaración, editar esquema por draft/validación/promoción y registrar una clase Python existente; (8) comprobar integridad del store y del índice de aristas mediante los reportes públicos de store check y edge check; (9) consultar journal e historial de documento/procedencia; (10) leer StoreFingerprint.store_hash y usar esa huella como precondición atómica de escritura del store completo, rechazando si ya cambió; (11) revertir escritura confirmada según lo que pron §4 define para kb_undo. El contrato normativo de undo se limita a la forma undo de pron §4 y la regla de §1 de que escrituras por forma dejan MoveDoc; no inferir más semántica. Si no basta para decidir equivalencia, anotar la ambigüedad y preguntar al desk SLDB. No considerar disponible una precondición global si solo existe source_hash por documento o si el llamador compara antes de escribir sin rechazo atómico. Model:name es el nombre estable registrado por SLDB; citar la forma documentada sldb://document/Model:name solo si esa documentación la respalda y señalar el argumento real de cada API. Los filtros son los predicados definidos por sldb.api.where; anotar si search exige además término de texto. La necesidad describe conducta, no firma MCP. Estado disponible solo si la conducta exacta está en API pública directamente o por composición documentada; si hay API relacionada pero falta comportamiento, requiere-extensión-en-SLDB; si no hay operación relacionada, faltante. Acciones: usar/componer para disponible; solicitar-extensión para no disponibles. La referencia handoff es el carácter EM DASH literal — en disponible y sldb:<note-id> en no disponible, referidas a una sola nota. El informe tiene sección Resumen con el ID o ausencia de nota. La conducta exacta de cada fila está definida en esta lista; no ampliar fuera de ella. Leer pron solo como referencia documental. No leer módulos internos de SLDB ni importar/ejecutar pron. Fuera: diseñar tools, escribir código, editar otros repos y decidir el contrato final de escritura.

## Implementation Path

_Outline the expected implementation route or affected surface._

Trabajar desde /home/jp/proyectos/SLDB_1/IR; rutas relativas parten de esa raíz y se inspecciona el working tree presente. Capturar antes de leer: git -C ../sldb rev-parse HEAD, git -C ../sldb branch --show-current y git -C ../sldb status --short --untracked-files=all. Dirty significa cambios tracked o untracked dentro del corpus inspeccionado; calcular y registrar SHA-256 de cada archivo inspeccionado cuyo estado esté modificado/untracked. Si git no está disponible, registrar ese hecho y calcular SHA-256 de todos los archivos inspeccionados. Escribir solo docs/auditoria/sldb-api-frente-a-mcp.md, crear docs/auditoria si hace falta. Inspeccionar recursivamente todos los archivos Python bajo ../sldb/src/sldb/api/; ../sldb/docs/README.md y addressability_model.md; y ../sldb/docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md y selectors.md. Para la fila 7, contrastar conducta con create_model, add_model, validate_model_draft y promote_model_draft y sus contratos documentados. Para fila 8, conducta requerida es producir diagnóstico público y de solo lectura equivalente a check_store y check_edges; no ejecutar ni reconstruir el store. Para fila 10, estado requerido es la raíz StoreFingerprint.store_hash de todo el store; comprobar si la API de escritura recibe esa raíz como expected y rechaza atómicamente un mismatch, no basta expected_source_hash por documento. Para fila 6, una fila cubre todos los cuatro tipos nombrados; documentar suboperaciones por tipo. Para fila 11, comparar solo el contrato escrito de pron §4; si no define comportamiento suficiente, clasificar no disponible por contrato indeterminado y preguntar al propietario. Leer ../pron/source/spec/14-superficie-mcp.md como único documento de contrato externo. Si alguna fila es no disponible, enviar exactamente una nota a sldb: título [specIR] Brechas API pública SLDB para MCP; para cada fila incluir necesidad numerada, rutas/símbolos revisados, conducta faltante, pregunta de aclaración al propietario y referencia task-ir01. Si el mensaje no se envía o no retorna ID, registrar comando/resultado/fecha en Resumen y no cerrar como notificado. Registrar ID sldb:<id> en Resumen y filas afectadas cuando sí se envíe. Si todas están disponibles, cada handoff contiene el carácter literal — y Resumen declara que no se envió nota. No leer módulos internos de SLDB ni importar/ejecutar pron.

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

