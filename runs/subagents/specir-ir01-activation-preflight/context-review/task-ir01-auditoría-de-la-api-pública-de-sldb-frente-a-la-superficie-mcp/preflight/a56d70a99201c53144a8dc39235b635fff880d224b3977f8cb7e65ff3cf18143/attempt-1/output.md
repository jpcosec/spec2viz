**REFORMULACION**

Nodo ejecutable (TaskDoc), no agregado. Encargo: auditar la API pública de SLDB frente a las necesidades de la futura superficie MCP de specIR y producir `docs/auditoria/sldb-api-frente-a-mcp.md`, una matriz de 11 capacidades con campos fijos y estados cerrados. Repo: specIR (cwd `IR`). Límites: no escribir código, no modificar SLDB, no diseñar tools MCP, no importar/ejecutar pron ni depender de `sldb.store`/`sldb.core`. Solo se permite leer `pron/source/spec/14-superficie-mcp.md` como referencia documental. Si hay capacidades no disponibles, notificar por una única nota al desk de SLDB y registrar su ID.

**AMBIGUEDADES**

1. “Si hay alguna fila no disponible, enviar una única nota agregada al desk de SLDB” frente a “Solo si una fila queda como faltante real (no existe ni se puede componer con operaciones públicas existentes), se envía una nota”. Obliga a inventar si `requiere-extensión-en-SLDB` también dispara nota o solo `faltante`.

2. “Cada fila usa campos fijos: capacidad; […] referencia de handoff”. No define qué valor lleva ese campo cuando la fila es `disponible` o `requiere-extensión`. Obliga a inventar formato (¿ID de nota, ruta, “N/A”?).

3. “Listar los módulos API y documentos de arquitectura revisados para que la ausencia sea comprobable”. No enumera los documentos de arquitectura ni un mínimo exigible. Obliga a inventar el corpus documental que cuenta como revisado.

**DRY-RUN**

Un ejecutor leería el TaskDoc, sus pills, `sldb/src/sldb/api/`, documentación de arquitectura de SLDB y `pron/source/spec/14-superficie-mcp.md` como referencia. Construiría la matriz de 11 filas, clasificaría cada capacidad con evidencia y citas públicas, y redactaría `docs/auditoria/sldb-api-frente-a-mcp.md`. Si procede, enviaría una nota por `deskops message send`, registraría su ID en Resumen y filas afectadas. Dependencias: acceso a SLDB, deskops y rutas citadas. Validaciones futuras: 11 capacidades, estados/acciones permitidos, citas existentes, fuentes listadas, coherencia de la nota y ausencia de imports/ejecución de pron. Sin ejecutar nada.

**FUTURO**

Otro nodo o humano valida la auditoría, decide extensiones de SLDB y el contrato de escritura, y usa la matriz para diseñar la superficie MCP.
