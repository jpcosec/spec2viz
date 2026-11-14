REFORMULACION
Nodo ejecutable de documentación/auditoría. Propósito: auditar la API pública de SLDB frente a 11 capacidades requeridas por la futura superficie MCP de specIR. Resultado: un único informe en `docs/auditoria/sldb-api-frente-a-mcp.md`, con snapshot, matriz de 7 columnas, resumen y fuentes; si hay brechas, enviar una nota al desk SLDB y reflejar handoff/ID; si no, resumen exacto y handoff `—`. Repo: trabajar desde `/home/jp/proyectos/SLDB_1/IR`; leer corpus acotado de `../sldb` y secciones 1 y 4 de `../pron/source/spec/14-superficie-mcp.md`; no leer módulos internos ni importar/ejecutar pron. Límites: solo escribir ese archivo; no diseñar tools ni decidir política de escritura; una fila por capacidad 1–11.

AMBIGUEDADES
1. “La fila 4 representa las suboperaciones en cada celda relevante como dos entradas etiquetadas `select_documents:` y `search:` usando `<br>`”. No define qué celdas son “relevantes”; obligaría a inventar si también se parten Necesidad, Estado, Acción y Handoff o solo Evidencia/Brecha.
2. “deshacer escritura confirmada de kb_undo/forma undo” junto con “no inferir historial, selección de operación, repetición ni otras semánticas de undo”. No aclara si “confirmada” exige evidencia de commit/ack previo o solo una escritura ya aplicada; obligaría a inventar el criterio de confirmación.

DRY-RUN
Lecturas: archivos Python bajo `../sldb/src/sldb/api/` y docs listados; `git -C ../sldb rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all` limitado al corpus; SHA-256 de modificados/untracked; secciones 1 y 4 de la spec pron. Cambios previstos: redactar la matriz de 11 filas, decidir estados/acciones con evidencia citada, componer snapshot y resumen, y escribir solo el informe. Si hay no disponibles, construir `message_body` y ejecutar una vez `deskops message send...`; si falla, registrar código/stderr/stdout y handoff `ERROR`. Dependencias: `../sldb`, `../pron`, git y deskops. Validaciones futuras: 11 filas, columnas y estructura exactas, estados/acciones cerrados, fila 4 separada, snapshot/hashes, fuentes solo leídas, pills como guardrails, mensaje/ID o error.

FUTURO
Otro nodo o humano debe proveer el corpus SLDB y la spec pron en las rutas indicadas, disponer de deskops y validar el informe final; la decisión de política de escritura queda para IR02.
