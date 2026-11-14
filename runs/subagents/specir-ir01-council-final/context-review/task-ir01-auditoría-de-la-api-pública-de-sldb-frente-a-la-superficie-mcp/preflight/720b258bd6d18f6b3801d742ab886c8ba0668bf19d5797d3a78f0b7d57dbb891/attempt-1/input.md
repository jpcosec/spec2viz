FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T04:23:35Z'
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

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

Auditar exactamente 11 filas para el cliente MCP de specIR, con agente MCP como actor y nombre de fila igual a la frase tras su número: (1) catálogo de modelos y tipos de relación con campos/tipos; (2) leer payload/campo por identidad estable Model:name; (3) vecinos y recorrido dirigido de aristas con profundidad; (4) seleccionar por predicados con sldb.api.select_documents y buscar texto rankeado con sldb.api.search, anotando requisito de texto además de where; (5) ejecutar una ViewDoc existente; (6) crear/editar/borrar documentos ordinarios, RelationDoc, RelationTypeDoc y RuleDoc con validación de modelo/reglas; (7) crear modelos, editar esquema, validar/promover draft y registrar clase Python existente; (8) diagnósticos públicos de integridad del store e índice de aristas; (9) consultar journal e historial de documento/procedencia; (10) leer StoreFingerprint.store_hash y usar la huella global como precondición atómica de escritura, rechazando mismatch; (11) detectar operación pública SLDB que cumpla la capacidad de deshacer escritura confirmada de kb_undo/forma undo. Para fila 11 no inferir detalles ausentes en pron §4: si SLDB ofrece función relacionada pero no documenta el comportamiento requerido, clasificar requiere-extensión-en-SLDB y preguntar al desk que lo integre/documente; si no hay operación relacionada, faltante y solicitarla. En toda fila, si SLDB ofrece operación relacionada pero no demuestra la conducta requerida en una fuente permitida, requiere-extensión-en-SLDB; si no hay operación relacionada, faltante. Disponibilidad requiere evidencia directa o composición explícita en docstring sldb.api o doc SLDB listado. Composición explícita significa que las fuentes nombran las operaciones y describen la relación/orden que produce la capacidad; no se infiere solo por similitud de firmas o por combinar funciones sin contrato documentado. Cada una de las dos suboperaciones de fila 4 recibe su propia evidencia, resultado de disponibilidad y brecha dentro de esa fila; si difieren, la fila usa el estado más restrictivo y enumera ambas. Una fila por número; suboperaciones relacionadas no crean filas extra. La decisión final de política de escritura queda fuera solo como decisión de producto de IR02; las filas 6, 10 y 11 inventarían (es decir, registrarían) las APIs existentes frente a las necesidades declaradas. Actor de todas las necesidades: agente MCP de specIR operando un store SLDB. Model:name es la identidad estable registrada por SLDB; usar sldb://document/Model:name solo si ../sldb/docs/addressability_model.md la respalda. Predicados limitados a sldb.api.where. Estados exactos: disponible, requiere-extensión-en-SLDB, faltante; acciones: usar/componer para disponible y solicitar-extensión para no disponible. Handoff disponible: EM DASH literal —. Tras envío, repetir el mismo sldb:<stem> en filas no disponibles, con stem como basename del path JSON sin .md. Si falla el envío, conservar estado y acción de cada fila según la evidencia, cambiar solo handoff a ERROR literal, no afirmar que fue notificada y dejar tarea abierta. Resumen enviado exacto: Nota enviada; ID: sldb:<stem>. Sin brechas exacto: No se envió nota: todas las capacidades están disponibles. Una nota única puede contener de 1 a 11 secciones, solo una por fila no disponible. El informe no diseña tools ni decide política final de escritura. Fuera: código, cambios en otros repos, lectura de módulos internos SLDB, importar/ejecutar pron. El nombre canónico y capacidad de cada fila es la frase completa tras su número en la lista 1–11; usar esa misma frase en título de fila y mensaje. El valor de handoff disponible es exactamente el carácter —, sin texto adicional. Si falla cualquier comando Git, usar el fallback para el bloque snapshot completo: los tres metadatos como desconocido/no disponible y el error completo; hashear todos los archivos del corpus. Ordenar las secciones de la nota por número ascendente de capacidad. La evidencia de API consiste en docstring de la función pública citada o documentación SLDB listada que describa esa operación; puede estar en su módulo exportado, no se requiere docstring del paquete. El destinatario `--to sldb` es el desk SLDB; “Pregunta al desk” es el campo textual dentro de cada sección y no cambia ese destinatario. Si `deskops message send` falla, registrar en Resultado el código de salida, stderr completo y stdout completo (incluido JSON si lo produjo), en ese orden; no escoger uno ni descartar el otro.

