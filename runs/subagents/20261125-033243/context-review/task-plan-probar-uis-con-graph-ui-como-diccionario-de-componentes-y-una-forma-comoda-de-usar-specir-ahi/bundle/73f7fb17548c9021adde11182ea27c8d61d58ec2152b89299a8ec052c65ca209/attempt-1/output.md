## REFORMULACION
Producir un plan en `desk/drawer/plans/graph-ui-diccionario-de-componentes/` que defina graph_ui como diccionario de componentes para la capa UX de specIR, su generación mediante el extractor React TSX, su uso para probar UIs, una ergonomía de uso y un DAG de tareas pequeñas con `depends_on`. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: solo documentos de planificación; no implementar código.

## AMBIGUEDADES
1. «que prueba lee el diccionario: auto_user_test, flujos, controles esperados»: no se especifica cuál prueba, formato de lectura ni criterio de éxito; obligaría a inventar la prueba concreta.
2. «comando o tool MCP»: no se elige interfaz ni contrato; obligaría a inventar la ergonomía.
3. «anotar que sale y que falta»: falta criterio de completitud del extractor; obligaría a inventar qué se considera faltante.
4. «Decisiones abiertas como task.decision para JP»: no se define esquema ni granularidad; obligaría a inventar el formato de esas decisiones.

## DRY-RUN
Lecturas hipotéticas: README, DESIGN, `auto_user_test` y `src` de `UIs/graph_ui`; `src/specir/extract/react_tsx.py`; `models/domain.py`; rituales y Board. Cambios previstos: crear documentos del plan, inventario, resultados del extractor, propuesta de diccionario/ergonomía, DAG y decisiones. Dependencias: acceso a graph_ui, extractor ejecutable y `/mnt/ssd/tmp/sldb1` escribible. Validaciones futuras: ejecutar el extractor sobre un store temporal, revisar cobertura y ejecutar `ls desk/drawer/plans/graph-ui-diccionario-de-componentes/`. No se ejecuta nada.

## FUTURO
Otro nodo implementará las tareas del DAG; JP resolverá las decisiones abiertas. El cierre dependerá de que el plan exista con inventario, resultado real del extractor, propuesta y DAG.
