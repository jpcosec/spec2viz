REFORMULACION
Nodo ejecutable `task.code` del repo IR (workspace desk); no es agregado. Propósito: cerrar IR13d de la migración de spec2viz. Resultado: comando `specir` (`specir.cli:main`) con grupos `diagram` y `catalog`, `catalog build`, alias `render/validate/lint/schema/build` y `about`; API pública en `specir.visual`; `skills/use-specir/SKILL.md`; `docs/spec2viz/correspondencia-cli.md`; pruebas portadas y paquete instalable sin spec2viz. Límites: no implementar capacidades (IR11/IR12/IR13a/b), no instalar la skill en otros repos, no migrar consumidores, no duplicar comandos/API de sldb, no reexportar `load`/`validate`, sin mocks.

AMBIGUEDADES
1. “comando de specIR con equivalentes de todos los comandos y subgrupos de spec2viz (diagram, notation, palette, catalog…)” frente a “Los subgrupos notation y palette … no tienen equivalente en specIR”. Obligaría a inventar si se crean grupos o solo filas que remiten a sldb.
2. “La habilidad de agente nombra solo comandos que existen en el comando de specIR” frente a que la skill enseña `sldb notations …` y `sldb serve`. Obligaría a decidir si nombrar sldb invalida la skill o si la validación se limita a `specir`.
3. “un venv nuevo en /dev/shm” frente a `test_packaging.py`, que usa `tmp_path` y `uv`. Obligaría a fijar ubicación real y comportamiento si `uv` o la red no están disponibles.

DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout, pills y átomos ligados; `src/specir/cli.py`, `visual/__init__.py`, `visual/commands.py`, `pyproject.toml`, skill, correspondencia, matriz y tests listados. Cambios previstos: montar grupos y alias, añadir `about` y `catalog build`; completar exportaciones públicas; escribir skill y tabla; portar pruebas de CLI/API/empaquetado; apuntar `specir` a `specir.cli:main`. Dependencias: IR13a/IR13b/IR12 e IR11 transitiva, `sldb.api`, `uv`/venv. Validaciones futuras: pytest de `tests/visual/test_cli.py`, `test_api.py` y `test_packaging.py`; `--help`/`about`; instalación limpia; `import spec2viz` falla; ningún comando de sldb duplicado.

FUTURO
IR13 marcả filas de la matriz y evalúa el gate de retiro; sldb publicará su comando de validación y entonces se retirará el provisional; JP decide la fuente de verdad del YAML; los repos consumidores ejecutan su migración.
