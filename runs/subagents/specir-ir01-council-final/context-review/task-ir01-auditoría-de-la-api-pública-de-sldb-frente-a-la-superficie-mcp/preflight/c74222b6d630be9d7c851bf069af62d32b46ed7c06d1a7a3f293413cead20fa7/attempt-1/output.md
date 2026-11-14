REFORMULACION

Propósito: auditar la API pública de SLDB frente a 11 capacidades de la superficie MCP de specIR, clasificando cada fila como disponible, requiere-extensión-en-SLDB o faltante. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con matriz de 11 filas (capacidad, necesidad, estado, evidencia, brecha, acción, handoff) y, si hay brechas, una única nota al desk SLDB. Repo: `/home/jp/proyectos/SLDB_1/IR`; inspeccionar `../sldb` y leer `../pron/source/spec/14-superficie-mcp.md` §4. Límites: no diseñar tools, escribir código, editar otros repos, importar/ejecutar pron ni leer módulos internos de SLDB; el informe no decide el contrato final de escritura. Nodo ejecutable, no agregado.

AMBIGUEDADES

1. «addressability_model.md» figura sin prefijo junto a «../sldb/docs/README.md» y «../sldb/docs/architecture/...»; obliga a inventar si la ruta es relativa a IR, a `../sldb/docs` u otra.
2. «TaskDoc IR01» no define si es texto literal, ruta, título, ID o enlace; obliga a inventar su representación en el cuerpo.
3. «si falla usa Nota no enviada; tarea abierta, con comando, resultado y fecha UTC» no fija frase exacta ni formato/orden; obliga a inventar el literal del Resumen y la disposición de esos datos.

DRY-RUN

Lecturas: ejecutaría `git -C ../sldb rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all`; si falla, registraría el error. Leería recursivamente `../sldb/src/sldb/api/*.py`, documentos citados —resolviendo `addressability_model.md`— y pron §4; calcularía SHA-256 de modificados/untracked. Cambios previstos: crear solo `docs/auditoria/` y el informe; no tocar SLDB ni pron. Dependencias: git, archivos/documentos citados, deskops y pron §4. Validaciones futuras: 11 filas exactas; estados/acciones cerrados; evidencia con rutas/símbolos públicos; snapshot commit/branch/status/hashes; si hay brechas, un `deskops message send` con ID exacto en Resumen y filas, o ERROR y Resumen de fallo; si no, handoffs «—» y Resumen exacto.

FUTURO

El desk SLDB decide aceptar/priorizar extensiones y el contrato final de escritura. Un nodo posterior de diseño MCP consume la matriz. Un humano valida el cierre y la calidad; deskops solo registra la solicitud.
