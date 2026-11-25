## REFORMULACION
Propósito: retirar spec2viz de las pruebas de paridad de IR (acta, punto 6) congelando sus salidas. Resultado: ningún archivo de IR importa ni invoca spec2viz; las comparaciones usan goldens versionados en `tests/visual/goldens/`, grabados desde el checkout de spec2viz con commit en el nombre; se borran pruebas vivas ya cubiertas; `tests/test_matriz_cobertura_spec2viz.py` deja de importar `spec2viz.cli`; la cobertura no baja. Repo: IR (`/mnt/ssd/proyectos/SLDB_1/IR`). Límites: dentro pruebas de paridad, imports nombrados, goldens y script de grabación en el run dir; fuera `src/`, la matriz, el acta, el store y el repo spec2viz (solo lectura). Nodo `task.code` ejecutable, no agregado.

## AMBIGUEDADES
1. “Si un caso ya está cubierto por un golden existente, la prueba en vivo se borra.” Obliga a inventar el criterio de equivalencia (caso, aserción o salida) y qué prueba exacta se elimina.
2. “La cobertura de la paridad no baja: los casos que hoy pasan con spec2viz instalado siguen comprobados.” Obliga a inventar cómo medir “mismo número” y mapear cada caso a un golden, pues p1 no fija artefacto base.
3. “un script de grabación que vive fuera de tests/ (en runs/<run>/, que el comprobador no audita)” Obliga a inventar ruta concreta, si se versiona/commitea y qué `<run>` se usa.
4. “grabado desde spec2viz (el checkout ... con su commit en el nombre del archivo, como los spec2viz-2de1056*.json)” Obliga a inventar commit exacto, formato del nombre y si se reutiliza 2de1056 o el HEAD.
5. “usa el golden o una lista congelada de comandos” Obliga a elegir una alternativa no fijada para `test_matriz`.
6. “Fuera: src/, la matriz, el acta...” frente a “Dentro: ... tests/test_matriz_cobertura_spec2viz.py” Obliga a inventar qué abarca “la matriz” y si su test puede modificarse sin tocar ese artefacto.

## DRY-RUN
Hipotético, sin ejecutar. Lecturas: TaskDoc, rituales, pruebas parity, goldens existentes, checkout spec2viz y script del run dir. Cambios previstos: grabar goldens faltantes fuera de `tests/`; editar pruebas para cargar el golden y quitar imports/`importorskip`; borrar casos vivos cubiertos; ajustar `test_matriz`; commit de rutas con `Task-Id`. Dependencias: pytest, spec2viz solo para grabación, commit del checkout, worktree/run dir de dispatch, goldens previos y `specir retirement check`. Validaciones futuras, sin ejecutar: el pytest indicado con `TMPDIR=/tmp`, comparación de los mismos casos de paridad, retirement check con las rutas y ausencia de imports/invocaciones.

## FUTURO
El dispatch entrega worktree y run dir; la ejecución produce goldens, cambios y commit; closeout/phase verifican validación e integración. El resultado de pytest y del retirement check se observa; el humano/Board decide el cierre si algo falla.
