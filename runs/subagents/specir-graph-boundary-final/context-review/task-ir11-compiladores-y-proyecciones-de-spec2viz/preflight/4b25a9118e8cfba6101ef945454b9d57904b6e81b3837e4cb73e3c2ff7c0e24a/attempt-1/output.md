REFORMULACION
El encargo es ejecutable (`task.code`), no un agregado. Propósito: migrar a specIR los compiladores y proyecciones de spec2viz. Resultado: compilar los ocho tipos de diagrama —clase, secuencia, estado, componente, actividad, despliegue, matriz y reflexión— desde specs autorados y desde proyecciones del grafo, produciendo una representación intermedia visual propia. Repo: `src/specir/visual/` (`spec_models`, `loader`, `validator`, `ir`, `compilers`, `projections`, `__init__`) y pruebas en `tests/visual/`. Límites: no crear índice/backend genérico, renderizado, linter, recursos, sincronización, catálogos ni retirar spec2viz; consumir store, índice, aristas y recorridos mediante API pública de SLDB; reutilizar el vocabulario visual de SLDB; ningún módulo bajo `src/specir/` importa spec2viz.

AMBIGUEDADES
1. «según el contrato decidido en la tarea de cobertura»: el input no incluye ese contrato. Obligaría a inventar qué se compila desde YAML, qué desde grafo y qué casos quedan fuera.
2. «la diferencia está declarada en la fila correspondiente de la matriz de cobertura con su prueba equivalente»: no se aportan filas ni formato de matriz. Obligaría a inventar el mapeo fixture-diferencia-prueba.
3. «salvo que la decisión de la tarea de cobertura diga otra cosa»: no consta esa decisión sobre errores tipados. Obligaría a inventar equivalencias o excepciones de validación.
4. «proyecciones del grafo del blog»: no se concretan fixtures, identificadores ni grafo disponible. Obligaría a inventar el escenario de Post y su obtención por API.

DRY-RUN
Lecturas: los archivos listados, dependencias IR07/IR06, pills y, como oráculo de pruebas, fixtures de spec2viz. Cambios previstos: modelos, carga/validación, IR, ocho compiladores, proyecciones y pruebas; `__init__.py` se crea aquí y IR13d lo extiende después. Dependencias: API pública de SLDB (`run_view`, `evaluate_projection_view`, `resolve_view`) y spec2viz solo en tests de paridad. Validaciones futuras: paridad estructural normalizada, prueba de normalización, errores tipados, proyecciones del blog, equivalencia spec/proyección, ausencia de clases de vocabulario duplicadas y prueba de imports.

FUTURO
IR13d extiende la API pública; la cadena IR13a/IR12 condiciona su orden. Otro nodo o humano debe aportar el contrato de cobertura, las filas de matriz y la decisión sobre errores. La retirada de spec2viz y la sustitución del oráculo quedan para una fase posterior.
