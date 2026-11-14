REFORMULACION
Encargo ejecutable de auditoría documental: desde `/home/jp/proyectos/SLDB_1/IR`, inspeccionar el working tree de `../sldb` y producir `docs/auditoria/sldb-api-frente-a-mcp.md`. Propósito: decidir, para once capacidades MCP, si la API pública de SLDB las ofrece directamente o por composición documentada, requiere extensión o falta. Resultado: matriz de once filas con capacidad, necesidad, estado, evidencia, brecha, acción y handoff; snapshot de commit/branch/fecha/`git status` y hashes si hay cambios sin commit; sección Resumen. Si hay brechas, enviar una única nota a SLDB con título y cuerpo indicados y registrar `sldb:<id>`; si falla, registrar error sin reintentar ni cerrar como notificada. Límites: solo leer `../sldb/src/sldb/api/`, docs listados y `../pron/source/spec/14-superficie-mcp.md`; no leer módulos internos, no importar/ejecutar pron, no diseñar tools, escribir código, editar otros repos ni decidir el contrato final.

AMBIGUEDADES
1. «revisar integridad del store e índice de aristas» no define comprobaciones ni evidencia admisible; obligaría a inventar criterios de integridad.
2. «leer una huella/estado del store» no concreta fuente, forma ni granularidad documentada; obligaría a inventar qué constituye estado comparable.
3. «registrar/promover modelos Python ya definidos» no define ambas operaciones ni el cambio esperado; obligaría a inferir semántica desde los nombres.
4. «crear, editar y borrar documentos y RelationDoc/RelationTypeDoc/RuleDoc» agrupa varias operaciones, mientras Validation exige «exactamente once capacidades»; obligaría a decidir si son una fila o varias.
5. «si los archivos auditados tienen modificaciones sin commit» no aclara si incluye archivos no trackeados; obligaría a fijar el alcance del snapshot.

DRY-RUN
Un ejecutor futuro verificaría el directorio, obtendría commit/branch/estado/fecha de `../sldb`, calcularía hashes si procede, leería recursivamente los Python públicos y los documentos indicados, y consultaría la spec pron solo como documento. Construiría once filas, citando rutas y símbolos existentes; clasificaría cada necesidad según conducta pública exacta o composición documentada, marcaría extensión/faltante y redactaría la nota única si corresponde. Escribiría únicamente el informe. Dependencias: acceso al working tree de SLDB, docs, spec pron y `deskops message send`. Validaciones posteriores: once filas completas, estados/acciones cerrados, evidencia real, snapshot, handoffs e ID o fallo registrados, y ausencia de lecturas prohibidas.

FUTURO
El equipo propietario de SLDB responde la nota y aclara contratos; deskops devuelve el ID; un revisor humano acepta o rechaza la matriz. El diseño de tools y el contrato final de escritura quedan fuera de este nodo.
