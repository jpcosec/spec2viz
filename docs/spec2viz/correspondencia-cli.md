# Correspondencia de la CLI de spec2viz con specIR y sldb

Tabla comando por comando de la CLI de spec2viz (revisión `2de1056`, filas SV-K de
`docs/spec2viz/matriz-de-cobertura.md`) con su equivalente. La escribe IR13d.

Regla (JP, 2026-11-15): lo genérico es de sldb y specIR es la capa visual y el mapeo de dominio. Si un
comando de spec2viz lo cubre un comando de sldb, specIR **no** lo duplica: el equivalente es el comando de
sldb y se usa directamente. specIR no envuelve la CLI ni la API de sldb.

- Comando de specIR: `specir` (script del paquete, `specir.cli:main`; también `python -m specir.cli`).
- Comando de sldb: `sldb` (paquete `structuredLanguageDB`, dependencia de specIR).
- La columna «Equivalente» se lee como código: `tests/visual/test_cli.py` extrae cada comando de esa columna
  y lo invoca con `--help` (los de sldb, como proceso aparte), y comprueba que cada opción nombrada aparece
  en la ayuda. Las funciones de la API de sldb (sin comando en sldb todavía) se invocan sobre una builtin.
- La prueba también comprueba que la primera columna cubre exactamente el árbol de comandos de spec2viz.

| ID | Comando de spec2viz | Modo | Equivalente | Prueba que lo invoca |
|---|---|---|---|---|
| SV-K30 | `spec2viz --help` | migrar tal cual | `specir --help` | test_help_mentions_taxonomy_groups_and_renderers |
| SV-K01 | `spec2viz about` | migrar tal cual | `specir about` | test_about_names_the_commands_of_specir_and_sldb |
| SV-K02 | `spec2viz build` | migrar tal cual | `specir build` | test_catalog_build_alias_matches_legacy_build, test_build_command* |
| SV-K03 | `spec2viz catalog` | migrar tal cual | `specir catalog` | test_help_mentions_taxonomy_groups_and_renderers |
| SV-K04 | `spec2viz catalog build` | migrar tal cual | `specir catalog build` | test_catalog_build_alias_matches_legacy_build, test_catalog_build_embeds_the_annotations_saver_of_ir13b |
| SV-K05 | `spec2viz catalog schema` | migrar tal cual | `specir catalog schema` | test_catalog_schema_stdout |
| SV-K06 | `spec2viz catalog serve` | reemplazar | `sldb serve --store --cors` | test_every_equivalent_of_the_table_answers_its_help; flujo completo en test_catalog_annotations.py (IR13b) |
| SV-K07 | `spec2viz catalog sync` | migrado a sldb | `sldb notations sync --catalog` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_catalog_parity.py (IR13b) |
| SV-K08 | `spec2viz catalog validate` | migrado a sldb | `sldb notations sync --catalog --check` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_catalog_parity.py (IR13b) |
| SV-K09 | `spec2viz diagram` | migrar tal cual | `specir diagram` | test_help_mentions_taxonomy_groups_and_renderers |
| SV-K10 | `spec2viz diagram from-graph` | migrado a sldb | `sldb notations from-graph --snapshot --store` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_sync_generation_parity.py (IR13a) |
| SV-K11 | `spec2viz diagram generate` | migrado a sldb | `sldb notations from-graph --python --output` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_sync_generation_parity.py (IR13a) |
| SV-K12 | `spec2viz diagram lint` | migrar tal cual | `specir diagram lint` | test_lint_alias_matches_diagram_lint; casos en test_lint_mermaid.py (IR12) |
| SV-K13 | `spec2viz diagram render` | migrar tal cual | `specir diagram render --renderer --backend --out` | test_render_* de test_render_commands.py (IR12) |
| SV-K14 | `spec2viz diagram schema` | migrar tal cual | `specir diagram schema --type --out` | test_schema.py (IR12) |
| SV-K15 | `spec2viz diagram sync` | migrado a sldb | `sldb notations sync --spec --notation --strict` | test_every_equivalent_of_the_table_answers_its_help; paridad en test_sync_generation_parity.py (IR13a) |
| SV-K16 | `spec2viz diagram validate` | migrado a sldb (provisional en specIR) | `specir diagram validate` | test_diagram_validate_valid, test_diagram_validate_invalid (ver la decisión de abajo) |
| SV-K17 | `spec2viz lint` | migrar tal cual | `specir lint` | test_lint_alias_matches_diagram_lint |
| SV-K18 | `spec2viz notation` | usar sldb directamente | `sldb notations` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K19 | `spec2viz notation list` | usar sldb directamente | `sldb notations list` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K20 | `spec2viz notation sync` | usar sldb directamente | `sldb notations sync --notation` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K21 | `spec2viz notation validate` | usar sldb directamente | `sldb.notations.load_notation` (API; sldb aún no tiene comando) | test_every_equivalent_of_the_table_answers_its_help |
| SV-K22 | `spec2viz notation view` | usar sldb directamente | `sldb notations view --store` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K23 | `spec2viz palette` | usar sldb directamente | `sldb notations` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K24 | `spec2viz palette list` | usar sldb directamente | `sldb notations list` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K25 | `spec2viz palette sync` | usar sldb directamente | `sldb notations sync --palette` | test_every_equivalent_of_the_table_answers_its_help |
| SV-K26 | `spec2viz palette validate` | usar sldb directamente | `sldb.notations.load_palette` (API; sldb aún no tiene comando) | test_every_equivalent_of_the_table_answers_its_help |
| SV-K27 | `spec2viz render` | migrar tal cual | `specir render --renderer --backend --out` | test_render_* (alias) de test_cli.py |
| SV-K28 | `spec2viz schema` | migrar tal cual | `specir schema --type --out` | test_schema_stdout, test_schema_outfile, test_schema_diagram_store_stdout, test_schema_invalid_type_fails |
| SV-K29 | `spec2viz validate` | migrado a sldb (provisional en specIR) | `specir validate` | test_validate_valid, test_validate_invalid, test_validate_all_types |

