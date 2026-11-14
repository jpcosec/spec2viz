## REFORMULACION
El nodo `task.code` encarga implementar en specIR, en `src/specir/visual/sync.py`, `graph_import.py` y `generate_python.py`: sincronizar un spec al store creando/borrando `SpecDoc`, `SpecNodeDoc`, `RelationDoc` y el `RelationTypeDoc` faltante; compilar un grafo —de store o snapshot— a un spec de componentes; y generar un spec de componentes desde el AST de Python. Debe escribir solo por la API pública de SLDB, no importar spec2viz y demostrar paridad portando pruebas a `tests/visual/`. Fuera: catálogos, notaciones/paletas, CLI, consumidores y retiro de spec2viz. El repo no se nombra explícitamente; las rutas indican `src/specir`. El resultado es que pasen las validaciones y se cumplan las filas de sincronización, grafo y generación de la matriz.

## AMBIGUEDADES
1. «según el modo que le asigne la matriz de cobertura»: no se aporta la matriz; obliga a inventar el modo y el criterio migrar/reemplazar.
2. «con el mismo resultado que spec2viz» y «equivalente al de spec2viz»: faltan versión, fixtures y oráculo de equivalencia; obliga a inventar qué significa equivalencia.
3. «un store de prueba»: no se define su provisión ni configuración; obliga a inventar el entorno.
4. «el índice de aristas valida después de sincronizar»: no se nombra índice ni validador; obliga a inventar la comprobación.
5. «compilación de un grafo de store o de un snapshot»: no se especifica formato ni punto de entrada; obliga a inventar el contrato de entrada.

## DRY-RUN
Sin ejecutar: un ejecutor leería el TaskDoc, los módulos y pruebas listados, las dependencias IR07/IR11, las pills y, si existen, pruebas/fixtures de spec2viz y la matriz. Cambios previstos: implementar los tres módulos y portar pruebas; sincronizar mediante API pública; borrar documentos ausentes; crear `RelationTypeDoc`; compilar grafo/snapshot; generar desde AST. Dependencias: modelos/compiladores de IR11, matriz de IR07, API pública de SLDB y fixtures. Validaciones futuras: paridad de documentos, borrado, tipo de relación e índice, equivalencia grafo y AST, y ausencia de import de spec2viz.

## FUTURO
IR07/IR11 deben entregar matriz y compiladores; un humano decide el modo migrar/reemplazar y acepta la equivalencia; otro nodo o el repo debe aportar fixtures, store de prueba y validador del índice. La tarea no es un agregado: produce código y pruebas.
