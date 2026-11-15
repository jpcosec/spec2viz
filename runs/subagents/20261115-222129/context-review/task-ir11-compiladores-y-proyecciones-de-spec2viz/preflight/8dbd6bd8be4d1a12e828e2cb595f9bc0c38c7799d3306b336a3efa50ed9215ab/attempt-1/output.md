## REFORMULACION
Propósito: migrar a specIR los compiladores y proyecciones de spec2viz, aplicando la decisión YAML/grafo fijada por la tarea de cobertura. Resultado: compiladores para los ocho tipos —clase, secuencia, estado, componente, actividad, despliegue, matriz y reflexión— que producen una representación intermedia visual desde un spec autorado o desde una proyección del grafo, con paridad estructural frente a spec2viz. Repo: specIR, bajo `src/specir` y `tests/visual`; el input no nombra remoto. Límites: dentro, importar de SLDB los modelos de spec y vocabulario visual por API pública, definir la IR y los compiladores, materializar proyecciones con `run_view`, `evaluate_projection_view` y `resolve_view`, portar fixtures/pruebas y crear `src/specir/visual/__init__.py`; fuera, índice/backend, renderizado, linter, recursos, sincronización, catálogos/consumidores y retiro de spec2viz. El nodo es ejecutable (`task.code`), no un agregado.

## AMBIGUEDADES
1. “según el contrato decidido en la tarea de cobertura”: el contrato no está incluido; obligaría a inventar la decisión YAML/grafo y los criterios de la matriz.
2. “los fixtures y pruebas de compiladores de spec2viz se portan”: no se fija versión, ubicación ni formato de “resultados guardados de su última ejecución”; obligaría a inventar el oráculo y su almacenamiento.
3. “Los specs YAML existentes validan en specIR”: no se identifica el corpus ni los errores tipados esperados; obligaría a inventar qué specs y qué errores comparar.
4. “proyecciones del grafo del blog muestran la entidad Post”: no se define el fixture, store ni identidad de Post; obligaría a inventar el grafo del blog.
5. “`run_view`… `evaluate_projection_view`… `resolve_view`”: no se dan firmas ni contratos de retorno; obligaría a inventar la forma exacta de consumo.

## DRY-RUN
Un ejecutor futuro leería el TaskDoc, sus pills, las salidas de IR07, IR06 y D3, la API pública de SLDB, los fixtures/pruebas de spec2viz, los specs YAML y el grafo del blog. Previsto: crear `src/specir/visual/__init__.py`; implementar IR visual, normalización, compiladores y `projections.py`; portar fixtures y pruebas de paridad a `tests/visual/`; añadir pruebas de imports, nombres, normalización, ocho tipos, errores YAML, Post y equivalencia spec/proyección. Dependencias: modelos y API de SLDB, contrato/matriz de IR07, tipos de IR06 y secuencia posterior de IR13d. Validaciones futuras: paridad estructural normalizada, normalización probada, errores tipados equivalentes, Post con un solo documento, ausencia de clases de vocabulario/modelos de spec redefinidas y de imports de spec2viz bajo `src/`. Sin ejecutar nada.

## FUTURO
IR07 decide contrato, matriz, diferencias declaradas y condición de retiro; SLDB/D3 entrega modelos y API; IR06 entrega tipos y cadena de prueba; IR13d extiende `__init__.py`; un humano o CI ejecuta las pruebas y decide el cierre.
