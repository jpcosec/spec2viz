## REFORMULACION
Propósito: auditar la API pública de SLDB frente a 11 capacidades necesarias para la futura superficie MCP de specIR. Resultado: un informe Markdown con snapshot, matriz de siete columnas, resumen y fuentes revisadas; si hay brechas, una única nota al desk SLDB vía `deskops message send`. Repo de trabajo: `/home/jp/proyectos/SLDB_1/IR`; único archivo a escribir: `docs/auditoria/sldb-api-frente-a-mcp.md`. Límites: no tocar otros repos, no leer módulos internos de SLDB, no importar/ejecutar pron, no diseñar tools ni decidir política de escritura; las pills son guardrails, no evidencia.

## AMBIGUEDADES
1. “acciones: usar/componer para disponible y solicitar-extensión para no disponible” frente a “disponible usa usar/componer”. No queda claro si la celda Acción debe contener literalmente `usar/componer` o elegir `usar` o `componer` según el caso; obligaría a inventar el criterio y el valor exacto.
2. “después líneas Necesidad, Rutas/símbolos revisados, Brecha, Pregunta al desk, TaskDoc”. No se fija sintaxis exacta de esas líneas —por ejemplo, si llevan `**Negrita:**`, `-` o solo `Etiqueta:`—; obligaría a inventar el formato del cuerpo del mensaje pese a exigirse “formato exacto”.
3. “Fuentes revisadas enumera cada archivo Python del corpus efectivamente leído” frente a “Corpus exacto de snapshot: todos los archivos Python bajo ../sldb/src/sldb/api/”. No se especifica si hay que leer todo el corpus o solo los candidatos relevantes; obligaría a inventar la cobertura de lectura y, por tanto, la lista de fuentes.

## DRY-RUN
Lecturas: TaskDoc, rituales, pills, átomos y corpus SLDB/pron indicado; comandos Git de snapshot. Cambios previstos: solo `docs/auditoria/sldb-api-frente-a-mcp.md`. Dependencias: repos `../sldb` y `../pron`, y CLI `deskops`. Validaciones futuras: 11 filas, columnas exactas, estados/acciones cerrados, evidencia citada, fila 4 desdoblada, snapshot con hashes si procede, fuentes revisadas, y nota única con ID o registro exacto de fallo. Sin ejecutar nada.

## FUTURO
Un ejecutor futuro leerá archivos, ejecutará Git y `deskops`, y escribirá el informe. El desk SLDB podrá responder o implementar extensiones. IR02 decidirá la política final de escritura.
