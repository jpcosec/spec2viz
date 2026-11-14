REFORMULACION
Propósito: implementar en el paquete specIR un servidor MCP de solo lectura sobre la API pública de SLDB. Resultado: tools para listar/describir modelos y tipos de relación, leer documentos o campos, consultar vecinos salientes/entrantes filtrados, obtener vecindad por dirección y profundidad, buscar por predicados, resolver vistas a JSON e inspeccionar integridad. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`, con los archivos declarados en `files`. Límites: sin escrituras, paths, dominios nuevos, extractores, renderizado, índices/recorridos/parser/backend propios, mocks ni datos fabricados; pruebas contra copia aislada del store real, con deskops y spec2viz federados en solo lectura.

AMBIGUEDADES
1. “el SDK de MCP como extra opcional”: no fija paquete, versión ni nombre del extra; obligaría a inventar dependencias.
2. “buscar por predicados”: no define sintaxis, operadores ni API SLDB; obligaría a inventar semántica o parser.
3. “inspeccionar integridad del store”: no concreta tool, operación ni JSON; obligaría a inventar contrato.
4. “resolver una vista (ViewDoc o SpecDoc) a JSON”: no fija direccionamiento ni forma de salida; obligaría a inventar esquema.
5. “La vecindad multi-salto recorre los tipos de relación del índice según la dirección”: no enumera valores de dirección; obligaría a inventar el vocabulario público.
6. “una marca cuando quedó cortado”: no nombra el campo; obligaría a inventar el formato paginado.

DRY-RUN
Lecturas: TaskDoc, pills, dependencia ir01, `pyproject.toml`, módulos `src/specir/mcp/*`, tests, API pública de SLDB y stores reales. Cambios previstos: crear/ajustar servidor, tools, direcciones, paginación y pruebas listadas. Dependencias: matriz de auditoría de ir01, `sldb.api`, SDK MCP y stores federados. Validaciones futuras: cliente MCP real por stdio, paginación, resolución de `class.sldb-models`, integridad, imports permitidos, ausencia de escrituras y comparación de árboles antes/después. Sin ejecutar nada.

FUTURO
Otro nodo entrega la matriz de auditoría de ir01; un humano confirma versiones del SDK, contrato JSON y semántica de predicados/dirección; el ejecutor futuro produce código y pruebas.
