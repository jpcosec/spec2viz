## REFORMULACION

**Propósito:** dotar a specIR de reglas semánticas entre capas y de un análisis de impacto consultable por MCP, sin escribir en el grafo.

**Resultado:** `layer_rules.yaml` con RuleDoc para cinco brechas (acción sin operación de API, campo de interfaz ausente del serializer, operación sin handler, entidad sin persistencia, política sin representación en interfaz), cada hallazgo con severidad, regla y evidencia; `impact.py` que, dado un nodo, devuelve afectados en otras capas con camino de relaciones y procedencia por tramo; `mcp/impact_tools.py` con tools de solo lectura para reglas e impacto.

**Repo:** specIR, nodo `delivery` de código.

**Límites:** no propone parches ni corrige el grafo; no ejecuta la aplicación; depende de IR06 (tipos y store del blog), IR08 (backend/datos) e IR09 (interfaz).

## AMBIGUEDADES

1. «reglas RuleDoc, distribuidas por specIR como documentos» frente a `src/specir/data/rules.yaml` en IR06: ¿`layer_rules.yaml` sustituye, extiende o duplica las reglas de IR06? Obligaría a inventar la política de convivencia y el destino de instalación.
2. «cada hallazgo con severidad»: no se define escala ni valores. Obligaría a inventar el vocabulario de severidad.
3. «una operación de análisis de impacto… tool MCP de solo lectura para ambas»: ¿una tool combinada o dos? Obligaría a inventar la superficie MCP.
4. «Sobre el grafo completo del blog sin brechas sembradas»: no se dice qué store concreto (el de IR06, el extraído por IR08/IR09, o su unión). Obligaría a inventar el corpus de validación.
5. «Las pruebas anteriores pasan»: no hay pruebas previas definidas en este nodo. Obligaría a inventar qué suite se hereda.

## DRY-RUN

**Lecturas:** `models/domain.py`, `data/relation_types.yaml`, `data/rules.yaml`, `fixtures/blog_chain.yaml`, salidas de IR08/IR09 y `sldb.api`.
**Cambios previstos:** crear los cinco archivos de `output_scope`; las reglas como datos, el motor de brechas y el recorrido de impacto como código, tools MCP delgadas.
**Dependencias:** tipos de relación y procedencia de IR06/IR08/IR09; taxonomía de procedencia ya decidida.
**Validaciones futuras:** ejecutar `tests/rules/test_layer_rules.py` y `tests/test_impact.py`; sembrar cada brecha en un store y comprobar severidad/regla/evidencia; grafo del blog sin hallazgos; consulta `status` → `PublishButton` con camino y procedencia por tramo; comparación del árbol del store antes/después; inspección de que ninguna respuesta incluya parches.

## FUTURO

IR06 aporta tipos y store del blog; IR08 e IR09 producen el grafo extraído y sus marcas de inferencia; un nodo posterior consume estos hallazgos para reporte o UI; un humano decide la escala de severidad y el corpus exacto de validación.
