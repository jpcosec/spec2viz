REFORMULACION
Propósito: que un agente explore por MCP un store SLDB real sin esperar decisiones de escritura. Resultado: servidor MCP por stdio en specIR con tools delgadas sobre sldb.api para listar/describir modelos y tipos de relación, leer documento o campo, vecinos salientes/entrantes filtrados, vecindad por dirección y profundidad, búsqueda por predicados, resolución de ViewDoc/SpecDoc a JSON e inspección de integridad. Repo: specIR, con structuredLanguageDB y SDK MCP como extra opcional. Límites: solo sldb.api; sin escrituras, paths, extractores, renderizado ni índice/recorrido/parser propios; pruebas sobre copia aislada del store real y federación deskops/spec2viz en solo lectura, sin mocks ni datos fabricados; ante bloqueo, detenerse.

AMBIGUEDADES
1. "buscar por predicados": no define sintaxis ni operadores; obligaría a inventar el contrato de predicados.
2. "resolver una vista (ViewDoc o SpecDoc) a JSON": no fija esquema ni distinción de tipo; obligaría a inventar la salida.
3. "inspeccionar integridad del store": no nombra operación pública ni qué reporta; obligaría a inventar tool y resultado.
4. "Todo conjunto llega paginado, con su total y una marca cuando quedó cortado": no define parámetros ni campos; obligaría a inventar la API de paginación.
5. "cada tool devuelve JSON estructurado y, por cada documento, su dirección estable": no define sobre ni formato de dirección; obligaría a inventar ambos.
6. "el contrato no promete filtrar un tipo específico en cada salto" frente a "consultar vecinos salientes/entrantes filtrados por tipo de relación y obtener la vecindad a profundidad por dirección": no aclara el alcance del filtro; obligaría a inventar la semántica.

DRY-RUN
Lecturas: TaskDoc, rituales, pills, átomos, archivos listados, store original/federados y class.sldb-models. Cambios previstos: pyproject (extra MCP), src/specir/mcp/{server,read_tools,addresses,paging}.py, tests/conftest.py (copia con stores update/edges rebuild/check/add) y tests/mcp/*, tests/test_imports.py. Dependencias: IR01, sldb.api, SDK MCP, stores reales. Validaciones futuras: servidor stdio y cliente real, comparación de árboles, pytest, paginación, vacíos explicados, imports.

FUTURO
IR01 entrega la matriz de operaciones existentes. Un humano tramita en el desk de SLDB toda carencia general; si falta el store de spec2viz o class.sldb-models, el ejecutor se detiene y reporta. Cierre y commit: ritual closeout. Tools de paths: otra tarea.
