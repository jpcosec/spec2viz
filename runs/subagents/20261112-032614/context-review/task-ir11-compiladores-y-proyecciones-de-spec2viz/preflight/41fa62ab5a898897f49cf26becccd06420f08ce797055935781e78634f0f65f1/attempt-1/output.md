## REFORMULACION
La tarea IR11, en `/home/jp/proyectos/SLDB_1/IR`, encarga migrar a specIR los compiladores y proyecciones de spec2viz: modelos de spec, carga/validación de ocho tipos de diagrama, representación intermedia, un compilador por tipo y materialización desde ViewDoc y SpecDoc/SpecNodeDoc. El resultado es código y pruebas bajo `src/specir/visual/` y `tests/visual/`, con paridad estructural normalizada frente a fixtures de spec2viz. Límites: no renderizado, linter, recursos empaquetados, sincronización, catálogos, consumidores ni retirada de spec2viz; no redefinir vocabulario visual de SLDB; `src/` no importa spec2viz. No es un agregado: es una tarea ejecutable.

## AMBIGUEDADES
1. «según el contrato decidido en la tarea de cobertura»: el contrato no está en el input; obliga a inventar la decisión spec YAML frente a grafo.
2. «según el modo que le asigne la matriz de cobertura»: no se incluye la matriz ni sus modos; obliga a inventar qué piezas se migran o reemplazan.
3. «los fixtures y pruebas de compiladores de spec2viz»: no hay rutas ni nombres; obliga a inventar su ubicación y formato.
4. «resultados guardados de su última ejecución»: no se define formato, ubicación ni cómo se sustituye el oráculo.
5. «proyecciones del grafo del blog»: no se especifica el grafo, la API ni los fixtures; obliga a inventar cómo obtener Post y su vista.
6. «specs YAML existentes»: no se indica corpus ni ruta; obliga a inventar qué specs validar.
7. «diferencia declarada en la fila correspondiente de la matriz»: no se define el esquema de declaración; obliga a inventar cómo registrarla.

## DRY-RUN
Un ejecutor futuro leería el TaskDoc, las tareas IR06/IR07, las pills, la matriz de cobertura, el código/pruebas de spec2viz y la API pública de SLDB. Crearía los módulos `spec_models.py`, `loader.py`, `validator.py`, `ir.py`, `compilers.py`, `projections.py` y `__init__.py`, portaría fixtures y añadiría pruebas de compiladores, proyecciones, normalización, imports y equivalencia spec/proyección. Dependencias: IR06, IR07, API pública de SLDB y spec2viz solo como oráculo en tests. Validaría después: ocho tipos, equivalencia normalizada, errores tipados, Post sin duplicar store, no importar spec2viz desde `src/` y ausencia de modelos visuales redefinidos. Sin ejecutar nada.

## FUTURO
Otro nodo o humano debe aportar el contrato y los modos de la matriz, la ubicación de fixtures/corpus y el formato del oráculo guardado. IR13d extenderá `__init__.py` después; la matriz determinará el retiro y la aceptación final verificará paridad y condiciones de retiro.
