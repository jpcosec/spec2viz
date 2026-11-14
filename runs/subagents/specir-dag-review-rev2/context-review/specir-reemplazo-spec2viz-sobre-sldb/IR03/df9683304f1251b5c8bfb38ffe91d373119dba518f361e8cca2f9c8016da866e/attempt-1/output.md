REFORMULACION
Propósito: entregar en specIR un servidor MCP de solo lectura por stdio sobre la API pública de SLDB para descubrir modelos/tipos de relación, leer documentos/campos, recorrer relaciones, buscar por predicados, resolver ViewDoc/SpecDoc e inspeccionar integridad. Resultado: código y pruebas en output_scope (pyproject, src/specir/mcp/*, tests/*). Repo: specIR. Nodo code, no agregado. Límites: nada de escrituras, tipos de dominio nuevos, extractores ni renderizado; no modificar copia ni stores originales; no mocks ni documentos inventados; no importar pron, spec2viz ni SLDB fuera de sldb.api.

AMBIGUEDADES
1. “Las pruebas anteriores pasan”: no hay pruebas previas en el input; obliga a inventar cuáles son.
2. “la copia aislada del store real de este repo” y “federación de la copia”: no define store fuente, cómo se crea/refresca la copia ni configuración federada de deskops/spec2viz; obliga a inventar montaje.
3. “su dirección estable”: no fija esquema ni unicidad; obliga a inventar formato.
4. “el modelo con más documentos del store”: no dice si es original, copia o federado, ni desempate; obliga a elegir.
5. “resolver una vista (ViewDoc o SpecDoc)”: no aclara si ambas son obligatorias; obliga a decidir alcance.
6. “Una consulta sobre algo que el store no declara”: no define qué consulta ni cuándo es vacío frente a error; obliga a inventar criterio.
7. “mismo id y contenido”: no define canonicalización para comparar JSON; obliga a inventar igualdad.

DRY-RUN
Un ejecutor leería el nodo, la matriz de IR01, la API pública de SLDB, la configuración de copia/federación y los archivos existentes en output_scope. Crearía/actualizaría servidor, read_tools, addresses, paging, pyproject y pruebas. Depende de IR01 y de un cliente MCP real. Validaría después: stdio real, JSON estructurado, direcciones, existencia/contenido contra desk/, paginación en el modelo mayor, resolución de class.sldb-models, árbol sin cambios, store original intacto, consulta no declarada con vacío explicado e imports permitidos.

FUTURO
IR01 entrega la matriz de capacidades de la API; IR04 consumirá las tools de lectura; IR07 usará la resolución de vistas. Un humano valida la evidencia y decide si faltan capacidades o configuración del store.
