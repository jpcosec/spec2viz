REFORMULACION
Propósito: auditar la API pública de SLDB frente a 11 capacidades que necesita la superficie MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con matriz de 11 filas (necesidad, estado cerrado, evidencia, brecha, acción y handoff), snapshot git y fuentes. Repo: IR (`/home/jp/proyectos/SLDB_1/IR`). Límites: escribir solo ese archivo; no tocar código ni otros repos; no abrir módulos internos de SLDB; no importar/ejecutar pron —solo leer su spec §§1,4—; enviar como máximo una nota condicional al desk de SLDB. No es agregado ni paquete: es una tarea documental única, sin hijos.

AMBIGUEDADES
1. «las filas 6, 10 y 11 sí inventarían las APIs existentes frente a las necesidades declaradas». Contradice «no cita rutas o símbolos inventados». Obliga a inventar si deben inventarse APIs o inventariarse las existentes, y qué significa «sí».
2. «cita ruta existente bajo sldb/src/sldb/api/ y todos los símbolos públicos». No define el universo de «todos»: ¿del módulo citado, de `sldb.api` o solo de las operaciones usadas? Obliga a inventar el alcance exigido.
3. «Una fila por número; suboperaciones relacionadas no crean filas extra», junto a la fila 4 que une `select_documents` y `search`. No aclara si cada operación requiere evidencia y estado propios o una casilla conjunta. Obliga a inventar la granularidad.

DRY-RUN
El ejecutor futuro, hipotéticamente, leería el TaskDoc, rituales, pills, átomos, el corpus exacto de `../sldb` y la spec pron §§1,4; capturaría commit, branch y status limitado al corpus; hashearía los archivos modificados/untracked. Construiría 11 filas, clasificaría cada capacidad y redactaría únicamente `docs/auditoria/sldb-api-frente-a-mcp.md`. Si hay filas no disponibles, compondría el `message_body`, invocaría una vez `deskops message send`, extraería el stem del `path` y completaría handoffs y Resumen; si falla, registraría el error exacto sin reintentar. Si todas están disponibles, no enviaría nota y usaría `—`. Dependencias: repo SLDB, binario `deskops` y documento pron. Validaciones futuras: exactamente 11 filas, estados/acciones cerrados, citas verificables, snapshot y mensaje único correcto.

FUTURO
El desk de SLDB decide y atiende las extensiones solicitadas; IR02 decide la política final de escritura; un humano corrige la contradicción de Scope; el cierre valida y autoriza el commit.
