FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T04:35:18Z'
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

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

Auditar exactamente 11 filas para el cliente MCP de specIR, con agente MCP como actor y nombre de fila igual a la frase tras su número: (1) catálogo de modelos y tipos de relación con campos/tipos; (2) leer payload/campo por identidad estable Model:name; (3) vecinos y recorrido dirigido de aristas con profundidad; (4) seleccionar por predicados con sldb.api.select_documents y buscar texto rankeado con sldb.api.search, anotando requisito de texto además de where; (5) ejecutar una ViewDoc existente; (6) crear/editar/borrar documentos ordinarios, RelationDoc, RelationTypeDoc y RuleDoc con validación de modelo/reglas; (7) crear modelos, editar esquema, validar/promover draft y registrar clase Python existente; (8) diagnósticos públicos de integridad del store e índice de aristas; (9) consultar journal e historial de documento/procedencia; (10) leer StoreFingerprint.store_hash y usar la huella global como precondición atómica de escritura, rechazando mismatch; (11) detectar operación pública SLDB que cumpla la capacidad de deshacer escritura confirmada de kb_undo/forma undo. Para fila 11 no inferir detalles ausentes en pron §4: si SLDB ofrece función relacionada pero no documenta el comportamiento requerido, clasificar requiere-extensión-en-SLDB y preguntar al desk que lo integre/documente; si no hay operación relacionada, faltante y solicitarla. En toda fila, si SLDB ofrece operación relacionada pero no demuestra la conducta requerida en una fuente permitida, requiere-extensión-en-SLDB; si no hay operación relacionada, faltante. Disponibilidad requiere evidencia directa o composición explícita en docstring sldb.api o doc SLDB listado. Composición explícita significa que las fuentes nombran las operaciones y describen la relación/orden que produce la capacidad; no se infiere solo por similitud de firmas o por combinar funciones sin contrato documentado. Cada una de las dos suboperaciones de fila 4 recibe su propia evidencia, resultado de disponibilidad y brecha dentro de esa fila; si difieren, la fila usa el estado más restrictivo y enumera ambas. Una fila por número; suboperaciones relacionadas no crean filas extra. La decisión final de política de escritura queda fuera solo como decisión de producto de IR02; las filas 6, 10 y 11 documentarán las APIs existentes frente a las necesidades declaradas. Actor de todas las necesidades: agente MCP de specIR operando un store SLDB. Model:name es la identidad estable registrada por SLDB; usar sldb://document/Model:name solo si ../sldb/docs/addressability_model.md la respalda. Predicados limitados a sldb.api.where. Estados exactos: disponible, requiere-extensión-en-SLDB, faltante; acciones: usar/componer para disponible y solicitar-extensión para no disponible. Handoff disponible: EM DASH literal —. Tras envío, repetir el mismo sldb:<stem> en filas no disponibles, con stem como basename del path JSON sin .md. Si falla el envío, conservar estado y acción de cada fila según la evidencia, cambiar solo handoff a ERROR literal, no afirmar que fue notificada y dejar tarea abierta. Resumen enviado exacto: Nota enviada; ID: sldb:<stem>. Sin brechas exacto: No se envió nota: todas las capacidades están disponibles. Una nota única puede contener de 1 a 11 secciones, solo una por fila no disponible. El informe no diseña tools ni decide política final de escritura. Fuera: código, cambios en otros repos, lectura de módulos internos SLDB, importar/ejecutar pron. El nombre canónico y capacidad de cada fila es la frase completa tras su número en la lista 1–11; usar esa misma frase en título de fila y mensaje. El valor de handoff disponible es exactamente el carácter —, sin texto adicional. Si falla cualquier comando Git, usar el fallback para el bloque snapshot completo: los tres metadatos como desconocido/no disponible y el error completo; hashear todos los archivos del corpus. Ordenar las secciones de la nota por número ascendente de capacidad. La evidencia de API consiste en docstring de la función pública citada o documentación SLDB listada que describa esa operación; puede estar en su módulo exportado, no se requiere docstring del paquete. El destinatario `--to sldb` es el desk SLDB; “Pregunta al desk” es el campo textual dentro de cada sección y no cambia ese destinatario. Si `deskops message send` falla, registrar en Resultado el código de salida, stderr completo y stdout completo (incluido JSON si lo produjo), en ese orden; no escoger uno ni descartar el otro. Para la fila 4, la severidad es disponible < requiere-extensión-en-SLDB < faltante; el estado conjunto es el más severo de sus dos suboperaciones. Las frases en cursiva heredadas de la plantilla bajo los encabezados describen el tipo de contenido esperado y no son requisitos adicionales de esta tarea. Para cada nombre de capacidad, tomar literalmente el texto después de su número hasta el siguiente punto y coma; excluir número, paréntesis y separador final, y conservar el resto de la frase. Una operación es relacionada solo si su nombre o documentación pública declara propósito, entrada o salida que coincide con una parte de la necesidad de esa fila; similitud incidental de firma no basta. La conducta está demostrada solo cuando el docstring de la operación pública o los docs permitidos describen explícitamente el resultado/precondición que la fila requiere; evidencia parcial se clasifica requiere-extensión-en-SLDB. La matriz puede describir brechas y compatibilidad, pero no recomienda política, arquitectura ni nivel de mutabilidad de escritura; eso lo decide IR02. La referencia a pron §1 y §4 significa únicamente las secciones 1 y 4, no el intervalo 1–4. La fila 11 requiere solo identificar una operación pública que revierta una escritura ya confirmada, que es el significado mínimo indicado por pron §4; no inferir historial, selección de operación, repetición ni otras semánticas de undo. El ID sldb:<stem> se repite en el campo handoff de cada fila no disponible; no se añade al cuerpo de la nota. Al formar el nombre de capacidad se quita solo el marcador numérico inicial `(N)` y el separador `;` o punto final de la lista; cualquier paréntesis dentro de la frase se conserva. Los docs SLDB permitidos son exactamente los enumerados en Implementation Path. En una fuente documental, una mención nominal de una función sin descripción de su comportamiento no demuestra la capacidad. La celda de evidencia debe citar únicamente fuentes que describan explícitamente la conducta requerida. Las pills asociadas al TaskDoc son guardrails obligatorios para el trabajo, no fuentes de evidencia técnica. Para la celda Necesidad, formular la entrada como “solicitud MCP para <nombre canónico>” y el resultado como el resultado explícito en la misma frase de capacidad; no añadir requisitos de producto. En la pregunta al desk usar: “¿Puede SLDB exponer o documentar <conducta faltante> mediante la API pública para soportar <nombre canónico>?” Para fila 11, “escritura confirmada” significa una operación nivel 1 o 2 cuya evaluación terminó con éxito; buscar el equivalente público de la forma `(undo)` de pron §4. Excluir edición de modelos nivel 3, que la misma sección declara no reversible. No inferir qué escritura elige undo ni su historial. En fallback Git, los tres valores desconocidos son commit=desconocido, branch=desconocida y status=no disponible; conservar la fecha UTC real y copiar el error Git completo en Snapshot. La fecha no se sustituye. Fuentes revisadas enumera cada archivo Python del corpus efectivamente leído y cada documento `.md` efectivamente leído, incluida la spec pron con §1 y §4; las rutas de API que se citan en filas también aparecen en esa lista. La clasificación fila 11 toma los niveles de pron §4: nivel 1 contenido/documentos y aristas; nivel 2 reglas del mundo (tipos, condiciones y transiciones); excluye nivel 3 modelos/esquema. Para disponibilidad, se acepta como evidencia suficiente una ruta pública citada o un doc SLDB listado que describa explícitamente el contrato; la fila cita el tipo de fuente que realmente lo demuestra y nunca inventa símbolos. Si la fuente es un doc, la celda Evidencia no tiene que incluir ruta bajo sldb/api. Excepción de nombre: para la fila 4, el nombre termina en `sldb.api.search`; la frase “anotando requisito de texto además de where” es instrucción de necesidad, no parte del nombre. Para fila 11, éxito de escritura en la especificación pron significa que la evaluación devuelve `outcome: done`; la referencia a escrituras usa los registros con `done` que describe pron §4. En Snapshot, incluir el stdout literal de git status en bloque fenced (vacío se rotula `clean`); hashes son un bloque separado de archivos dirty. En un error de envío, Fecha UTC es la hora del intento de envío, independiente del timestamp de snapshot.

