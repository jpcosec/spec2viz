REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: que un agente explore por MCP un store SLDB real en solo lectura, sin esperar decisiones de escritura. Resultado: servidor MCP en el paquete Python `specIR`, por stdio y sobre la API pública de SLDB, con tools para listar/describir modelos y tipos de relación, leer documento o campo, vecinos y recorrido, búsqueda por predicados, resolver `ViewDoc`/`SpecDoc` a JSON e integridad. Repo: el que contiene `pyproject.toml`, `src/specir` y `tests`; la superficie MCP está bajo `src/specir/mcp`. Límites: sin escrituras, tipos de dominio nuevos, extractores ni renderizado de diagramas; dependencia de `structuredLanguageDB` y SDK MCP como extra opcional; las tools envuelven solo operaciones existentes según la matriz de auditoría.

AMBIGUEDADES
1. “Pruebas con un cliente MCP contra un store de prueba” frente a “un store SLDB real” / “un store real”: obliga a decidir si el ejecutor crea un fixture, de dónde sale y si un store sintético contradice el guardrail de no fabricar datos.
2. “las tools son envoltorios de las operaciones que la matriz de auditoría marca como existentes”: la matriz no está incluida; obliga a inventar operaciones, nombres y firmas.
3. “el SDK de MCP como extra opcional”: obliga a inventar nombre del extra, versión y comportamiento si no está instalado.
4. “su dirección estable” y “JSON estructurado”: obliga a inventar formato, campos y contrato de error/vacío.
5. “Todo conjunto llega paginado, con su total y una marca cuando quedó cortado”: obliga a inventar parámetros, límites y nombre de la marca.
6. “búsqueda por predicados”: obliga a inventar sintaxis y alcance de predicados.

DRY-RUN
Lecturas: TaskDoc, pills, tarea IR01/matriz de auditoría, `pyproject.toml`, `src/specir`, tests y `conftest.py`. Cambios previstos: `mcp/server.py`, `read_tools.py`, `addresses.py`, `paging.py`, `mcp/__init__.py`, extra en `pyproject.toml` y pruebas MCP. Dependencias: API pública `sldb.api`, SDK MCP y operaciones declaradas por IR01. Validaciones futuras: cliente MCP contra store, paginación con total/corte, árbol del store sin cambios, consulta no declarada como vacío explicado e imports sin `pron`, `spec2viz` ni módulos SLDB fuera de `sldb.api`.

FUTURO
IR01 debe entregar la matriz de operaciones existentes; otro nodo o un humano debe proveer el store real y aceptar el recorrido final del agente.
