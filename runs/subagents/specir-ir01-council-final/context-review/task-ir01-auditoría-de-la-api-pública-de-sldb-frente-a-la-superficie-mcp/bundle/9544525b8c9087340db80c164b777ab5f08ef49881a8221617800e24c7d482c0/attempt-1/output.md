## REFORMULACION
Propósito: auditar 11 capacidades del cliente MCP de specIR frente a la API pública de SLDB y producir una matriz de disponibilidad/brecha. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con Snapshot, Matriz de 7 columnas, Resumen y Fuentes; si hay filas no disponibles, enviar una única nota al desk SLDB y repetir su ID. Repo: `/home/jp/proyectos/SLDB_1/IR`; solo se escribe ese informe. Límites: no código, no cambios en otros repos, no módulos internos de SLDB, no importar/ejecutar pron; evidencia solo de `sldb.api` público y docs listados; leer de pron únicamente §§1 y 4. El nodo es una tarea ejecutable de documentación, no un agregado.

## AMBIGUEDADES
1. “Registrar la fecha/hora UTC del snapshot en ISO-8601 `YYYY-MM-DDTHH:MM:SSZ`.” No fija si el instante se toma antes o después de leer corpus/git; obliga a inventar una convención y puede alterar el snapshot.
2. “excluir número, paréntesis y separador final” frente a “cualquier paréntesis dentro de la frase se conserva.” Obliga a decidir si los paréntesis internos del nombre canónico se eliminan o se conservan.
3. “Las filas 6, 10 y 11 documentarán las APIs existentes frente a las necesidades declaradas” y “no recomienda política, arquitectura ni nivel de mutabilidad de escritura.” Obliga a inventar dónde termina la descripción de compatibilidad y empieza una recomendación de política.

## DRY-RUN
Lecturas: TaskDoc, rituales, pills, átomos; todos los `.py` bajo `../sldb/src/sldb/api/`; docs SLDB enumerados; §§1 y 4 de `../pron/source/spec/14-superficie-mcp.md`. Capturar `git rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all` limitado al corpus; hashes SHA-256 si hay dirty o fallback. Cambios previstos: solo crear el informe con estructura fijada y 11 filas. Dependencias: git, SHA-256, deskops. Si hay brechas, construir `message_body` solo con filas no disponibles, enviar una vez y registrar path/ID o error exacto. Validaciones futuras: 11 filas, estados/acciones cerrados, fila 4 con `select_documents:`/`search:` y severidad, evidencia citada, sin módulos internos, Resumen/handoff exactos. Sin ejecutar nada.

## FUTURO
IR02 decide la política final de escritura y mutabilidad. El desk SLDB decide si expone/documenta las conductas faltantes. Un humano o nodo de closeout valida, cierra y commitea; si el envío falla, decide el seguimiento sin declarar notificada la tarea.
