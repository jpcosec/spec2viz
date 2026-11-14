## REFORMULACION

El nodo task-ir10 es tarea de código ejecutable (no agregado), draft, ritual-execution. Propósito: detectar brechas entre capas y explicar el impacto de un cambio. Resultado: reglas RuleDoc como documentos con severidad, regla y evidencia, y una operación MCP de solo lectura que, dado un nodo, devuelve afectados con camino y procedencia. Repo: solo specIR (`src/specir/...` y `tests/...`). Límites: no editar otros repos; solo `sldb.api`; sin mocks ni datos fabricados; no proponer parches ni modificar el grafo; no ejecutar la aplicación; si falta capacidad general de SLDB, pedirla por su desk y detenerse.

## AMBIGUEDADES

1. "el lenguaje de reglas de SLDB": sin API, versión ni forma de evaluación; inventar módulo/firma.
2. "tool MCP de solo lectura para ambas": sin nombres, esquema ni errores; inventar contrato.
3. "cada tramo del camino devuelto lleva su procedencia": sin taxonomía ni formato; inventar estructura y valores.
4. "store de prueba con la brecha sembrada": no distingue fixture real de store sembrado y choca con "sin datos fabricados"; inventar criterio.
5. "cada hallazgo con severidad": sin escala; inventar niveles.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout, tres pills, tres átomos y los cinco archivos listados. Cambios previstos: reglas en `layer_rules.yaml`; recorrido en `impact.py`; tools en `mcp/impact_tools.py`; pruebas en `tests/rules/test_layer_rules.py` y `tests/test_impact.py`. Dependencias: API pública de reglas y recorrido de SLDB; salidas de ir06, ir08 e ir09. Si falta API, mensaje al desk SLDB y parada. Validaciones futuras: prueba por regla con brecha sembrada; grafo del blog sin hallazgos; caso `status` → `PublishButton`; procedencia por tramo; no escritura comparando el árbol; ausencia de parches. Sin ejecutar.

## FUTURO

Otros nodos producen ir06/ir08/ir09 y el store del blog; el desk de SLDB puede aportar la API faltante. Un humano decide, si no se fija antes, taxonomía de severidad, contrato MCP y formato de camino/procedencia. El ritual de fase valida la integración; closeout actualiza tablero y commit.
