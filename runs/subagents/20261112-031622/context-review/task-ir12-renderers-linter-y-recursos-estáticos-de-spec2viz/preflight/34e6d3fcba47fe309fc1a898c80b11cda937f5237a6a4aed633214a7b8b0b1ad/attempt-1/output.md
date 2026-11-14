## REFORMULACION

Encargo ejecutable en el repo specIR: completar la migración de las salidas de spec2viz. El propósito es que specIR produzca todos los formatos que consumen los usuarios de spec2viz, no solo los usados hoy. El resultado esperado son renderizadores Mermaid, PlantUML, D2, Vega, BPMN y visor, árbol, HTML de grafo, antonia HTML y JSON; linter de Mermaid; export de JSON Schema de specs y catálogos; recursos empaquetados y comandos equivalentes a render, lint y schema, con paridad verificable. Se trabaja sobre `src/specir/visual/` y `tests/visual/`. Límites: fuera compiladores, sincronización al store, catálogos y consumidores, y retirar spec2viz. Depende de `task-ir11-compiladores-y-proyecciones-de-spec2viz`. Es una unidad ejecutable, no un agregado.

## AMBIGUEDADES

1. “según la matriz de cobertura” y “la diferencia está declarada en la matriz de cobertura”: no se indica ubicación, formato ni criterio de decisión; obligaría a inventar la matriz y sus reglas.
2. “la representación intermedia de la tarea de compiladores”: no se define su contrato, tipos ni API; obligaría a inventar la interfaz de IR11.
3. “los fixtures de spec2viz” y “su golden”: no se listan rutas ni versión; obligaría a inventar el corpus de paridad.
4. “los que requiera cada formato” y “bpmn-js”: no se fijan versiones, licencias ni inventario; obligaría a inventar recursos empaquetados.
5. “comandos equivalentes a render, lint y schema”: no se especifican nombres, flags ni salida; obligaría a inventar la CLI.
6. “Todos los valores del selector de renderizador de spec2viz”: no se identifica el selector ni su fuente; obligaría a inventar el conjunto exigido.

## DRY-RUN

Lecturas previstas: TaskDoc, pills, archivos listados, contrato de IR11, fuentes/fixtures/goldens de spec2viz y matriz de cobertura. Cambios previstos: implementar los renderizadores y helpers en `src/specir/visual/renderers/`, `lint_mermaid.py`, `schema.py` y plantillas; añadir pruebas en `tests/visual/`. Dependencias: salida de IR11, corpus de spec2viz, recursos empaquetables y decisiones de paridad. Validaciones futuras: ejecutar las cuatro suites visuales, comprobar HTML BPMN/grafo sin recursos externos, verificar selector, schema exportado, linter y ausencia de imports de spec2viz.

## FUTURO

IR11 debe entregar la representación intermedia y su contrato. Un humano o nodo de cobertura debe fijar la matriz y aprobar diferencias declaradas. CI o un nodo de validación ejecutará las suites y decidirá el retiro de spec2viz.
