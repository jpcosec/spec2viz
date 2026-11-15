# Contrato de escritura y nivel de mutabilidad del MCP de specIR

> **Estado: DECIDIDO — JP aceptó las cuatro recomendaciones el 2026-11-15 (chat con el supervisor).**
> Tarea: `task-ir02-decisión-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp`.
> Redactado: 2026-11-14 por el ejecutor (agente) con alternativas y recomendación; elección de
> JP registrada el 2026-11-15 en cada sección. Los atoms de cada decisión están en la última sección.

## Insumos y alcance

- Matriz de la auditoría IR01: [docs/auditoria/sldb-api-frente-a-mcp.md](../auditoria/sldb-api-frente-a-mcp.md)
  (SLDB `b51e966`, 2026-11-14), con tres brechas notificadas a SLDB en la nota
  `sldb:20261114-074447-suggestion-specir-brechas-api-p-blica-sldb-para-mcp`: journal,
  `store_hash` como precondición atómica y deshacer.
- Contrato de referencia: `../pron/source/spec/14-superficie-mcp.md` §§4-5 (niveles 0-3,
  `dry_run`, `confirm`, simulación de efecto en el nivel 2). Se adopta como contrato, no como
  código (atom `atom-specir-no-depende-de-pron-adopta-contratos-no-código`): no hay formas,
  `MoveDoc` ni sesiones de diálogo.
- Restricción dura: toda escritura al store pasa por la API pública de SLDB
  (atom `atom-specir-depende-solo-de-la-api-pública-de-sldb`).
- Fuera: implementar; permisos multiusuario.

Evidencia de SLDB verificada en `sldb@6aeba3eb` (HEAD al 2026-11-14), además de la matriz:

| símbolo | qué hace (lo relevante aquí) |
|---|---|
| `sldb.api.apply_batch` (`src/sldb/api/documents/apply_batch.py`) | prevalida una lista de cambios (`create`, `update`, `move`, `delete`, `track`, `untrack`) y los aplica en una sola `transaction`: todo o nada. Acepta por cambio los guardas `expected_source_hash` y `expected`. Documentado en `docs/architecture/transactions.md` §`apply_batch`. |
| `sldb.api.documents.batch_prevalidate.prevalidate_changes` | la prevalidación de `apply_batch` (forma, modelo registrado, round-trip del payload bajo el modelo, guardas, destino libre). Existe como módulo dentro de `sldb.api` pero **no** está re-exportada en `sldb.api.__all__`, y `apply_batch` no tiene `dry_run`. |
| `sldb.api.transaction` / `Transaction.update(ref, payload, expected_source_hash=None, expected=None)` | guarda por documento; un guarda que no coincide es `sldb.api.ConflictError`. |
| `sldb.api.store_fingerprint(store_path).store_hash` | huella global del store; ninguna escritura la acepta como precondición (brecha IR01). |
| `sldb.api.documents.document_history.document_history` | historia de un documento desde git: por commit, `by/at/via/authority`, `source_hash`, `content_hash`, `changed_fields`. **No** devuelve payloads; las escrituras sin commit no aparecen (`docs/architecture/journal-authority.md` §1). |
| `sldb.api.journal` | retirado: devuelve siempre lista vacía (brecha IR01). |
| `sldb.api.actor.current_actor` / `SLDB_ACTOR` | quién firma el `by` de la procedencia; es una cadena declarada por el proceso, sin autenticación. |
| `sldb.api.stores.policy.Policy` (`.sldb/store.yaml`, clave `policy`) | política de hallazgos por modelo (`ignore/allow/alert/error/reindex/hook`); no tiene noción de nivel de escritura. |

Hallazgo para IR01 (no cambia su cierre, pero conviene registrarlo): la matriz no lista
`apply_batch`, que es la operación pública que mejor sostiene «proponer → validar → aplicar»
como lote atómico. Tampoco nota que `apply_batch` comprueba los guardas en la prevalidación y
luego llama a `Transaction.update(id, payload)` sin ellos: es comprobar-y-escribir dentro de
una llamada, sin cerrojo entre procesos (una carrera es posible con dos escritores
concurrentes).

---

## D1. Qué es una propuesta de cambio

**Contexto.** Plan_IR.md (fase 1) y fundamentos §7 piden `changes.propose / validate / apply`
como pasos separados. Hay que decidir qué objeto viaja entre esos pasos.

**Alternativas.**

