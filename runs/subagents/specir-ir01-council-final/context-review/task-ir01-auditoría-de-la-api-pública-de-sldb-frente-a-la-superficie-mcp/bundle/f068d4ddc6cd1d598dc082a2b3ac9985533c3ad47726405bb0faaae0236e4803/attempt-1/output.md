## REFORMULACION

Nodo ejecutable `task.docs`, no agregado. **Propósito:** auditar la API pública de SLDB frente a las 11 capacidades que necesita la superficie MCP de specIR. **Resultado:** `docs/auditoria/sldb-api-frente-a-mcp.md` con matriz de 11 filas —capacidad, necesidad, estado, evidencia, brecha, acción y handoff—, snapshot de SLDB y, si hay filas no disponibles, una única nota al desk SLDB. **Repo:** trabajar desde `/home/jp/proyectos/SLDB_1/IR`; escribir solo ese informe, sin tocar SLDB ni otros repos. **Límites:** evidencia solo de `sldb.api` pública y docs listados; pron §§1,4 solo como documento; prohibido leer módulos internos, importar/ejecutar pron y diseñar tools o política de escritura (IR02).

## AMBIGUEDADES

1. «Para cada nombre de capacidad, tomar literalmente el texto después de su número hasta el siguiente punto y coma» frente a la fila 11, que termina en punto: «(11) detectar operación pública SLDB que cumpla la capacidad de deshacer escritura confirmada de kb_undo/forma undo.» Obliga a inventar si el terminador es el punto final.
2. «todos los archivos Python bajo ../sldb/src/sldb/api/»: no aclara si «bajo» incluye recursivamente subdirectorios; obliga a inventar el perímetro exacto del corpus.
3. «Registrar la fecha/hora UTC del snapshot»: no fija el instante (antes/después de git o de los hashes); obliga a inventar el criterio temporal.

## DRY-RUN

**Lecturas:** corpus exacto de Python bajo `../sldb/src/sldb/api/`, docs SLDB listados, `../pron/source/spec/14-superficie-mcp.md` §§1,4; `git -C ../sldb rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all` limitado al corpus. **Cambios previstos:** crear únicamente `docs/auditoria/sldb-api-frente-a-mcp.md`; si hay filas no disponibles, construir `message_body` y ejecutar una vez `deskops message send ... --to sldb ... --format json`. **Dependencias:** disponibilidad de git y deskops; el JSON debe devolver `path` para obtener el ID. **Validaciones futuras:** once filas y estados cerrados; acciones coherentes; evidencia con rutas/símbolos existentes; fila 4 separada y con estado más severo; snapshot y hashes si hay modificados; nota única o resumen sin envío; registro exacto de error de envío; fuentes revisadas sin módulos internos ni ejecución de pron.

## FUTURO

Un ejecutor futuro redacta la matriz, ejecuta el snapshot y envía —o no— la nota. El desk SLDB recibe las solicitudes de extensión. IR02 decide la política de escritura. El ritual de closeout valida, actualiza el board y prepara el commit.
