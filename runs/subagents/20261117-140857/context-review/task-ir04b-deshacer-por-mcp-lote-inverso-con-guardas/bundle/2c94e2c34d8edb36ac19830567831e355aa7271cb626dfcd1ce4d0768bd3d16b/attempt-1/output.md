REFORMULACION
Propósito: verificar desde specIR que el `undo_changes` de `sldb mcp` deshace los últimos lotes de la sesión con la extensión de specIR montada. Resultado: pruebas nuevas en `tests/` con cliente MCP real y copia montada; solo si hace falta, ajuste en `src/specir/mcp_extension.py`. Repo: solo specIR. Límites: no registrar la tool, no guardar pila ni construir inversos (son de sldb mcp); fuera deshacer entre sesiones y nivel 3; si sldb mcp no sirve `undo_changes`, se detiene. Es ejecutable, no agregado.

AMBIGUEDADES
1. "niveles 1 y 2" frente a "los niveles 0 y 1 se respetan": obliga a inventar si se prueba nivel 2.
2. "add_batch_validator" no existe en el `mcp_extension.py` incluido: habría que inventar su API y cómo interviene en `sldb.api.apply_batch`.
3. "undo_changes responde applied false, rejected stale y document": sin nombre de tool, argumentos ni esquema; habría que inventarlos.
4. "copia montada del store" / "store real" frente a fixtures: `store_copy` es de solo lectura y `blog` es un store nuevo; no hay copia montada escribible. Habría que inventar el fixture.
5. "una vez revertido el cambio ajeno": no se define cómo; habría que inventar un segundo lote.
6. El átomo dice "specIR solo guarda esos inversos en la sesión del servidor" y la tarea "no registra la tool ni guarda la pila": obliga a decidir qué manda.
7. "deskops graph missing --root .": sin cwd ni certeza de disponibilidad; habría que inventar la invocación.

DRY-RUN
El ejecutor futuro leería TaskDoc, rituales, pills, átomos y `conftest.py`; confirmaría el cierre del espejo de `undo_changes`; inspeccionaría el contrato real de la tool; montaría una copia escribible de nivel 1; escribiría `tests/test_*undo*.py`; aplicaría un lote creación/edición/arista, lo desharía, compararía digests, probaría stale y niveles; correría `pytest` acotado, `grep -nE "undo_changes|inverse" src/specir` y `deskops graph missing --root .`. Dependencias: sldb mcp con `undo_changes`, fixtures y validadores. Sin ejecutar.

FUTURO
sldb produce el cierre del espejo y el contrato/implementación de `undo_changes`; un humano decide si entra el nivel 2 y si un hallazgo se escala al desk de sldb.
