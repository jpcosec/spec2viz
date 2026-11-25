REFORMULACION
Propósito: eliminar de IR los goldens de spec2viz y todo test, helper o marcador que solo exista para compararlos, conforme a la decisión de JP y al guardrail reescrito; la paridad se acredita con pruebas de aceptación. Resultado: `tests/` sin goldens, oracle, parity ni marcador `parity`, con suite verde y grep final vacío. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: solo `tests/` y `pyproject.toml`; no se toca `src/`, `docs/spec2viz/` queda histórico y `specir retirement check` queda sin prueba de gate; se conservan pruebas de comportamiento. Nodo ejecutable `task.code`; no es agregado ni paquete.

AMBIGUEDADES
1. “de una exploracion de johanes, no de correr la suite”: inventario no verificado; obliga a inventar si el conjunto real difiere.
2. “decidir con el mismo criterio”: criterio no operacional; obliga a inventar qué significa “solo existe para comparar”.
3. “test_render_projections.py o similar”: destino no fijado; obliga a inventar archivo y ubicación.
4. “salvo nombres de capacidades en docstrings, anotados”: no define capacidad ni anotación; obliga a inventar excepciones.
5. “Revisar tambien tests/conftest.py, test_refs_models.py y test_visual_names.py”: no indica borrar, editar o conservar; obliga a inventar la acción.
6. “la paridad se acredita por pruebas de aceptacion”: no identifica archivos ni comando; obliga a inventar la suite de aceptación.

DRY-RUN
Hipotético, sin ejecutar. Lecturas: TaskDoc, rituales, `pyproject.toml`, `tests/conftest.py`, archivos nombrados e inventario por grep. Cambios previstos: borrar `tests/visual/goldens/`, `oracle.py`, `parity.py`, `render_parity.py` y los tests de paridad listados; mover antes los casos de comportamiento —al menos `test_the_projected_states_of_the_blog_render`—; quitar casos `*matches_spec2viz*` y `oracle.expect(...)`; eliminar el marcador `parity`. Dependencias: specIR editable en el venv, pytest con `-n 4`, `TMPDIR`. Validaciones futuras: `tests/extract` y `tests/models`; grep final; comando pytest indicado.

FUTURO
Closeout produce commit y actualización del board; la fase aporta validación integrada. Un humano confirma inventario, criterio, destino del test movido y excepciones de docstrings.
