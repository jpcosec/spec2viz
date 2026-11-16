# Informe del worker IR13d

Tarea: `task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual`, directo en IR main, sin push.

## Commits

| sha | Qué |
|---|---|
| `354a753` | Código: `src/specir/cli.py`, API en `specir.visual`, `commands.py` sin `main` provisional, script `specir` → `specir.cli:main`, `skills/use-specir/SKILL.md`, `docs/spec2viz/correspondencia-cli.md`, matriz y pruebas (`test_cli.py`, `test_api.py`, `test_packaging.py`; cinco pruebas de IR12 importan `main` de `specir.cli`). |
| `abbed7e` | desk: precisiones de preflight-2 y bundle-2 en el Implementation Path, `files` de la tarea, reviews preflight-2 y bundle-2 dispuestas como `accepted`. |
| `ab08aa1` | closeout resolved-by (refs `354a753` y `abbed7e`; tests `tests/visual/test_cli.py`, `test_api.py` y `test_packaging.py`). |

## Comando `specir` (src/specir/cli.py)

- `diagram`: render, validate, lint y schema (los grupos de IR12, montados).
- `catalog`: schema (IR12) y **build** (nuevo). `build` tiene las opciones de spec2viz y además `--annotations`, `--sldb-url <url>` y `--annotations-doc <id>`, que pasan un `AnnotationsTarget` de IR13b. Con `--annotations` solo, la página toma el servidor de su URL.
- Alias de primer nivel: `render`, `validate`, `lint`, `schema` y `build`. Usan los mismos helpers y los mismos parámetros que su comando de grupo.
- `about`: muestra el store que hay sobre el directorio actual, el flujo a HTML con comandos de specIR y los comandos de sldb para el store y las anotaciones (incluido `sldb models add …CatalogAnnotationsDoc`).
- Ayuda raíz con la taxonomía. También funciona `python -m specir.cli`.
- **Sin comando en specIR** (equivalente: el comando de sldb, por la regla de JP):
  - los subgrupos `notation` y `palette`;
  - `diagram sync`, `from-graph` y `generate`;
  - `catalog sync`, `validate` y `serve`.

  Una prueba comprueba que specIR no define ninguno de ellos.

## API pública (`specir.visual`)

Se añadió lo que faltaba de lo que exportaba spec2viz:

- `render`, `RENDERER_MAP`, `EXT_MAP` y `DEFAULT_RENDERER`;
- `render_to_file`, `with_provenance`, `provenance_header` y `provenance_text`;
- `json_schema` y `write_json_schema`.

Además se exportan `lint_mermaid`, `assert_mermaid_ok`, `MermaidLintError`, `render_catalog`, `build_catalog` y `AnnotationsTarget`. Se mantienen todas las exportaciones de IR11.

`load` y `validate` de spec2viz **no** se reexportan: son `sldb.api.notations.load_spec` y `validate_spec` (SV-J01). `test_every_public_name_of_spec2viz_has_its_equivalent` lee el `__init__` de spec2viz y comprueba cada nombre.

## Decisión SV-K16 / SV-K29

sldb aún no tiene un comando que valide un spec. Está pedido en la nota de su inbox `20261115-192054-…validar-una-notación-una-paleta-o-un-spec…`. `sldb validate` no sirve: valida contra un modelo, sin despachar por tipo de diagrama ni hacer la validación semántica.

Decisión:
- `specir diagram validate` y el alias `specir validate` quedan **provisionales** en specIR. Solo llaman a `load_spec`/`validate_spec` de sldb y no redefinen nada.
- Cuando sldb publique su comando, se retiran, la cabecera de procedencia pasa a nombrar el comando de sldb y la fila pasa a «usar sldb directamente».

Queda registrado en la fila SV-K16 de la matriz, en el pendiente 3 (marcado como decidido) y en la correspondencia. No envié notas nuevas a sldb.

## Habilidad

`skills/use-specir/SKILL.md` reemplaza a use-spec2viz y sigue su formato. Incluye:
- una tabla de qué es de specIR y qué es de sldb;
- la taxonomía y el contrato de los 9 renderers;
- el flujo a HTML;
- las anotaciones con `sldb serve`;
- la API Python;
- la validación.

Las pruebas comprueban la habilidad así:
- `test_the_skill_names_only_commands_that_exist` extrae cada `specir …`/`sldb …` (de los bloques de código y del código en línea) y lo invoca con `--help`, verificando que las opciones que nombra aparecen en la ayuda.
- `test_the_skill_names_no_spec2viz_command` comprueba que no nombra ningún comando de spec2viz.

