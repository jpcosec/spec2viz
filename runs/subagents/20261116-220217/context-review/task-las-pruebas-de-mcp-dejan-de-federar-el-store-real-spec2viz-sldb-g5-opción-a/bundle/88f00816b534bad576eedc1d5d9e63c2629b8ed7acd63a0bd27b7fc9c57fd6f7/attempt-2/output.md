## REFORMULACION

**Propósito:** que las pruebas MCP de IR sigan verificando la lectura de una spec desde un store enlazado, sin leer ni federar el store real `../spec2viz/.sldb`.

**Resultado:** `tests/conftest.py` y `tests/test_mcp_extension.py` modificados: `FEDERATED` solo con deskops; fixture de sesión `spec_store` que construye un store real temporal desde la fixture `class-sldb-models.yml` con `sldb.api`; `mount_copy` lo enlaza con alias `spec2viz`; los digests cubren ese store; docstrings actualizados.

**Repo:** IR (`/mnt/ssd/proyectos/SLDB_1/IR`).

**Límites:** solo esos dos archivos; fuera acta/matriz, retirement check, `tests/visual/test_api.py:45`, spec2viz y sldb. Sin mocks ni stores fabricados.

## AMBIGUEDADES

1. **El input ya contiene la solución.** Los archivos adjuntos muestran `build_spec_store(tmp_path_factory)`, `def mount_copy(..., spec_store: Path)` y `def test_a_spec_of_the_linked_spec2viz_store_is_read_through_the_server(mcp, spec_store: Path)`. Si el ejecutor los toma como estado actual, no sabría si debe verificar, reescribir o cerrar sin cambios; obligaría a inventar si son línea base o resultado esperado.

2. **Dependencias sin contenido.** El TaskDoc declara `depends_on:` con `task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents` y `task-espejo-deskops-deskops-sldb-deja-de-enlazar-el-store-de-spec2viz-g5-opción-b`, pero el input no incluye sus resultados. Obligaría a inventar si ya están cerradas y si sus cambios condicionan `mount_copy`.

## DRY-RUN

Leería completos ambos tests, la fixture YAML, `tests/visual/test_notations_parity.py`, las pills y el TaskDoc. Compararía el árbol actual con el objetivo; si ya coincide, no duplicaría cambios. Si no: quitaría spec2viz de `FEDERATED`; añadiría `build_spec_store`, `spec_store` y su digest; propagaría `spec_store` a `mount_copy`, `store_copy`, `copy_digest` y `copy_digest_before`; ajustaría la prueba para leer el SpecDoc temporal; actualizaría docstrings.

Dependencias: `sldb.api.init_store`, `SpecSync`, CLI pública `sldb`, `tmp_path_factory`, fixture YAML y cierre de las tareas prerequisito. Validaría con el grep indicado, pytest de `test_mcp_extension.py`, `git diff --stat`, suite completa bajo `flock` y `deskops graph missing`. No ejecuto nada.

## FUTURO

Las tareas prerequisito deben cerrar y aportar sus resultados. Un ejecutor aplicará o verificará los cambios y correrá las validaciones. Un humano debe resolver la ambigüedad 1 indicando si el contenido adjunto es línea base o estado final. Closeout actualizará el Board y preparará el commit; IR13 decidirá el retiro del store real.
