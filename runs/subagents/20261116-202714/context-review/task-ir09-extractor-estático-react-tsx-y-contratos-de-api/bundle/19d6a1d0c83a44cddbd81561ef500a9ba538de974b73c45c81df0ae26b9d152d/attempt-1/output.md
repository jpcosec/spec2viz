## REFORMULACION

Encargo: implementar en specIR un mapeo de dominio, no un analizador, que convierta facts y anclas del reader de frontend de SLDB —TS, TSX y JS/React— en elementos de interfaz del grafo, relaciones `triggers`/`invokes` y vínculos con operaciones de API, con evidencia de archivo, línea y hash e idempotencia. Resultado: el fixture React del blog produce `PublishButton`, `PublishAction` y su vínculo con la operación de publicar, usando los tipos de dominio. Límites: solo API pública de SLDB; sin leer/analizar TS, TSX o JS; sin observación dinámica; sin inventar operaciones; sin extractores propios; si falta un fact/reader, pedirlo a SLDB y detenerse si bloquea. Depende de B2, IR05 e IR06.

## AMBIGUEDADES

1. “con los tipos de la tarea de tipos de dominio”: no se nombran los tipos concretos de `PublishButton`/`PublishAction`. Obligaría a inventar nombres y esquema; debe tomarlos del resultado de IR06.
2. “una relación marcada como inferida o un hueco declarado”: no se define cómo se representa el hueco ni qué vocabulario de procedencia usar. Obligaría a inventar un nodo/relación o estados no especificados.
3. “las operaciones validadas de escritura de sldb”: no se identifican las operaciones concretas de la API pública. Obligaría a inventar llamadas si no se consultan docs/código de SLDB.
4. “Si un reader o un fact no existe en sldb, se pide por el desk de sldb y no se reimplementa”: no aclara si IR09 se detiene, queda bloqueada o avanza parcialmente. Obligaría a inventar la política de bloqueo.

## DRY-RUN

Un ejecutor futuro leería TaskDoc, rituales, pills, átomos, fixture del blog, tipos de IR06, criterios de IR05, documentación de la API pública de SLDB y operations existentes. Crearía el módulo de mapeo en `specir.extract` y pruebas contra store SLDB real y fixture real; no tocaría módulos internos de SLDB ni añadiría parser TS/TSX/JS. Dependencias: facts/anclas de B2, tipos de IR06, procedencia/divergencia de IR05 y operaciones de API ya pobladas. Validaría: `PublishButton`/`PublishAction`; mismo código para `.ts`, `.tsx`, `.js`; anclas archivo/línea/hash; URL no resuelta como inferida o hueco; endpoint ausente como brecha; doble ejecución idempotente; validación de `RelationTypeDoc`. Sin ejecutar nada.

## FUTURO

B2 debe entregar reader/facts y fixture; IR06, los tipos; IR05, criterios de procedencia/divergencia. Un humano decide si falta un reader (detener y pedir a SLDB) y autoriza cierre/commit tras validación e integración de fase.
