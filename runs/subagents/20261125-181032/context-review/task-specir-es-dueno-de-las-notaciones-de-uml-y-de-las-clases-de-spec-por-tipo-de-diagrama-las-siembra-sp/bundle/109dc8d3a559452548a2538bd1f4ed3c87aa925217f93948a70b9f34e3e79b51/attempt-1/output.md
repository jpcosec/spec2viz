## REFORMULACION
Encargo del nodo: trasladar a specIR el contenido de las notaciones UML y las clases de spec por tipo de diagrama, sembrarlas mediante `specir.install` en un store y eliminar su importación desde `sldb.models.notation.diagram_specs` y la lectura de `sldb/notations/builtin`. Resultado: store nuevo con notaciones registradas, 38 specs de fixtures válidas y `tests/test_imports.py` sin exenciones para esos módulos. Repo: SLDB_1/IR, con cambios en `src/specir/` y tests. Límites: no borrar nada de sldb, no tocar BPMN ni la notación de capas.

## AMBIGUEDADES
1. «las ocho notaciones viven en sldb/src/sldb/notations/builtin/» frente a «Fuera: ... la notación BPMN, la de capas.»: no se enumeran las ocho ni cuáles quedan; obligaría a inventar el inventario exacto a migrar.
2. «las clases de spec por tipo de diagrama»: no se nombran clases ni correspondencia con tipos; obligaría a inventar el mapeo.
3. «Que ... un store las reciba al instalar specIR en él» y «specir install»: no se define ruta del store, formato ni firma del comando; obligaría a inventar la interfaz de instalación.
4. «Las 38 specs de tests/visual/fixtures validan»: no se listan ni se indica selección; obligaría a asumir que el directorio completo contiene exactamente 38.
5. «la exención de tests/test_imports.py para esos dos módulos se quita»: no se transcribe la exención ni su forma; obligaría a inventar qué entradas eliminar.

## DRY-RUN
Lecturas: ADR `mechanism-in-sldb-content-in-specir.md`, `paridad-por-capacidades.md`, `notations-and-views.md`, `store-declaration.md`; `sldb/src/sldb/notations/builtin/`, `sldb.models.notation.diagram_specs`, `src/specir/visual/spec_models.py`, `notation_style.py`, `install.py`, fixtures y `tests/test_imports.py`. Cambios previstos: incorporar datos y clases a specIR, implementar siembra en install, sustituir importaciones y retirar exenciones. Dependencias: API pública de sldb (`NotationDoc`, `GlyphDoc`, `LinkDoc`, resolver, validar) estable. Validaciones futuras, sin ejecutar: primero `pytest -q tests/test_imports.py tests/test_install.py`, luego `pytest -q`.

## FUTURO
Otro nodo de sldb eliminará los originales después de esta tarea. Un humano decide el destino de BPMN y capas y aprueba el inventario si no consta. El entorno de ejecución debe proporcionar el store y las dependencias para las validaciones.
