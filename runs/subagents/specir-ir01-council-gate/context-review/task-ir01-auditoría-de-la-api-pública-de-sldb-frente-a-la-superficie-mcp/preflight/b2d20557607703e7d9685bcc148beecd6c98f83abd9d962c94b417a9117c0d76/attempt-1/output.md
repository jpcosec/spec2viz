REFORMULACION
Nodo ejecutable, no agregado. Propósito: auditar la API pública de SLDB frente a 11 capacidades necesarias para la superficie MCP de specIR, sin reimplementar lo general ni depender de internos o de pron. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, con matriz de 11 filas —necesidad, estado cerrado, evidencia, brecha, acción y handoff—, snapshot git/SHA-256 y, si hay filas no disponibles, una única nota a SLDB cuyo ID figure en Resumen y handoffs. Repo: IR en `/home/jp/proyectos/SLDB_1/IR`; fuentes `../sldb` y `../pron` relativas. Límites: escribir solo ese archivo; no código, cambios externos, módulos internos SLDB, importar/ejecutar pron; no diseñar tools ni decidir la política de escritura, que corresponde a IR02.

AMBIGUEDADES
1. «docstring sldb.api»: no aclara si exige docstring del paquete, del módulo o de cada función pública. Obligaría a inventar qué docstring cuenta como evidencia admisible.
2. «Resultado: <stderr o JSON completo>»: si el fallo produce ambos, no indica cuál registrar. Obligaría a inventar el criterio de captura y el contenido exacto del Resumen de error.
3. «preguntar al desk que lo integre/documente» frente a «deskops message send ... --to sldb»: no distingue si el destinatario es el desk o SLDB. Obligaría a inventar si «Pregunta al desk» es solo texto y la notificación va a SLDB.

DRY-RUN
Lecturas: corpus Python de `../sldb/src/sldb/api/`, docs SLDB listados y `../pron/source/spec/14-superficie-mcp.md` §§1,4; metadatos git y hashes si procede. Cambios: crear únicamente el informe. Dependencias: `git`, `sha256sum` o equivalente y `deskops` solo si hay brechas. Validaciones futuras: 11 filas exactas; estados/acciones cerrados; evidencia y brecha por fila; fila 4 separada; snapshot y hashes; mensaje único y Resumen exactos; sin internos ni ejecución de pron.

FUTURO
Quedan para otro nodo o humano: la validación/cierre del gate, la decisión de producto de IR02 sobre política de escritura, la respuesta e integración/documentación por el desk SLDB, y la aprobación de cualquier ejecución o envío real.
