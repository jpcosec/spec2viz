REFORMULACION  
IR09 es un encargo de código (delivery) en el repo specIR: construir un extractor estático de React JSX/TSX y contratos de API que produzca controles, acciones, estados y relaciones `triggers`/`invokes` hacia operaciones de backend, con evidencia de archivo, línea y hash, e idempotencia. Resultado: `src/specir/extract/react_tsx.py`, `src/specir/extract/api_contracts.py`, sus pruebas y el `package.json` del fixture. Límites: no observar DOM/eventos ni comportamiento dinámico no deducible —se marca inferido o desconocido—; no generar ni modificar código de interfaz.

AMBIGUEDADES  
1. “Las pruebas anteriores pasan sobre el fixture y la mitad de interfaz…” no define qué pruebas son “anteriores” ni qué parte de la interfaz es “la mitad”. Obligaría a inventar el conjunto de pruebas y el alcance esperado de la extracción.  
2. “controles, acciones (handlers de eventos), estados locales declarados” no precisa qué elementos, eventos ni APIs de estado se soportan. Obligaría a inventar el subconjunto sintáctico reconocido.  
3. “contratos de API disponibles (por ejemplo OpenAPI)” no fija formato, versión ni ubicación. Obligaría a inventar los contratos soportados y su descubrimiento.  
4. “una relación marcada como inferida o un hueco declarado” no da criterio para elegir entre ambas salidas. Obligaría a inventar la regla de decisión y la representación del hueco.  
5. “hash del fragmento fuente” no especifica algoritmo ni límites del fragmento. Obligaría a inventar el cálculo y su granularidad.  
6. “deja el store idéntico” no define identidad: orden, marcas de tiempo, normalización. Obligaría a inventar el criterio de comparación.

DRY-RUN  
Un ejecutor futuro leería el fixture del blog, los contratos de API y las salidas de IR05/IR06; implementaría el parser, la resolución de llamadas y la emisión de nodos/relaciones con evidencia; añadiría pruebas. Dependencias: tipos de dominio, RelationTypeDoc y taxonomía de procedencia. Validaría: fixture, evidencia por nodo/relación, URL no resuelta, endpoint inexistente como brecha, doble ejecución idéntica y validación RelationTypeDoc. Sin ejecutar nada.

FUTURO  
IR06 aporta tipos, RelationTypeDoc y store; IR05, la taxonomía de procedencia; IR10 consumirá el grafo y las brechas para reglas e impacto. Un humano decide los criterios de las ambigüedades y la aceptación final.
