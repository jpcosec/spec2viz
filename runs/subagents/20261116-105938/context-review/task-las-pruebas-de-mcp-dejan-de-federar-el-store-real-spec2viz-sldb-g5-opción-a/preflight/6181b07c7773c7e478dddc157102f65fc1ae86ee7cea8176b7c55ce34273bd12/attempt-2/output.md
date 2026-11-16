REFORMULACION
Propósito: desacoplar las pruebas MCP de IR del store real `../spec2viz/.sldb`. Resultado: probar la lectura de una spec de un store enlazado usando un store temporal creado desde una fixture de IR, sin leer ni enlazar el store real; mantener el alias `spec2viz`, cubrir el chequeo de “untouched” y actualizar docstrings. Repo: IR (`/mnt/ssd/proyectos/SLDB_1/IR`). Límites: fuera de `desk/`, `.sldb/` y `runs/`, solo `tests/conftest.py` y `tests/test_mcp_extension.py`; no tocar spec2viz/sldb, acta/matriz, universo de retirement check ni `tests/visual/test_api.py:45`; usar API pública sldb, sin mocks; detenerse si SpecSync no construye el store fuera de git o falta API. No es agregado ni paquete: es `task.code` ejecutable.

AMBIGUEDADES
1. “crear el store con `sldb.api.init_store(<dir>)` y sincronizar la spec con `SpecSync(<dir>/.sldb)`” frente a “Devuelve la ruta de su `.sldb`” y “`sldb stores add <ruta>/.sldb`”: no queda claro si `<dir>`/`<ruta>` es el proyecto o el propio `.sldb`; obligaría a inventar la ruta exacta y evitar un doble `.sldb`.
2. “sus llamadores (`store_copy` y los demás que lo usen)” no enumera todos; obligaría a inventar qué llamadores existen y cambiar firmas.
3. “las mismas pruebas que hoy comparan `federated_digest` u `original_digest`” no las nombra; obligaría a inventar el conjunto exacto de pruebas a modificar.
4. “`tree_digest(spec_store)` más el sha256 de cada archivo `.md` bajo su proyecto” no define el proyecto, ni cómo combinar/ordenar digests, ni si incluye YAML; obligaría a inventar el algoritmo.
5. “si su ruta indexada o su payload no cumplen […] se ajusta la prueba” no fija el límite del ajuste; obligaría a inventar qué se puede cambiar sin relajar aserciones.

DRY-RUN
Un ejecutor leería completos `tests/conftest.py`, `tests/test_mcp_extension.py`, `tests/visual/test_notations_parity.py`, la fixture `class-sldb-models.yml` y la API pública de sldb. Cambios previstos: quitar spec2viz de `FEDERATED`; añadir `build_spec_store` y fixture de sesión `spec_store`; pasar `spec_store` a `mount_copy` y enlazar el `.sldb` temporal como `spec2viz`; hacer que la prueba de lectura use el fixture; ampliar los digests de “untouched”; actualizar docstrings. Dependencias: `tmp_path_factory`, `sldb.api.init_store`/`SpecSync`, CLI `sldb stores add`, fixture existente. Validaciones futuras: grep sin `../spec2viz`, pytest de `test_mcp_extension`, `git diff --stat`, suite completa bajo `flock` y `deskops graph missing`; sin ejecutar ahora.

FUTURO
El ejecutor futuro implementa y valida; si SpecSync no construye fuera de git o falta API, se detiene y reporta para decisión humana. JP/otro nodo decide el retiro IR13 y el archivo del store; esta tarea no lo ejecuta.
