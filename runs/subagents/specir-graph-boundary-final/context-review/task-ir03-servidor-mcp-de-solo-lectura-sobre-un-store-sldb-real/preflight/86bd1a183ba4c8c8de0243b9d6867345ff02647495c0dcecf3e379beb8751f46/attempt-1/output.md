## REFORMULACION
Tarea de código ejecutable en el repo specIR: construir un servidor MCP de solo lectura por stdio sobre un store SLDB real. Propósito: que un agente descubra modelos, lea documentos/campos, recorra relaciones y resuelva vistas e integridad. Resultado: tools delgadas sobre `sldb.api` (sin índice, recorrido, parser ni backend propios) y pruebas con servidor/cliente MCP reales sobre copia aislada del store, con deskops y spec2viz federados en solo lectura. Límites: sin escrituras, mocks, datos inventados, tipos de dominio, extractores, diagramas, imports de pron/spec2viz ni API SLDB fuera de `sldb.api`. Depende de task-ir01.

## AMBIGUEDADES
1. “SDK de MCP como extra opcional”: faltan paquete, versión y API; obligaría a inventar `pyproject.toml`.
2. “sldb stores update... edges rebuild... stores check... stores add”: faltan sintaxis, orden y rutas; obligaría a inventar comandos.
3. “tools para listar... resolver una vista”: faltan nombres, parámetros, esquema JSON, paginación y formato de “dirección estable”; obligaría a inventar el contrato MCP.
4. “graph_path o graph_paths, según la operación” frente a “graph_path/graph_paths no son necesarios”: contradicción; obligaría a decidir si existen tools de caminos.
5. “el modelo con más documentos” y “conjunto vacío con explicación”: faltan criterio/desempate y forma de explicación; obligaría a inventar ambos.

## DRY-RUN
Lecturas: task doc, `pyproject.toml`, `src/specir`, tests, firmas de `sldb.api`, salida de task-ir01 y SDK MCP. Cambios previstos: extra MCP; `src/specir/mcp/{server,read_tools,addresses,paging}.py`; fixture de copia en `tests/conftest.py`; tests MCP e imports. Dependencias: task-ir01, API pública SLDB, SDK MCP y stores reales deskops/spec2viz. Validaciones futuras: cliente/servidor por stdio, paginación, SpecDoc real, árboles antes/después, ausencia de escrituras e imports prohibidos, y vacío explicado. No se ejecuta nada.

## FUTURO
task-ir01 entrega la matriz que fija operaciones existentes; un humano decide nombres/esquemas y rutas; otro nodo ejecuta la implementación y las validaciones; SLDB decide una extensión si falta filtro por relación.
