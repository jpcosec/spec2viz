## REFORMULACION
IR12 es un nodo de entrega `code` del repo `specIR`: portar o reemplazar la capa de salida de spec2viz —renderizadores Mermaid, PlantUML, D2, Vega, BPMN y visor, árbol, HTML de grafo, antonia HTML y JSON—, el linter Mermaid, el export de JSON Schema y los recursos empaquetados, con paridad verificable. Resultado esperado: módulos bajo `src/specir/visual/`, plantilla `default.html` y pruebas de renderers, lint, schema y recursos. Límites: no incluye compiladores ni IR (IR11), catálogos/átomos, CLI/API final ni retirada de spec2viz.

## AMBIGUEDADES
1. “Cada pieza se migra tal cual o se reemplaza, según la matriz de cobertura”: no se aporta la matriz ni la decisión por pieza; obligaría a inventar qué renderizadores se copian y cuáles se reescriben.
2. “los que requiera cada formato”: no hay inventario de recursos estáticos; obligaría a inventar dependencias empaquetadas y su ubicación.
3. “comandos equivalentes a render, lint y schema”: no se define si IR12 implementa entrada de comandos o solo funciones, y solapa con IR13D; obligaría a inventar el límite.
4. “fixtures de spec2viz” y “golden”: no se indican rutas, nombres ni selección; obligaría a inventar el conjunto de paridad.

## DRY-RUN
Sin ejecutar: un ejecutor leería IR12, el repo `specIR`, la salida de IR11, la matriz de cobertura, fixtures/goldens de spec2viz y recursos como bpmn-js. Crearía o ajustaría renderizadores, `lint_mermaid.py`, `schema.py`, `templates/default.html` y las cuatro pruebas indicadas. Dependencias: IR11, fixtures/goldens, matriz y assets empaquetables. Validaciones futuras: paridad contra golden o diferencia declarada, hallazgos de lint equivalentes, schema igual o declarado, apertura HTML sin recursos externos faltantes, selector completo y ausencia de imports de spec2viz.

## FUTURO
IR11 produce la representación intermedia y compiladores. IR13B reutiliza renderizadores; IR13D expone CLI/API; el gate de IR13 y la matriz deciden diferencias aceptadas y retirada de spec2viz. Un humano o nodo responsable debe aportar la matriz, fixtures/goldens y criterios de recursos.
