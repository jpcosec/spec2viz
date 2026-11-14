REFORMULACION
Tarea documental que no es agregado ni paquete: la ejecuta un futuro ejecutor. Propósito: auditar las 11 capacidades de la superficie MCP de specIR, con actor agente MCP operando un store SLDB, frente a la API pública y documentación de SLDB, sin reimplementar ni usar módulos internos. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con snapshot git/SHA-256, matriz de 11 filas (necesidad, evidencia, estado, brecha, acción, handoff) y, si hay filas no disponibles, una única nota al desk SLDB. Repo: raíz `/home/jp/proyectos/SLDB_1/IR`; lecturas `../sldb` y `../pron/source/spec/14-superficie-mcp.md` §§1,4. Límites: no código, no cambios en otros repos, no módulos internos SLDB, no importar/ejecutar pron, no diseñar tools ni decidir la política final de escritura.

AMBIGUEDADES
1. “_State what is in scope and what is out of scope._” (repetida) y “_Outline the expected implementation route or affected surface._”: plantillas sin sustituir; obligaría a inventar si son requisitos o texto residual.
2. “la fila usa el estado más restrictivo”: no define el orden entre `disponible`, `requiere-extensión-en-SLDB` y `faltante`; obligaría a inventar la jerarquía para la fila 4.

DRY-RUN
Lecturas: TaskDoc, pills de guardrail, corpus Python de `../sldb/src/sldb/api/`, docs SLDB listados, spec pron §§1,4 y metadatos git limitados al corpus. Cambios previstos: escribir solo el informe, con snapshot, fuentes y 11 filas; si hay no disponibles, construir `message_body` y enviar una sola vez `deskops message send ... --to sldb`; reflejar ID o fallo. Dependencias: repositorios SLDB/pron, git, deskops y JSON de respuesta. Validaciones futuras: 11 filas, estados/acciones cerrados, evidencia existente, fila 4 separada, hashes si hay modificados, formato/título/cuerpo de la nota, ID en Resumen y handoffs, y registro exacto del fallo. Sin ejecutar nada.

FUTURO
IR02 decide la política final de escritura; el desk SLDB recibe la nota y decide si integra/documenta extensiones; un humano puede resolver las plantillas o la jerarquía si no se aclaran. El ejecutor real produce el informe y la notificación o su registro de error.
