## REFORMULACION
Propósito: completar IR13a dentro de specIR, materializando specs en el store de SLDB y generando specs de componentes desde un grafo y desde el AST de Python, con paridad demostrada frente a spec2viz. Resultado: módulos `sync.py`, `graph_import.py` y `generate_python.py`, más pruebas portadas en `tests/visual/`, sin importar spec2viz ni módulos internos de SLDB. Repo: specIR (rutas `src/specir/` y `tests/`). Límites: dentro, sincronización, borrado derivado, RelationTypeDoc faltante, compilación desde grafo/snapshot y generación desde AST; fuera, catálogos, notaciones y paletas, CLI, consumidores y retiro de spec2viz. Depende de IR07 e IR11 y usa solo `sldb.api`.

## AMBIGUEDADES
1. “los mismos SpecDoc, SpecNodeDoc y RelationDoc que spec2viz sobre los fixtures de sincronización”: no se nombran rutas ni golden concretos; obligaría a inventar qué fixtures y comparaciones exactas usar.
2. “según el modo que le asigne la matriz de cobertura”: la matriz no está en el bundle; obligaría a inventar si cada pieza se migra tal cual o se reemplaza.
3. “o su reemplazo por proyección tiene la prueba equivalente declarada en la matriz”: no se define cuándo elegir reemplazo ni el criterio de equivalencia; obligaría a inventar la decisión y la prueba.
4. “un paquete Python de fixture”: no se identifica el paquete; obligaría a inventar el insumo de generación desde AST.

## DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout, pills, átomos, módulos existentes, pruebas y fixtures de spec2viz como referencia de solo lectura, y matriz de cobertura si está disponible. Cambios previstos: implementar sincronización y borrado sobre la API pública, importación de grafo y generación AST; portar pruebas y fixtures reales. Dependencias: compiladores/modelos de IR11, filas de IR07, store SLDB de prueba real y API pública suficiente. Validaciones futuras: las seis de la sección Validation, ejecutadas primero sobre pruebas focalizadas y luego sobre la suite visual; `tests/test_imports.py` para dependencias. Sin ejecución.

## FUTURO
IR11 debe entregar compiladores y modelos utilizables. IR07 debe aportar la matriz con modo y condición de retiro por fila. SLDB debe proveer cualquier operación general faltante. Un humano o nodo de cierre valida paridad, actualiza la matriz y decide el avance; otro nodo posterior migra consumidores, CLI y retiro de spec2viz.
