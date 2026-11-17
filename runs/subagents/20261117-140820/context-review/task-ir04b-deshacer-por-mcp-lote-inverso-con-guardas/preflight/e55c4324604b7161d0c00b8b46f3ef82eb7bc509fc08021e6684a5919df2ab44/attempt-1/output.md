REFORMULACION
Propósito: verificar, desde specIR, que el `undo_changes` servido por sldb mcp deshace los últimos lotes de la sesión —incluidos los que pasan por los validadores de la extensión de specIR— sobre una copia montada del store. Resultado: una prueba nueva en `tests/` con cliente MCP real, sin mocks y, solo si es imprescindible, ajustes en `src/specir/mcp_extension.py`; specIR no registra la tool, no guarda pila inversa ni construye lotes inversos. Repo: specIR (rutas citadas). Límites: no deshacer entre sesiones ni nivel 3; no implementar inversión ni guardas; si sldb mcp no sirve `undo_changes`, no se ejecuta.

AMBIGUEDADES
1. "Esperar a que cierre el espejo task-espejo-sldb-sldb-mcp-sirve-undo-changes…" frente a tres `depends_on`: no dice si bastan uno o los tres ni qué evidencia acredita "sirve undo_changes"; obligaría a inventar el criterio de arranque.
2. "niveles 1 y 2" y "nivel 0… nivel 1… nivel 3": no define la escala; obligaría a inventar la taxonomía y qué permite cada nivel.
3. "Si hace falta algo en la extensión… se agrega": no fija cuándo "hace falta"; obligaría a inventar el umbral de cambio.
4. "un archivo de prueba nuevo bajo tests/": sin nombre ni convención; obligaría a inventar la ruta.
5. "el resultado queda escrito": no dice dónde (informe, aserción, desk); obligaría a inventar el destino.
6. "grep … no encuentra una implementación propia": el patrón también hallaría referencias; obligaría a inventar qué cuenta como "propia".
7. "sha256 de los .md y del store": no define cómo se hashea el store; obligaría a inventar el método.

DRY-RUN
Lecturas: taskdoc, pills, `tests/conftest.py` (mount_copy, store_copy, sesión MCP), `src/specir/mcp_extension.py`, pruebas existentes y tareas espejo. Cambios previstos: nuevo test de undo; posible ajuste mínimo en `mcp_extension.py`. Dependencias: sldb mcp con `undo_changes` y pila por sesión; niveles 0/1 configurables. Validaciones futuras: igualdad sha256 antes/después; stale → `applied false`, `rejected stale`, sin escritura y lote persistente; nivel 0 sin escrituras ni undo; nivel 1 rechaza RelationTypeDoc/RuleDoc; comportamiento ante validadores de dominio; grep sin implementación propia; `deskops graph missing --root .` rc 0.

FUTURO
Los espejos de sldb producen `undo_changes`/pila y su cierre habilita el arranque; hallazgos sobre niveles o validadores los decide el equipo de sldb; un humano valida el criterio de dependencias y niveles; deskops graph confirma el grafo.
