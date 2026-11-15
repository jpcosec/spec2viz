REFORMULACION

El nodo pide migrar a specIR (repo SLDB_1/IR) la salida de spec2viz 2de1056: nueve renderizadores (plantuml, mermaid, vega, d2, antonia-html, tree, graph, bpmn, json), linter de Mermaid, JSON Schema de specs y catálogos, recursos empaquetados (default.html, vendor/bpmn-js 18.31.1) y comandos render/lint/schema/validate y catalog schema, con paridad verificable en src/specir/visual/ y tests/visual/, package-data y script specir en pyproject. Fuera: compiladores (IR11), sync al store, catálogos/consumidores y retiro de spec2viz.

AMBIGUEDADES

1. "los 36 que validan, dibujados con los nueve renderers" frente a "una salida idéntica a su golden": varios renderers lanzan RenderError sobre IR ajenos, de modo que no hay salida; obliga a inventar si la paridad de esos casos es la clase y mensaje de error.
2. "una diferencia se declara en la condición de retiro de su fila" y "La matriz no acredita filas: las cita IR13" frente a "la diferencia está declarada en la matriz de cobertura": ¿IR12 edita la matriz o solo la cita? Obliga a inventar el mecanismo de declaración.
3. "Transición sin estado de origen (pendiente de IR11): ANY_STATE... pasa a ser parte del contrato de la IR (src/specir/visual/ir.py)", cuando ir.py ya lo define: obliga a inventar si IR12 edita ir.py o solo lo consume.
4. "Hasta que lo haga, src/specir/visual/notation_style.py es el único módulo..." no fija cuándo se cierra la carencia de sldb ni si IR12 espera: obliga a inventar el criterio de parada.

DRY-RUN

Lecturas: TaskDoc y precisiones, filas SV-A14/A15/A16, SV-C01 a SV-C15, SV-D01, SV-J04/J05 y G08, pills, ir.py, compilers, spec_models, notation_style, fixtures y goldens spec2viz-2de1056-*, render_parity.py. Cambios previstos: los renderers y auxiliares, lint_mermaid, schema, render_file, commands, templates y vendor, pyproject (package-data y script) y tests/visual/*. Dependencias: IR11 (compile_ir, IR), sldb.api.notations (load_spec, validate_spec, resolve_view), carencia de sldb (resolve_style, load_palette, NotationError, AnyDiagram, DiagramType, DiagramStoreEnvelope) y spec2viz instalado solo para regenerar goldens. Validaciones futuras: pytest tests/visual, marker parity, prueba de wheel/empaquetado, test_imports y filas de la matriz.

FUTURO

IR13 cita y acredita las filas y evalúa el gate de retiro; IR13d monta src/specir/cli.py, alias y API pública; el desk de sldb exporta lo carente y entonces se retiran las excepciones de test_imports; IR13b consume plantilla y catálogos. Un humano decide las diferencias declaradas y el momento de retirar spec2viz.
