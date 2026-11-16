## REFORMULACION

Propósito: implementar en el repositorio **specIR** un módulo `specir.extract` que no lea código ni use parsers propios, sino que consuma únicamente la API pública de sldb —facts y anclas de `sldb/code`, y `apply_batch` para escritura— y traduzca una aplicación Django/DRF y su esquema SQL Postgres a documentos y relaciones del dominio specIR. Resultado: el grafo de backend y datos del fixture del blog, con procedencia por nodo y relación, idempotente y sin población manual. Límites: fuera quedan lectores/facts/anclas, otros dialectos SQL, frontend, análisis en tiempo de ejecución, reglas no deducibles, análisis de impacto y parches al código; si falta un fact, se solicita a sldb.

## AMBIGUEDADES

1. «los facts y anclas de sldb/code sobre el código del fixture» y «tarea espejo B2»: no se detallan nombres, esquema ni API de esos facts; obligaría a inventar su contrato.
2. «traducida a la taxonomía de la tarea de procedencia»: no se incluye la taxonomía ni la tabla de traducción; obligaría a inventar categorías y correspondencias.
3. «los mismos tipos y relaciones» que pobló la tarea de tipos de dominio: no se enumeran; obligaría a inventar el grafo canónico esperado.
4. «señala los nodos anclados a ese archivo como cambiados»: no define marca, estado ni mecanismo sin borrado; obligaría a inventar su semántica.
5. «deja el store idéntico (comparación del árbol del store)»: no precisa serialización ni normalización; obligaría a inventar el criterio de igualdad.
6. «la del blog de ejemplo, versionada en el repo de specIR»: no indica ruta ni versión exacta; obligaría a elegir el fixture.

## DRY-RUN

Un ejecutor futuro leería este TaskDoc, sus pills, las tareas IR05, IR06 y B2, la documentación pública de `sldb.api` y el fixture. Previsto: crear el módulo de mapeo y pruebas; consumir facts/anclas y escribir mediante `apply_batch`; añadir pruebas de tipos, procedencia, idempotencia, cambio detectado, no-borrado y validación de `RelationTypeDoc`/`RuleDoc`. Dependencias: formato de facts de B2, taxonomía de IR05, tipos de IR06 y dialecto Postgres. Validaciones futuras: ejecutar dos extracciones, comparar store, modificar un archivo y comprobar el grafo y las reglas.

## FUTURO

B2 debe entregar el contrato de readers/facts SQL; IR05, la taxonomía de procedencia; IR06, los tipos y relaciones de dominio. Un humano decide la ruta/versión del fixture y acepta el grafo resultante.
