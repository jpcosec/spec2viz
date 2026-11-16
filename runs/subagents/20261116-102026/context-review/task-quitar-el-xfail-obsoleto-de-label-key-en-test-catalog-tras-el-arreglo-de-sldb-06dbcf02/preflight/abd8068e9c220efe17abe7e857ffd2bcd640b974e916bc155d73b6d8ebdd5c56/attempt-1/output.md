## REFORMULACION

El nodo es una tarea ejecutable (`task.code`), no un agregado. Su propósito es retirar de `tests/visual/test_catalog.py` el `xfail` obsoleto de `test_label_key_of_sldb_splits_underscores_like_norm_key`, porque el arreglo de sldb `06dbcf02` hace que pase y el `xfail(strict=True)` produzca XPASS estricto. Resultado: la prueba corre normal y pasa; la suite completa de IR sale con rc 0. Repo: IR, con sldb editable en `../sldb`. Límites: tocar solo ese decorador; conservar cuerpo, docstring y `@needs_node`; no tocar otros archivos/pruebas, la matriz de cobertura, el acta, sldb ni cambios sin commitear ajenos; si la prueba sin xfail falla, detenerse sin cambiar aserciones.

## AMBIGUEDADES

1. «Borrar las dos líneas del decorador xfail» frente a «quitar solo el decorador `pytest.mark.xfail(strict=True, ...)`»: si no ocupa exactamente dos líneas físicas, obliga a decidir entre contar líneas y eliminar el decorador completo.
2. «la suite completa se corre con ellos presentes, porque sin el cambio de tests/conftest.py la suite falla»: no fija si ese cambio es precondición bloqueante o solo contexto; obligaría a inventar si detenerse o ejecutar y reportar cuando falte.
3. «correr la prueba sola para ver el XPASS(strict)»: puede significar un único test o el archivo; la validación usa `tests/visual/test_catalog.py`, pero no explicita la granularidad del primer comando.

## DRY-RUN

Lecturas: TaskDoc, `result-summary.md`, la prueba y su decorador, `git status`/`git diff`, estado de sldb. Cambio previsto: eliminar únicamente el decorador xfail, preservando `@needs_node`, cuerpo y docstring. Dependencias: sldb con `06dbcf02` ancestro de HEAD; cambios ajenos presentes e intactos; `.venv`, `TMPDIR=/dev/shm`, `flock` y `SPECIR_MMDC`. Validaciones futuras: prueba focalizada antes/después, diff limitado a la eliminación, suite completa una vez bajo lock con rc 0 y `deskops graph missing --root .` rc 0. Sin ejecutar nada.

## FUTURO

Un nodo ejecutor aplicará el cambio y correrá las validaciones. Un humano u operador decidirá ante un bloqueo por cambios ajenos ausentes o fallos no atribuibles. IR13e acreditará las filas SV-G08/SV-I02; sldb no se modifica.
