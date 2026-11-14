## REFORMULACION

Encargo: producir un registro de decisión en `docs/decisiones/contrato-de-escritura-mcp.md` con cuatro decisiones (qué es una propuesta de cambio; precondición contra store cambiado; dónde se declara el nivel de escritura; si hay deshacer), cada una con contexto, alternativas, operación de la API pública de SLDB que la sostiene, alternativa elegida, motivo y fecha. Después, crear cuatro atoms durables (uno por decisión, con `--provenance` al registro), anotar sus ids en el registro y en las referencias de la tarea, y editar el atom de principios de seguridad de la superficie MCP para citar los mecanismos decididos. Repo/workspace: `desk` del proyecto SLDB/IR. Límites: fuera implementar y decidir permisos multiusuario; ningún camino de escritura puede saltarse la API pública de SLDB. La elección la hace el dueño del proyecto; el ejecutor redacta alternativas y recomendación.

## AMBIGUEDADES

1. "el dueño del proyecto elige" — no se indica canal, formato ni momento de la elección; obligaría a inventar el mecanismo de recibo owner.
2. "según la matriz de la tarea de auditoría" — la matriz no está en el input; obligaría a inventar su contenido o esquema.
3. "creados con deskops add atom" y "deskops edit atom" — no se da sintaxis ni campos obligatorios; obligaría a inventar la interfaz.
4. "un atom durable por cada decisión" — no se define el esquema del atom (id, título, cuerpo) más allá de provenance.
5. "las referencias de la tarea" — no se especifica dónde ni en qué formato se anotan los ids.

## DRY-RUN

Lecturas previstas: registro existente si lo hubiera, matriz de auditoría de IR01, atom `atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir`, pill de guardrail, task doc. Cambios previstos: crear el registro con cuatro secciones; tras la elección del dueño, crear cuatro atoms vía `deskops add atom --provenance ...`; editar el atom de seguridad; actualizar referencias del task doc; anotar ids en el registro. Dependencias: IR01 completada (matriz), elección del dueño, disponibilidad de `deskops`. Validaciones futuras: las seis de Validation (secciones completas, operación API citada, atoms coincidentes con provenance, ids listados, sin rutas de escritura fuera de la API, atom de seguridad actualizado). No se ejecuta nada.

## FUTURO

El dueño del proyecto elige cada alternativa y emite el recibo owner. IR01 entrega la matriz de operaciones de la API pública. `deskops` provee los comandos de atoms. Otro nodo implementará la escritura MCP citando estos mecanismos.
