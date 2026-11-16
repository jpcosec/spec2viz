## REFORMULACION
**Propósito:** que la copia aislada del store que construye el fixture `mount_copy` incluya los RunDoc (`runs/subagents/*/run.md`), hoy ausentes, para que `sldb stores update` no falle por documentos faltantes y la suite de IR pueda pasar con RunDocs registrados.

**Resultado:** en `tests/conftest.py`, tras copiar `COPIED`, copiar cada `runs/subagents/*/run.md` a la misma ruta relativa bajo la raíz de la copia; declarar el patrón como constante de módulo y actualizar el docstring. No tocar `.sldb`, `desk`, `runs` del repo, digests, `FEDERATED` ni otros archivos.

**Repo:** IR. **Límites:** solo `tests/conftest.py`, concretamente `mount_copy` y sus constantes; fuera de alcance cualquier otro cambio.

## AMBIGUEDADES
1. «copia solo .sldb, sldb y desk (COPIED)» — cita el Rationale. `COPIED` enumera `.sldb, sldb y desk`; no queda claro si «sldb» es un tercer directorio distinto o errata de `.sldb`. Obligaría a inventar la lista real de `COPIED`.
2. «runs/subagents/deskops-e-31500ac1cfa1/run.md y runs/subagents/deskops-t-5a39cc2dfbf8/run.md» — Validation. El Rationale solo cita `deskops-t-5a39cc2dfbf8`; se asume que ambos existen hoy, pero no se aclara si la validación debe cubrir uno o todos los RunDoc presentes.
3. «mount_copy (línea 70)» — Implementation Path. La referencia posicional puede no coincidir con el archivo real; obligaría a localizar el fixture por nombre.

## DRY-RUN
**Lecturas previstas:** `tests/conftest.py` (`COPIED`, `mount_copy`, docstring), `runs/subagents/*/run.md` existentes.
**Cambios previstos:** añadir constante `RUN_DOCS = 'runs/subagents/*/run.md'`; en `mount_copy`, tras `COPIED`, iterar `sorted(REPO.glob(RUN_DOCS))`, crear padre y `shutil.copy2` a `root / relative_to(REPO)`; ajustar docstring.
**Dependencias:** `shutil`, `REPO`, fixture `mount_copy` y tests que dependen de la copia.
**Validaciones futuras (no ejecutadas):** pytest de `tests/test_mcp_extension.py` con `TMPDIR=/dev/shm`; `git diff --stat`; suite completa bajo `flock`; `deskops graph missing --root .`.

## FUTURO
Otro nodo deberá ejecutar la edición y las validaciones; un humano decidirá si la evidencia de RunDocs y la interpretación de `COPIED` son correctas antes de cerrar.