## Opciones de `catalog build` que cambian

- `--config`, `--out`, `--base-dir`, `--atoms-dir`, `--atoms-tag` y `--strict-atoms`: iguales que en spec2viz.
- Nuevas (IR13b e IR13d): `--annotations`, `--sldb-url <url>` y `--annotations-doc <id>`. La página guarda
  sus anotaciones en un `CatalogAnnotationsDoc` del store a través de `sldb serve --cors`. El modelo se
  registra en el store con sldb: `sldb models add specir.visual.catalog.annotations:CatalogAnnotationsDoc`.
  Esto sustituye a `catalog serve`, que las escribía en un JSON junto al HTML.

## Decisión sobre SV-K16 y SV-K29 (validar un spec por CLI)

- La lógica es de sldb (`load_spec` y `validate_spec` de `sldb.api.notations`, D3). sldb no tiene todavía
  un comando que valide un spec por ruta: está pedido en su inbox (nota
  `20261115-192054-suggestion-sldb-notations-validar-una-notaci-n-una-paleta-o-un-spec-por-nombre-o-ruta-desde-la-cli`,
  que también pide validar notaciones y paletas, SV-K21 y SV-K26).
- `sldb validate` no lo cubre: valida un documento o unos datos contra un modelo, sin elegir el tipo de
  diagrama ni hacer la validación semántica de `validate_spec`.
- Decisión (IR13d): mientras sldb no tenga el comando, `specir diagram validate` y su alias `validate`
  siguen en specIR. Solo llaman a `load_spec` y `validate_spec` de sldb y no redefinen nada. La cabecera de
  procedencia de las proyecciones nombra `specir diagram validate`.
- Cuando sldb publique su comando, `specir diagram validate` y `specir validate` se retiran, la cabecera
  pasa a nombrar el comando de sldb y esta fila pasa a «usar sldb directamente».
