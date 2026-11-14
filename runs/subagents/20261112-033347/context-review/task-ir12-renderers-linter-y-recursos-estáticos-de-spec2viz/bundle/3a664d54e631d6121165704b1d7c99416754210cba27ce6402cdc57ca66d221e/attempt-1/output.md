## REFORMULACION

Encargo: implementar en el paquete specIR la capa visual heredada de spec2viz —renderizadores Mermaid, PlantUML, D2, Vega, BPMN y visor, árbol, HTML de grafo, antonia HTML y JSON—, el linter de Mermaid, la exportación de JSON Schema de specs y catálogos, y los recursos empaquetados (plantillas HTML, bpmn-js y los de cada formato), más comandos equivalentes a render, lint y schema. Resultado: cada formato produce, desde la representación intermedia de IR11, salida con paridad verificable frente a golden de spec2viz, o diferencia declarada en la matriz de cobertura con prueba equivalente. Repo: specIR (src/specir/visual/, tests/visual/). Límites: fuera compiladores, sincronización al store, catálogos/consumidores y retirar spec2viz; sin mocks ni datos fabricados; solo API pública de SLDB; sin importar spec2viz (pills y átomo ligados).

## AMBIGUEDADES

1. «Cada pieza se migra tal cual o se reemplaza, según la matriz de cobertura»: la matriz no está en el bundle; obligaría a inventar qué filas existen y cuáles ya declaran reemplazo.
2. «los que requiera cada formato» (recursos): obligaría a inventar el inventario exacto de assets por renderizador.
3. «comandos equivalentes a render, lint y schema»: sin nombres, flags ni contrato de salida; obligaría a inventar la interfaz CLI.
4. «Todos los valores del selector de renderizador de spec2viz»: no se enumera el selector; obligaría a inventar su conjunto de valores.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout, tres pills, átomo, los 16 archivos listados, spec2viz/tests y sus golden y docs/spec2viz/matriz-de-cobertura.md (solo lectura). Cambios previstos: crear/portar módulos de renderers y lint_mermaid y schema en src/specir/visual/, plantilla y assets empaquetados, comandos, y portar fixtures/golden y pruebas a tests/visual/. Dependencias: salida de IR11 (representación intermedia), API pública de SLDB, golden de spec2viz. Validaciones futuras: pruebas de paridad por renderizador, hallazgos del linter sobre fixtures, igualdad de JSON Schema, prueba de empaquetado sin recursos externos faltantes, cobertura del selector y prueba de no importar spec2viz. Sin ejecutar nada.

## FUTURO

IR11 entrega la representación intermedia y sus compiladores. El dueño o el nodo de matriz decide las filas, las diferencias declaradas y la condición de retiro; si falta una operación general de SLDB, se detiene y se pide al desk de SLDB. Closeout liga conocimiento durable y actualiza el board.
