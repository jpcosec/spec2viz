## REFORMULACION

La tarea pide auditar la API pública de SLDB frente a la superficie MCP de specIR y escribir `docs/auditoria/sldb-api-frente-a-mcp.md` en IR (`/home/jp/proyectos/SLDB_1/IR`). Resultado: matriz de exactamente 11 capacidades con necesidad (actor/entrada/resultado), estado (`disponible`, `requiere-extensión-en-SLDB`, `faltante`), evidencia, brecha, acción (`usar/componer` o `solicitar-extensión`) y handoff (`—`, `sldb:<id>` o `ERROR`); además snapshot de SLDB, fuentes y hashes. Límites: solo ese informe; no tools/código, no otros repos, no módulos internos de SLDB, no importar/ejecutar pron, máximo una nota `deskops`; el informe no decide el contrato final de escritura.

## AMBIGUEDADES

1. "si se envía usa ID sldb:<id>" frente a "Resumen de éxito exacto: Nota enviada; ID: sldb:<id>." Obliga a inventar la forma exacta del Resumen: solo ID o cadena completa.
2. "Dirty incluye tracked y untracked dentro del corpus." No define "corpus". Obliga a inventar el alcance de "dirty" (todo `../sldb`, archivos inspeccionados o solo Python/docs), afectando estado y hashes.
3. "preguntar al desk SLDB" frente a "no preguntar antes ni mandar otra nota". Obliga a decidir precedencia: consulta previa o solo nota única final.

## DRY-RUN

Sin ejecutar: leería `git -C ../sldb` (HEAD, branch, status), `.py` bajo `../sldb/src/sldb/api/`, docs SLDB listados y `../pron/source/spec/14-superficie-mcp.md` (§1 y §4). Registraría errores de git y SHA-256 de archivos inspeccionados modificados/untracked. Cambiaría solo `docs/auditoria/sldb-api-frente-a-mcp.md`. Depende de símbolos públicos, evidencia para `Model:name`/URI y `deskops`. Validaría 11 filas, estados/acciones cerrados, evidencia real, composición nombrada, snapshot/hashes, nota única, Resumen/handoff exactos y que no se lean módulos internos ni se ejecute pron.

## FUTURO

El desk SLDB recibe y decide la nota de brechas; el contrato final de escritura y cualquier extensión de SLDB quedan fuera de esta tarea. El flujo de ejecución/closeout decidirá commit y cierre; esta revisión no decide ni ejecuta.