| | alternativa | operación SLDB que la sostiene | consecuencias |
|---|---|---|---|
| D1-A | **Lote efímero prevalidado.** `propose` devuelve un lote en la forma de cambios de `apply_batch` (más los guardas que el servidor rellena, D2) y el resultado de la prevalidación; `apply` recibe ese mismo lote. El servidor no guarda nada entre pasos. | `apply_batch` para aplicar. Para validar sin escribir: `prevalidate_changes` (no re-exportada) o pedir a SLDB `apply_batch(..., dry_run=True)` público. | Sin estado en servidor ni en store; `propose` no escribe (consultas sin efectos). Encaja con el `dry_run` adoptado de pron §4. Un humano no puede revisar la propuesta salvo que el agente se la muestre. |
| D1-B | **Documento persistente de propuesta** (`ChangeProposalDoc` en el store, con estado propuesta/validada/aplicada/rechazada). | `create_document` / `save_document_payload` para la propuesta; `apply_batch` para aplicar. | Revisable y auditable en git; habilita revisión humana asíncrona. Pero proponer ya escribe en el store, hay que registrar un modelo de specIR en cada store servido, y hay que limpiar propuestas viejas. |
| D1-C | **Híbrido**: D1-A por defecto; `persist: true` guarda la propuesta como en D1-B. | las de A y B. | Flexible; dos caminos que mantener desde el día uno. |

**Recomendación: D1-A.** Es lo mínimo que cumple «proponer, validar y aplicar separados» sin
escribir al proponer, y se apoya entero en `apply_batch`. La revisión humana persistente (B)
se agrega cuando la fase de síntesis (Plan_IR fase 6) la necesite. Requiere un pedido a SLDB:
un `dry_run` público de `apply_batch` (o re-exportar `prevalidate_changes`); mientras no
exista, specIR no debe importar el módulo interno sin que SLDB lo declare público.

- Alternativa elegida: **D1-A (lote efímero prevalidado)**
- Motivo: se acepta la recomendación: proponer no escribe y aplicar es todo o nada por `apply_batch`; el `dry_run` público se pide a SLDB.
- Fecha: 2026-11-15
- Decidió: JP (chat con el supervisor)

## D2. Qué precondición protege la aplicación

**Contexto.** «No se aplica un cambio sobre un estado que ya no es el que se validó»
(atom de principios de seguridad). IR01 pidió a SLDB `store_hash` como precondición atómica.

**Alternativas.**

| | alternativa | operación SLDB | consecuencias |
|---|---|---|---|
| D2-A | **Guarda por documento**: al validar, el servidor anota `expected_source_hash` de cada documento que el lote toca (update, move, delete, untrack); `create`/`track` exigen ausencia. | `apply_batch` con `expected_source_hash` (y opcional `expected`); `ConflictError`. Disponible hoy. | Rechaza solo conflictos reales sobre lo tocado. No ve cambios en documentos leídos pero no escritos (p. ej. un `RelationTypeDoc` que cambió y altera la validez de una arista nueva). Carrera residual entre procesos (ver hallazgo). |
| D2-B | **Huella global**: el lote lleva el `store_hash` visto al validar; `apply` rechaza si cambió. | `store_fingerprint` para leer; la comparación atómica **no existe** (brecha IR01, nota enviada). Emularla en specIR (leer huella y luego `apply_batch`) no es atómico. | Máxima seguridad; falsos conflictos ante cualquier escritura ajena (en un store activo, casi siempre). Depende de SLDB. |
| D2-C | **A ahora, B cuando SLDB la entregue, por nivel**: nivel 1 con guarda por documento; nivel 2 (reglas, cuya simulación depende de todas las aristas del tipo) con `store_hash` atómico. | A hoy; B tras la extensión pedida. | Cada nivel con la guarda que su validez necesita. Hasta que SLDB responda, el nivel 2 aplica con guarda por documento y vuelve a simular justo antes de `apply_batch`, aceptando la carrera residual. |

**Recomendación: D2-C.** El guarda por documento es obligatorio y lo rellena el servidor, nunca
el agente. La huella global solo vale para el nivel 2, donde la validez depende del store
entero; ahí la extensión pedida a SLDB es la que cierra el hueco. Si JP prefiere no depender
de SLDB, D2-A solo es suficiente para el nivel 1.

- Alternativa elegida: **D2-C (guarda por documento en nivel 1; `store_hash` atómico para nivel 2 cuando SLDB lo entregue)**
- Motivo: se acepta la recomendación: cada nivel con la guarda que su validez necesita.
- Fecha: 2026-11-15
- Decidió: JP (chat con el supervisor)

## D3. Dónde se declara el nivel de escritura permitido

**Contexto.** Niveles de pron §5: 0 lectura; 1 contenido (documentos y aristas); 2 reglas
(tipos de relación, `RuleDoc`, transiciones); 3 modelos. El atom de seguridad exige que «los
límites de escritura los impone el servidor, no el agente ni la interfaz»; pron añade que el
nivel nunca sale de un argumento del tool.

**Alternativas.**

