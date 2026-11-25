## REFORMULACION
**Propósito:** dar al agente coherencia entre capas: detectar brechas y explicar qué se rompe al cambiar un campo, endpoint o regla. **Resultado:** reglas RuleDoc de dominio evaluadas con el motor de sldb y una operación de impacto de solo lectura sobre `graph_path`/`graph_paths`, expuesta como extensión de sldb mcp, con evidencia y procedencia por tramo. **Repo:** solo specIR. **Límites:** no recorrer el grafo en specIR, no proponer parches, no escribir en el store, no ejecutar la aplicación; las carencias generales se piden a SLDB. No es un agregado: es una tarea de código ejecutable cuando sus dependencias estén satisfechas.

## AMBIGUEDADES
1. “Por cada regla hay un store de prueba con la brecha sembrada”: no se define ubicación, formato ni fixture; obligaría a inventar el store y el sembrado.
2. “Sobre el grafo completo del blog sin brechas sembradas”: no se identifica qué blog ni qué store concreto; obligaría a elegir un fixture no especificado.
3. “tool de solo lectura para ambas, registrada como extensión de sldb mcp”: faltan nombre, esquema de entrada/salida y punto de registro; obligaría a inventar el contrato de la tool.
4. “Dado el campo status de la tabla de posts, la operación de impacto devuelve PublishButton”: no se explicita el mapeo entre nodos de dominio y tipos afectados; obligaría a inventar esa correspondencia.
5. “cada hallazgo con severidad”: no se definen niveles ni criterio; obligaría a inventar la escala.

## DRY-RUN
**Lecturas:** TaskDoc, rituales execution/testing/closeout, pills y átomos; contratos públicos de `sldb.api` para reglas y `graph_path`/`graph_paths`; tarea espejo B3; registro MCP existente; fixtures del blog. **Cambios previstos:** documentos RuleDoc, tool de impacto de solo lectura y pruebas; sin tocar otros repos. **Dependencias:** IR06, IR08, IR09 y B3; solo API pública; sin mocks. **Validaciones futuras:** las seis de Validation, incluida ausencia de escritura y de parches.

## FUTURO
B3 entrega `graph_path`/`graph_paths`; IR06/IR08/IR09 entregan tipos y extractores; el desk de SLDB resuelve carencias del lenguaje o recorrido; un humano valida evidencia, cierre y commit.
