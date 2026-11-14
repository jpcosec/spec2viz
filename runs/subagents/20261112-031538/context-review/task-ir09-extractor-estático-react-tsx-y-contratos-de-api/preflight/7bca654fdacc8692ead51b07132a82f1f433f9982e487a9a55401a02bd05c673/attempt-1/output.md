## REFORMULACION
**Propósito:** extraer estáticamente la interfaz React/TSX para incorporarla al grafo de specIR y vincular controles/acciones con operaciones de API. **Resultado:** módulos `react_tsx.py` y `api_contracts.py`, pruebas y fixture del blog, produciendo nodos y relaciones `triggers`/`invokes` con evidencia de archivo, línea y hash, de forma idempotente. **Repo:** paquete specIR (`src/specir/extract/`, `tests/extract/`, fixture `tests/fixtures/blog_frontend/`). **Límites:** solo análisis estático; no DOM, ejecución dinámica ni generación/modificación de UI; lo no deducible se marca inferido o desconocido. Es una tarea ejecutable, no un agregado.

## AMBIGUEDADES
1. “el analizador de JSX y TSX se elige en la tarea activa”: no se nombra parser ni versión; obligaría a inventar la dependencia y su configuración.
2. “contratos de API disponibles (por ejemplo OpenAPI)”: no se fija formato, ubicación ni prioridad; obligaría a inventar el mecanismo de descubrimiento y parseo.
3. “pobladas a mano o por el extractor de backend”: no se aclara si ese extractor existe o es dependencia; obligaría a inventar el origen de las operaciones.
4. “relación marcada como inferida o un hueco declarado”: no se da criterio para elegir entre ambas; obligaría a inventar la política.
5. “hash del fragmento fuente”: no se especifica algoritmo ni canonicalización; obligaría a inventar el cálculo.
6. “las relaciones extraídas pasan la validación de sus RelationTypeDoc”: no se adjunta el esquema; obligaría a inventar campos y reglas.
7. “store idéntico”: no se define si incluye orden, marcas de tiempo o metadatos; obligaría a inventar el criterio de comparación.

## DRY-RUN
**Lecturas previas:** TaskDoc, pills, tareas IR05/IR06, código existente del store y `RelationTypeDoc`, fixture React y contratos de API. **Cambios previstos:** implementar ambos extractores aislados tras una interfaz; añadir pruebas y ajustar el fixture si falta estructura mínima. **Dependencias:** tipos de dominio de IR06, criterio procedencia/divergencia de IR05, operaciones de API ya presentes en el grafo y parser JSX/TSX. **Validaciones futuras:** pruebas del fixture, evidencia archivo/línea/hash, tratamiento de URL no resuelta y endpoint inexistente, doble ejecución idempotente y validación de RelationTypeDoc. No se ejecuta nada.

## FUTURO
IR05 e IR06 deben entregar criterios y tipos consumibles. Otro nodo o un humano decide el parser concreto, la fuente contractual y el esquema de validación; el extractor de backend o una carga manual puebla las operaciones. La aceptación de relaciones inferidas y brechas queda para revisión humana.
