REFORMULACION
Propósito: auditar la API pública de SLDB frente a once capacidades necesarias para la futura superficie MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, con matriz de campos fijos, estados cerrados, evidencia, brechas, acciones, handoff y fuentes; si aplica, una nota agregada al desk de SLDB y su ID. Repo: specIR; solo se escribe dentro de specIR. Límites: no escribir código, no modificar SLDB, no diseñar tools MCP, no importar/ejecutar pron, no fijar el contrato final de escritura. No es agregado ni paquete: es una tarea documental.

AMBIGUEDADES
1. «Si hay alguna fila no disponible, enviar una única nota agregada» frente a «Solo si una fila queda como faltante real... se envía una nota». Obliga a inventar si `requiere-extensión-en-SLDB` también dispara la nota; la validación sugiere que sí.
2. «referencia de handoff» no se define ni se dan valores admisibles. Obliga a inventar formato y contenido, sobre todo en filas disponibles sin nota.
3. «no depende de sldb.store, sldb.core» no aclara si prohíbe leerlos o solo importarlos/depender de ellos. Obliga a decidir el alcance de la inspección.

DRY-RUN
Lecturas: TaskDoc, rituales, pills y átomos; inventario de `sldb/src/sldb/api/` y símbolos públicos; documentación de arquitectura de SLDB; `pron/source/spec/14-superficie-mcp.md` solo como referencia. Cambios previstos: crear el informe; eventual mensaje `deskops message send --to sldb` si se resuelve la ambigüedad 1. Dependencias: rutas/documentos citables y API pública suficiente. Validaciones futuras: once filas, estados/acciones permitidos, citas existentes, módulos inspeccionados en no disponibles, fuentes listadas, resumen con ID o declaración de no envío, sin importar/ejecutar pron. No se ejecuta nada.

FUTURO
Un humano o revisor fija las ambigüedades 1–3; el desk de SLDB atiende la nota; otro nodo diseñará la superficie MCP y el contrato de escritura.
