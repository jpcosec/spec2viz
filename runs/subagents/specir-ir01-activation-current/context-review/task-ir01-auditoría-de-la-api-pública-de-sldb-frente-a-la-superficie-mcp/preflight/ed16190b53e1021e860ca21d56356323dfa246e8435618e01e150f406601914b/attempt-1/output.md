## REFORMULACION

**Propósito:** auditar, antes de diseñar la superficie MCP de specIR, qué capacidades de SLDB ya existen en su API pública. **Resultado:** `docs/auditoria/sldb-api-frente-a-mcp.md`, con una matriz de exactamente 11 filas y, si hay brechas, una única nota a SLDB mediante `deskops message send`. **Repo:** trabajar desde `/home/jp/proyectos/SLDB_1/IR`; leer el corpus indicado de `../sldb/src/sldb/api/` y documentos SLDB, y `../pron/source/spec/14-superficie-mcp.md` §1/§4. **Límites:** escribir solo el informe; no abrir módulos internos de SLDB ni importar/ejecutar pron; no diseñar MCP ni decidir el contrato final de escritura; no reintentar el envío. No es un agregado ni paquete: es una tarea ejecutable de documentación.

## AMBIGUEDADES

1. «Hay exactamente 11 filas, una por el listado numerado anterior.» El input no contiene ese listado. Obligaría a inventar las 11 capacidades y sus nombres.
2. «las capacidades 6, 10 y 11 permanecen en esta auditoría como inventario de APIs existentes.» No se identifica cuáles son. Obligaría a inventar su correspondencia.
3. «Cada fila usa uno de los estados cerrados y la acción correspondiente». No se enumeran los estados cerrados. Obligaría a inventar el vocabulario exacto de estados.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, los archivos Python bajo `../sldb/src/sldb/api/`, los documentos SLDB enumerados y la spec pron §1/§4. Capturaría `git -C ../sldb rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all` limitado al corpus; si hay modificados/untracked, calcularía SHA-256 solo de esos archivos. Construiría la matriz de 11 capacidades, clasificaría cada una como disponible/no disponible, citaría rutas y símbolos públicos existentes y registraría brechas. Escribiría únicamente `docs/auditoria/sldb-api-frente-a-mcp.md`. Si hay filas no disponibles, prepararía el cuerpo exacto y ejecutaría una sola vez el comando `deskops message send`; tomaría el stem de `path` para el ID. Dependencias: el listado de capacidades y los estados cerrados, ausentes del input. Validaciones futuras: once filas, estados/acciones coherentes, citas existentes, snapshot y hashes, ID exacto en Resumen y filas, y ausencia de imports/ejecución de pron.

## FUTURO

`deskops message send` producirá el JSON con `path` o el error; el desk de SLDB decidirá si acepta las extensiones; IR02 decidirá el contrato final de escritura; un humano cerrará la tarea o gestionará el fallo de envío.
