REFORMULACION

Propósito: que specIR materialice specs en el store y genere specs de componentes desde un grafo o desde el AST de Python, con resultado equivalente a spec2viz. Resultado: `src/specir/visual/sync.py`, `graph_import.py`, `generate_python.py` y sus pruebas. Repo: specIR. Límites: dentro sincronización SpecDoc/SpecNodeDoc/RelationDoc, RelationTypeDoc faltante, borrado de salientes, compilación grafo/snapshot y generación AST; fuera catálogos, notaciones/paletas, CLI, consumidores y retiro de spec2viz.

AMBIGUEDADES

1. “el mismo resultado que spec2viz” / “equivalente al de spec2viz”: no define igualdad (orden, IDs, timestamps, metadata). Obligaría a inventar la normalización de comparación.
2. “borrado de los documentos que salieron del spec”: no acota propiedad ni documentos compartidos. Obligaría a inventar una regla de borrado seguro.
3. “creación del RelationTypeDoc que falte”: no dice qué hacer si existe con esquema distinto. Obligaría a inventar política crear/actualizar/fallar.
4. “generación ... desde el AST de Python”: no enumera constructos ni mapeo a componentes. Obligaría a inventar qué clases, funciones o imports se traducen.
5. “El paquete no importa spec2viz”: no aclara si incluye pruebas de paridad. Obligaría a inventar el límite entre runtime y tests.

DRY-RUN

Lecturas: contrato IR13A, matriz IR07 para modo y condición de filas, salidas de IR11 (IR/compiladores/proyecciones), fixtures de spec2viz, API pública de SLDB y store de prueba. Cambios previstos: sync con upsert/delete y RelationTypeDoc; importador grafo/snapshot; generador AST; pruebas de equivalencia. Dependencias: IR07, IR11, fixtures y store. Validaciones futuras: comparar documentos, resincronizar con borrado, validar índice de aristas, equivalencia grafo/AST y prueba de imports.

FUTURO

IR13 consume la evidencia y ejecuta el gate final; el dueño de spec2viz decide archivarlo. IR07 decide modos y condiciones de retiro. IR11 provee compiladores y proyecciones. Nada de esto se ejecuta aquí.
