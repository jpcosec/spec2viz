## REFORMULACION
Propósito: auditar la API pública de SLDB frente a 11 capacidades necesarias para la superficie MCP de specIR. El nodo es una tarea documental ejecutable, no un agregado. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con exactamente 11 filas, snapshot, estados cerrados, evidencia, brechas, acciones y handoff; si hay filas no disponibles, un único mensaje `deskops` a SLDB con formato exacto. Repo: `/home/jp/proyectos/SLDB_1/IR`; lecturas externas permitidas: corpus exacto de `../sldb` y secciones 1 y 4 de `../pron/source/spec/14-superficie-mcp.md`. Límites: no código, no cambios en otros repos, no módulos internos SLDB, no importar/ejecutar pron, no diseñar tools ni decidir política de escritura; solo escribir el informe.

## AMBIGUEDADES
1. «Una matriz que diga, capacidad por capacidad...» no fija columnas ni orden visual; obligaría a inventar el esquema de tabla. La validación enumera campos, pero no su disposición.
2. «cada fila incluye capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha...» no define el texto de la brecha para una fila disponible; obligaría a inventar una fórmula, por ejemplo «ninguna».

## DRY-RUN
Lecturas: TaskDoc, pills de guardrail, archivos Python de `../sldb/src/sldb/api/`, docs SLDB listados y secciones 1 y 4 de pron. Cambios previstos: crear solo el informe; si hay no disponibles, preparar y enviar una vez el mensaje con `--to sldb`. Dependencias: git, SHA-256, `deskops`, disponibilidad de rutas y del directorio `docs/auditoria`. Validaciones futuras: 11 filas y nombres canónicos; estados/acciones coherentes; fila 4 separada y estado más severo; snapshot y hashes; mensaje/ID o fallback exacto. Sin ejecutar.

## FUTURO
IR02 decide la política de escritura. El desk SLDB recibe la nota y decide si integra o documenta extensiones. Un humano interviene si falla el envío o falta una fuente. La tarea no se cierra como notificada si no hay ID.