## Implementation Path

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

Trabajar desde /home/jp/proyectos/SLDB_1/IR. Corpus exacto de snapshot: todos los archivos Python bajo ../sldb/src/sldb/api/; ../sldb/docs/README.md; ../sldb/docs/addressability_model.md; y ../sldb/docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md, selectors.md. Capturar git -C ../sldb rev-parse HEAD, branch --show-current y status --short --untracked-files=all limitado a esas rutas; archivos fuera del corpus no cuentan. Dirty incluye tracked/untracked dentro del corpus. Hashear SHA-256 solo archivos del corpus modificados/untracked; excluir IR/pron. Si cualquier comando git falla, escribir commit=desconocido, branch=desconocida, status=no disponible, el error completo, y hashear todos los archivos del corpus. Escribir solo docs/auditoria/sldb-api-frente-a-mcp.md. Fila 7: add_model(model_ref) registra clase StructuredNLDoc por referencia module:ClassName; create_model crea clase desde campos; add_model_field, remove_model_field, edit_model_template, validate_model_draft y promote_model_draft editan/promueven. Fila 8 revisa check_store/check_edges sin ejecutarlos. Fila 10 requiere que StoreFingerprint.store_hash global sea aceptada y comparada dentro de la escritura con rechazo atómico; source_hash por doc no basta. Fila 4 distingue select_documents (predicados) y search (texto rankeado más where). Fuentes de composición: solo docstrings públicos sldb.api y docs SLDB listados. Leer únicamente las secciones 1 y 4 (no 1–4) de ../pron/source/spec/14-superficie-mcp.md como documento externo. Si hay filas no disponibles, message_body contiene solo esas filas, formato exacto por fila: encabezado ## Capacidad N: <nombre>; después líneas Necesidad (con el mismo Actor/Entrada/Resultado de la fila), Rutas/símbolos revisados, Brecha, Pregunta al desk, TaskDoc: task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp. No introducción ni filas disponibles. Enviar una sola vez desde IR: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json. El campo path del JSON devuelve el archivo creado; el ID es basename sin .md. Repetirlo como sldb:<stem> y usar Resumen exacto Nota enviada; ID: sldb:<stem>. Si falla/no hay path, estado/acción siguen igual; handoff ERROR; Resumen de error exacto por campos: Nota no enviada; tarea abierta; Comando: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json; Resultado: <código de salida; stderr completo; stdout completo>; Fecha UTC: <ISO-8601>. No reintentar ni declarar notificada. Sin brechas, handoff literal — y Resumen exacto No se envió nota: todas las capacidades están disponibles. Rutas ../sldb y ../pron relativas a raíz IR. Registrar la fecha/hora UTC del snapshot en ISO-8601 `YYYY-MM-DDTHH:MM:SSZ`. Estructura del informe, en este orden: título `# Auditoría de la API pública de SLDB frente a la superficie MCP de specIR`; `## Snapshot` con commit, branch, fecha UTC ISO-8601, status y hashes; `## Matriz` con las siete columnas en el orden de Validation; `## Resumen`; `## Fuentes revisadas`. La fila 4 divide Necesidad, Estado, Evidencia, Brecha y Acción en entradas `select_documents:` y `search:` usando `<br>`; Handoff es común a la fila. Estado muestra el de cada suboperación y luego `fila: <estado más severo>`, con orden disponible < requiere-extensión-en-SLDB < faltante. El Resumen va debajo de la matriz y contiene exactamente la cadena requerida por Scope. Fuentes revisadas enumera solo documentos efectivamente leídos. Para la respuesta de message send, el envío es exitoso solo si código de salida es cero, JSON es válido y path es una cadena no vacía; cualquier otro resultado es fallo, aunque incluya path, y registra código, stderr y stdout completos. La sección Snapshot incluye el stdout exacto del comando de status como bloque fenced, con encabezado `git status (corpus):`; si no hay salida, mostrar `clean`. La lista de hashes es separada y solo contiene rutas dirty. En el registro de error del envío, Fecha UTC corresponde al inicio del intento de envío, no al snapshot.

