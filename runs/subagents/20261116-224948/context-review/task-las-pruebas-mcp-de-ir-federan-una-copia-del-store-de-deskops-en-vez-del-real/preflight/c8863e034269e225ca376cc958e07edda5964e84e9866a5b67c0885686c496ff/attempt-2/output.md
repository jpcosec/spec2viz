REFORMULACION

Encargo: en el repo IR, hacer que las pruebas MCP usen una copia del store de deskops tomada al inicio de la sesión, no el store real, para que la suite completa sea reproducible aunque deskops escriba. Resultado: `build_deskops_copy(tmp_path_factory)` crea `<tmp>/deskops` con el `.sldb` (sin caché) y los archivos de `git ls-files`; un fixture de sesión la monta; se crean symlinks `sldb`, `pron`, `scion` a los repos reales; `FEDERATED` recibe la copia por fixture; `federated_digest` digiere la copia y `mount_copy` la registra como `deskops`. Las aserciones de `test_reading_through_every_tool_leaves_every_store_untouched` no se relajan. Límites: solo `tests/conftest.py` y `tests/test_mcp_extension.py`; no cambiar deskops ni sldb; depende de la tarea de federación spec2viz ya integrada (closeout `4f1e108`). Nodo ejecutable, no agregado.

AMBIGUEDADES

1. «sin la caché»: no define qué es caché ni qué rutas excluir; obligaría a inventar reglas de exclusión.
2. «git -C <deskops> ls-files»: `<deskops>` no se define como ruta concreta; obligaría a inventar la raíz del repo.
3. «Si copiar el store de deskops rompe la resolución de sus enlaces»: no fija el criterio de “rompe”; obligaría a inventar el umbral entre fallo de enlace y fallo de prueba.
4. «Suite completa una vez bajo flock»: no indica el comando exacto de “suite completa”; obligaría a inventar la invocación.
5. «el origen de la copia dentro de build_deskops_copy»: no define qué coincidencias del grep son aceptables; obligaría a inventar el criterio de aceptación del grep.

DRY-RUN

Lecturas: `tests/conftest.py`, `tests/test_mcp_extension.py`, patrón `build_spec_store`, `store_index` de deskops y salida de `git ls-files`; verificar closeout previo. Cambios previstos: auxiliar de copia, fixture de sesión, symlinks, `FEDERATED` por fixture, digest y montaje sobre la copia. Dependencias: repos deskops, sldb, pron y scion disponibles; CLI `sldb`. Validaciones futuras: grep de rutas reales, pytest MCP, `stores list` sobre la copia, suite completa bajo `flock`, `deskops graph missing`. Nada ejecutado.

FUTURO

Un nodo ejecutor realizará los cambios y validaciones; un humano decidirá si un fallo de resolución de enlaces constituye bloqueo y si la tarea previa está efectivamente integrada.
