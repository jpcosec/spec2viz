REFORMULACION
Nodo de código, no agregado. Propósito: entregar en specIR un servidor MCP de solo lectura por stdio sobre la API pública de SLDB, para que un agente descubra modelos, lea documentos y campos, recorra relaciones, busque por predicados, resuelva vistas e inspeccione integridad. Resultado: tools MCP con JSON estructurado y dirección estable por documento, más pruebas contra una copia aislada del store real y su federación con deskops y spec2viz. Límites: sin escritura, tipos de dominio nuevos, extractores ni renderizado de diagramas. Repo: specIR. Depende de IR01; contrato de vecino no revisado.

AMBIGUEDADES
1. “copia aislada del store real de este repo”, “federación de la copia”, “stores federados de deskops y de spec2viz”: no se definen rutas, composición ni configuración; obliga a inventar layout y montaje.
2. “dirección estable” por documento: no fija formato ni unicidad; obliga a inventar el esquema de direcciones.
3. “Todo conjunto llega paginado, con su total y una marca cuando quedó cortado”: faltan parámetros, límites y forma de la marca; obliga a inventar el contrato de paginación.
4. “búsqueda por predicados” e “integridad del store”: no se especifica lenguaje de predicados ni informe de integridad; obliga a inventar API y salida.
5. “resolver una vista (ViewDoc o SpecDoc) a JSON” y “mismo contenido”: no se define esquema JSON, normalización ni tool; obliga a inventar resolución y comparación.
6. “cliente MCP real” y “servidor real lanzado por stdio”: no se fija versión/capacidades MCP ni comando de arranque; obliga a inventar la integración.
7. “Las pruebas anteriores pasan”: no hay pruebas previas en el input; obliga a inventar cuáles son.

DRY-RUN
Lecturas: IR03, matriz IR01, API pública `sldb.api`, árbol del store y `desk/`, store de spec2viz. Cambios previstos: solo archivos de `output_scope` (`pyproject.toml`, `src/specir/mcp/*`, `tests/*`). Dependencias: IR01, API pública de SLDB, copia aislada y federación, cliente/servidor MCP real. Validaciones futuras: pytest con MCP por stdio; JSON y direcciones; documentos contra `desk/`; paginación en el modelo mayor; SpecDoc `class.sldb-models`; diff de árboles sin escritura; original intacto; vacío explicado; imports permitidos; sin dobles. Sin ejecutar.

FUTURO
IR01 produce la matriz y notifica faltantes a SLDB; SLDB decide si extiende su API. IR04 e IR07 consumen IR03. Un humano valida la disponibilidad del store real/federación y aprueba el contrato MCP si se concreta.
