## REFORMULACION
Nodo ejecutable de documentación, no agregado. **Propósito:** auditar la API pública de SLDB frente a las 11 capacidades necesarias para la superficie MCP de specIR. **Resultado:** `docs/auditoria/sldb-api-frente-a-mcp.md` con matriz de 11 filas —capacidad, necesidad, estado, evidencia, brecha, acción y handoff—, snapshot de SLDB y, si hay brechas, una única nota a SLDB. **Repo:** solo IR, desde `/home/jp/proyectos/SLDB_1/IR`. **Límites:** no diseñar tools, escribir código, editar otros repos, importar/ejecutar pron ni leer módulos internos de SLDB; leer la spec pron indicada sí está permitido.

## AMBIGUEDADES
1. «El contrato final de escritura queda fuera.» No define si excluye las filas 10/11, la precondición atómica o solo el diseño posterior; obligaría a inventar el borde del alcance.
2. «Una composición se considera disponible solo si docstring/documento declara expresamente que las operaciones juntas cubren la conducta.» No aclara si basta docstring o documento, ni el umbral de “expresamente”; obligaría a inventar el criterio de clasificación.
3. «Cada fila no disponible enumera módulos existentes inspeccionados» no precisa si “módulos” son archivos, rutas de importación o símbolos públicos; obligaría a inventar la granularidad exigida.

## DRY-RUN
**Lecturas:** TaskDoc, rituales, pills y átomos; corpus Python de `../sldb/src/sldb/api/`; docs SLDB listados; `../pron/source/spec/14-superficie-mcp.md` §4 y §1 MoveDoc. **Cambios previstos:** crear solo el informe, con las 11 filas, snapshot —commit, branch, UTC, `git status --short --untracked-files=all`, SHA-256 de modificados/untracked— y handoffs. Si hay no disponibles, redactar `message_body` con esas filas y ejecutar una sola vez `deskops message send ...`; registrar ID o error sin reintento. **Dependencias:** git, archivos del corpus, CLI deskops; ninguna importación/ejecución de SLDB o pron. **Validaciones futuras:** exactamente 11 filas; estados/acciones cerrados; evidencia pública citada; snapshot y hashes; nota única con título/cuerpo/ID correctos; fuentes revisadas sin módulos internos.

## FUTURO
Un humano o nodo de cierre decide commit y cierre; SLDB responde a la nota y determina extensiones.
