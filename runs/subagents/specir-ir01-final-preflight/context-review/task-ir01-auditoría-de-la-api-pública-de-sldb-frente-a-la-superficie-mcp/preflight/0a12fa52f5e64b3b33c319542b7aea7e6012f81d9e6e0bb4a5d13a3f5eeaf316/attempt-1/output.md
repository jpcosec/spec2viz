## REFORMULACION
Encargo documental: auditar la API pública de SLDB frente a las necesidades de la futura superficie MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, con una matriz de once capacidades y campos fijos, estados cerrados, evidencia, brecha, acción y referencia de handoff. Repo: specIR. Límites: no escribir código, no modificar SLDB, no diseñar tools MCP, no usar pron directamente ni decidir el contrato final de escritura.

## AMBIGUEDADES
1. “guardar el ID en el resumen y las filas afectadas”: no se especifica qué “resumen” (¿summary del TaskDoc, informe, otro campo?). Obligaría a inventar el destino del ID.
2. “Agrupar todos los faltantes/extensiones en una sola nota” frente a “si no hay faltantes, declarar que no se envió nota”: no aclara si una fila `requiere-extensión-en-SLDB` sin `faltante` exige nota. Obligaría a inventar la regla.
3. “salvo que la necesidad dependa de una decisión pendiente del dueño”: no define criterio ni dueño. Obligaría a inventar cuándo usar acción `ninguna`.
4. “usar pron directamente” frente a “como referencia de contrato, pron/source/spec/14-superficie-mcp.md”: no aclara si leer ese documento cuenta como uso directo. Obligaría a inventar el límite.
5. “resolver una dirección estable”: no define qué dirección ni contrato. Obligaría a inventar la semántica auditada.

## DRY-RUN
Nodo ejecutable documental, no agregado. Lecturas previstas: inventario bajo `sldb/src/sldb/api/`, documentación de arquitectura de SLDB y, si se permite, la referencia indicada de pron. Cambio previsto: crear el informe con once filas. Dependencias: acceso a ambos repos, identificación de símbolos públicos y, solo si hay faltantes reales, `deskops message send` al desk de SLDB. Validaciones futuras: once filas, estados/acciones permitidos, rutas existentes, símbolos citados, ausencia de dependencia de `sldb.store`, `sldb.core` o pron, y nota agregada única si corresponde.

## FUTURO
Un revisor valida la matriz y sus citas. El dueño resuelve decisiones pendientes. El desk de SLDB recibe la nota agregada, si existe.
