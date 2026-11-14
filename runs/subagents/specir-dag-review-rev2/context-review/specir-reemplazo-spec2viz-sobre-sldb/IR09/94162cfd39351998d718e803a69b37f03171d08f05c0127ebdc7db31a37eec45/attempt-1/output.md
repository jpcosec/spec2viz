REFORMULACION

IR09 es un nodo de código (no agregado) del repo specIR. Su propósito es construir un extractor estático de React JSX/TSX y contratos de API que produzca elementos de interfaz del grafo specIR y los vincule a operaciones backend, con evidencia de origen. El resultado esperado son `react_tsx.py`, `api_contracts.py`, sus pruebas y el fixture `blog_frontend/package.json`, capaces de extraer controles, acciones, estados locales, llamadas HTTP y relaciones `triggers`/`invokes`, con archivo, línea y hash, de forma idempotente. Límites: incluye lectura estática y contratos disponibles; excluye DOM, ejecución dinámica, generación/modificación de código y afirmar comportamiento no deducible. Depende de IR05 (taxonomía de procedencia) e IR06 (tipos de dominio, RelationTypeDoc y store del blog).

AMBIGUEDADES

1. “mitad de interfaz de la cadena de publicar un post se obtiene sin poblarla a mano”: no define qué mitad ni el umbral. Obligaría a inventar el criterio de completitud.
2. “fixture del blog”: solo se lista `tests/fixtures/blog_frontend/package.json`, sin componentes TSX/JSX ni contratos. Obligaría a inventar contenido y rutas del fixture.
3. “contratos de API disponibles (por ejemplo OpenAPI)”: no fija formato, versión ni ubicación. Obligaría a inventar descubrimiento y soporte.
4. “hash del fragmento fuente”: no indica algoritmo ni canonicalización. Obligaría a inventar el cálculo.
5. “marcada como inferida o un hueco declarado”: permite dos salidas sin criterio. Obligaría a inventar cuándo usar cada una.
6. “queda registrada como brecha”: no define representación ni documento destino. Obligaría a inventar el esquema de brecha.
7. “store idéntico”: no define identidad, orden ni metadatos. Obligaría a inventar la comparación de idempotencia.

DRY-RUN

Un ejecutor futuro leería IR05, IR06, el fixture y contratos; implementaría extractores y pruebas; ejecutaría las validaciones de aceptación: extracción de PublishButton/PublishAction y su operación, evidencia por nodo/relación, URL no resuelta inferida o hueco, endpoint inexistente como brecha, doble ejecución idéntica y validación contra RelationTypeDoc. No se ejecuta nada aquí.

FUTURO

IR05 decide la taxonomía; IR06 produce tipos, RelationTypeDoc y store; IR10 consume las relaciones extraídas para reglas e impacto; un humano valida ambigüedades y aceptación.
