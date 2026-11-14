**REFORMULACION**

Propósito: cerrar en specIR la entrega de salidas de spec2viz —renderizadores, linter de Mermaid, export de JSON Schema y recursos estáticos— con paridad verificable frente a spec2viz.

Resultado: módulos bajo `src/specir/visual/renderers/`, `lint_mermaid.py`, `schema.py`, `templates/default.html` y pruebas de renderers, lint, schema y recursos.

Repo: `specIR`.

Límites: dentro, los formatos Mermaid, PlantUML, D2, Vega, BPMN/visor, árbol, HTML de grafo, antonia HTML, JSON, linter, schema y recursos empaquetados. Fuera: compiladores, sincronización al store, catálogos/consumidores y retirar spec2viz. Depende de IR11. No es agregado: es una entrega de código implementable por un ejecutor futuro; el paquete no debe importar spec2viz.

**AMBIGUEDADES**

1. “según la matriz de cobertura” y “su condición de retiro cumplida”: no se incluye la matriz ni sus filas. Obliga a inventar modos de migración, diferencias aceptadas y condiciones de retiro.
2. “los fixtures de spec2viz producen en specIR una salida idéntica a su golden”: no se listan fixtures, goldens ni versión de spec2viz. Obliga a inventar el conjunto de paridad.
3. “o la diferencia está declarada”: no se define dónde ni con qué formato se declara. Obliga a inventar el mecanismo de excepción.
4. “Todos los valores del selector de renderizador de spec2viz existen en specIR”: no se enumeran esos valores. Obliga a inventar la lista y su fuente.
5. “los recursos que requiera cada formato”: es abierto. Obliga a inventar el inventario de recursos empaquetados.

**DRY-RUN**

Un ejecutor futuro leería el contrato IR12, las salidas de IR11 (IR, compiladores, proyecciones), la matriz de cobertura, goldens/fixtures de spec2viz y el selector de renderizadores. Crearía o ajustaría los módulos de `output_scope`, la plantilla HTML y las pruebas. Dependencias: IR11; recursos locales; spec2viz solo como referencia de pruebas. Validaría con pruebas de paridad por renderizador, lint sobre fixtures, igualdad de schema, apertura offline de HTML BPMN/grafo, cobertura del selector y prueba de imports sin spec2viz. Sin ejecutar nada.

**FUTURO**

La matriz de cobertura y el gate de retiro los confirma otro nodo/humano; IR13 valida el conjunto y los consumidores migrados. IR11 entrega la representación intermedia.
