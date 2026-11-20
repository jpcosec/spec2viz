---
sldb:
  by: agent
  at: '2026-11-20T23:08:20Z'
  authority: generated
  via: save_document_payload
id: task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-ef3b25a2dd59 FALLA sobre 1be6fc1 (ya
  está en main por el reap). (1) Validation 1 pide sha256 idéntico de los .md y del
  store tras deshacer, y quedó como xfail estricto. Por el contrato de sldb (nota
  20261118-211934, sldb efd5ebb8: ''mismo contenido salvo procedencia''; deshacer
  re-sella sldb.at/sldb.via y los hashes derivados), esa validación se cumple comparando
  el contenido sin el bloque sldb: el sha256 del texto sin bloque sldb, como sldb/api/documents/content_hash.py
  de sldb, igual antes y después, documento por documento, y el store por el mismo
  criterio. Intento 2: reescribir esa prueba así, sin xfail, y que pase. (2) Regresiones
  bloqueantes: tests/models/test_blog_chain.py::test_an_agent_does_not_verify_through_the_mcp
  y tests/models/test_domain_tools.py::test_the_write_tools_come_with_the_extension_from_level_1
  esperan que propose_changes falle como error de herramienta con ''IR05 D2-E'' en
  el mensaje y en su descripción. El commit lo movió a un validador de add_batch y
  cambió ese comportamiento. Intento 2: conservar ese comportamiento (propose_changes
  sigue rechazando con un error de herramienta que nombra ''IR05 D2-E'' y su descripción
  lo menciona) sin tocar los asserts de esas dos pruebas. Antes de entregar, correr
  tests/test_mcp_undo.py, tests/models/test_blog_chain.py, tests/models/test_domain_tools.py
  y tests/test_mcp_extension.py, de a uno, todos en verde. Commit desde tu worktree
  con ''git commit -- <rutas>'' y trailer Task-Id.'
references:
- desk/inbox/20261116-232335-suggestion-sldb-responde-ir04b-undo-changes-mensaje-de-notationspec-ir13e-y-regresi-n-de-b2.md
depends_on:
- task-espejo-sldb-sldb-mcp-servidor-mcp-genérico-a
- task-espejo-sldb-apply-batch-devuelve-el-lote-inverso-deshacer
- task-espejo-sldb-sldb-mcp-sirve-undo-changes-con-la-pila-de-lotes-inversos-de-la-sesión
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- src/specir/mcp_extension.py
- tests/conftest.py
- tests/test_mcp_extension.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
---

# IR04b Deshacer por MCP: adaptador sobre el lote inverso de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

IR02 decidió (D4) que el deshacer del MCP es un lote inverso con guardas para los últimos lotes de la sesión en niveles 1 y 2, pero IR04 dejó el deshacer fuera de su alcance y ninguna tarea lo cubre.

## Goal

_Describe the concrete result this task must produce._

Verificar desde specIR, con un cliente MCP real sobre sldb mcp y la extensión de dominio de specIR montada, que el undo_changes que sirve sldb mcp deshace los últimos lotes de la sesión, incluidos los que pasan por los validadores de dominio de specIR. sldb decidió (nota de inbox 20261116-232335) que undo_changes y la pila de lotes inversos por sesión son de sldb mcp. specIR no registra la tool ni guarda la pila.

## Scope

_State what is in scope and what is out of scope._

Dentro: pruebas de specIR que, sobre una copia montada del store, aplican lotes por MCP con la extensión de specIR montada y los deshacen con el undo_changes de sldb mcp; comprobar que el store queda como antes, que un lote stale se rechaza sin escribir, y que los niveles 0 y 1 se respetan. Si hace falta algo en la extensión de specIR para que el deshacer pase por sus validadores, se agrega en src/specir/mcp_extension.py. Fuera: registrar undo_changes en specIR, guardar la pila o construir lotes inversos, porque todo eso es de sldb mcp; deshacer entre sesiones; nivel 3. Si sldb mcp no sirve undo_changes, la tarea no se ejecuta.

## Implementation Path

_Outline the expected implementation route or affected surface._