## Validation

_List the checks required before this task can close._

- El informe contiene exactamente once capacidades y cada fila incluye capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha, acción y referencia de handoff.
- Cada fila usa uno de los estados cerrados y la acción correspondiente; disponible usa usar/componer y cada no disponible usa solicitar-extensión.
- Cada fila disponible cita la ruta/símbolo público o el doc SLDB listado que efectivamente documenta la conducta; no inventa símbolos para evidencia documental. Cuando usa composición, cita y describe cada operación y su relación documentada.
- La fila 4 informa por separado la evidencia y disponibilidad de select_documents y search; no combinar sus resultados en una sola afirmación. La fila conserva un único estado global más restrictivo y explica cada suboperación.
- Cada fila no disponible enumera módulos existentes inspeccionados y explica la conducta que falta; no cita rutas o símbolos inventados.
- El informe lista el snapshot: commit/branch de sldb si existen, fecha UTC y git status; si los archivos de fuente están modificados, incluye hashes SHA-256 para fijar la revisión auditada.
- Si hay filas no disponibles, se envió un único mensaje cuyo título y cuerpo siguen Implementation Path, y el ID exacto aparece en Resumen y filas afectadas; si no hay filas no disponibles, Resumen declara que no se envió nota y cada handoff disponible contiene el carácter literal —.
- Si deskops message send falla o no retorna ID, Resumen registra el resultado y la tarea no se cierra como notificada.
- El informe lista fuentes revisadas y no abre módulos internos de SLDB ni importa/ejecuta pron; leer la spec pron como documento está permitido.
- La tabla usa exactamente este orden de columnas: Capacidad, Necesidad, Estado, Evidencia, Brecha, Acción, Handoff.
- Para toda fila disponible, Brecha dice exactamente “Ninguna: la conducta requerida está documentada.”; para filas no disponibles describe la conducta requerida ausente o parcialmente documentada.
- La celda Necesidad usa exactamente `Actor: ...; Entrada: ...; Resultado esperado: ...`; el actor se mantiene “agente MCP de specIR operando un store SLDB”.
- Las filas no disponibles citan las rutas de los módulos existentes bajo sldb/api que se abrieron y evaluaron para esa capacidad. Si no existe símbolo relacionado, indicar “sin operación relacionada” y citar los archivos del corpus donde se buscaron candidatos por nombre/concepto; no se exige listar archivos no abiertos ni probar ausencia global fuera del corpus.
- El documento usa exactamente la estructura y títulos fijados en Implementation Path.
- La celda Necesidad usa la entrada y salida acotadas por Scope, sin agregar requisitos.
- La fila 4 divide Necesidad, Estado, Evidencia, Brecha y Acción con los sublabels `select_documents:` y `search:`; Handoff es común, y Estado incluye el estado por suboperación y el estado global más severo.
- Cada fila no disponible usa la plantilla literal de Pregunta al desk establecida en Scope; cambia solo capacidad y conducta faltante.
- Las pills asociadas se cumplen como guardrails, pero no se citan como evidencia técnica.

