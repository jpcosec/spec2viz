## REFORMULACION

Propósito: dotar al MCP de specIR de escritura controlada sobre el store SLDB mediante pasos separados de proponer, validar y aplicar. Resultado: tools MCP de escritura con ejecución en seco, validación de aristas y reglas, procedencia y límite de mutabilidad. Repo: specIR, con cambios previstos en `src/specir/mcp/` y `tests/mcp/`. Límites: usar solo `sldb.api`; no crear ni editar clases Python de modelos por MCP; no sintetizar código de aplicación; sin mocks; detenerse si falta una capacidad real. Depende de IR02 (contrato de escritura) e IR03 (servidor/store real). Es una tarea de código, no un agregado.

## AMBIGUEDADES

1. “con el mecanismo decidido en la tarea de contrato de escritura” y “cómo se representa una propuesta, qué precondición protege la aplicación, dónde se declara el nivel de escritura permitido y qué taxonomía de procedencia se usa están pendientes de decisión”: sin ese contrato, habría que inventar representación, precondición, niveles y procedencia.
2. “según la severidad de la regla”: no define severidades ni cuándo rechazar o reportar; obligaría a inventar la taxonomía y el mapeo.
3. “store que cambió después de la validación”: no define cómo detectar el cambio ni la forma del error; obligaría a inventar versionado, hash o condición.
4. “Cada documento escrito lleva en su procedencia quién y por qué operación”: no define campos ni formato; obligaría a inventar el esquema de procedencia.

## DRY-RUN

Lecturas: TaskDoc, rituales `execution`, `testing` y `closeout`, pills, átomos, salidas de IR02/IR03, API pública de SLDB y pruebas existentes. Cambios previstos: `src/specir/mcp/write_tools.py`, `changes.py`, `mutability.py`; `tests/mcp/test_write_tools.py`, `test_dry_run.py`, `test_mutability.py`. Dependencias: contrato de IR02, store real de IR03 y `sldb.api`. Validaciones futuras: ejecutar pruebas; comprobar dry-run sin escritura; rechazo por estado obsoleto; validación de aristas y reglas; argumentos tipados; procedencia; nivel de escritura; ausencia de tools que modifiquen Python; `tests/test_imports.py`. Sin ejecutar nada.

## FUTURO

IR02 produce el mecanismo de escritura; IR03 aporta el servidor y store de solo lectura; un humano decide lo que el contrato deje pendiente; el desk de SLDB añade la API general faltante; closeout actualiza el board y prepara el commit.
