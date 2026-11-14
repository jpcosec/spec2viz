## REFORMULACION

Encargo ejecutable (`task.code`, no agregado: sin hijos). **Propósito:** primer hito del proyecto, que un agente explore por MCP un store SLDB real; la lectura no espera decisiones de escritura. **Resultado:** en el paquete `specIR` de este repo, un servidor MCP por stdio, solo lectura, con tools para listar/describir modelos y tipos de relación, leer documento o campo, vecinos y recorrido por relación, búsqueda por predicados, resolver una vista (ViewDoc/SpecDoc) a JSON e integridad del store. **Repo/superficie:** `pyproject.toml`, `src/specir/mcp/*`, `tests/mcp/*`, `tests/conftest.py`. **Límites:** sin escrituras, tipos de dominio, extractores ni renderizado; depende de `task-ir01`; solo API pública de SLDB (`sldb.api`), sin pron/spec2viz ni dobles; store de prueba = copia aislada del store real, con deskops y spec2viz federados en solo lectura.

## AMBIGUEDADES

1. «las tools son envoltorios de las operaciones que la matriz de auditoría marca como existentes»: la matriz no está en el input; obliga a inventar qué operaciones existen y sus firmas.
2. «dependencia en structuredLanguageDB y el SDK de MCP como extra opcional»: obliga a inventar nombre de distribución, versión, clave del extra y si MCP es opcional también en pruebas.
3. «búsqueda por predicados»: obliga a inventar gramática, operadores y forma JSON.
4. «resolver una vista (ViewDoc o SpecDoc) a JSON»: obliga a inventar nombres de tools, argumentos y envoltura de salida.
5. «Todo conjunto llega paginado, con su total y una marca cuando quedó cortado»: obliga a inventar nombres de campos (`total`, `truncated`, cursor) y parámetros.
6. «por cada documento, su dirección estable»: obliga a inventar el formato de dirección.
7. «e integridad del store»: obliga a inventar qué API pública y qué esquema de informe.
8. «se vuelve a enlazar en la copia con sldb stores add apuntando a su ruta real»: obliga a inventar resolución de rutas relativas, alias y si el fixture invoca CLI o API.
9. «solo operan herramientas públicas de SLDB: sldb stores update...»: obliga a decidir binario/ruta de `sldb` y su disponibilidad en tests.

## DRY-RUN

**Lecturas:** TaskDoc, pills, `pyproject.toml`, `src/specir/__init__.py`, `src/specir/mcp/*`, `tests/conftest.py`, `tests/mcp/*`, `tests/test_imports.py`, salida de IR01, stores `.sldb/`, `sldb/`, `desk/` y `../spec2viz/.sldb`. **Cambios previstos:** crear `server.py`, `read_tools.py`, `addresses.py`, `paging.py`; ampliar `pyproject.toml`; crear fixture de copia aislada; tests de lectura, paginación, vistas, no-escritura e imports. **Dependencias:** matriz de IR01, API pública SLDB, SDK MCP, stores federados existentes. **Validaciones futuras:** suite completa, comparación de árboles antes/después, SpecDoc `class.sldb-models`, conjunto vacío explicado, test de imports, ausencia de dobles.

## FUTURO

IR01 entrega la matriz de operaciones existentes; un humano decide nombres/esquemas de tools, paginación y direcciones; se confirma disponibilidad del SDK MCP y de `../spec2viz/.sldb` con `class.sldb-models`.
