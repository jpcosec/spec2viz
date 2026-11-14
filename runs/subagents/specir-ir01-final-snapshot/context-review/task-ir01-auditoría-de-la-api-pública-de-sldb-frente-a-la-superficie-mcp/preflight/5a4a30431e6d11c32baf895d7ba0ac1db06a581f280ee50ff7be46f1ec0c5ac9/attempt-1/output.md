## REFORMULACION
El encargo es una auditoría documental ejecutable, no un agregado ni paquete: no hay hijos que recorrer. Propósito: contrastar 11 capacidades concretas de la futura superficie MCP de specIR con la API pública de SLDB. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, con matriz de 11 filas, estados cerrados, evidencia, acciones y handoff; si hay brechas, una única nota a SLDB. Repo: `/home/jp/proyectos/SLDB_1/IR`; corpus `../sldb/...` y spec `../pron/...`. Límites: no diseñar tools, escribir código, editar otros repos, leer módulos internos de SLDB, importar/ejecutar pron, reintentar el envío ni tratar el contrato final de escritura.

## AMBIGUEDADES
1. “si falla el envío, ERROR en cada no disponible”: no define contenido ni formato del ERROR por fila; obligaría a inventar su texto.
2. “construir message_body con solo esas filas”: no aclara si el cuerpo lleva encabezado, tabla o únicamente filas; obligaría a inventar su estructura.
3. “usar ese ID igual como sldb:<id>”: no dice si el ID del JSON ya incluye prefijo; obligaría a inventar una normalización.
4. “si ese texto no permite decidir equivalencia”: no fija criterio de equivalencia; obligaría a inventar el umbral de decisión.
5. “docstring/documento declara expresamente”: no jerarquiza fuentes; obligaría a inventar si vale documentación externa o solo docstrings del API.

## DRY-RUN
Lecturas previstas: TaskDoc; recursivamente los Python de `../sldb/src/sldb/api/`; los docs enumerados de `../sldb/docs/`; `../pron/source/spec/14-superficie-mcp.md`; `git -C ../sldb rev-parse HEAD`, `branch --show-current`, `status --short --untracked-files=all --` sobre el corpus; SHA-256 de archivos modificados/untracked del corpus. Cambio previsto: crear solo `docs/auditoria/sldb-api-frente-a-mcp.md`. Dependencias: git, hashing SHA-256, filesystem y `deskops message send`. Validaciones futuras: exactamente 11 filas; estados/acciones cerrados; evidencia con rutas y símbolos reales; snapshot con commit/branch/fecha/status/hashes; una sola nota con título y cuerpo exigidos; ID repetido en filas no disponibles y Resumen exacto; si no hay brechas, Resumen exacto y handoff `—`; ausencia de lecturas/ejecuciones prohibidas.

## FUTURO
SLDB recibe la nota y decide si extiende su API o aclara equivalencias; `deskops` devuelve el ID o el fallo. Un humano valida el cierre y, si falla el envío, la tarea queda abierta.
