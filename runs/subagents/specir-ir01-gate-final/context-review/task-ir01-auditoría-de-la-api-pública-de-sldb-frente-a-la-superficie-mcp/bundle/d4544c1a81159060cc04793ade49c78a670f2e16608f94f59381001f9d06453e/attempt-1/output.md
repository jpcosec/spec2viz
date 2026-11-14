## REFORMULACION
El nodo audita la API pública de SLDB frente a 11 capacidades exigidas por la futura superficie MCP de specIR y produce `docs/auditoria/sldb-api-frente-a-mcp.md` en el repo specIR. Debe clasificar cada capacidad como `disponible`, `requiere-extensión-en-SLDB` o `faltante`, con necesidad, evidencia, brecha, acción y handoff, y notificar las brechas al desk SLDB mediante `deskops message send`. Límites: solo lee el corpus SLDB enumerado y las secciones 1 y 4 de pron como documento; no abre módulos internos de SLDB, no importa/ejecuta pron, no edita otros repos, no diseña tools ni decide la política de escritura. Es un nodo ejecutable de documentación, no un agregado.

## AMBIGUEDADES
1. “excluir número, paréntesis y separador final” frente a “cualquier paréntesis dentro de la frase se conserva”. Obliga a decidir si se eliminan paréntesis internos del nombre canónico; ambas lecturas son literales.
2. “Registrar la fecha/hora UTC del snapshot en ISO-8601”. No define si es el instante de captura o la fecha del commit; obliga a inventar el criterio.

## DRY-RUN
Un ejecutor futuro leería el TaskDoc, rituales, pills y átomos; inspeccionaría solo los archivos Python bajo `../sldb/src/sldb/api/` y los docs SLDB listados; leería las secciones 1 y 4 de `../pron/source/spec/14-superficie-mcp.md`. Capturaría commit, branch, fecha UTC, status y hashes del corpus. Clasificaría las 11 filas, redactaría el informe con la estructura fijada y, si hay filas no disponibles, enviaría un único mensaje a `--to sldb`. Validaría después: 11 filas, estados/acciones cerrados, evidencia citada, fila 4 desdoblada, snapshot, formato del Resumen y resultado del envío. Nada de esto se ejecuta aquí.

## FUTURO
IR02 decide la política final de escritura, arquitectura y mutabilidad. El desk SLDB decide si integra o documenta la conducta faltante. El humano prioriza brechas, autoriza el cierre y el commit tras la validación. Si falla el envío, un humano decide reintento o escalado; el nodo no declara notificación exitosa.