## Done When

_Name the observable condition that makes the task complete._

La matriz está escrita, cada fila tiene estado y cita, y los faltantes reales (si los hay) están notificados a SLDB.

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:48Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-specir-solo-usa-la-api-pública-de-sldb
status: active
summary: Dependencias permitidas del paquete specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: specIR solo usa la API pública de SLDB

## What

_Define the context or guardrail this pill carries._

El código de specIR importa de SLDB únicamente sldb.api. No importa sldb.store, sldb.core ni otros módulos internos, y no importa pron ni spec2viz.

## Why

_Explain why this context matters for safe execution._

specIR es un repo periférico sobre SLDB; pron quedó descartado como base y spec2viz va a retirarse. Acoplarse a módulos internos de SLDB es lo que desfasó a pron.

## When

_Describe when an agent should apply this pill._

En toda tarea que escriba o modifique código bajo src/specir/ o tests/.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/ y tests/; lo comprueba tests/test_imports.py.

## How

_Describe the correct way to apply this guidance._

Si falta una operación general, se documenta la carencia y se pide en el desk de SLDB con deskops message send --to sldb; la tarea se detiene en ese punto si la carencia la bloquea.

## How Not

_Describe the shortcut or failure mode to avoid._

No reimplementar en specIR lo que es general de SLDB; no copiar código de pron ni de spec2viz como dependencia; no alcanzar módulos internos de SLDB aunque funcione.

