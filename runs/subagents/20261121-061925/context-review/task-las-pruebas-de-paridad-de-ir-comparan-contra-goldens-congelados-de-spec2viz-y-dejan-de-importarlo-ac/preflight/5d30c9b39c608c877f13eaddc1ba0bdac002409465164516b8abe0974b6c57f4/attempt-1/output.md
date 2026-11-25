## REFORMULACION

Encargo ejecutable sobre el repo IR (`/mnt/ssd/proyectos/SLDB_1/IR`): eliminar toda dependencia de las pruebas de IR respecto de spec2viz, sustituyendo las comparaciones en vivo por goldens congelados y versionados en `tests/visual/goldens/`, grabados desde el checkout `/mnt/ssd/proyectos/SLDB_1/spec2viz` con su commit en el nombre. Resultado: ningún archivo de IR importa ni invoca spec2viz; `specir retirement check` no lista dependencias de IR; la cobertura de paridad no baja. Límites: solo `tests/visual/*parity*.py`, `tests/visual/parity.py`, `tests/visual/render_parity.py`, líneas de import en cinco tests y `tests/test_matriz_cobertura_spec2viz.py`, goldens y script de grabación en el run dir. Fuera: `src/`, matriz, acta, store y repo spec2viz (solo lectura).

## AMBIGUEDADES

1. «en `runs/<run>/`»: no se identifica el run concreto; obligaría a inventar la ruta del script de grabación.
2. «los mismos casos pasan sin spec2viz instalado»: no define cómo garantizar que no sea importable (entorno, desinstalación, `PYTHONPATH`); obligaría a inventar el método de verificación.
3. «Si un caso ya está cubierto por un golden existente»: no fija el criterio de equivalencia; obligaría a inventar cuándo borrar la prueba en vivo.
4. «el worktree que dispatch te da»: no aparece su ruta ni el `Task-Id`; obligaría a inventar ambos para el commit.
5. «spec2viz 2de1056» frente a «el checkout»: no garantiza que el checkout esté en ese commit; obligaría a inventar la procedencia del golden.
6. «pytest -m parity»: no consta que exista ese marcador; obligaría a inventar la selección de casos.

## DRY-RUN

Lecturas: TaskDoc, acta punto 6, los trece archivos de prueba citados, goldens `spec2viz-2de1056*.json` y metadata del checkout spec2viz. Cambios previstos: añadir script de grabación en el run dir; grabar goldens faltantes; editar cada prueba para cargar JSON sin importar spec2viz; borrar casos ya cubiertos; quitar `importorskip`. Dependencias: spec2viz instalado solo para la línea base y el script de grabación; pytest disponible. Validaciones futuras: `pytest -q tests/visual tests/test_matriz_cobertura_spec2viz.py`, `specir retirement check` con las rutas indicadas, y commit con trailer `Task-Id`. Sin ejecutar nada.

## FUTURO

Dispatch debe entregar worktree y `Task-Id`; un humano decide el run dir y acepta la equivalencia de cobertura y la procedencia del commit del golden. CI valida la suite y el retirement check.
