REFORMULACION  
Propósito: auditar la API pública de SLDB frente a 11 capacidades necesarias para la superficie MCP de specIR, con actor “agente MCP de specIR operando un store SLDB”. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, con matriz de 11 filas —capacidad, necesidad, estado, evidencia, brecha, acción y handoff—, snapshot git/fecha/hashes y, si hay filas no disponibles, una única nota al desk SLDB. Repo: IR; `../sldb` y `../pron` relativos a IR. Límites: solo lectura del corpus SLDB y de pron §1 y §4; no módulos internos SLDB; no importar/ejecutar pron; no código ni cambios en otros repos; única escritura el informe.

AMBIGUEDADES  
1. “necesidad con actor/entrada/resultado” (Validation): no define formato, etiquetas ni orden. Obligaría a inventar la estructura interna de la columna Necesidad.  
2. “Cada fila no disponible enumera módulos existentes inspeccionados” (Validation): no fija qué módulos ni granularidad para un faltante sin operación relacionada. Obligaría a inventar un inventario o un criterio de exhaustividad.  
3. “La evidencia de API consiste en docstring de la función pública citada o documentación SLDB listada que describa esa operación” (Implementation Path): no aclara si una mención en README sin descripción de conducta cuenta. Obligaría a fijar un umbral de evidencia no escrito.

DRY-RUN  
El nodo es ejecutable, no agregado. Un ejecutor leería: comandos git limitados al corpus, archivos Python bajo `../sldb/src/sldb/api/`, docs SLDB listados y pron §1/§4. Luego construiría las 11 filas, aplicaría estados/acciones cerrados, resolvería fila 4 por suboperaciones y severidad, y registraría snapshot/hashes. Cambio previsto: crear solo el informe; si hay filas no disponibles, componer y enviar una única nota con `deskops message send`, sin reintentar. Dependencias: git, deskops, JSON con `path`. Validaciones futuras: 11 filas exactas, columnas ordenadas, evidencia citada, fila 4 separada, handoff `—` o `sldb:<stem>`, resumen exacto y ausencia de imports/ejecución.

FUTURO  
Otro nodo o humano ejecutará el envío real, aportará el ID/error y decidirá si la tarea queda abierta; también revisará el informe final y la clasificación de brechas.
