## REFORMULACION
Encargo ejecutable `task.docs`, no agregado. Propósito: auditar la API pública de SLDB frente a once capacidades necesarias para la futura superficie MCP de specIR. Resultado: crear únicamente `docs/auditoria/sldb-api-frente-a-mcp.md`, con matriz de capacidad, necesidad, estado, evidencia, brecha, acción y referencia de handoff. Repo destino: `SLDB_1/IR`; lecturas en `../sldb` y referencia documental `../pron`. Límites: no implementar código, no modificar SLDB, no diseñar tools MCP, no abrir/importar módulos internos de SLDB ni ejecutar/importar pron. Si hay capacidades no disponibles, enviar una única nota agregada a SLDB y registrar su ID.

## AMBIGUEDADES
1. «Crear solo docs/auditoria/sldb-api-frente-a-mcp.md. Inspeccionar todos los módulos bajo ../sldb/src/sldb/api/»: no fija el directorio base de las rutas relativas; obligaría a inventar el directorio de ejecución o raíz del repo.
2. «enviar una sola nota agregada con deskops message send --to sldb»: no define cuerpo, formato ni campos de la nota; obligaría a inventar su contenido exacto.
3. «detectar estado para rechazar escritura obsoleta»: no define qué constituye estado ni obsolescencia; obligaría a inventar el criterio técnico si los documentos no lo precisan.
4. «leer documento por la identidad canónica ya documentada por SLDB»: nombra la identidad pero no la fija en el input; obligaría a inventar el contrato si la documentación revisada no la identifica unívocamente.

## DRY-RUN
Lecturas previstas: módulos de `../sldb/src/sldb/api/`; documentos enumerados en Implementation Path; `../pron/source/spec/14-superficie-mcp.md` solo como referencia. Cambios previstos: crear el informe y, condicionalmente, enviar una nota con `deskops`. Dependencias: acceso a rutas, documentación SLDB, disponibilidad de `deskops` y asignación de ID. Validaciones futuras: once filas completas; estados y acciones cerrados; rutas y símbolos públicos en filas disponibles; módulos inspeccionados y justificación en no disponibles; Resumen con resultado de la nota; fuentes listadas; ausencia de dependencia de `sldb.store`, `sldb.core` o ejecución de pron. Nada se ejecuta ahora.

## FUTURO
`deskops` devuelve el ID de la nota; SLDB decide si acepta la solicitud de extensión; un humano o nodo revisor valida el informe y cierra la tarea; otro nodo podrá diseñar la superficie MCP usando la matriz.
