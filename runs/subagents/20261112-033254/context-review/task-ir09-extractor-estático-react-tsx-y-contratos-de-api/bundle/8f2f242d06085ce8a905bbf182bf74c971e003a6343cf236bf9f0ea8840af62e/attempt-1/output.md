## REFORMULACION
Propósito: que el grafo specIR represente la interfaz y su vínculo con backend sin poblarla a mano. Resultado: un extractor estático en `src/specir/extract/` que, desde código React (JSX/TSX) y contratos API, produce controles, acciones, estados y relaciones `triggers`/`invokes` hacia operaciones del grafo, con archivo, línea y hash por nodo/relación, e idempotente. Repo: specIR (paquete python), fixture `tests/fixtures/blog_frontend/`. Límites: fuera DOM/ejecución, comportamiento dinámico no deducible (se marca inferido o desconocido) y generación/modificación de código UI; solo `sldb.api`, sin mocks, detenerse ante bloqueo. Nodo ejecutable (`task.code`), no agregado.

## AMBIGUEDADES
1. "el analizador de JSX y TSX se elige en la tarea activa": no hay criterio ni candidato; obligaría a inventar la elección (p. ej. tree-sitter vs Babel) y su aislamiento.
2. "contratos de API disponibles (por ejemplo OpenAPI)": formato, versión y ubicación no definidos; obligaría a inventar el parser de contrato.
3. "marcada como inferida o un hueco declarado": la disyuntiva no se resuelve; obligaría a inventar cuándo aplicar cada salida.
4. "con los tipos de la tarea de tipos de dominio": no se cita nombre de tipos ni interfaz de IR06; obligaría a inventar el contrato de importación.
5. "hash del fragmento fuente": algoritmo, granularidad (archivo vs fragmento) y codificación no especificados; obligaría a inventar la evidencia.
6. "la operación de API de publicar": no se nombra el id/RelationTypeDoc exacto; obligaría a inventar identificadores.

## DRY-RUN (hipotético, sin ejecutar)
Lecturas: TaskDoc, rituales execution/testing/closeout, ambas pills, átomos; `package.json` y componentes TSX/JSX del fixture; contrato(s) OpenAPI; operaciones y RelationTypeDocs ya en el grafo (IR05/IR06). Cambios previstos: `react_tsx.py`, `api_contracts.py`, tests `test_react_tsx.py`/`test_api_contracts.py`, `package.json` del fixture. Dependencias: IR05 (procedencia/divergencia), IR06 (tipos transversales), analizador elegido, store SLDB de prueba real, `test_imports.py`. Validaciones futuras: las seis condiciones del TaskDoc sobre el fixture (PublishButton/PublishAction→publicar, evidencia, inferido vs observado, brecha, idempotencia, RelationTypeDoc), más guardrail de imports.

## FUTURO
Decide un humano/otra tarea: analizador JSX/TSX, formato de contratos, taxonomía inferido/brecha, ids y RelationTypeDoc concretos, y provisión del fixture real. IR05 e IR06 entregan procedencia y tipos; el cierre corresponde al ritual closeout.
