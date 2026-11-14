## REFORMULACION
El encargo es un nodo ejecutable `task.code` de specIR: definir reglas RuleDoc que detecten brechas entre capas y una operación de análisis de impacto, expuesta por MCP en solo lectura, devolviendo nodos afectados, caminos de relaciones y procedencia de cada tramo. Resultado esperado: `layer_rules.yaml`, `impact.py`, `impact_tools.py` y pruebas asociadas. Repo: no se explicita ruta; las rutas apuntan a `src/specir`, pero el root no queda confirmado. Límites: no proponer parches ni cambios de código, no corregir el grafo, no ejecutar la aplicación; si el lenguaje de reglas no alcanza, la carencia se resuelve en SLDB, no con lógica paralela en specIR. Depende de ir06, ir08 e ir09.

## AMBIGUEDADES
1. “src/specir/impact.py”: no se declara repo/root; obligaría a inventar la ruta de trabajo.
2. “cada hallazgo con severidad”: no define niveles ni criterio; obligaría a inventar la escala.
3. “el camino de relaciones que lo explica y la procedencia de cada tramo”: no fija esquema, orden ni formato; obligaría a inventar el contrato de respuesta.
4. “un store de prueba con la brecha sembrada”: no indica formato ni ubicación; obligaría a inventar el fixture.
5. “el grafo completo del blog” y “el campo status de la tabla de posts”: no da identificadores ni fixture; obligaría a inventar nombres y datos.
6. “Si el lenguaje de reglas no alcanza”: no establece criterio de insuficiencia; obligaría a inventar el umbral para escalar a SLDB.

## DRY-RUN
Lecturas previstas: TaskDoc, pills, archivos listados, salidas de ir06/ir08/ir09 y API pública de SLDB. Cambios previstos: crear/ajustar reglas, operación de impacto, tools MCP y pruebas. Dependencias: tipos de dominio y cadena del blog, extractores Django/DRF/SQL y React/TSX/contratos. Validaciones futuras: brecha sembrada por regla; blog limpio sin hallazgos; `status` afecta `PublishButton` con camino completo; procedencia por tramo e inferidas señaladas; árbol del store sin cambios; ausencia de parches. Nada se ejecuta aquí.

## FUTURO
Un nodo ejecutor implementará reglas, impacto, tools y pruebas. Si falta capacidad, se pedirá por el desk de SLDB. Un humano confirmará repo, severidades y contrato de respuesta si no están fijados. Un validador ejecutará las pruebas y comprobará el cierre.
