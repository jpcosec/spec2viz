REFORMULACION
Propósito: auditar la API pública de SLDB frente a 11 capacidades para la superficie MCP de specIR, sin diseñar tools. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con matriz de 11 filas y, si hay no disponibles, una nota única. Repo: specIR (`/home/jp/proyectos/SLDB_1/IR`); solo se escribe ese informe. Límites: leer el corpus exacto de `../sldb` y `../pron/source/spec/14-superficie-mcp.md §1/§4`; no abrir módulos internos de SLDB, no importar/ejecutar pron, no cambiar otros repos, no decidir política de escritura (IR02). No es agregado ni paquete no ejecutable: tarea documental ejecutable.

AMBIGUEDADES
1. "Pregunta al desk": no se define su texto. Obligaría a inventar la formulación enviada.
2. "la falta de explicación explícita se clasifica no disponible" / "suficiente semántica": umbral no definido. Obligaría a inventar criterio.
3. "Hashear SHA-256 solo los archivos ... modificados/untracked": no cubre borrados. Obligaría a inventar su tratamiento.
4. "Una matriz" / "El informe": no fija sintaxis de tabla ni orden de campos, aunque Validation los enumera. Obligaría a inventar formato.
5. "Fecha UTC: <ISO-8601>": no fija precisión ni sufijo. Obligaría a inventar formato.

DRY-RUN
Lecturas: TaskDoc, rituales, pills, átomos; `.py` bajo `../sldb/src/sldb/api/`; docs SLDB nombrados; spec pron §1/§4. Ejecutaría `git -C ../sldb rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all` con pathspecs; si git falla, registraría error y hashearía todo el corpus. Cambio previsto: escribir solo `docs/auditoria/sldb-api-frente-a-mcp.md`. Dependencias: git, lectura, y `deskops message send` solo si hay no disponibles. Validaciones: 11 filas; estados/acciones cerrados; evidencia existente; snapshot con commit/branch/fecha/status y hashes si procede; una sola nota con título/cuerpo/ID o Resumen de no envío; sin imports internos ni ejecución de pron.

FUTURO
IR02 decide política de escritura. El desk de SLDB atiende la nota. `deskops message send` devuelve path/stem o falla; si falla, tarea abierta. Un humano resuelve preguntas y confirma evidencia externa.
