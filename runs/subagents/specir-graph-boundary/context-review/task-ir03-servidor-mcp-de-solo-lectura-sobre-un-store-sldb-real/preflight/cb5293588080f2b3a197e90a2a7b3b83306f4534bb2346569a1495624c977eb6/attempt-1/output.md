## REFORMULACION

Propósito: habilitar el primer hito —que un agente explore por MCP un store SLDB real— sin esperar las decisiones de escritura. Resultado: un servidor MCP de solo lectura en el paquete specIR, por stdio, con tools para listar/describir modelos y tipos de relación, leer documento o campo, vecinos, recorrido por relación, búsqueda por predicados, resolver vistas (ViewDoc/SpecDoc) a JSON e integridad. Repo: specIR (Python; SLDB como dependencia y SDK MCP como extra opcional), superficie en `files`. Límites: ninguna escritura; tools de grafo como adaptadores delgados sobre `sldb.api`; sin índice de aristas, algoritmo, parser ni backend propios; sin tipos de dominio, extractores ni renderizado; sin mocks ni datos fabricados; pruebas sobre copia aislada del store real y stores federados deskops/spec2viz en solo lectura.

## AMBIGUEDADES

1. «`graph_path` o `graph_paths`, según la operación»: no fija qué operación usa cada función; obligaría a inventar el mapeo.
2. «búsqueda por predicados»: no define sintaxis ni forma del predicado; obligaría a inventar el contrato de entrada (y choca con prohibir parser propio).
3. «cada tool devuelve JSON estructurado»: no fija esquema ni campos de salida; obligaría a inventar el contrato.
4. «con su total y una marca cuando quedó cortado»: no nombra la marca ni el campo de total.
5. «devuelve conjunto vacío con explicación»: no define la forma de la explicación.
6. «resolver una vista (ViewDoc o SpecDoc)»: no da criterio para distinguirlas ni qué tool decide.

## DRY-RUN

Lecturas: TaskDoc, pills, `pyproject.toml`, `src/specir/__init__.py`, `tests/conftest.py`, `.sldb/`, `sldb/`, `desk/` y stores federados. Cambios previstos: crear `src/specir/mcp/{server,read_tools,addresses,paging}.py`, `tests/mcp/test_read_tools.py`, `tests/mcp/test_no_writes.py`, `tests/test_imports.py` y el extra MCP en pyproject. Dependencias: matriz de IR01, API pública de SLDB, SDK MCP, stores deskops y spec2viz. Validaciones futuras (pytest): cliente real por stdio, contenido idéntico a `desk/`, paginación sobre el modelo con más documentos (se deriva del store), SpecDoc `class.sldb-models`, árbol antes/después en copia, original y federados, vacío con explicación, e imports sin pron/spec2viz/sldb fuera de `sldb.api`.

## FUTURO

IR01 entrega la matriz que fija qué operaciones existen y, por tanto, los envoltorios. Otro nodo o un humano debe decidir el esquema JSON de cada tool, el formato de predicados, la marca de corte y el criterio ViewDoc/SpecDoc si no se fijan antes. Las decisiones de escritura quedan fuera de este hito.
