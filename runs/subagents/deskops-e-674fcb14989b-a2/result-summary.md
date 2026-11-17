# IR04b intento 2 (deskops-e-674fcb14989b-a2): EJECUTOR BLOQUEADO: hallazgos para sldb

Sin commit, sin git add. Tocados: `src/specir/mcp_extension.py`, `tests/test_mcp_extension.py`, `tests/test_mcp_undo.py` (nuevo).

## Qué cambió en la extensión
- Ya no crea `WriteTools`, no quita ni registra `propose_changes`/`apply_changes`. Con nivel >= 1 registra `context.add_batch_validator(verification_is_not_written)`: finding `{code: specir_agent_verifies, level: error, what, subject}` por cada cambio que escribe `verificacion: verificado`. `claims_verified` reconoce `CreateDocument`/`UpdateDocument`/`AssertEdge` (propose) y `BatchChange` (apply). Un update de lote lleva el payload entero: solo cuenta como reclamo si el documento guardado no estaba ya verificado.
- Resultado real por MCP: `{'applied': False, 'rejected': 'domain', 'explanation': '1 domain check(s) failed', 'written': False, 'findings': [...]}` (create, update de nodo, update `attributes.verificacion` de arista, assert_edge).
- Con la extensión montada el `undo_changes` de sldb ya encuentra lo aplicado (`undone: 1`): se corrigió la causa del intento 1.

## Pruebas (validation.log)
- test_mcp_extension 11 passed (nuevos: tools de escritura son las de sldb; rechazo `domain` en propose sin escribir; el validador registrado rechaza `BatchChange` reales de una propuesta; edición de un nodo ya verificado no es reclamo). En apply no se llega al validador con una propuesta manipulada: el sello se comprueba antes; se prueba el validador con BatchChange reales.
- test_imports 9, test_sync_generation_parity 22 passed.
- **test_mcp_undo: 2 passed (nivel 0 sin tools/undo; grep (f)), 6 failed por hallazgos de sldb** (abajo). No se usó xfail.
- Fuera de mi alcance y rotos por el cambio de forma del rechazo (coordinador): `tests/models/test_blog_chain.py::test_an_agent_does_not_verify_through_the_mcp` (esperaba error de herramienta con "IR05 D2-E"; ahora es respuesta `domain`) y `tests/models/test_domain_tools.py::test_the_write_tools_come_with_the_extension_from_level_1` (esperaba "IR05 D2-E" en la descripción de propose_changes; ahora la descripción es la de sldb).

## Hallazgos para sldb (salida exacta en undo-run3.log)
1. **Deshacer no deja el store idéntico.** El undo de un lote (crear + editar + arista) devuelve el contenido, pero re-sella la procedencia: el `.md` `undo/domain/seed-op.md` cambia solo en `sldb.at` (`'2026-11-17T16:50:50Z'` -> `'...16:51:13Z'`); el índice `.sldb/core/documents/DomainOperationDoc/undo-seed-op.yaml` cambia `source_hash`, `at` y `via: create_document -> save_document_payload`; `core/models/DomainEntityDoc.yaml` pasa `sections_index: ''` -> `.sldb/runtime/sections/DomainEntityDoc.yaml`; `DomainOperationDoc.yaml` cambia `model_hash`/`roster_hash`; `store_index.yaml` cambia `store_hash`. Falla Validation 1 (sha256 de .md y del store). Pruebas: `test_the_store_files_are_byte_identical_after_the_undo` (estricta) y `..._to_the_same_documents`.
2. **El guard stale no se satisface tras revertir el cambio ajeno.** Cambio ajeno por `sldb.api.apply_batch` fuera de la sesión, revertido a su contenido; `undo_changes` sigue respondiendo `{'applied': False, 'rejected': 'stale', 'explanation': "... undo-seed-op changed in the store: expected '213c32e8...', found '4baced0e...'. It stays in the stack.", 'written': False, 'document': 'undo-seed-op', 'remaining': 1}`. El guard compara `source_hash`, que incluye la procedencia re-sellada, y ningún lote que devuelva el contenido puede reproducirlo. Falla Validation 2 (el undo posterior lo deshace).
3. **`steps=2` sobre el mismo documento escribe a medias.** Dos lotes (el segundo edita una entidad del primero): `undo_changes(steps=2)` -> `{'applied': False, 'rejected': 'stale', 'explanation': "... undo-entity-d1 ... ", 'written': True, ...}`: el inverso del segundo se escribió y el del primero se rechazó, porque el primero espera el hash anterior al segundo. Es la misma causa de fondo que 1-2.
4. Nivel 1: un lote con RuleDoc se rechaza en propose (`LevelError ... needs write level 2`), no hay lote de reglas en la pila, y un nivel 1 no deshace un lote de nivel 2 (`nothing_to_undo`). Nivel 2 deshace el lote con RuleDoc (`applied True`). Cumple. Su comprobación final de store idéntico falla por 1.
5. Tras el undo: `sldb rules check` rc 0 ("sin hallazgos") y `sldb edges check` rc 0 (nota: stores enlazados con stale, no propios). Los validadores registrados corridos sobre el documento del lote: sin errores (el test llega a esa comprobación solo si pasa la anterior; en la corrida el assert previo de digest falla por 1, así que **no quedó verificado en esta corrida**). sldb aplica el inverso con `apply_batch` directo, por lo que los validadores de dominio no corren sobre el undo.
6. grep (f): única coincidencia en bpmn-js minificado de terceros (vendor); specIR no define undo ni guarda lotes. `deskops graph missing --root .` rc 0.

## Revisar por el supervisor
- Decidir si 1-3 se piden a sldb por su desk (inbox) o se relaja la Validation a "mismo contenido salvo procedencia".
- Ajustar los dos tests de `tests/models/` citados.
- `.scion/settings.yaml` sin seguimiento ya existía.