FILE:desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk
status: active
summary: Frontera de edición de las tareas de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: los cambios en otros repos se piden por su desk

## What

_Define the context or guardrail this pill carries._

Una tarea de specIR solo crea o modifica archivos dentro del repo de specIR. Lo que deba cambiar en SLDB, graph_ui, deskops, spec2viz u otro repo se pide con un mensaje a su desk y se registra como evidencia.

## Why

_Explain why this context matters for safe execution._

Cada desk es dueño de sus tareas; editar otro repo desde aquí salta sus gates y deja el cambio sin dueño.

## When

_Describe when an agent should apply this pill._

Cuando una tarea detecta una carencia en SLDB o necesita que un consumidor de spec2viz migre.

## Where

_Name the files, surfaces, or scope this pill applies to._

Fuera de specIR: sldb/, UIs/graph_ui/, deskops/, spec2viz/ y los stores de otros repos.

## How

_Describe the correct way to apply this guidance._

deskops message send --to <repo> con el pedido concreto y la referencia a la tarea de specIR; el criterio de validación de la tarea se cumple con la evidencia del cambio hecho por el otro repo.

## How Not

_Describe the shortcut or failure mode to avoid._

No editar archivos de otros repos; no listar rutas de otros repos en el campo files de una tarea de specIR; no dar por cumplido un criterio externo sin evidencia.

FILE:desk/atoms/atom-specir-depende-solo-de-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:34Z'
  authority: generated
  via: create_document
id: atom-specir-depende-solo-de-la-api-pública-de-sldb
title: specIR depende solo de la API pública de SLDB
five_wh_one_plus: how
tags:
- system:specir
- system:sldb
- topic:dependencias
- layer:arquitectura
---

# specIR depende solo de la API pública de SLDB

## Answer

specIR se construye directamente sobre la API pública de SLDB (sldb.api), como hace deskops. Una capacidad general que falte (por ejemplo una operación de grafo o de store) se pide o se agrega en SLDB; no se reimplementa dentro de specIR ni se alcanza por módulos internos de SLDB. En specIR vive lo específico: el servidor MCP, los tipos y reglas del modelado de sistemas de software, y más adelante la capa visual.

FILE:desk/atoms/atom-specir-no-depende-de-pron-adopta-contratos-no-código.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:33Z'
  authority: generated
  via: create_document
