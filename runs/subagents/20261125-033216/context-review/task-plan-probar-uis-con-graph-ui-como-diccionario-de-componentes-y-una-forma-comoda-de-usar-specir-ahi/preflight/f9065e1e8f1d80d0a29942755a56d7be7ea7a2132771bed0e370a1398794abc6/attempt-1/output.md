## REFORMULACION
**Propósito:** planificar —solo documentación— cómo probar UIs usando `graph_ui` como diccionario de componentes y definir una ergonomía de specIR en ese contexto.
**Resultado:** un plan en `desk/drawer/plans/graph-ui-diccionario-de-componentes/` que contenga: qué componente de `graph_ui` corresponde a qué nodo de la capa UX de specIR; cómo se genera el diccionario con el extractor React de specIR; qué prueba lo consume; la ergonomía (comando o tool MCP); un DAG de tareas con `depends_on`; y decisiones abiertas como `task.decision` para JP.
**Repo:** árbol SLDB_1, cwd `IR/`; las rutas `UIs/graph_ui` y `src/specir/...` se citan relativas a una raíz no declarada.
**Límites:** solo plan; fuera de alcance el código. Lecturas limitadas a `graph_ui` (README, DESIGN, `auto_user_test`, `src`) y al extractor/modelos de specIR. Salida únicamente en el drawer.

## AMBIGUEDADES
1. «UIs/graph_ui, jpcosec/graph_ui» — no se declara la raíz del repo; obligaría a inventar la ruta absoluta.
2. «src/specir/extract/react_tsx.py y models/domain.py» — la ubicación de `models/domain.py` es ambigua; obligaría a inventarla.
3. «como diccionario de componentes» — no define granularidad ni esquema del mapeo; obligaría a inventar el formato.
4. «una forma comoda de usar specIR ahi» — «cómoda» no es criterio medible; obligaría a inventar el criterio de aceptación.
5. «que prueba lee el diccionario: auto_user_test, flujos, controles esperados» — no aclara si se propone modificar `auto_user_test` o solo consumirlo; obligaría a inventar el alcance.
6. «store temporal bajo /mnt/ssd/tmp/sldb1» — no indica comando ni procedimiento; obligaría a inventar la invocación del extractor.
7. «DAG de tareas chicas con depends_on» — «chicas» solo se acota con «menos de 2 h»; el esquema de `depends_on` no se define; obligaría a inventarlo.
8. «Decisiones abiertas como task.decision para JP» — no especifica formato ni campos; obligaría a inventarlos.
9. «Un plan en desk/drawer/plans/graph-ui-diccionario-de-componentes/» — no fija nombres ni estructura de archivos; obligaría a inventarlos.

## DRY-RUN
Sin ejecutar nada: un ejecutor futuro leería README, DESIGN, `auto_user_test` y `src` de `graph_ui`; `react_tsx.py` y `models/domain.py`. Redactaría los documentos del plan en el drawer (inventario, salida real del extractor, propuesta de diccionario y ergonomía, DAG, decisiones). Dependencias: acceso a esas rutas, store temporal escribible y extractor ejecutable. Validación futura: `ls` del directorio y revisión de que el plan contiene todas las piezas de «Done When».

## FUTURO
JP resuelve las `task.decision`; los nodos del DAG implementarán código y tests; la corrida del extractor aporta la salida real; la validación final confirma la existencia del plan.
