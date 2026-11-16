REFORMULACION
Propósito: en el repo IR (`/mnt/ssd/proyectos/SLDB_1/IR`), quitar solo el decorador `@pytest.mark.xfail(strict=True, reason=...)` de `test_label_key_of_sldb_splits_underscores_like_norm_key` en `tests/visual/test_catalog.py`. Resultado: esa prueba corre sin xfail y pasa, y la suite completa de IR sale con rc 0. Repo: IR, con sldb editable en `../sldb` y el commit `06dbcf02` ancestro de `HEAD`. Límites: no tocar cuerpo, docstring ni `@needs_node`; no tocar otros archivos/pruebas, matriz/acta ni sldb; si la prueba falla o falta una precondición, detenerse y reportar sin cambiar aserciones. Es un nodo ejecutable, no un agregado.

AMBIGUEDADES
1. «los 5 archivos de IR13e» y «Son precondición bloqueante de la suite completa». No se enumeran ni se indica cómo comprobarlos; solo se manda verificar `tests/conftest.py`. Obligaría a inventar qué archivos son y si su ausencia bloquea.
2. «El árbol de trabajo tiene además cambios sin commitear de otras dos tareas». Se afirma un estado que el ejecutor debe asumir; no se define qué hacer si no coincide, salvo para `conftest.py`. Obligaría a inventar una comprobación y una decisión.

DRY-RUN
Lecturas previstas: TaskDoc, `runs/subagents/deskops-t-8825fdd278af/result-summary.md`, `tests/visual/test_catalog.py`, `git status`/`git diff --stat tests/conftest.py`, y `git -C ../sldb merge-base --is-ancestor 06dbcf02 HEAD`.
Cambios previstos: borrar únicamente la línea del decorador xfail; nada más.
Dependencias: sldb editable con `06dbcf02`; cambio `mount_copy` en `tests/conftest.py`; `.venv`, `TMPDIR=/dev/shm`, `SPECIR_MMDC`, `flock` y pytest con `-n 4`.
Validaciones futuras: prueba aislada (primero para observar XPASS, luego sin xfail), `pytest tests/visual/test_catalog.py`, `git diff` limitado al archivo, suite completa bajo `flock`, y `deskops graph missing --root .`; todo sin ejecutar ahora.

FUTURO
Otro nodo produjo `result-summary.md`; IR13e acreditará SV-G08/SV-I02 en su ciclo. Si la prueba falla, falta `mount_copy`/IR13e o la suite falla por causas ajenas, el ejecutor se detiene y reporta; la decisión corresponde a un humano u otra tarea.