## Implementation Path

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

Trabajar desde /home/jp/proyectos/SLDB_1/IR. Corpus exacto de snapshot: todos los archivos Python bajo ../sldb/src/sldb/api/; ../sldb/docs/README.md; ../sldb/docs/addressability_model.md; y ../sldb/docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md, selectors.md. Capturar git -C ../sldb rev-parse HEAD, branch --show-current y status --short --untracked-files=all limitado a esas rutas; archivos fuera del corpus no cuentan. Dirty incluye tracked/untracked dentro del corpus. Hashear SHA-256 solo archivos del corpus modificados/untracked; excluir IR/pron. Si cualquier comando git falla, escribir commit=desconocido, branch=desconocida, status=no disponible, el error completo, y hashear todos los archivos del corpus. Escribir solo docs/auditoria/sldb-api-frente-a-mcp.md. Fila 7: add_model(model_ref) registra clase StructuredNLDoc por referencia module:ClassName; create_model crea clase desde campos; add_model_field, remove_model_field, edit_model_template, validate_model_draft y promote_model_draft editan/promueven. Fila 8 revisa check_store/check_edges sin ejecutarlos. Fila 10 requiere que StoreFingerprint.store_hash global sea aceptada y comparada dentro de la escritura con rechazo atómico; source_hash por doc no basta. Fila 4 distingue select_documents (predicados) y search (texto rankeado más where). Fuentes de composición: solo docstrings públicos sldb.api y docs SLDB listados. Leer ../pron/source/spec/14-superficie-mcp.md §§1,4 como único doc externo. Si hay filas no disponibles, message_body contiene solo esas filas, formato exacto por fila: encabezado ## Capacidad N: <nombre>; después líneas Necesidad, Rutas/símbolos revisados, Brecha, Pregunta al desk, TaskDoc: task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp. No introducción ni filas disponibles. Enviar una sola vez desde IR: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json. El campo path del JSON devuelve el archivo creado; el ID es basename sin .md. Repetirlo como sldb:<stem> y usar Resumen exacto Nota enviada; ID: sldb:<stem>. Si falla/no hay path, estado/acción siguen igual; handoff ERROR; Resumen de error exacto por campos: Nota no enviada; tarea abierta; Comando: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json; Resultado: <código de salida; stderr completo; stdout completo>; Fecha UTC: <ISO-8601>. No reintentar ni declarar notificada. Sin brechas, handoff literal — y Resumen exacto No se envió nota: todas las capacidades están disponibles. Rutas ../sldb y ../pron relativas a raíz IR.

## Validation

_List the checks required before this task can close._

- El informe contiene exactamente once capacidades y cada fila incluye capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha, acción y referencia de handoff.
- Cada fila usa uno de los estados cerrados y la acción correspondiente; disponible usa usar/componer y cada no disponible usa solicitar-extensión.
- Cada fila disponible cita rutas existentes bajo sldb/src/sldb/api/ y nombra los símbolos públicos invocados como evidencia para esa capacidad; no se exige inventariar símbolos ajenos a la operación citada. Cuando la evidencia usa composición, cita y describe cada operación de la secuencia documentada.
- La fila 4 informa por separado la evidencia y disponibilidad de select_documents y search; no combinar sus resultados en una sola afirmación. La fila conserva un único estado global más restrictivo y explica cada suboperación.
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

