## REFORMULACION
Encargo: auditar la API pública de SLDB frente a once capacidades requeridas por la futura superficie MCP de specIR, actuando como agente MCP. Resultado: una matriz en `docs/auditoria/sldb-api-frente-a-mcp.md`, con estado, evidencia, brecha, acción y referencia de handoff por capacidad. Repo: `/home/jp/proyectos/SLDB_1/IR`. Límites: leer recursivamente `.py` bajo `../sldb/src/sldb/api/` y solo los documentos enumerados; usar `../pron/source/spec/14-superficie-mcp.md` como referencia documental; no leer módulos internos de SLDB, no importar/ejecutar pron, no editar otros repos, no diseñar tools ni decidir el contrato de escritura. El nodo es una tarea documental ejecutable, no un agregado.

## AMBIGUEDADES
1. “La ausencia se justifica contra ese corpus exacto.” No fija commit, rama ni instantánea del corpus; obligaría a inventar si se audita el working tree, HEAD o una revisión concreta.
2. “copiar el ID devuelto como sldb:<id> al Resumen del informe y filas afectadas.” No define qué hacer si el envío falla o no devuelve ID; obligaría a inventar si se bloquea la tarea, se registra un fallo o se reintenta.
3. “Toda fila disponible lleva referencia de handoff —”. No aclara si “—” es literal o mero marcador; obligaría a decidir el formato exacto de esa celda.

## DRY-RUN
Un ejecutor futuro leería todos los `.py` bajo `../sldb/src/sldb/api/`, los documentos indicados y la spec MCP de pron solo como referencia. Redactaría una matriz de once filas y un `# Resumen`; si hay filas no disponibles, enviaría una única nota con `deskops message send --to sldb` y copiaría su ID. Cambio previsto: crear o actualizar solo `docs/auditoria/sldb-api-frente-a-mcp.md`. Dependencias: rutas y documentación existentes, disponibilidad de `deskops`, y que la spec pron describa el contrato MCP. Validaciones futuras: cubrir las once capacidades; usar estados y acciones permitidos; citar rutas/símbolos públicos en disponibles; justificar no disponibles sin inventar símbolos; declarar la nota o su ausencia; listar fuentes; no depender de `sldb.store`, `sldb.core` ni ejecutar pron.

## FUTURO
El equipo propietario de SLDB responde a la nota y decide extensiones o contrato de escritura. Un humano valida el informe y el envío de la nota si este falla. Otro nodo podría ejecutar la escritura del informe; esta tarea no diseña tools ni implementa cambios.
