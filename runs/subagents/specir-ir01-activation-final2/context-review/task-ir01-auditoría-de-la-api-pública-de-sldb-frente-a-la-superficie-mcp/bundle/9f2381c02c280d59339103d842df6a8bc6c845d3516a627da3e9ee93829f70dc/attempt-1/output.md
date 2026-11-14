## REFORMULACION
**Propósito:** auditar la API pública de SLDB frente a las once necesidades de la futura superficie MCP de specIR. **Resultado:** `docs/auditoria/sldb-api-frente-a-mcp.md`, con matriz por capacidad (necesidad, estado, evidencia, brecha, acción, referencia) y sección `# Resumen`; si hay filas no disponibles, una única nota al desk de SLDB con su ID. **Repo:** solo se escribe en specIR/IR; se lee `../sldb/src/sldb/api/` y los documentos indicados, y `../pron/source/spec/14-superficie-mcp.md` como referencia. **Límites:** no diseñar tools, escribir código, editar otros repos ni decidir el contrato de escritura; no leer módulos internos de SLDB ni importar/ejecutar pron.

## AMBIGUEDADES
1. «Toda fila disponible lleva referencia de handoff —»: el guion no define formato ni valor. Obligaría a inventar si se copia literalmente, se deja vacío o se usa otro marcador.
2. «revertir un cambio ya confirmado con efecto persistente y registro durable, como exige pron kb_undo»: no queda claro si `kb_undo` es criterio normativo detallado o mera referencia. Obligaría a inventar garantías de reversión no especificadas en el input.

## DRY-RUN
**Lecturas previstas:** recursivamente los `.py` bajo `../sldb/src/sldb/api/`; `../sldb/docs/README.md`, `addressability_model.md` y los nueve documentos de `architecture/` enumerados; `../pron/source/spec/14-superficie-mcp.md`. **Cambios previstos:** crear `docs/auditoria/` si falta y escribir únicamente `docs/auditoria/sldb-api-frente-a-mcp.md`. **Dependencias:** `deskops message send --to sldb`, solo si alguna capacidad resulta `requiere-extensión-en-SLDB` o `faltante`; una sola nota agregada. **Validaciones futuras:** cubrir once capacidades con todos los campos; estados y acciones cerrados; citar rutas y símbolos públicos en filas disponibles; justificar ausencias contra el corpus inspeccionado; declarar ID de nota o ausencia de envío; listar fuentes; confirmar que no se usó `sldb.store`, `sldb.core` ni se ejecutó pron.

## FUTURO
Un nodo ejecutor realizará las lecturas, redactará la matriz, enviará la nota si procede y registrará su ID. El equipo propietario de SLDB decidirá y ejecutará cualquier extensión solicitada; el humano valida el informe y la evidencia del handoff.
