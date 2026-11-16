## REFORMULACION
Propósito: retirar el `xfail` ya obsoleto de `test_label_key_of_sldb_splits_underscores_like_norm_key`, porque sldb lo arregló en `06dbcf02` y el `strict=True` convierte el éxito en fallo. Resultado: esa prueba corre normal y pasa; el diff de `tests/visual/test_catalog.py` solo borra el decorador; la suite completa de IR da rc 0. Repo: IR, con sldb editable en `../sldb`. Límites: no tocar cuerpo, docstring ni `@needs_node`; no tocar otros archivos, `matriz-de-cobertura.md`, el acta ni sldb; si la prueba sin xfail falla, detenerse sin cambiar aserciones.

## AMBIGUEDADES
1. «comprobar con git diff --stat tests/conftest.py que el cambio de mount_copy (RUN_DOCS) está presente»: no define qué texto/estado cuenta como “presente”; obligaría a inventar un criterio verificable.
2. «la suite completa de IR vuelve a salir con rc 0» frente a «El árbol de trabajo tiene además cambios sin commitear de otras dos tareas»: no aclara si esos cambios ajenos son precondición válida o posible causa de fallo; obligaría a decidir responsabilidad.
3. «deskops graph missing --root . sale con rc 0» aparece en Validación pero no en la ruta de implementación; no dice si un fallo previo bloquea o es solo comprobación final.
4. «hoy ocupa una sola línea» depende del estado del archivo; si el decorador estuviera partido, no define el alcance exacto de líneas a borrar.

## DRY-RUN
Lecturas: TaskDoc, rituales, pill, `tests/visual/test_catalog.py`, referencia `result-summary.md`, estado git de IR y sldb. Cambios previstos: eliminar únicamente el decorador `@pytest.mark.xfail(...)` sobre la prueba indicada. Dependencias: `06dbcf02` ancestro de HEAD en sldb; `conftest.py` con cambio `mount_copy`; `.venv`; `flock`; node para pruebas marcadas. Validaciones futuras: comprobar ancestro; ejecutar solo la prueba y ver XPASS estricto antes de editar; tras editar, ejecutar `tests/visual/test_catalog.py`; revisar `git diff`; ejecutar suite completa bajo `flock`; ejecutar `deskops graph missing`. Nada se ejecuta ahora.

## FUTURO
El ejecutor decide si se detiene por precondiciones; el commit y cierre corresponden al ritual de closeout. IR13e acredita las filas SV-G08/SV-I02 en su ciclo. Un humano resuelve bloqueos externos de sldb, conftest o suite compartida.
