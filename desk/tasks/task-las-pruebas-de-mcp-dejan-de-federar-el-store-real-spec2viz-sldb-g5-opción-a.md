---
sldb:
  by: agent
  at: '2026-11-16T10:44:15Z'
  authority: generated
  via: save_document_payload
id: task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:pruebas
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-021430-suggestion-g5-decisi-n-de-jp-sobre-spec2viz-sldb.md
depends_on:
- task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
files:
- tests/conftest.py
- tests/test_mcp_extension.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Las pruebas de MCP dejan de federar el store real spec2viz/.sldb (G5, opción A)

## Rationale

_Explain why this task exists or the business driver behind it._

JP decidió G5 el 2026-11-16 con la opción A: el store spec2viz/.sldb se archiva junto con el repo spec2viz cuando specir retirement check dé 0 (nota desk/inbox/20261116-021430-suggestion-g5-decisi-n-de-jp-sobre-spec2viz-sldb.md). Pero las pruebas de IR todavía federan ese store real. tests/conftest.py lo declara en FEDERATED (línea 27, WORKSPACE / "spec2viz" / ".sldb"), mount_copy lo enlaza con «sldb stores add … --name spec2viz» y federated_digest lo incluye. Además, tests/test_mcp_extension.py (SPEC_STORE = "spec2viz" en la línea 24; test_a_spec_of_the_linked_spec2viz_store_is_read_through_the_server) lee de él el SpecDoc class.sldb-models. Cuando se archive el store, esas pruebas se rompen, y mientras tanto la suite de IR depende de un store de otro repo.

## Goal

_Describe the concrete result this task must produce._

Las pruebas de IR siguen probando la lectura de una spec de un store enlazado a través del servidor MCP, pero contra un store de specs que se construye en un directorio temporal a partir de una fixture que ya está en IR, sin leer ni enlazar ../spec2viz/.sldb.

## Scope

_State what is in scope and what is out of scope._

Dentro, en tests/conftest.py y tests/test_mcp_extension.py: (1) quitar spec2viz de FEDERATED, de modo que FEDERATED solo enlace el store real de deskops; (2) agregar un fixture de sesión que construya el store de specs. En un directorio de tmp_path_factory, copiar tests/visual/fixtures/spec2viz/docs/architecture/spec2viz/class-sldb-models.yml (id class.sldb-models) a la subcarpeta docs/architecture/spec2viz/ de ese directorio, con el mismo nombre de archivo, crear el store con sldb.api.init_store(<dir>) y sincronizar la spec con sldb.api.notations.SpecSync(<dir>/.sldb).sync(<ruta del yml>), igual que hace tests/visual/test_notations_parity.py; (3) en mount_copy, enlazar ese store en vez del real, con el mismo alias spec2viz («sldb stores add <dir>/.sldb --name spec2viz --store .sldb», cwd=root), de modo que SPEC_STORE y los nombres de las pruebas no cambian; (4) que las pruebas de «untouched» (federated_digest y las que comparan digests antes y después) cubran también el store de specs temporal, para que se siga comprobando que leer por MCP no escribe en ningún store enlazado; (5) actualizar los docstrings del módulo de conftest.py y de test_mcp_extension.py, que hoy dicen que el store de spec2viz se enlaza en su lugar. Fuera: el acta y la matriz; quitar spec2viz/.sldb del universo de specir retirement check (se hace al declarar el retiro, IR13); tests/visual/test_api.py:45 (lee ../spec2viz/spec2viz/__init__.py, que es el repo y no el store); cambiar spec2viz o sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer primero tests/conftest.py completo (FEDERATED, tree_digest, federated_digest, original_digest, mount_copy, store_copy, copy_digest_before y mcp) y tests/test_mcp_extension.py completo. El SpecDoc que produce SpecSync se identifica por el id del YAML (class.sldb-models). Si su ruta indexada o su payload no cumplen lo que espera la prueba que lee la spec (store / core / documents / SpecDoc / <SPEC>.yaml, con path y content_hash), se ajusta la prueba para leer los datos del store temporal, sin relajar ninguna aserción sobre lo que devuelve el servidor (found, store, address, path, version y payload). Si SpecSync no puede construir el store fuera de un repo git, o falta algo de sldb.api, detenerse y reportarlo: no se crea un store a mano ni se fabrican documentos. Sin mocks: el store temporal es un store sldb real, creado con la API pública. Comandos desde la raíz de IR con TMPDIR=/dev/shm y el .venv del repo. Precisiones (bundle-1): (a) el store de specs lo construye una función auxiliar build_spec_store(tmp_path_factory) -> Path, llamada desde un fixture de sesión spec_store, en un directorio de tmp_path_factory.mktemp("spec-store") que queda fuera de la copia montada (root). Devuelve la ruta de su .sldb. (b) mount_copy recibe ese .sldb como parámetro nuevo (spec_store: Path), y sus llamadores (store_copy y los demás que lo usen) lo reciben del fixture spec_store. Así se enlaza con sldb stores add <ruta>/.sldb --name spec2viz --store .sldb usando como cwd la copia montada (la variable root de mount_copy). (c) La prueba que lee la spec pide el fixture spec_store y lee de ahí el SpecDoc indexado, en lugar de FEDERATED[SPEC_STORE]. SPEC_STORE sigue siendo "spec2viz" como alias. (d) Para el chequeo de que nada se toca: federated_digest sigue cubriendo los stores de FEDERATED (solo deskops). El store de specs se digiere con tree_digest(spec_store) más el sha256 de cada archivo .md bajo su proyecto (spec_store.parent, recorrido con rglob, porque no es repo git). Ese digest se toma antes de la sesión MCP y se compara después, en las mismas pruebas que hoy comparan federated_digest u original_digest.

## Validation

_List the checks required before this task can close._

- grep -nE 'WORKSPACE / "spec2viz"|\.\./spec2viz' tests/conftest.py tests/test_mcp_extension.py no encuentra nada.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mcp_extension.py sale con rc 0, sin skipped, y test_a_spec_of_the_linked_spec2viz_store_is_read_through_the_server pasa.
- git diff --stat muestra, fuera de desk/, .sldb/ y runs/, solo tests/conftest.py y tests/test_mcp_extension.py.
- Suite completa una vez, bajo flock /dev/shm/sldb1-tests.lock, con el comando SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/ que sale con rc 0.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

Ninguna prueba de IR lee ni enlaza ../spec2viz/.sldb. La lectura de una spec de un store enlazado por MCP se sigue probando contra un store temporal construido desde la fixture de IR, el chequeo de que los stores no se tocan lo cubre, y la suite completa pasa.
