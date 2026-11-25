## REFORMULACION

Encargo: en el repo /mnt/ssd/proyectos/SLDB_1/IR, eliminar todo golden de spec2viz y toda prueba, helper o marcador que exista únicamente para compararse con ellos, conservando las pruebas de comportamiento y dejando la suite verde. Resultado: sin `tests/visual/goldens/`, sin `oracle.py`/`parity.py`/`render_parity.py`, sin casos `*matches_spec2viz*` ni usos de `oracle.expect(...)`, sin marcador `parity`, y con grep final limpio. Límites: solo `tests/` y `pyproject.toml`; no se toca `src/`, ni `docs/spec2viz/`, ni el comando `specir retirement check`. Previamente se mueven los casos de comportamiento embebidos en archivos de paridad (p. ej. `test_the_projected_states_of_the_blog_render`). Es una tarea ejecutable, no un agregado.

## AMBIGUEDADES

1. "solo los casos *matches_spec2viz*" — no aclara si se borran funciones completas o aserciones, ni si el archivo desaparece al quedarse sin casos. Obligaría a inventar la unidad de borrado.
2. "cualquier -m parity en conftest o config" — no nombra los archivos concretos ni el perímetro de búsqueda.
3. "tests/visual/test_render_projections.py o similar" — el nombre destino queda abierto.
4. "salvo nombres de capacidades en docstrings, anotados" frente a Done When "el grep final esta vacio" — excepción y criterio de cierre se contradicen.
5. "anotarlo en result-summary.md" — ruta y formato del archivo no se especifican.
6. "Correr la suite completa de tests/visual y los archivos editados" frente a Validation, que solo lista `tests/visual tests/test_cli_mcp.py`; y "verificar que tests/extract y tests/models pasan" no aparece en Validation.
7. "los JSON spec2viz-2de1056-*" — no confirma si hay otros goldens bajo ese directorio; se resuelve borrando la carpeta, pero no se dice.

## DRY-RUN

Lecturas: TaskDoc, `tests/`, `pyproject.toml`, `tests/conftest.py`, `result-summary.md` si existe. Cambios: mover casos de comportamiento; borrar goldens, helpers y pruebas de paridad; editar los cinco archivos mixtos; quitar marcador. Dependencias: venv con specIR editable; `tests/extract` y `tests/models` verdes antes. Validación futura: `TMPDIR=... PYTHONPATH=src ... pytest -q -p no:cacheprovider -n 4 tests/visual tests/test_cli_mcp.py` más archivos editados y grep final.

## FUTURO

Un humano decide las ambigüedades 1–7 y confirma el criterio de cierre; otro nodo ejecuta el borrado y reporta en `result-summary.md`; la revisión final valida el grep y la suite.
