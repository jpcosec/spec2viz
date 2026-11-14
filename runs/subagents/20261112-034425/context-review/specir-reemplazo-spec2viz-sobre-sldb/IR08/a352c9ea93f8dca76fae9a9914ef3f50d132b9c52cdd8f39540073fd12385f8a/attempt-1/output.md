REFORMULACION
IR08 es un nodo de entrega de tipo `code` en el repo `specIR`. Su propósito es construir un extractor estático de una aplicación Django/DRF y su esquema SQL. El resultado debe ser documentos y relaciones de los tipos de dominio de specIR, con evidencia de archivo, línea y hash, procedencia según la taxonomía de IR05 e idempotencia del store. Límites: dentro, lectura estática de rutas, vistas, serializers, modelos y SQL, y producción de operaciones, handlers, entidades, tablas y relaciones; fuera, frontend, ejecución de la aplicación, reglas de negocio no deducibles, análisis de impacto y parches al código. No es un agregado ni un paquete no ejecutable: es un nodo de implementación.

AMBIGUEDADES
1. “a partir de una aplicación Django REST Framework y su esquema SQL”: no se define formato ni ubicación del esquema SQL. Obligaría a inventar si es un archivo DDL, migraciones o introspección.
2. “lectura estática (AST y metadatos, sin ejecutar la aplicación)”: no se aclara qué metadatos ni si se permite cargar Django/DRF. Obligaría a inventar el alcance real de la lectura estática.
3. “Las pruebas anteriores pasan”: no identifica pruebas previas. Obligaría a inventar cuáles son o asumir una suite no enumerada.
4. “señala los nodos anclados a ese archivo como cambiados”: no define cómo se representa o reporta el cambio. Obligaría a inventar el estado o el formato de salida.

DRY-RUN
Un ejecutor futuro leería la taxonomía de IR05, los tipos y store de IR06, el fixture del blog y las fuentes Django/DRF y SQL. Implementaría los módulos de `output_scope`, sin tocar otros. Dependencias: IR05 e IR06. Validaría con pruebas de fixture, procedencia, idempotencia, detección de cambios, no contaminación de inferidos, RelationTypeDoc/RuleDoc y prohibición de imports fuera de `sldb.api`. No se ejecuta nada.

FUTURO
IR05 entrega la taxonomía canónica; IR06 entrega tipos de dominio y cadena del blog; un humano valida aceptación; IR10 consume el grafo extraído.
