## REFORMULACION
Propósito: auditar capacidad por capacidad la API pública de SLDB frente a la superficie MCP que necesitará specIR, decidiendo si ya existe, debe extenderse en SLDB o falta. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con una matriz de filas con estado y cita. Repo: specIR; solo se crea ese documento. Límites: no código, no modificar SLDB, no diseñar tools; no usar `sldb.store`, `sldb.core` ni pron; cambios externos solo por `deskops message send`. Tarea documental única, no agregado.

## AMBIGUEDADES
1. "una fila por capacidad ... listar y describir modelos y tipos de relación": no fija granularidad verbo/par; obliga a inventar la desagregación.
2. "ya lo ofrece, hay que extenderlo en SLDB, o falta" frente a "no existe ni se puede componer": falta estado para lo componible; obliga a inventar etiqueta y criterio.
3. "Cada fila ... cita una ruta existente ... o declara ... que la capacidad falta": no dice qué citar en filas "extender"; obliga a inventar su evidencia.
4. "identificador de estado del store utilizable como precondición de escritura": no define forma admisible (versión, hash, ETag); obliga a inventar el criterio de "utilizable".
5. "forma de deshacer una escritura": no aclara si vale transacción, historial o compensación; obliga a inventar qué cuenta como deshacer.
6. "Por cada fila ... existe una nota" frente a "se envía una nota": no fija si es una por fila o agregada; obliga a inventar granularidad.

## DRY-RUN
Lecturas: TaskDoc, rituales, pills, átomos; `sldb/src/sldb/api/` y arquitectura de SLDB; `pron/source/spec/14-superficie-mcp.md`. Cambios: crear la matriz; si hay faltantes, nota(s) al desk de SLDB; ningún código. Dependencias: lectura de SLDB y pron, y `deskops`. Validaciones: citas existentes, ausencia de store/core/pron, respuesta explícita a estado y deshacer, notas que cubran faltantes. Después, closeout y commit en specIR.

## FUTURO
El desk de SLDB decide aceptar y planificar extensiones; el dueño decide adoptar contratos de pron; otro nodo diseña las tools MCP a partir de la matriz; el cierre registra commit y board.