Esperar a que cierre el espejo task-espejo-sldb-sldb-mcp-sirve-undo-changes-con-la-pila-de-lotes-inversos-de-la-sesión. Después, escribir las pruebas en un archivo de prueba nuevo bajo tests/, dedicado al deshacer, usando los fixtures de tests/conftest.py (mount_copy, store_copy y la sesión mcp) contra el sldb mcp real. Sin mocks. La única lógica nueva en specIR, si hace falta, es la que su extensión necesite para que el deshacer pase por sus validadores; ni inversión ni guardas. Precisiones (preflight-1 y bundle-1): (a) los tres espejos de depends_on están cerrados (undo_changes en sldb d0ee07a3/02ea724e, en origin). (b) Niveles de sldb mcp, en sldb/src/sldb/mcp/mutability.py: 0 read, 1 content y 2 rules (RelationTypeDoc y RuleDoc); el 3 no se sirve. Se prueban 0, 1 y 2: con 2 se deshace un lote que tocó RelationTypeDoc o RuleDoc. (c) La copia escribible es la de mount_copy de tests/conftest.py, con su sesión MCP de escritura arrancada con el nivel de cada caso; el store_copy de solo lectura no sirve. La huella es tree_digest de la copia. (d) Las tools y respuestas son las de sldb mcp: apply_changes y undo_changes(steps), con rechazo {applied: false, rejected: stale, document, written: false}. Revertir el cambio ajeno es aplicar otro lote que devuelve el documento a su contenido anterior. (e) Corrección tras el hallazgo del intento 1 (coordinador, 2026-11-17): src/specir/mcp_extension.py crea un segundo WriteTools de sldb y reemplaza propose_changes y apply_changes; ese WriteTools tiene su propia pila, así que el undo_changes de la sesión no encuentra lo aplicado (nothing_to_undo). Se corrige en specIR: la extensión deja de crear WriteTools y de quitar o registrar propose_changes y apply_changes, y registra su regla IR05 D2-E (no escribir verificacion: verificado) con context.add_batch_validator de sldb mcp, como hallazgo de nivel error; el validador recibe Change tipados en propose_changes y BatchChange en apply_changes, y debe reconocer ambos. Las pruebas existentes de tests/test_mcp_extension.py que esperaban el rechazo anterior se ajustan al rechazo domain de sldb, sin debilitar lo que comprueban. Tras undo_changes el store pasa sldb rules check y sldb edges check, y se deja escrito qué hace undo_changes con los validadores de dominio (sldb aplica el lote inverso con apply_batch directo). (f) Cuenta como implementación propia una def, una tool registrada o una estructura que guarde lotes; las menciones en docstrings y las llamadas a la tool de sldb no cuentan. (g) La prueba va en un módulo nuevo de la carpeta de pruebas, llamado test_mcp_undo; deskops graph missing se corre desde la raíz de IR.

## Validation

_List the checks required before this task can close._

- Con un cliente MCP real sobre una copia montada del store, aplicar un lote de creación, edición y arista y deshacerlo con undo_changes deja la copia idéntica a antes (sha256 de los .md y del store).
- Si un documento del lote cambió después de aplicarlo, undo_changes responde applied false, rejected stale y document con ese documento, sin escribir nada, y el lote sigue en la pila (un undo_changes posterior, una vez revertido el cambio ajeno, lo deshace).
- Con nivel 0 no hay herramientas de escritura ni undo_changes; con nivel 1 no se deshace un lote que tocó RelationTypeDoc o RuleDoc (si sldb mcp lo permitiera, es un hallazgo para sldb: se registra y la tarea se detiene, no se implementa en specIR).
- Si el lote deshecho pasó por los validadores de dominio de specIR (add_batch_validator), se comprueba qué hace undo_changes con ellos (sldb lo aplica con sldb.api.apply_batch directo) y el resultado queda escrito; si el deshacer deja el store en un estado que esos validadores rechazarían, es un hallazgo para sldb.
- specIR no define undo_changes ni guarda lotes inversos: grep -nE "undo_changes|inverse" src/specir no encuentra una implementación propia.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

Un agente por MCP aplica un lote y lo deshace con el undo_changes de sldb mcp, con la extensión de specIR montada, sobre una copia del store real, y el store queda como estaba; specIR no implementa el deshacer.