## Correspondencia (`docs/spec2viz/correspondencia-cli.md`)

Tiene una fila por SV-K01 a SV-K30.
- `test_the_table_covers_exactly_the_command_tree_of_spec2viz` compara la tabla con el árbol de la CLI de spec2viz, leído de su fuente.
- `test_every_equivalent_of_the_table_answers_its_help` invoca cada equivalente. Los comandos de sldb corren como proceso aparte. `load_notation` y `load_palette` (SV-K21 y K26 no tienen comando en sldb) se llaman sobre cada builtin.

## Pruebas (TMPDIR=/dev/shm, una por archivo)

| Archivo | rc | Resultado |
|---|---|---|
| tests/visual/test_cli.py | 0 | 44 passed |
| tests/visual/test_api.py | 0 | 31 passed (los 27 de test_api de spec2viz más 4 propios) |
| tests/visual/test_packaging.py | 0 | 3 passed (con instalación en venv limpio: wheel + sldb, sin spec2viz; `--help`, `about`, `render` y `validate` arrancan; `import spec2viz` falla) |
| tests/visual/test_render_commands.py | 0 | 33 passed |
| tests/visual/test_schema.py | 0 | 13 passed |
| tests/visual/test_lint_mermaid.py | 0 | 8 passed, 7 skipped (mmdc) |
| tests/visual/test_render_cases.py | 0 | 27 passed, 3 skipped (mmdc) |
| tests/visual/test_bpmn.py | 0 | 26 passed |
| tests/test_imports.py | 0 | 9 passed |
| tests/visual/test_visual_names.py | 0 | 4 passed |
| tests/test_matriz_cobertura_spec2viz.py | 0 | 5 passed |
| tests/visual/test_resources.py | 0 | 7 passed |
| **tests/ completo, `-n 4`** | **0** | **629 passed, 10 skipped (mmdc), 3 xfailed** (segunda corrida) |

La primera corrida completa dio rc 1, con 1 fallo: `test_visual_projections.py::test_a_composed_view_projects_like_a_projection_view` (`ViewDoc:post-persistence is not in the store`). Es el flake de IR11 que ya informó IR12. La máquina estaba cargada con un `sldb bench` ajeno. El archivo solo pasó 2 de 2 veces (9 passed) y la segunda suite completa salió limpia. Durante las corridas no se tocó desk.

La prueba de venv limpio instala primero desde la caché de uv (`--offline`). Si falta algo, instala desde la red, como pasó la primera vez porque `click` no estaba en caché. Si no hay ni caché ni red, se salta con el motivo.

## graph missing

3 (rc 1 por haber faltantes; antes eran 7). Los 4 de IR13d desaparecieron. Los 3 que quedan son de IR13 (`acta-de-retiro.md` ×2 y `test_retirement_gate.py`).

## Limpieza

- Borré todo lo mío en /dev/shm: `ir13d-*` (logs, textos del Implementation Path, el script de la matriz y los basetemps `ir13d-bt/`). También borré `pytest-of-robocop/pytest-47`, la basetemp de una corrida de test_cli que corté (comprobé que solo tenía mis casos).
- No toqué nada ajeno: ni el resto de `pytest-of-robocop` ni `pytest-current`.
- No toqué el RoleDoc/RuntimeProfileDoc de la otra sesión.

## Pendientes para IR13 y otros

1. **IR13**: marcar como cumplidas las filas SV-J02, J03, J07, J08, J09 y SV-K01 a K30, más la parte de comando de SV-G01. Ya citan las pruebas de IR13d.
2. **sldb**: el comando de validación de spec, notación y paleta (nota del 20261115-192054). Cuando exista hay que:
   - retirar `specir diagram validate`/`validate`;
   - cambiar `COMMAND` y la cabecera de `render_file.py`;
   - actualizar la correspondencia, la habilidad y SV-K16, K21, K26 y K29.
3. **Observación**: antes de pasar a configs en tmp, una prueba construía el catálogo con `tests/visual/fixtures/catalog/examples/catalog/project.yml`. Dentro del repo IR, eso tardó varios minutos con CPU al 100 %. Parece que la búsqueda del store o de los átomos sube hasta el `.sldb` de IR. Las pruebas de paridad de IR13b no lo notaron. Conviene medirlo en IR13 o por parte del dueño de IR13b, porque afecta a `specir catalog build` cuando se ejecuta dentro de un repo con un store grande.
4. Instalar la habilidad en otros repos y migrar consumidores (deskops, pron, graph_ui) queda fuera de alcance; es de IR13.
