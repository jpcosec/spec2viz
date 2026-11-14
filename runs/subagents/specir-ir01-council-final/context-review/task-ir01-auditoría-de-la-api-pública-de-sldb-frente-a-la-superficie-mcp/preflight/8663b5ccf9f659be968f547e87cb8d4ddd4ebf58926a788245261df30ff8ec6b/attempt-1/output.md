## REFORMULACION
Propósito: auditar la API pública de SLDB frente a 11 capacidades del cliente MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con exactamente 11 filas que incluyan necesidad —actor agente MCP—, estado cerrado, evidencia, brecha, acción y handoff; si hay filas no disponibles, enviar una única nota al desk SLDB y reflejar ID o error. Repo: `/home/jp/proyectos/SLDB_1/IR`, con `../sldb` y `../pron` relativos. Límites: solo docstrings públicos `sldb.api` y docs SLDB listados; leer `../pron/source/spec/14-superficie-mcp.md` §§1,4; no leer módulos internos, no importar/ejecutar pron, no tocar otros repos ni escribir código; solo se escribe el informe. Es una tarea documental ejecutable, no un agregado.

## AMBIGUEDADES
1. “si SLDB ofrece operación relacionada pero no demuestra la conducta requerida”: no define umbral de “relacionada” ni qué cuenta como “demuestra”; obligaría a inventar un criterio de similitud/evidencia, aunque luego exige composición explícita.
2. “fecha UTC”: solo el caso de error exige ISO-8601; el formato de fecha del snapshot no se fija; obligaría a elegir formato.
3. “El nombre canónico y capacidad de cada fila es la frase completa tras su número”: no aclara si conserva puntuación y paréntesis de la lista; obligaría a decidir el recorte exacto.
4. “La decisión final de política de escritura queda fuera solo como decisión de producto de IR02”: “solo” no delimita si el informe puede recomendar; obligaría a inferir el alcance.

## DRY-RUN
Lecturas: archivos Python bajo `../sldb/src/sldb/api/`, docs SLDB listados y pron §§1,4; metadatos Git limitados al corpus. No ejecutar checks ni importar nada. Cambios previstos: escribir únicamente el informe; si hay filas no disponibles, construir `message_body` con secciones exactas y ejecutar una vez `deskops message send`. Dependencias: `../sldb`, `../pron`, Git y `deskops`. Validaciones futuras: 11 filas, estados/acciones, evidencia por fila y por suboperación de la fila 4, snapshot/hashes, formato y resultado del mensaje.

## FUTURO
IR02 decide la política de escritura; el desk SLDB integra o documenta extensiones; `deskops` confirma ID o error; una revisión humana valida el informe.
