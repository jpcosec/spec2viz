## REFORMULACION

**Propósito:** auditar la API pública de SLDB (`sldb.api`) frente a las once capacidades que necesitará la superficie MCP de specIR, sin diseñar tools MCP.

**Resultado:** un único informe `docs/auditoria/sldb-api-frente-a-mcp.md` con matriz de once filas (capacidad, necesidad, estado, evidencia, brecha, acción, referencia de handoff) y sección `# Resumen`; si hay carencias, una nota agregada al desk de SLDB.

**Repo:** specIR. Solo se crea ese archivo de informe.

**Límites:** lectura de `../sldb/src/sldb/api/` y de los documentos SLDB enumerados; la spec de pron solo como referencia documental. No importar ni ejecutar pron, no abrir módulos internos de SLDB, no editar otros repos.

## AMBIGUEDADES

1. «todos los módulos de ../sldb/src/sldb/api/»: no aclara si incluye subpaquetes ni profundidad; obligaría a inventar el alcance de inspección.
2. «derived-store-boundary.md, edges.md, journal-authority.md…»: rutas sin prefijo; obligaría a inferir `docs/architecture/`.
3. «Necesidad se redacta como una frase con actor, entrada y resultado»: no define el actor; obligaría a inventarlo (¿cliente MCP, specIR?).
4. «escrituras validadas»: no dice si la validación es parte de la operación o del llamador; obligaría a inventar el contrato.
5. «detectar estado para rechazar escritura obsoleta»: no define qué es “estado” (versión, journal, etag); obligaría a inventar semántica.
6. «revertir una escritura si existe operación pública»: no fija qué estado asignar si no existe; obligaría a decidir el mapeo.
7. «búsqueda por filtros ya soportados»: criterio circular; podría forzar a inventar qué filtros cuentan.
8. «todas referidas a la nota agregada única» frente al caso «todas están disponibles» sin nota: contradice el literal `—`.

## DRY-RUN

**Lecturas:** módulos bajo `../sldb/src/sldb/api/`; documentos SLDB listados; `../pron/source/spec/14-superficie-mcp.md` solo como referencia.

**Cambios previstos:** crear `docs/auditoria/sldb-api-frente-a-mcp.md` (y el directorio si falta).

**Dependencias:** `deskops message send --to sldb`; presencia de `../sldb` y `../pron`.

**Validaciones futuras:** once capacidades cubiertas; estados y acciones cerrados; rutas y símbolos públicos citados; resumen con ID de nota o constancia de no envío; fuentes listadas; sin imports internos ni de pron.

## FUTURO

Si hay brechas, el desk de SLDB decide y atiende la extensión; un humano valida la nota y el informe. El cierre y commit corresponden al ritual de closeout. Este nodo es una tarea ejecutable de documentación, no un agregado.
