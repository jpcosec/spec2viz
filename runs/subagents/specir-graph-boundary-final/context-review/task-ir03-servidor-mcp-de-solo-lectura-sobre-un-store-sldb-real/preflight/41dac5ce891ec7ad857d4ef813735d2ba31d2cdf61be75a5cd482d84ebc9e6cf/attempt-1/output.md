REFORMULACION
Propósito: habilitar el primer hito, que un agente explore por MCP un store SLDB real en solo lectura. Resultado: paquete specIR con servidor MCP por stdio que liste/describa modelos y relaciones, lea documentos/campos, consulte vecinos y vecindad por dirección/profundidad, busque por predicados, resuelva vistas a JSON e inspeccione integridad, delegando en `sldb.api` sin grafo, índice ni parser propios. Repo: este repositorio, sobre los archivos listados (`src/specir/mcp/*`, tests, `pyproject.toml`). Límites: nada de escrituras, paths (`graph_path`/`graph_paths`), tipos de dominio, extractores ni renderizado; sin mocks, datos fabricados ni backend de grafo propio; pruebas sobre copia aislada del store real y federaciones deskops/spec2viz en solo lectura.

AMBIGUEDADES
1. “Las tools de grafo son adaptadores MCP delgados.” No fija nombres, esquemas de entrada ni JSON de salida; obligaría a inventar la interfaz MCP.
2. “Todo conjunto llega paginado, con su total y una marca cuando quedó cortado” no define tamaño, parámetros ni nombre de la marca; obligaría a inventar el contrato de paginación.
3. “obtener la vecindad a profundidad por dirección” no fija profundidad por defecto ni máxima; obligaría a inventar límites.
4. “Una consulta sobre algo que el store no declara devuelve conjunto vacío con explicación” no define “no declara” ni forma de la explicación; obligaría a inventar semántica y formato.
5. “resolver una vista (ViewDoc o SpecDoc) a JSON” no fija el esquema JSON ni qué variantes cubre; obligaría a inventar el contrato de resolución.
6. “el store federado deskops ... se vuelve a enlazar ... y ... se enlaza además el store real de spec2viz” no indica alias ni nombres de enlace; obligaría a inventar identificadores.

DRY-RUN
Nodo ejecutable (`task.code`), no agregado. Lecturas: task, pills, `pyproject.toml`, API pública SLDB, archivos actuales y tests. Cambios previstos: crear/ajustar `server.py`, `read_tools.py`, `addresses.py`, `paging.py`, `__init__.py`, extra MCP y pruebas. Dependencias: structuredLanguageDB, SDK MCP opcional y stores reales. Validaciones futuras: copiar `.sldb/`, `sldb/`, `desk/` sin caché; reconstruir índices; relanzar servidor real por stdio con cliente real; comparar árboles; probar paginación, documento externo, imports y ausencia de escrituras. Sin ejecutar nada.

FUTURO
Un humano decide nombres/esquemas de tools, paginación, profundidades, formato de explicaciones y manejo de la dependencia externa spec2viz. Otro nodo (IR01) aporta la matriz de auditoría que confirma qué operaciones existen en `sldb.api`; no son ambigüedades de este encargo.
