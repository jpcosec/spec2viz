REFORMULACION
Encargo: auditar, en el repo specIR (`/home/jp/proyectos/SLDB_1/IR`), la API pública de SLDB frente a las necesidades de la futura superficie MCP de specIR. Resultado: un informe en `docs/auditoria/sldb-api-frente-a-mcp.md` con exactamente 11 capacidades, cada una con necesidad, estado cerrado, evidencia, brecha, acción y handoff; además, snapshot de `../sldb` y, si hay brechas, una única nota a SLDB por `deskops message send`. Límites: no escribir código, no editar otros repos, no leer módulos internos de SLDB, no importar/ejecutar pron. Solo se lee el corpus público indicado y `../pron/source/spec/14-superficie-mcp.md` §1/§4.

AMBIGUEDADES
1. “Cada fila disponible cita ruta existente bajo sldb/src/sldb/api/ y todos los símbolos públicos; la composición nombra cada operación.” Si una capacidad se compone de varios módulos, el singular “ruta” no aclara si basta una ruta representativa o deben citarse todas; obligaría a inventar el criterio de evidencia.
2. “Fila 7, add_model(model_ref) registra una clase StructuredNLDoc con referencia module:ClassName”. No se explicita si `add_model(model_ref)` es la firma pública exacta que debe citarse o una descripción funcional; obligaría a inventar la firma.
3. “Hashear SHA-256 solo los archivos de ese corpus modificados/untracked”. Con `git status --short`, “modificados” no distingue staged de unstaged; obligaría a decidir qué entradas cuentan para el hash.

DRY-RUN
Un ejecutor futuro leería el corpus enumerado, capturaría commit/branch/status y hashes según las reglas; clasificaría las 11 filas con los estados cerrados; redactaría el informe y, si hay filas no disponibles, enviaría una sola nota con el formato exacto y registraría el `sldb:<stem>` o el error sin reintentar. Dependencias: existencia del corpus, git y `deskops`. Validaciones posteriores: 11 filas, estados/acciones correctos, citas existentes, snapshot/hashes, mensaje e ID, fuentes revisadas. No se ejecuta nada.

FUTURO
IR02 o el dueño del producto decide el contrato final de escritura y el diseño de tools MCP; el desk de SLDB atiende las extensiones solicitadas; otro nodo valida y cierra la tarea.
