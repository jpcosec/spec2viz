## REFORMULACION

**Propósito:** desacoplar las pruebas MCP de IR del store real `../spec2viz/.sldb`, conforme a la decisión G5 opción A, manteniendo la cobertura de lectura de una spec de un store enlazado y de que los stores no se modifican.

**Resultado:** `tests/conftest.py` y `tests/test_mcp_extension.py` dejan de leer/enlazar el store de spec2viz; construyen un store temporal real desde una fixture de IR, lo enlazan con alias `spec2viz`, conservan las aserciones del servidor y amplían la comprobación de “untouched”.

**Repo:** `SLDB_1/IR`. **Límites:** solo esos dos archivos; no tocar `spec2viz`, `sldb`, acta/matriz, `tests/visual/test_api.py:45` ni el universo de retirement check. Sin mocks ni documentos fabricados; usar API pública y detenerse ante bloqueo.

## AMBIGUEDADES

1. «las que comparan digests antes y después»: no nombra las pruebas exactas; obliga a inventar cuáles deben ampliarse.
2. «se ajusta la prueba para leer los datos del store temporal, sin relajar ninguna aserción»: no define qué ajuste es admisible; obliga a inventar el criterio.
3. «el store real de deskops»: no indica ruta ni alias; obliga a inferirlos de `FEDERATED`.
4. «cwd=root»: no define `root`; obliga a inventar si es raíz del repo o del fixture.
5. «el .venv del repo»: no precisa el repo; obliga a asumir que es la raíz de IR.

## DRY-RUN

Nodo ejecutable, no agregado.

**Lecturas:** ambos tests completos, `tests/visual/test_notations_parity.py`, la fixture `class-sldb-models.yml` y la nota de decisión.

**Cambios previstos:** quitar `spec2viz` de `FEDERATED`; añadir fixture de sesión que copie el YAML a un directorio temporal, ejecute `init_store` y `SpecSync(...).sync(...)`; enlazar ese store en `mount_copy` con alias `spec2viz`; incluir el store temporal en `federated_digest` y comprobaciones de digest; actualizar docstrings.

**Dependencias:** `sldb.api.init_store`, `SpecSync`, fixtures pytest, store de deskops y comportamiento de enlace de `sldb`.

**Validaciones futuras:** grep sin referencias a `../spec2viz`; pytest de `test_mcp_extension.py` sin skips; `git diff --stat` limitado; suite completa bajo `flock`; `deskops graph missing`.

## FUTURO

Un humano confirma la decisión G5 y el momento del archivo; otro nodo o IR13 retira `spec2viz/.sldb` del universo de retirement check. Si `SpecSync` o la API pública no permiten crear el store temporal, el ejecutor debe detenerse y reportarlo.
