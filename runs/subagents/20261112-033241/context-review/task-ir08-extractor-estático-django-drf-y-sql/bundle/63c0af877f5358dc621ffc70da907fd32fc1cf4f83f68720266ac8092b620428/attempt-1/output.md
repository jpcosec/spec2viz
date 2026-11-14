REFORMULACION

Encargo: ejecutar la tarea `task.code` IR08, no un agregado. Propósito: que el grafo de specIR se pueble desde código Django/DRF y SQL existente, sin ejecutar la aplicación. Resultado: módulo extractor estático en `src/specir/extract/` y pruebas en `tests/extract/`, con nodos y relaciones tipados y procedencia por archivo, línea y hash. Repo: specIR, con fixture real del blog en `tests/fixtures/blog_backend/`. Límites: solo lectura estática; fuera frontend, runtime, reglas de negocio no deducibles, análisis de impacto y parches; solo `sldb.api`, sin `pron`, `spec2viz` ni internos de SLDB; sin mocks ni datos fabricados.

AMBIGUEDADES

1. “la taxonomía decidida en la tarea de procedencia” y “taxonomía canónica”: el input no incluye esa taxonomía; obligaría a inventar valores y reglas de procedencia.
2. “las mismas operaciones validadas que la superficie MCP de escritura”: no se enumeran operaciones concretas; obligaría a inventar el contrato de escritura.
3. “si la tarea de procedencia lo decide así”: decisión condicional ausente; obligaría a elegir por adelantado si usar anclas de SLDB.
4. “los mismos tipos y relaciones” que pobló a mano la tarea de tipos de dominio: faltan esos tipos y la cadena exacta; obligaría a inventar el modelo esperado.
5. “señala los nodos anclados a ese archivo como cambiados, sin borrar hechos validados”: no se define representación de “cambiado” ni de hecho validado; obligaría a inventar estados y mecanismo.
6. “hash del fragmento fuente”: no se fija algoritmo ni canonicalización; obligaría a elegir uno.

DRY-RUN

Lecturas: TaskDoc, rituales enrutados, pills y átomos, artefactos de IR05/IR06, fixture del blog, documentación de `sldb.api`, RelationTypeDoc y RuleDoc. Cambios previstos: implementar `provenance.py`, `django_drf.py`, `sql_schema.py`, `__init__.py` y pruebas. Dependencias: taxonomía y anclas de IR05; tipos y cadena de IR06; API pública de SLDB; fixture real; documentos de validación. Validaciones futuras: extraer el fixture y comparar con la cadena manual; comprobar procedencia por nodo/relación; doble extracción con store idéntico; modificar fuente y verificar marcado sin borrar validados; impedir inferidos como observados/validados; validar RelationTypeDoc/RuleDoc; comprobar imports permitidos. Sin ejecutar nada.

FUTURO

IR05 decide taxonomía, anclas y estados. IR06 aporta tipos y cadena de referencia. El desk de SLDB añade operaciones públicas faltantes. Un humano resuelve bloqueos, aprueba validaciones y cierra/commit.
