REFORMULACION
Propósito: trasladar a specIR la propiedad de las notaciones UML y de las clases de spec por tipo de diagrama, sembrarlas al instalar specIR y dejar de importarlas desde sldb. Resultado: un store nuevo recibe las notaciones mediante `specir install`; las 38 specs de `tests/visual/fixtures` validan; ningún módulo de specIR importa `sldb.models.notation.diagram_specs` ni lee `sldb/notations/builtin`; se elimina la exención correspondiente en `tests/test_imports.py`. Repo: no declarado explícitamente; el alcance nominal es `src/specir/` y `tests/test_imports.py`, usando `sldb/docs/...` y `sldb.api` como fuente de mecanismo. Límites: dentro, datos de notación, clases de spec, `install.py`, `visual/spec_models.py`, `visual/notation_style.py` y `tests/test_imports.py`; fuera, borrar de sldb, BPMN y notación de capas. Es una tarea de código, no un agregado.

AMBIGUEDADES
1. “las ocho notaciones” y “las clases de spec por tipo de diagrama”: no se enumeran; obliga a inventar cuáles son y su correspondencia exacta.
2. “specir install deja las notaciones registradas”: no se fija comando/API ni store de prueba; obliga a inventar invocación y fixture.
3. “la exención de tests/test_imports.py para esos dos módulos se quita”: no se indica formato ni ubicación; obliga a inventar la edición.
4. “Las 38 specs de tests/visual/fixtures validan contra las clases de specIR”: no se define el criterio/harness de validación; obliga a inventar cómo comprobarlo.

DRY-RUN
Lecturas previstas: TaskDoc; `sldb/docs/architecture/notations-and-views.md` y `store-declaration.md`; `sldb/notations/builtin/`; `sldb.models.notation.diagram_specs`; módulos visuales de specIR; tests y fixtures citados. Cambios previstos: incorporar datos y clases en `src/specir/`, sembrar en `install.py`, sustituir imports exentos, retirar la exención y ajustar tests. Dependencias: API pública de sldb, store de prueba y fixtures. Validaciones futuras: ejecutar los dos `pytest` indicados, instalar en store nuevo, comprobar `sldb notations validate` y verificar por inspección que no queden imports ni lecturas prohibidas. Sin ejecutar nada.

FUTURO
Un nodo ejecutor implementará y correrá validaciones; una tarea posterior de sldb borrará los originales; un humano o nodo de aceptación confirmará raíz, entorno y cumplimiento del ADR.
