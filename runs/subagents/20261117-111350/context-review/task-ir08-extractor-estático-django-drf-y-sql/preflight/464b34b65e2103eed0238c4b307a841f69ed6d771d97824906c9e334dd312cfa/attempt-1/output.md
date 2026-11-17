REFORMULACION
Propósito: extraer, sin leer código, el dominio backend/datos de una app Django REST Framework y su SQL Postgres a partir de los facts genéricos de `sldb.api.code.code_facts`. Resultado: documentos y relaciones de los tipos de dominio de specIR —rutas, viewsets, handlers, serializers, modelos, estados, tablas y claves— con procedencia por nodo/relación e idempotencia. Repo: specIR, módulo `src/specir/extract` (según rutas y validaciones). Límites: solo API pública de sldb y `write_anchor`/`apply_batch`; prohibido tree-sitter, ast, regex sobre fuentes, pglast directo, otros dialectos y frontend; si falta un fact, se pide a sldb y se detiene. Es una tarea `task.code` ejecutable, no un agregado.

AMBIGUEDADES
1. “documentos y relaciones de los tipos de dominio de specIR” y “traducida a la taxonomía de la tarea de procedencia”: no enumera tipos, campos ni correspondencia; obligaría a inventarlos si no se leen IR05/IR06.
2. “sin borrar hechos validados por una persona”: no define cómo detectarlos ni preservarlos; obligaría a inventar una política de merge.
3. “sldb mínimo en origin main: C1, C2 y C5 en 3dc9a526, C4 en 691a0e89 y C3 de Python en ad6f8842”: no aclara qué artefactos son C1–C5 ni cómo comprobarlos; obligaría a inventar el criterio.
4. “governed_by por can_publish”: no indica de qué fact, archivo o convención sale esa relación; obligaría a inventar la regla.

DRY-RUN
Lecturas: TaskDoc, salidas de IR05/IR06, API pública de sldb, fixture `tests/fixtures/blog_app` en `ad51a0f` y pills. Cambios previstos: crear `specir.extract` con tabla de reglas Django/DRF sobre facts; consumir `code_facts`, `write_anchor` y `apply_batch`; añadir extra `postgres` y pruebas. Dependencias: versiones sldb indicadas, extra postgres y fixture. Validaciones futuras: cadena del blog, claves SQL, procedencia, idempotencia, cambio en copia temporal, no inferidos como observados, RelationTypeDoc/RuleDoc, grep prohibido, pytest y `deskops graph missing`. Sin ejecutar nada.

FUTURO
IR09/IR10 consumen el mapeo; el desk de sldb recibe solicitudes si falta un fact; un humano valida procedencia inferida y conflictos de merge; IR05/IR06 entregan taxonomía y tipos.
