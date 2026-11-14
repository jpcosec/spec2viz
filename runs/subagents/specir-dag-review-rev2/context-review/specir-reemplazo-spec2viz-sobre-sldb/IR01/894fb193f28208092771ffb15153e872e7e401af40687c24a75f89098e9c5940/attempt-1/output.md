## REFORMULACION
IR01 es una auditoría documental: producir `docs/auditoria/sldb-api-frente-a-mcp.md` con una matriz que, capacidad por capacidad de la superficie MCP, indique si la API pública de SLDB ya la ofrece, requiere extensión en SLDB o falta. Repo: `specIR`. Incluye modelos y tipos de relación, lectura, grafo, búsqueda, vistas, escritura validada, reglas/transiciones, edición de modelos, integridad, historia, identificador de estado y deshacer. Límites: no escribir código, no modificar SLDB, no diseñar tools. Entregable único; sin dependencias declaradas.

## AMBIGUEDADES
1. “una fila por capacidad de la superficie MCP: listar y describir modelos y tipos de relación; leer documento y campo; vecinos y recorrido del grafo…” no fija granularidad: ¿una fila por cada bloque separado por punto y coma o por operación atómica? Obliga a inventar el número y composición de filas.
2. “los faltantes reales (si los hay) están notificados a SLDB” y “nota enviada al desk de SLDB” no definen ruta, medio, formato ni identidad del desk. Obliga a inventar ubicación y estructura de la nota.

## DRY-RUN
Nodo de documentación ejecutable, no agregado. Un ejecutor futuro leería el árbol público bajo `sldb/src/sldb/api/`, recorrería las capacidades enumeradas, comprobaría rutas y símbolos públicos, verificaría que no se apoyan en `sldb.store`, `sldb.core` ni `pron`, y redactaría la matriz. Cambio previsto: crear/actualizar `docs/auditoria/sldb-api-frente-a-mcp.md`; si hay faltantes reales, crear una nota para el desk de SLDB, cuya ruta queda por resolver. Dependencias: API pública de SLDB y convención de notas del desk. Validaciones futuras: cada fila con estado y cita existente o declaración explícita de falta; respuesta explícita sobre identificador de estado y deshacer; nota por faltante real o constancia de que no hay faltantes.

## FUTURO
Los nodos dependientes consumirán la matriz para citar operaciones concretas o carencias. El desk/equipo de SLDB decide cómo atender las notas de faltantes.
