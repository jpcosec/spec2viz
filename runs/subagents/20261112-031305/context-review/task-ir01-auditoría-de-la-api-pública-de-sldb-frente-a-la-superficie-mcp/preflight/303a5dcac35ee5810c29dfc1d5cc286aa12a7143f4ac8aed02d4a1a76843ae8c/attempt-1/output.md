## REFORMULACION
Nodo ejecutable `task.docs`, no agregado. Propósito: auditar la API pública de SLDB frente a la superficie MCP de specIR antes de diseñarla. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, con una matriz capacidad por capacidad que indique si SLDB ya la ofrece, requiere extensión o falta. Repo de entrega: specIR; lecturas: `sldb/src/sldb/api/`, documentación de arquitectura de SLDB y, como referencia, `pron/source/spec/14-superficie-mcp.md`. Límites: no escribir código, no modificar SLDB ni diseñar las tools; usar solo API pública de SLDB; si hay faltante real, notificar al desk de SLDB.

## AMBIGUEDADES
1. “como referencia de contrato”: no aclara si la spec de pron es normativa o solo informativa; obligaría a decidir qué capacidades exigir.
2. “Una matriz que diga, capacidad por capacidad”: no define columnas, estados ni formato; obligaría a inventar el esquema.
3. “no existe ni se puede componer con operaciones públicas existentes”: no fija cuándo una composición cuenta como suficiente; obligaría a inventar el umbral.
4. “Cada fila de la matriz cita una ruta existente bajo sldb/src/sldb/api/ o declara explícitamente que la capacidad falta”: no indica cómo citar capacidades compuestas; obligaría a inventar esa regla.
5. “identificador de estado del store utilizable como precondición de escritura”: no define forma ni semántica; obligaría a inventar el criterio de aceptación.
6. “forma de deshacer una escritura”: no distingue undo, rollback o compensación; obligaría a inventar la semántica.
7. “se envía una nota al desk de SLDB con deskops message send”: no especifica destinatario ni formato; obligaría a inventarlos.

## DRY-RUN
Lecturas: task doc, pills, documento destino si existe, `sldb/src/sldb/api/`, arquitectura de SLDB y spec de pron. Cambios previstos: crear o editar únicamente `docs/auditoria/sldb-api-frente-a-mcp.md`. Dependencias: acceso de lectura a SLDB/pron y `deskops message send` solo si hay faltantes. Validaciones futuras: rutas citadas existentes o faltante declarado; ninguna fila apoyada en `sldb.store`, `sldb.core` ni pron; respuesta explícita sobre estado del store y deshacer; nota por cada faltante real. Sin ejecutar nada.

## FUTURO
El ejecutor futuro produce la matriz y, si corresponde, las notas. El desk de SLDB recibe y triagea esas notas. Un humano o revisor decide la aceptación del documento. El nodo de diseño de la superficie MCP consume la matriz como insumo.
