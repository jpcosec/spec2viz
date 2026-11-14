REFORMULACION
Propósito: que specIR materialice un spec en el store y genere specs de componentes desde un grafo o desde el AST de Python, con resultado equivalente a spec2viz. Resultado: `sync.py`, `graph_import.py`, `generate_python.py` y sus pruebas. Repo: specIR. Límites: fuera catálogos, notaciones/paletas, CLI, migración de consumidores y retiro de spec2viz. Es un nodo de código, no un agregado.

AMBIGUEDADES
1. “según el modo que le asigne la matriz de cobertura”: el nodo no incluye la matriz ni el modo de sincronización, importación de grafo y generación. Obliga a inventar si se migran tal cual o se reemplazan.
2. “el mismo resultado que spec2viz” / “equivalente al de spec2viz”: no define criterio de equivalencia ni normalización. Obliga a inventar comparación de orden, IDs o metadata.
3. “fixtures de sincronización”, “fixture de snapshot de spec2viz”, “paquete Python de fixture”: no da rutas, nombres ni contenido. Obliga a inventar localización y datos.
4. “el índice de aristas valida después de sincronizar”: no nombra API, comando ni criterio de éxito. Obliga a inventar la operación de validación y sus aserciones.
5. “Las pruebas anteriores pasan”: el antecedente no está en el nodo. Obliga a inventar qué suite previa se ejecuta.
6. “borrado de los documentos que salieron del spec”: no aclara si borra RelationDoc entrantes y salientes de nodos eliminados, ni orden o cascada. Obliga a inventar esa semántica.

DRY-RUN
Un ejecutor leería IR13a, la matriz de IR07, compiladores/proyecciones de IR11, la API de SLDB y los fixtures. Cambios previstos: solo los seis archivos de `output_scope`. Dependencias: IR07 para modo y condición; IR11 para IR y proyecciones; SLDB para store e índices. Validaciones futuras: sync contra spec2viz, re-sync con borrado, RelationTypeDoc no builtin e índice, compilación desde grafo/snapshot, generación desde AST y prueba de imports. Sin ejecutar.

FUTURO
IR07 decide el modo por fila y la prueba de equivalencia; IR11 entrega compiladores, proyecciones y normalización; IR13 ejecuta el gate y el acta; el dueño de spec2viz decide archivarlo.
