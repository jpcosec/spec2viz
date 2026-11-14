REFORMULACION
El nodo es una tarea documental ejecutable, no un agregado. Su propósito es auditar, en exactamente 11 filas, si la API pública de SLDB cubre la superficie MCP de specIR. El resultado es `docs/auditoria/sldb-api-frente-a-mcp.md`: matriz con necesidad, estado cerrado, evidencia, brecha, acción y handoff. Repo de trabajo: `/home/jp/proyectos/SLDB_1/IR`; solo se escribe ese informe. Límites: no diseñar tools, no escribir código, no editar otros repos, no leer módulos internos de SLDB ni importar/ejecutar pron; la spec pron se lee como documento. Si hay brechas, enviar una única nota al desk SLDB; si falla, registrar `ERROR` y dejar la tarea abierta.

AMBIGUEDADES
1. «Si el contrato no permite decidir equivalencia, preguntar al desk SLDB» frente a «Si hay una o más filas no disponibles, ejecutar una sola vez: deskops message send». ¿La consulta por equivalencia es un intercambio previo o parte de la nota única? Obligaría a inventar el flujo de consulta.
2. «--root .» con directorio de trabajo en `IR` y «--to sldb». ¿El root es el de IR o el de SLDB? Obligaría a inventar el alcance del comando.
3. «El cuerpo tiene una sección por fila». ¿Solo las no disponibles o las 11? Obligaría a inventar el contenido de la nota.
4. «si se envía usa ID `sldb:<id>`» para el Resumen. ¿Basta el ID o se exige texto adicional? Obligaría a inventar el formato del Resumen.
5. «usar `sldb://document/Model:name` solo si docs lo respaldan». ¿Docs de SLDB o cualquier documento inspeccionado? Obligaría a inventar la autoridad documental.
6. «Registrar SHA-256 de cada archivo inspeccionado modificado/untracked». ¿Solo `../sldb` o también la spec pron y el contexto? Obligaría a inventar el universo de hashes.

DRY-RUN
Lecturas: snapshot de `../sldb`; todo Python bajo `../sldb/src/sldb/api/`; los documentos SLDB enumerados; `../pron/source/spec/14-superficie-mcp.md` §4 y §1. Sin ejecutar checks. Cambios previstos: solo el informe. Dependencias: árboles `../sldb` y `../pron` presentes y `deskops` disponible si hay brechas. Validaciones futuras: once filas, estados/acciones permitidos, citas existentes, snapshot y hashes, coherencia del handoff, ausencia de imports internos. Si hay no disponibles, redactar una nota única y, si falla, no reintentar.

FUTURO
El desk SLDB decide y ejecuta extensiones de API; otro nodo podrá diseñar las tools MCP sobre el informe; el cierre verifica la matriz y la evidencia de la nota.
