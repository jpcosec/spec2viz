## REFORMULACION
Encargo: en el repo SLDB_1/IR, actualizar `docs/spec2viz/matriz-de-cobertura.md` para que SV-K16, SV-K21, SV-K26 y SV-K29 queden como “usar sldb directamente” con equivalente `sldb notations validate`, estado cumplida y cita de test; propagar el estado a SV-K09, SV-K18 y SV-K23 si todas sus hijas están cumplidas. Además, retirar de `src/specir` los comandos `specir diagram validate` y `specir validate`, redirigir su ayuda y `docs/spec2viz/correspondencia-cli.md` a `sldb notations validate`, ajustar `tests/visual/test_cli.py` y tests afectados, actualizar CHANGELOG si existe, ejecutar `specir retirement check` y commitear con trailer `Task-Id`. Resultado: solo SV-A17 abierta y los tests indicados pasando. Límites: fuera SV-A17, tests de paridad que importan spec2viz y el acta de retiro.

## AMBIGUEDADES
1. “specir retirement check con las rutas del inventario”: no se especifica el comando exacto ni dónde está el inventario; obliga a inventar rutas y sintaxis.
2. “commit desde tu worktree” y “trailer Task-Id”: no consta la ruta del worktree ni el valor literal del trailer; obliga a inventarlos.
3. “citando un test”: solo se nombra el test de ayuda; no queda claro qué test citar en cada una de las cuatro filas; obliga a elegir uno.
4. “SV-K09, SV-K18 y SV-K23 pasan a cumplida si todas sus hijas lo están”: no se enumeran sus hijas; obliga a inferirlas de la matriz.
5. “CHANGELOG si existe”: no se indica ruta ni formato; obliga a decidir dónde y cómo registrar el cambio.

## DRY-RUN
Lecturas previstas: TaskDoc, matriz, correspondencia CLI, definiciones de comandos en `src/specir`, `tests/visual/test_cli.py`, `tests/test_matriz_cobertura_spec2viz.py`, `tests/visual/test_retirement_gate.py` y CHANGELOG si aparece. Cambios previstos: p1 actualizar tabla/test de ayuda; p2 borrar ambos comandos y ajustar tests; p3 actualizar cuatro filas y tres subgrupos; p4 ejecutar retirement check y guardar salida en el run dir; p5 commit por rutas con trailer. Dependencias: `sldb notations validate` disponible, worktree e inventario localizables. Validaciones futuras: el pytest indicado y retirement check con solo SV-A17 abierta. No se ejecuta nada.

## FUTURO
El nodo ejecutor producirá el diff, la salida de retirement check y el commit. Un humano o nodo revisor confirmará que solo SV-A17 queda abierta y autorizará el cierre; CI o el gate de retiro validarán el resultado conjunto.
