## REFORMULACION

Propósito: migrar a specIR la compilación de diagramas de spec2viz y la materialización de proyecciones del grafo. Resultado: modelos de spec, carga/validación, representación intermedia (IR) y un compilador por tipo, más proyecciones desde `ViewDoc` y desde `SpecDoc`/`SpecNodeDoc` a la misma IR, con paridad demostrada mediante pruebas portadas. Repo: specIR (`src/specir/visual/`, `tests/visual/`). Límites: fuera renderizado, linter, recursos empaquetados, sincronización al store, catálogos, consumidores y retirada de spec2viz; solo API pública de SLDB, sin mocks ni redefinición del vocabulario visual.

## AMBIGUEDADES

1. «specIR compila todos los tipos de diagrama que compila spec2viz» frente a «los ocho tipos de diagrama compilan». Si spec2viz compilara un tipo no listado, obligaría a inventar si el conjunto de ocho es cerrado o si manda la cobertura real; el input no da el inventario.
2. «Los specs YAML existentes validan en specIR» no enumera cuáles son ni dónde están; obligaría a inventar el corpus de validación.
3. «Cuando spec2viz se retire, el oráculo se sustituye por los resultados guardados de su última ejecución» no dice dónde ni con qué formato se guardan; obligaría a inventar el mecanismo de golden.
4. «proyecciones del grafo del blog» no identifica el grafo, el fixture ni el store de prueba; obligaría a inventar el escenario.

## DRY-RUN

Lecturas: TaskDoc, rituales, pills y átomos adjuntos; matriz de cobertura de IR07; pruebas y fixtures de compiladores de spec2viz como oráculo; API pública de SLDB para modelos y resolvedor de vistas. Cambios previstos: crear o ajustar `spec_models.py`, `loader.py`, `validator.py`, `ir.py`, `compilers.py` y `projections.py`; crear `__init__.py` con exportaciones; portar fixtures y pruebas a `tests/visual/`. Dependencias: IR07 (contrato y modos), IR06 (tipos transversales), SLDB público y spec2viz disponible como oráculo. Validaciones futuras: paridad por tipo, prueba de normalización, errores tipados, proyecciones de componente/estado con `Post`, prueba de imports y ausencia de clases duplicadas. No se ejecuta nada.

## FUTURO

La matriz de IR07 decide el modo por fila y la permanencia del YAML; IR13d extiende `__init__.py`; el gate de retiro y los goldens sustitutos dependen de la retirada de spec2viz; si falta una operación en la API pública de SLDB, un humano decide y la tarea se detiene.
