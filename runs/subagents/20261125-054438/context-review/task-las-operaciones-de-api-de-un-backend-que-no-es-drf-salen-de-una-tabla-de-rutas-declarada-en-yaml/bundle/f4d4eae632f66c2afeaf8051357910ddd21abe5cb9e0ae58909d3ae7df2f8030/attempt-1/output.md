## REFORMULACION
**Propósito:** que un backend no DRF (graph_ui) produzca `ApiOperationDoc` desde una tabla de rutas YAML declarada, para que `extract_frontend` enlace `invokes`.  
**Resultado:** nuevo `src/specir/extract/routes.py` con `extract_routes(yaml_path, store)`, exportado en `specir.extract.__all__`; escritura idempotente vía `write_plan`; validación de `method`/`route`; rechazo de colisión con `ApiOperationDoc` de otro origen; reporte de declaradas obsoletas (`stale_declared`); docstring/asserts de `Planned.payload` admitiendo `declarado`; tests `(a)-(f)` y `test_frontend_extraction.py`. Opcional: comando `specir ux routes`.  
**Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`.  
**Límites:** fuera T6 (envoltorios HTTP) y el YAML real de graph_ui; no se ejecuta nada aquí.

## AMBIGUEDADES
1. «extract_routes lista en su reporte (campo nuevo, p. ej. stale_declared)»: no se define tipo ni forma del reporte; obligaría a inventar el contrato de retorno y el nombre exacto del campo.
2. «error legible si no»: para `route` inválida no se fija excepción ni formato; obligaría a inventar tipo de error y mensaje, salvo que se reutilice `ValueError`.
3. «Planned admite origen 'declarado' solo para entradas sin facts escritas por extract_routes»: no se define qué son “facts” ni cómo comprobar su ausencia; obligaría a inventar la condición y el assert.
4. «si T2 ya trajo el grupo ux (si no, solo la funcion)»: el input no dice si T2 existe; obligaría a decidir el estado de T2 o inventarlo, aunque puede resolverse leyendo el repo.

## DRY-RUN
**Lecturas:** TaskDoc y rituales; `django_drf.py:221`, `extract/__init__.py:56`, `plan.py:53`, `write_plan` y tests existentes.  
**Cambios previstos:** crear `routes.py`; exportar la función; añadir comando solo si existe el grupo `ux`; ajustar docstring/asserts de `Planned`; crear `tests/extract/test_declared_routes.py` con `(a)-(f)`.  
**Dependencias:** API de `store`/`write_plan`, comportamiento de `extract_frontend`, estado de T2 y formato real del YAML.  
**Validaciones futuras:** ejecutar exactamente el pytest indicado sobre `test_declared_routes.py` y `test_frontend_extraction.py`; comprobar idempotencia, colisión, obsoletas y enlace de `invokes`.

## FUTURO
T2 determina si existe `specir ux routes`. graph_ui aporta el YAML real. T6 define la regla de envoltorios HTTP. Un humano decide aceptación, cierre y commit.
