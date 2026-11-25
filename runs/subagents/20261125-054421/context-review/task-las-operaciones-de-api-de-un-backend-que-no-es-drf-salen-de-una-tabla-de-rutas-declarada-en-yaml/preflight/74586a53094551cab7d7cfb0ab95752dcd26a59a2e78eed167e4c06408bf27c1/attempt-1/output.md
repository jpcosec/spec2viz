## REFORMULACION
Encargo ejecutable `task.code` en repo `/mnt/ssd/proyectos/SLDB_1/IR`: crear `src/specir/extract/routes.py` con `extract_routes(yaml_path, store)`, que lea una tabla YAML `routes` (`method`, `route`, `title` opcional), valide y escriba un `ApiOperationDoc` por entrada con origen `declarado`, de forma idempotente, para que `extract_frontend` enlace `invokes`. Incluye exportarla en `specir.extract.__all__`, el comando `specir ux routes` solo si T2 ya trajo el grupo `ux`, y tests (a)-(f). También debe ajustar el docstring de `Planned.payload` para admitir `declarado` únicamente en entradas de `extract_routes`, rechazar choques de nombre con documentos de otro origen y reportar declaradas obsoletas sin borrarlas. Límites: fuera T6 (envoltorios HTTP) y el YAML real de graph_ui.

## AMBIGUEDADES
1. “el comando 'specir ux routes' si T2 ya trajo el grupo ux (si no, solo la funcion)”: el input no indica el estado de T2; obliga a inventar si el grupo existe o a inspeccionar fuera del input.
2. “Planned('ApiOperationDoc', node_name(...), {title, method, route}, 'declarado', ...)”: los argumentos restantes y la firma exacta quedan elididos; obliga a inventar parámetros y el contrato de `write_plan`.
3. “(d) ... enlaza invokes si los facts lo permiten, o el test deja constancia del no derivado esperado”: no fija el criterio observable; obliga a inventar qué resultado cuenta como aprobado.
4. “campo nuevo, p. ej. stale_declared”: no define nombre, tipo ni estructura exactos del reporte; obliga a inventar el esquema.

## DRY-RUN
Lecturas previstas: `django_drf.py:221`, `extract/__init__.py:56`, `plan.py:53`, tests de frontend y, si existe, el grupo `ux`. Cambios previstos: nuevo `routes.py`, exportación pública, docstring/assert de `Planned.payload`, tests (a)-(f) y, condicionado a T2, comando `ux routes`. Dependencias: API real de `Planned`, `node_name`, `write_plan` y consulta del store. Validación futura: ejecutar el pytest indicado y comprobar idempotencia, choque, obsoletas y enlace/no derivación.

## FUTURO
El ejecutor produce código, exportación, reporte y tests; un humano decide la interpretación de T2 y el criterio exacto del test (d). Otro nodo consumirá `stale_declared` o el comando si existe.
