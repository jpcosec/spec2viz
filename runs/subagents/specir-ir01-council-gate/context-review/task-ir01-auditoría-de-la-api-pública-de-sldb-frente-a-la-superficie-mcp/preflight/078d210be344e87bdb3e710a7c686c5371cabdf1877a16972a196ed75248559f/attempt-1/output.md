REFORMULACION
Propósito: auditar la API pública de SLDB frente a 11 capacidades necesarias para la superficie MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, matriz de 11 filas con necesidad, estado cerrado, evidencia, brecha, acción y handoff; si hay filas no disponibles, enviar una nota única a SLDB y registrar su ID. Repo: `/home/jp/proyectos/SLDB_1/IR`. Límites: leer solo el corpus público SLDB indicado y pron §§1,4 como documento; no abrir módulos internos SLDB, no importar/ejecutar pron, no tocar otros repos, no diseñar tools ni decidir política de escritura; escribir solo ese informe. No es agregado ni paquete no ejecutable: es una tarea documental ejecutable.

AMBIGUEDADES
1. “Resumen enviado exacto: Nota enviada; ID: sldb:<stem>” y “el ID exacto aparece en Resumen”: no se define si “Resumen” es sección del informe, campo de frontmatter o resumen de tarea. Obliga a inventar ubicación y encabezado.
2. “cada fila incluye capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha, acción y referencia de handoff”: no fija columnas, orden ni formato de tabla. Obliga a inventar el esquema y la celda de handoff.
3. “Handoff disponible: EM DASH literal —” y “cambiar solo handoff a ERROR literal”: no aclara si el handoff es columna, línea o campo separado en filas no disponibles. Obliga a inventar su representación.

DRY-RUN
Lecturas: TaskDoc y pills; archivos Python bajo `../sldb/src/sldb/api/`; docs SLDB listados; `../pron/source/spec/14-superficie-mcp.md` §§1,4. Snapshot: ejecutar `git -C ../sldb rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all` limitado al corpus; si falla, registrar desconocido/no disponible y hashear todo el corpus; si hay modificados/untracked, SHA-256 solo de ellos. Cambios: redactar la matriz de 11 filas y, si hay no disponibles, construir `message_body` y enviar una vez `deskops message send ... --format json`; registrar `sldb:<stem>` o el error exacto. Dependencias: repos/rutas presentes, git y deskops. Validaciones futuras: 11 filas, estados/acciones cerrados, citas reales, snapshot/hashes, mensaje único y exacto, sin módulos internos ni ejecución de pron, solo el informe escrito.

FUTURO
IR02 decide la política de escritura; el desk de SLDB integra/documenta extensiones o confirma faltantes; un humano resuelve fallos de deskops; el diseño MCP posterior consume la matriz; el revisor de aceptación cierra o devuelve la tarea.
