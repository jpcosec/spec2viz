## REFORMULACION
IR13b encarga a specIR implementar la capa de catálogos visuales: registro de vistas y stores jerárquicos, construcción de catálogo HTML autocontenido, sincronización al store, validación del registro, servidor local con autoguardado de anotaciones y emparejamiento de átomos —explícito y difuso— con cobertura por vista. El resultado esperado son los módulos y pruebas listados en `output_scope`, con paridad funcional frente a spec2viz y sin importarlo. Repo: `specIR`. Límites: fuera sincronización de un spec individual, notaciones y paletas, CLI y migración de consumidores. No es un nodo agregado: es una entrega de código acotada, aunque dependa de IR13a e IR12.

## AMBIGUEDADES
1. «La validación de un registro de vistas reporta en specIR los mismos errores tipados que spec2viz»: no se enumeran clases, mensajes ni casos; obligaría a inventar el catálogo de errores tipados y su correspondencia.
2. «emparejamiento de átomos con elementos de diagrama (explícito y difuso)»: no se define el criterio difuso ni umbrales; obligaría a inventar algoritmo, puntuación y desempates.
3. «construcción del catálogo HTML autocontenido» y «servidor local con autoguardado de anotaciones»: no aclara si las anotaciones viven en el HTML, en un archivo aparte o en el store; obligaría a inventar formato y ubicación de persistencia.
4. «las filas de catálogo y de emparejamiento de átomos de la matriz de cobertura tienen su condición de retiro cumplida»: la matriz no se incluye; obligaría a inventar qué filas y condiciones aplican.
5. «Las pruebas anteriores pasan»: no se identifican cuáles; obligaría a inventar el conjunto de pruebas heredadas.

## DRY-RUN
Un ejecutor futuro leería el contrato del nodo, los entregables de IR12 (renderers, schema, recursos) e IR13a (sincronización), la estructura actual de `src/specir/visual/`, tests y fixtures de catálogo/átomos. Cambiaría solo los archivos de `output_scope`: `catalog.py`, `catalog_serve.py`, `atoms.py` y sus tres tests. Dependencias: IR12 e IR13a disponibles. Validaría registro con fixtures, sincronización atómica al store de prueba, HTML sin recursos externos, persistencia de anotación tras recarga, paridad de átomos/cobertura y ausencia de import de spec2viz. No ejecutar nada aquí.

## FUTURO
IR13 usará la matriz y el gate para auditar cobertura y dependencias; IR13d expondrá catálogo y átomos por CLI/API; un humano decidirá el retiro de spec2viz tras el acta.
