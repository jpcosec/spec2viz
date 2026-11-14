REFORMULACION
IR10 es un nodo de entrega (`kind: code`) del repo `specIR`. Su propósito es implementar reglas RuleDoc que detecten brechas entre capas y una operación de análisis de impacto expuesta por MCP, de solo lectura, que devuelva elementos afectados con el camino de relaciones y la procedencia de cada tramo. El resultado esperado son `layer_rules.yaml`, `impact.py`, `mcp/impact_tools.py` y las pruebas asociadas. Límites: no propone parches ni cambios de código, no aplica correcciones al grafo y no admite reglas que requieran ejecutar la aplicación.

AMBIGUEDADES
1. “cada hallazgo con severidad”: no se define escala ni valores. Obliga a inventar criterios y niveles de severidad.
2. “Por cada regla hay un store de prueba con la brecha sembrada”: no aclara si es un store por regla o un store con brechas sembradas. Obliga a inventar estructura y aislamiento de fixtures.
3. “tool MCP de solo lectura para ambas”: no fija nombres, entradas, salidas ni formato del camino/procedencia. Obliga a inventar el contrato MCP.
4. “qué partes de la interfaz afecta un cambio en un campo, un endpoint o una regla”: no define cómo se propaga el impacto de una regla. Obliga a inventar dependencias semánticas de reglas.
5. “Cada tramo del camino devuelto lleva su procedencia”: no indica representación ni cómo se marca una relación inferida. Obliga a inventar el esquema de respuesta.

DRY-RUN
Un ejecutor futuro leería el nodo, los contratos de IR06 (modelos, RelationTypeDoc, RuleDoc, store del blog), IR08/IR09 (extractores, procedencia, fixtures) y la interfaz MCP existente. Cambiaría solo los archivos de `output_scope`: reglas, motor de impacto, tools MCP y pruebas. Dependería de IR06 para tipos y reglas base, y de IR08/IR09 para grafos y evidencia. Validaría: brechas sembradas detectadas con severidad/regla/evidencia; grafo del blog sin brechas sin hallazgos; `status` de posts devuelve `PublishButton` con camino completo; procedencia por tramo y marca de inferido; tools sin escritura por comparación del árbol; respuestas sin parches.

FUTURO
IR06, IR08 e IR09 entregan los contratos y grafos que IR10 consume. Otros nodos o un humano validarán la integración, la matriz de cobertura y el gate de retiro; no forma parte de las ambigüedades de IR10.
