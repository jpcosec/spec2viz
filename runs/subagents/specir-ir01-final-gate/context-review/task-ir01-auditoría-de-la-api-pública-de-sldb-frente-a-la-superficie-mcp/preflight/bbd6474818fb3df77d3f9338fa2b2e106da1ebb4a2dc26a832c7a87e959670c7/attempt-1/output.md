## REFORMULACION

El encargo es auditar la API pública de SLDB frente a las 11 capacidades que necesita la futura superficie MCP de specIR, clasificando cada fila como disponible, requiere-extensión-en-SLDB o faltante. El resultado es `docs/auditoria/sldb-api-frente-a-mcp.md`, con Snapshot, Matriz de siete columnas, Resumen y Fuentes revisadas. Se trabaja desde `/home/jp/proyectos/SLDB_1/IR`; SLDB y pron se leen como fuentes externas. Límites: no editar código ni otros repos, no leer módulos internos de SLDB, no importar/ejecutar pron; de pron solo se leen las secciones 1 y 4 de `14-superficie-mcp.md`. Si hay brechas, se envía una única nota al desk SLDB mediante `deskops message send`; la decisión de política de escritura queda para IR02.

## AMBIGUEDADES

Ninguna. El input explicita las variantes conflictivas: fila 4 con dos suboperaciones pero una sola fila; nombre de capacidad sin número ni separador; handoff `—` o `ERROR`; fallback Git; fecha de error de envío; y estados/acciones cerrados.

## DRY-RUN

Un ejecutor futuro leería todo archivo Python bajo `../sldb/src/sldb/api/` y los documentos SLDB enumerados en Implementation Path; leería solo §1 y §4 de `../pron/source/spec/14-superficie-mcp.md`. Ejecutaría `git -C ../sldb rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all` limitado al corpus, con fallback si falla Git. Construiría 11 filas, separaría `select_documents` y `search` en la fila 4, citaría evidencia pública y redactaría brechas. Escribiría únicamente el informe. Si hay filas no disponibles, compondría el cuerpo con una sección por fila, enviaría una vez `deskops message send ... --to sldb --format json`, y registraría el ID `sldb:<stem>` o el error completo. Validaría después: 11 filas, columnas exactas, estados/acciones coherentes, evidencia sin símbolos inventados, fila 4 desdoblada, Snapshot y Fuentes completos, y resultado del envío.

## FUTURO

El informe y, si procede, la nota al desk SLDB. IR02 decidirá la política de escritura. El desk SLDB decidirá si expone o documenta las extensiones solicitadas. Un humano o nodo posterior validará el cierre o tratará un fallo de envío; esta revisión no ejecuta ni decide nada.