| | alternativa | operación SLDB | consecuencias |
|---|---|---|---|
| D3-A | **Al arrancar el servidor**, por store montado (`--store NAME=PATH --level N`). | Ninguna: el servidor filtra antes de llamar a `sldb.api`. | Lo fija el operador, no el agente; simple; no viaja con el store (cada arranque lo repite). |
| D3-B | **En un documento del store** (como `mutability` del `ProjectionDoc` de pron). | Un modelo de specIR en el store (`create_document`), o una clave nueva en `.sldb/store.yaml` (hoy `Policy` no la tiene: pedido a SLDB). | Versionado con el store. Riesgo de escalada: un agente de nivel ≥1 podría editar el documento que le da el nivel, así que ese modelo debe quedar fuera de lo escribible. |
| D3-C | **Por actor** (`SLDB_ACTOR` / `actor=`). | `sldb.api.actor.current_actor`. | El actor es una cadena declarada, sin autenticación: no es una frontera de seguridad. Además cae en permisos multiusuario (fuera de alcance). |
| D3-D | **A como techo, B solo para bajar**. | las de A y B. | Seguro y versionable; más superficie. |

**Recomendación: D3-A**, con nivel **0 por defecto** (sin `--level`, el servidor es de solo
lectura, coherente con IR03) y los niveles acumulativos de pron. Es lo único que el agente no
puede tocar y no exige nada de SLDB. D3-D queda como evolución si un store necesita restringirse
por sí mismo.

- Alternativa elegida: **D3-A (al arrancar el servidor, por store montado; nivel 0 por defecto)**
- Motivo: se acepta la recomendación: es lo único que el agente no puede tocar y no exige nada de SLDB.
- Fecha: 2026-11-15
- Decidió: JP (chat con el supervisor)

## D4. Si existe deshacer

**Contexto.** pron §4 tiene `kb_undo` sobre su ledger. SLDB no tiene operación pública para
revertir una escritura completada (`transaction` revierte solo si el bloque lanza; brecha
IR01, nota enviada). El nivel 3 (modelos) queda excluido en cualquier caso.

**Alternativas.**

| | alternativa | operación SLDB | consecuencias |
|---|---|---|---|
| D4-A | **No hay deshacer; basta git.** | `document_history` para ver versiones; revertir es una escritura nueva por `apply_batch`. | Nada que construir. Pero `document_history` no da payloads (hay que leer la versión con `git show` y extraerla con `sldb.api.extract_document_payload`), y lo escrito sin commit no está en la historia: un error del agente entre commits no se recupera por la API. |
| D4-B | **Deshacer nativo de SLDB.** | No existe (brecha IR01). | Lo correcto a largo plazo; bloquea hasta que SLDB lo entregue. |
| D4-C | **Deshacer en specIR como lote inverso**: al aplicar, el servidor guarda el inverso del lote (update → payload anterior; create → delete; delete → create con payload y ruta; move → move de vuelta), con guardas `expected_source_hash` de lo que dejó el apply. `undo` aplica el inverso por `apply_batch` y falla con `ConflictError` si alguien escribió después. | `apply_batch`, guardas, `extract_document_payload`/`runtime_document` para capturar el antes. Todo público. | Funciona hoy y sin camino lateral. Alcance acotado: niveles 1-2, últimos N lotes de la sesión del servidor (se pierde al reiniciar salvo que se persista). |

**Recomendación: D4-C** (en memoria, últimos lotes de la sesión, niveles 1-2), con git como
historia durable y el pedido a SLDB abierto; si SLDB entrega D4-B, specIR la adopta y retira
la suya.

- Alternativa elegida: **D4-C (lote inverso con guardas en specIR, niveles 1-2, últimos lotes de la sesión; git como historia durable)**
- Motivo: se acepta la recomendación; si SLDB entrega deshacer nativo, specIR lo adopta y retira el suyo.
- Fecha: 2026-11-15
- Decidió: JP (chat con el supervisor)

---

## Comprobación: ningún camino lateral

Todas las alternativas recomendadas escriben solo por `sldb.api.apply_batch` (que delega en
`create_document`, `save_document_payload`, `delete_document`, `move_document`,
`track_document_file`, `untrack_document`). D4-A es la única que exige leer git fuera de SLDB,
y aun así escribe por la API.

## Pedidos a SLDB que se derivan (si se acepta la recomendación)

1. `dry_run` público en `apply_batch` (o re-exportar `prevalidate_changes`) — nuevo, D1.
2. Precondición atómica por `store_hash` — ya pedida en IR01, D2 (nivel 2).
3. Deshacer nativo — ya pedido en IR01, D4 (opcional si se adopta D4-C).
4. Guardas re-verificados dentro de la transacción de `apply_batch` o un cerrojo de escritura
   del store — nuevo, cierra la carrera residual de D2.

Se envían por `deskops message send --to sldb` después de la elección de JP (pill de guardrail).

## Atoms

Creados el 2026-11-15 con `deskops add atom --provenance docs/decisiones/contrato-de-escritura-mcp.md`:

- D1: `atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado`
- D2: `atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2`
- D3: `atom-el-nivel-de-escritura-del-mcp-se-fija-al-arrancar-el-servidor`
- D4: `atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas`
- Actualizado con `deskops edit atom`: `atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir`
  (cita los cuatro mecanismos y ya no los declara pendientes).
