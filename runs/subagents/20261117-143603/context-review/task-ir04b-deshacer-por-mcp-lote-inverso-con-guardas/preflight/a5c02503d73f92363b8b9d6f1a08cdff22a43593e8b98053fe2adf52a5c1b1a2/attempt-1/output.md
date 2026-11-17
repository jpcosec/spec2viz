## REFORMULACION

**Propósito:** verificar desde specIR, con cliente MCP real y la extensión de dominio montada, que el `undo_changes` servido por sldb mcp deshace los últimos lotes de la sesión, incluidos los que pasan por validadores de specIR. **Resultado:** pruebas nuevas en `tests/test_mcp_undo`, sin mocks, sobre copia escribible del store; evidencia en `result-summary.md`; ajuste mínimo en `src/specir/mcp_extension.py` solo si es imprescindible. **Repo:** IR/specIR; sldb es dependencia externa. **Límites:** no registrar `undo_changes`, no guardar pila ni construir lotes inversos, no deshacer entre sesiones ni nivel 3; cambios en otros repos se piden por su desk; si sldb mcp no sirve `undo_changes`, no se ejecuta.

## AMBIGUEDADES

1. “sha256 de los .md y del store” frente a “La huella es tree_digest de la copia”: no queda claro qué huella usar. Obligaría a inventar el criterio de comparación.
2. “usando los fixtures de tests/conftest.py (mount_copy, store_copy y la sesión mcp)”: no se detalla cómo se parametriza el nivel de la sesión MCP por caso. Obligaría a inventar una API de fixtures.
3. “Si hace falta algo en la extensión de specIR para que el deshacer pase por sus validadores, se agrega”: no define “hace falta”. Obligaría a inventar el umbral para modificar código.
4. “Un agente por MCP aplica un lote y lo deshace”: puede leerse como prueba automatizada o ejecución manual de un agente. Obligaría a inventar el modo de cierre.
5. “los niveles 0 y 1 se respetan” frente a “Se prueban 0, 1 y 2”: hay tensión sobre si nivel 2 es obligatorio. Obligaría a inventar el alcance final.

## DRY-RUN

Lecturas: TaskDoc, nota de inbox, pills, espejos de `depends_on`, `tests/conftest.py`, `src/specir/mcp_extension.py` y `sldb/src/sldb/mcp/mutability.py`. Cambios previstos: crear `tests/test_mcp_undo.py`; aplicar por MCP lotes de creación, edición y arista; deshacer; probar stale; probar niveles 0, 1 y 2; comparar huella; ejecutar `sldb rules check` y `edges check`; `grep -nE "undo_changes|inverse" src/specir`; `deskops graph missing --root .`. Dependencias: espejos cerrados y `undo_changes` disponible en sldb mcp. Sin ejecutar nada.

## FUTURO

Un humano resuelve las ambigüedades 1–5. sldb mcp provee el comportamiento real; si aparece un hallazgo, el equipo de sldb decide y corrige. Otro nodo valida el cierre con las pruebas y la evidencia.
