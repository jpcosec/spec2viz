REFORMULACION
IR01 es una entrega documental del repo specIR: producir `docs/auditoria/sldb-api-frente-a-mcp.md`, una matriz capacidad por capacidad de la superficie MCP que indique si la API pública de SLDB ya la ofrece, requiere extensión o falta, con estado y cita. No es agregado. Límites: no escribir código, no modificar SLDB ni diseñar tools.

AMBIGUEDADES
1. Cita: “si la API pública de SLDB ya lo ofrece, hay que extenderlo en SLDB, o falta”, pero la validación solo admite “cita una ruta existente [...] o declara explícitamente que la capacidad falta”. Obliga a inventar cómo representar “extender” y si requiere ruta.
2. Cita: “cada fila tiene estado y cita”. No define vocabulario de estados ni formato/granularidad de cita. Obliga a inventar taxonomía y convención.
3. Cita: “existe una nota enviada al desk de SLDB”, frente a `output_scope` limitado a `docs/auditoria/sldb-api-frente-a-mcp.md`. Obliga a inventar destino, formato y permiso de escritura fuera del alcance.
4. Cita: “una fila por capacidad de la superficie MCP: listar y describir modelos y tipos de relación...”. Obliga a decidir si cada viñeta es una fila o se subdivide.
5. Cita: “Ninguna fila se apoya en sldb.store, sldb.core ni en pron”. Obliga a interpretar “se apoya” como cita, import o mención.

DRY-RUN
Lecturas previstas: contrato IR01 y rutas existentes bajo `sldb/src/sldb/api/`; sin historial ni herramientas. Cambios previstos: crear la matriz con filas, estados, citas y respuestas explícitas sobre identificador de estado y deshacer; condicionado por las ambigüedades 1–3. Dependencias: ninguna (`depends_on: []`, `requires: []`). Validaciones futuras: comprobar existencia de rutas citadas, ausencia de dependencia de `sldb.store`/`sldb.core`/`pron`, respuestas explícitas y coherencia de notas por faltantes. Sin ejecutar.

FUTURO
IR02 usará la matriz para decidir el contrato de escritura; IR03 limitará su servidor a las capacidades de lectura confirmadas; IR05 citará la fila correspondiente si su taxonomía exige algo ausente. SLDB recibirá las notas de faltantes y decidirá cambios; el dueño del proyecto validará la clasificación y la notificación.
