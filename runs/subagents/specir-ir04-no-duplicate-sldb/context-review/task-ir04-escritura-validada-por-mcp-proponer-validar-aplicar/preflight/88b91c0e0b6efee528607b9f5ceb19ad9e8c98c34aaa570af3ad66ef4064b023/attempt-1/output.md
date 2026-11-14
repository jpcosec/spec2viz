## REFORMULACION

**Propósito:** dotar al MCP de specIR de escritura validada sobre un store SLDB real, de modo que un agente pueda proponer, validar y aplicar cambios sin dejar el modelo inconsistente y con rastro de autoría.

**Resultado:** tools MCP de escritura (crear/editar/borrar documentos de modelos registrados; afirmar/retirar RelationDoc; declarar/editar RelationTypeDoc y RuleDoc), todas con ejecución en seco, más pruebas en `tests/mcp/`.

**Repo:** `SLDB_1/IR`, paquete `src/specir/mcp/` (`write_tools.py`, `changes.py`, `mutability.py`).

**Límites:** no se crean clases Python de modelo ni CRUD propio; toda operación delega en `sldb.api` (`create_document`, `save_document_payload`, `delete_document`, `transaction`). Sin acceso directo a filesystem ni índices. Si falta capacidad en la API pública, no se implementa en specIR: se solicita a SLDB.

## AMBIGUEDADES

1. «con el mecanismo decidido en la tarea de contrato de escritura» — el resultado de IR02 no está en el input; obligaría a inventar contrato, forma del dry-run y precondiciones.
2. «según la severidad de la regla» — no se definen niveles; obligaría a inventar el mapeo severidad→rechazo/reporte.
3. «Una tool por encima del nivel de escritura permitido» — no se define la escala de niveles; obligaría a inventar la jerarquía y su comprobación.
4. «lleva en su procedencia quién y por qué operación se escribió» — no se especifican campos ni formato; obligaría a inventar el esquema de procedencia.
5. «contra un store de prueba» — no se define el fixture ni su ciclo de vida; obligaría a inventar la infraestructura de pruebas.

## DRY-RUN

**Lecturas:** TaskDoc, atoms y pills citados, salidas de IR02 e IR03, superficie pública de `sldb.api`.
**Cambios previstos:** tres módulos en `src/specir/mcp/` y tres tests.
**Dependencias:** IR02 (contrato/mutabilidad), IR03 (servidor solo-lectura), `sldb.api`.
**Validaciones futuras:** dry-run sin escritura; rechazo por cambio concurrente; validación de aristas por tipo/cardinalidad; reglas por severidad; solo argumentos tipados; procedencia; bloqueo por nivel; inexistencia de tools sobre módulos Python.

No es un nodo agregado: es una tarea de código ejecutable.

## FUTURO

IR02 fija el contrato y el nivel de mutabilidad; IR03 aporta el servidor de lectura; el desk SLDB decide y provee mecanismos ausentes de dry-run/precondición; un humano decide la edición de clases de modelo por MCP.
