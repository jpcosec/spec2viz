## REFORMULACION
Propósito: auditar la API pública de SLDB frente a las 11 capacidades MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, con matriz de siete columnas, snapshot, resumen y fuentes revisadas; si hay filas no disponibles, enviar una única nota al desk SLDB. Repo: IR; `../sldb` y `../pron` solo lectura. Límites: sin código, sin editar otros repos, sin módulos internos de SLDB, sin importar/ejecutar pron; evidencia solo desde docstrings públicos `sldb.api` y docs SLDB listados; de pron, solo §1 y §4 como documento. Es un nodo ejecutable de documentación, no un agregado.

## AMBIGUEDADES
1. “acciones: usar/componer para disponible y solicitar-extensión para no disponible”: no aclara si la celda Acción debe contener literalmente `usar/componer` o elegir `usar` o `componer`; obligaría a inventar el valor exacto de una celda validada.

## DRY-RUN
Lecturas: TaskDoc, rituales y pills; todos los `.py` bajo `../sldb/src/sldb/api/`; los docs SLDB enumerados; `../pron/source/spec/14-superficie-mcp.md`, solo §1 y §4; comandos Git de snapshot. Cambios previstos: escribir únicamente `docs/auditoria/sldb-api-frente-a-mcp.md`. Dependencias: Git para commit/branch/status y hashes de archivos dirty; `deskops message send` solo si hay filas no disponibles. Validaciones futuras: 11 filas exactas, columnas `Capacidad, Necesidad, Estado, Evidencia, Brecha, Acción, Handoff`; estados y acciones cerrados; fila 4 desdoblada con estado global más severo; snapshot con status fenced y hashes; fuentes revisadas; envío único con ID y resumen/handoff coherentes; sin apertura de módulos internos ni ejecución de pron.

## FUTURO
IR02 o un humano decide la política final de escritura. El desk SLDB recibe, prioriza y responde la nota; si corresponde, otro nodo de SLDB extiende o documenta la API. Si el envío falla, un humano decide el reintento o la reapertura. No son ambigüedades del encargo.