id: atom-specir-no-depende-de-pron-adopta-contratos-no-código
title: 'specIR no depende de pron: adopta contratos, no código'
five_wh_one_plus: how_not
tags:
- system:specir
- system:pron
- topic:dependencias
---

# specIR no depende de pron: adopta contratos, no código

## Answer

specIR no usa pron como base ni como dependencia: ningún import de pron y ninguna entrada suya en las dependencias del paquete. De la superficie MCP de pron (pron/source/spec/14-superficie-mcp.md) se pueden adoptar contratos reimplementados sobre SLDB: direcciones por URI, paginación con total y truncated, selectores que solo resuelven lo que el store declara, dry_run en toda escritura, niveles de mutabilidad y cero texto libre en el camino de la escritura. No se adoptan las formas, el léxico, las sesiones de diálogo ni el concepto de mundo. Decisión del dueño del proyecto, 2026-11-11: pron está desactualizado y no funciona bien como base.

FILE:instruccion
Cold-bundle de la tarea task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- El informe contiene exactamente once capacidades y cada fila incluye capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha, acción y referencia de handoff.
- Cada fila usa uno de los estados cerrados y la acción correspondiente; disponible usa usar/componer y cada no disponible usa solicitar-extensión.
- Cada fila disponible cita la ruta/símbolo público o el doc SLDB listado que efectivamente documenta la conducta; no inventa símbolos para evidencia documental. Cuando usa composición, cita y describe cada operación y su relación documentada.
- La fila 4 informa por separado la evidencia y disponibilidad de select_documents y search; no combinar sus resultados en una sola afirmación. La fila conserva un único estado global más restrictivo y explica cada suboperación.
- Cada fila no disponible enumera módulos existentes inspeccionados y explica la conducta que falta; no cita rutas o símbolos inventados.
- El informe lista el snapshot: commit/branch de sldb si existen, fecha UTC y git status; si los archivos de fuente están modificados, incluye hashes SHA-256 para fijar la revisión auditada.
- Si hay filas no disponibles, se envió un único mensaje cuyo título y cuerpo siguen Implementation Path, y el ID exacto aparece en Resumen y filas afectadas; si no hay filas no disponibles, Resumen declara que no se envió nota y cada handoff disponible contiene el carácter literal —.
- Si deskops message send falla o no retorna ID, Resumen registra el resultado y la tarea no se cierra como notificada.
- El informe lista fuentes revisadas y no abre módulos internos de SLDB ni importa/ejecuta pron; leer la spec pron como documento está permitido.
- La tabla usa exactamente este orden de columnas: Capacidad, Necesidad, Estado, Evidencia, Brecha, Acción, Handoff.
- Para toda fila disponible, Brecha dice exactamente “Ninguna: la conducta requerida está documentada.”; para filas no disponibles describe la conducta requerida ausente o parcialmente documentada.
- La celda Necesidad usa exactamente `Actor: ...; Entrada: ...; Resultado esperado: ...`; el actor se mantiene “agente MCP de specIR operando un store SLDB”.
- Las filas no disponibles citan las rutas de los módulos existentes bajo sldb/api que se abrieron y evaluaron para esa capacidad. Si no existe símbolo relacionado, indicar “sin operación relacionada” y citar los archivos del corpus donde se buscaron candidatos por nombre/concepto; no se exige listar archivos no abiertos ni probar ausencia global fuera del corpus.
- El documento usa exactamente la estructura y títulos fijados en Implementation Path.
- La celda Necesidad usa la entrada y salida acotadas por Scope, sin agregar requisitos.
- La fila 4 divide Necesidad, Estado, Evidencia, Brecha y Acción con los sublabels `select_documents:` y `search:`; Handoff es común, y Estado incluye el estado por suboperación y el estado global más severo.
- Cada fila no disponible usa la plantilla literal de Pregunta al desk establecida en Scope; cambia solo capacidad y conducta faltante.
- Las pills asociadas se cumplen como guardrails, pero no se citan como evidencia técnica.

