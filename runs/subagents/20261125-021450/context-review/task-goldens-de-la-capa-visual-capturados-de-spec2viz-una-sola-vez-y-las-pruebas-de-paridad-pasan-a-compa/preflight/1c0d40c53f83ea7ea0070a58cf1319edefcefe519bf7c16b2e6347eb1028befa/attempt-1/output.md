## REFORMULACION
Propósito: retirar spec2viz como oráculo vivo y sustituirlo por salidas de referencia versionadas. Resultado: capturar una vez las salidas de spec2viz, guardarlas en `tests/visual/goldens/` y reescribir las pruebas de paridad para comparar specIR contra esos archivos sin importar spec2viz; con spec2viz ausente, `pytest tests/visual` no debe saltarse pruebas por esa causa. Repo: IR, según cwd y rutas relativas; spec2viz se toma de `/mnt/ssd/proyectos/SLDB_1/spec2viz`. Límites: solo script de captura, goldens y tests de paridad; fuera quitar el marcador `parity` y la dependencia.

## AMBIGUEDADES
1. “goldens versionados bajo tests/visual/goldens/” no define formato, nombres ni estructura; obliga a inventar serialización y organización.
2. “corre spec2viz sobre los mismos casos” no enumera los casos; obliga a inferirlos de los tests existentes.
3. “script de captura de una sola vez” no aclara si se versiona, se conserva o se elimina; obliga a decidir su permanencia.
4. “comparan specIR contra esos archivos” no fija igualdad exacta, tolerancias ni tratamiento de binarios; obliga a inventar el criterio de comparación.
5. “spec2viz fuera del entorno” frente a “desinstalado del PYTHONPATH” no define el método de aislamiento; obliga a decidir si se desinstala, se oculta o se usa un entorno limpio.

## DRY-RUN
Un ejecutor futuro leería `tests/visual/parity.py`, `render_parity.py`, los `test_*_parity.py` y fixtures para inventariar casos y salidas. Crearía un script de captura que invoque spec2viz desde la ruta indicada y escriba goldens. Reescribiría los tests para cargar goldens, sin importar spec2viz ni omitir por su ausencia. Dependencias: spec2viz disponible durante la captura, pytest y `TMPDIR`. Validación futura: ejecutar el comando pytest indicado y comprobar que no hay saltos por spec2viz; no se ejecuta ahora.

## FUTURO
Decisión humana: aceptar formato y procedencia de goldens, y política de regeneración. Otro nodo: quitar marcador `parity` y dependencia de spec2viz.
