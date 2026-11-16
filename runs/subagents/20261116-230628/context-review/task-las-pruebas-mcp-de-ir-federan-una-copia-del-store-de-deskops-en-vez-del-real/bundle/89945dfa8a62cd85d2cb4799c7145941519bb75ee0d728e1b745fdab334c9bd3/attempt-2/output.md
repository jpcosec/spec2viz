## REFORMULACION

**Propósito:** que las pruebas MCP de IR no lean ni digieran el store real de deskops, sino una copia tomada al inicio de la sesión, para que la suite completa dé verde aunque deskops escriba durante la corrida.
**Resultado:** `tests/conftest.py` y `tests/test_mcp_extension.py` modificados: `build_deskops_copy` crea `<tmp>/deskops/.sldb` (store + archivos de `git ls-files`, sin caché), symlinks `sldb/pron/scion` en `<tmp>`, `FEDERATED` pasa a fixture, `federated_digest` digiere la copia y `mount_copy` monta la copia con alias `deskops`; la prueba `test_reading_through_every_tool_leaves_every_store_untouched` conserva sus aserciones.
**Repo:** IR. **Límites:** fuera cambiar deskops/sldb y la tarea de federación de spec2viz (dependencia previa, closeout 4f1e108).

## AMBIGUEDADES

1. "lo que haga falta para que sus enlaces resuelvan" / "sin la caché": no se define si "caché" es solo `.sldb_cache` ni si hay archivos no rastreados necesarios; obligaría a inventar el criterio de copia.
2. "se crean symlinks sldb, pron y scion a los repos reales del workspace": no dice qué hacer si `pron` o `scion` no existen en el workspace; obligaría a inventar fallback o fallo.
3. "los .md listados por git ls-files del proyecto real, leídos en la copia": mezcla listado del repo real con lectura en copia; no aclara qué pasa si deskops escribe entre ambos momentos; obligaría a inventar estrategia ante carrera.
4. "Suite completa una vez bajo flock /dev/shm/sldb1-tests.lock con rc 0": no da comando pytest ni timeout; obligaría a inventar la invocación exacta.
5. "Empezar con [dependencia] integrada (closeout 4f1e108 en main de IR)": no indica cómo verificar/actualizar la rama; obligaría a inventar el procedimiento de sincronización.
6. "deskops graph missing --root ." no define binario/entorno de `deskops`; obligaría a inventar su resolución.

## DRY-RUN (sin ejecutar)

**Lecturas:** `tests/conftest.py`, `tests/test_mcp_extension.py`, `.sldb` y `git ls-files` de deskops, store_index de la copia.
**Cambios previstos:** añadir `build_deskops_copy(tmp_path_factory)`; fixture sesión que la invoca; sustituir `FEDERATED` constante por fixture/dict; adaptar `federated_digest`, `mount_copy` y `copy_digest`; crear symlinks en `<tmp>`.
**Dependencias:** CLI `sldb`, `git`, `tmp_path_factory`, dependencia spec2viz integrada.
**Validaciones futuras:** grep de rutas reales, pytest del módulo con `TMPDIR=/dev/shm`, comprobación de alias temporal, suite completa bajo `flock`, `deskops graph missing`.

## FUTURO

- Otro nodo/humano confirma que `pron` y `scion` existen y cómo tratarlos si faltan.
- Humano valida la integración previa (4f1e108) antes de ejecutar.
- Closeout decide átomo/commit y el ritual de fase valida la suite integrada.
