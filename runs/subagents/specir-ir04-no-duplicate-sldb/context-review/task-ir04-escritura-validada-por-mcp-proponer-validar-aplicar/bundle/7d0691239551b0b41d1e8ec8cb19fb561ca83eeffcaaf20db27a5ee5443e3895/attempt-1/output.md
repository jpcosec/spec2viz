REFORMULACION
Nodo ejecutable de código, no agregado: construir la superficie de escritura del servidor MCP de specIR para que un agente proponga, valide y aplique cambios sobre un store SLDB. Propósito: permitir modelado sin dejar el grafo inconsistente y con rastro de autoría. Resultado: tools en `src/specir/mcp/write_tools.py`, `changes.py` y `mutability.py`, con pruebas en `tests/mcp/test_write_tools.py`, `test_dry_run.py` y `test_mutability.py`. Repo: `src/specir/` y `tests/`. Límites: solo tools MCP; toda operación delega en `sldb.api` (`create_document`, `save_document_payload`, `delete_document`, `transaction` y mecanismos existentes de dry-run/precondición); nada de CRUD propio, escritura directa a filesystem/índices, edición de clases Python ni síntesis de código; si falta capacidad, se pide a SLDB y se detiene.

AMBIGUEDADES
1. “la condición de su RelationTypeDoc”: no se define qué condición ni su semántica; obligaría a inventar el predicado y su evaluación.
2. “según la severidad de la regla”: no hay niveles ni mapeo a rechazo/reporte; obligaría a inventar taxonomía y política.
3. “Cada documento escrito lleva en su procedencia quién y por qué operación se escribió”: no hay esquema de procedencia; el átomo dice que la taxonomía está pendiente, así que obligaría a inventar campos y formato.

DRY-RUN
Lecturas: TaskDoc, rituales, pills, átomos, salidas de IR02 e IR03 y capacidades reales de `sldb.api`. Cambios previstos: tools tipadas de proponer/validar/aplicar para crear/editar/borrar documentos y afirmar/retirar aristas y documentos de tipo/regla; representar propuestas y precondiciones; imponer nivel de escritura; pruebas contra store SLDB real. Dependencias: contrato de escritura y niveles (IR02), servidor de solo lectura (IR03), registro de modelos y API de SLDB. Validaciones futuras: ejecutar `tests/mcp` y `tests/test_imports.py`; comprobar dry-run sin escritura, rechazo por estado obsoleto, aristas y reglas inválidas, solo argumentos tipados, procedencia, error por nivel y ausencia de tools que editen Python. Sin ejecutar nada.

FUTURO
IR02 debe entregar el mecanismo de escritura, los niveles de mutabilidad y el contrato de precondición/dry-run; IR03, el servidor de lectura. SLDB debe aportar o ampliar las operaciones que falten. Un humano decide si la brecha bloquea y autoriza la parada; el store real de prueba lo aporta el entorno.
