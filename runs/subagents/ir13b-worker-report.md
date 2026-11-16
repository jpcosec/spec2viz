# Informe del worker IR13b

Tarea: `task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos`, hecha directo en IR main y sin push.

## Commits

| sha | Qué |
|---|---|
| `2d28453` | Código: `specir.visual.catalog`, `templates/annotations-sldb.js`, pruebas, fixtures de catálogo, matriz y pyproject. |
| `67a7af4` | desk: precisiones de preflight y de bundle en el Implementation Path, `files` de la tarea, y las reviews preflight-2 y bundle-2 dispuestas como `accepted`. |
| `55e7f91` | closeout resolved-by: refs `2d28453` y `67a7af4`. Tests: `tests/visual/test_catalog.py`, `test_catalog_parity.py`, `test_catalog_annotations.py` y `tests/test_imports.py`. |

El commit `5b8ce32`, que quedó entre medio, no es mío. Lo hizo otra sesión y agrega el rol del ejecutor y el runtime scion.

## Qué quedó en sldb y qué en specIR

**En sldb**, usado directo y sin envoltorio:
- La regla de rutas del catálogo (`sldb.api.notations.catalog_paths`).
- `catalog_entries`, `check_catalog` y `sync_catalog`, más la CLI `sldb notations sync --catalog [--check]`. Reemplazan a `catalog validate` y `catalog sync`.
- `resolve_view`, `SpecSync` y `find_store`.
- Todo `sldb.api.matching` (D4): `raw_atoms_by_view`, `build_explicit_atoms`, `build_explicit_refs`, `attach_atom_edges`, `filter_atoms_payload`, `build_coverage_by_view`, `StoreReader`, `SpecView` y `UnknownAtomError`.
- `sldb serve` (`GET /document`, `POST /save`) para las anotaciones.

`tests/test_imports.py` comprueba dos cosas:
- specIR no define nada de esto (`test_specir_defines_no_atom_matching_and_no_catalog_path_rule`).
- La capa visual no levanta servidor HTTP (`test_the_catalog_runs_no_server_of_its_own`).

**En specIR** (`src/specir/visual/catalog/`), solo la parte visual:
- `loader`: el registro `vistas.yml`, los stores jerárquicos y `project.yml`, con anchors, tags y la inferencia de tipo y de proyecto.
- `sections`, `fragments` y `views`: el HTML de cada vista. Los tableros salen de la vista resuelta de sldb con el `view_mermaid` de IR12; si no, de su `src`.
- `atoms`: el adaptador de la vista a `SpecView` (con el descubrimiento del store de la vista y el límite de proyecto de spec2viz), `split_shared_atoms` y la inyección `window.*`.
- `annotations`: el modelo `CatalogAnnotationsDoc` (se registra con `add_model`), `AnnotationsTarget` y el script `templates/annotations-sldb.js`. El script lee con `GET /document` y guarda con `POST /save` usando `expected`. Si recibe un 409, mezcla con lo guardado y reintenta una vez.
- `build`: `render_catalog` y `build_catalog`. Si no se pasa `annotations`, la página es la de spec2viz.

**Lo nuevo frente a spec2viz:** `catalog serve` escribía `comentarios-arquitectura.json` junto al HTML. Ahora el HTML se abre como archivo y habla con `sldb serve --cors`. El servidor y el documento se fijan al construir o por la URL (`?sldb=<url>&annotations=<id>`).

**Quedan para IR13d:** el comando `catalog build`, el alias `build` y la opción de la CLI para las anotaciones.

## Tests (TMPDIR=/dev/shm)

| Archivo | rc | Resultado |
|---|---|---|
| tests/visual/test_catalog.py | 0 | 67 passed, 1 xfailed (estricto, ver notas a sldb) |
| tests/visual/test_catalog_parity.py | 0 | 29 passed (paridad viva con spec2viz) |
| tests/visual/test_catalog_annotations.py | 0 | 5 passed, contra un `sldb serve` real en puerto libre bajo `timeout` 120, cerrado en `finally` |
| tests/test_imports.py | 0 | 9 passed |
| tests/visual/test_visual_names.py | 0 | 4 passed (ORACLES incluye test_catalog_parity.py) |
| tests/visual/test_resources.py | 0 | 7 passed (la wheel lleva annotations-sldb.js) |
| tests/test_matriz_cobertura_spec2viz.py | 0 | 5 passed |
| tests/test_mcp_extension.py | 0 | 5 passed |
| **tests/ completo, `-n 4`** | **0** | **551 passed, 10 skipped (mmdc), 3 xfailed** |

La primera corrida completa dio 1 fallo en `test_mcp_extension.py::test_reading_through_every_tool_leaves_every_store_untouched`. Lo causé yo: dispuse la review bundle y edité la tarea con `deskops` mientras la suite corría, y esa prueba vigila que `.sldb` y `desk` del repo no cambien. Al repetir la suite sin tocar desk, rc fue 0.

Paridad (`test_catalog_parity.py`):
- **Validación:** `check_catalog` de sldb da la misma vista, spec, clase y mensaje de error que spec2viz sobre 14 registros:
  - las rutas faltantes y ambiguas;
  - las notaciones inexistentes, de otro tipo y las que solo están en el store;
  - el `vistas.yml` de spec2viz.
- **Sync:** el store queda con los mismos documentos que con spec2viz. Si una vista falla, ninguno de los dos escribe nada y ambos dan las mismas líneas `Invalid:`.
- **Página:** byte a byte igual a la de spec2viz sobre:
  - sus fixtures (`docs/architecture/vistas.yml`, `examples/catalog/`);
  - un proyecto sincronizado;
  - fuentes de todo tipo, con átomos y filtro por tags;
  - átomos explícitos, desconocidos y enlazados;
  - vistas resueltas;
  - stores de stores con overrides y fragmentos;
  - átomos y refs del store de una vista (store sldb real).

  La única diferencia declarada está en los avisos: son findings de sldb, no `{scope, message}`, y se comparan por su texto.
- **Modo estricto:** los dos lanzan `UnknownAtomError`.

Fixtures nuevos: `tests/visual/fixtures/catalog/`, copia de `docs/architecture/` (vistas.yml, specs, .mmd, .json) y de `examples/catalog/` de spec2viz 2de1056. Están fuera de `fixtures/spec2viz/` para no cambiar el CORPUS de IR11.

## Matriz

Las filas SV-G01 a SV-G08 y SV-I01 a SV-I05 citan las pruebas y las diferencias. Ninguna se marcó como cumplida: eso lo hace IR13.

## graph missing

7, igual que al empezar. En medio subió a 9 porque mis precisiones nombraban rutas de spec2viz; se reescribieron.

## Notas enviadas a sldb (sin commitear en sldb; las mete su coordinador)

1. `sldb/desk/inbox/20261115-214942-suggestion-ir13b-label-key-no-separa-y-normkey-del-cat-logo-s-matching-label-key-underscore.md`:
   - `label_key` conserva `_` (`\w`) y el `normKey` de la plantilla lo separa.
   - Efecto: un elemento sin label y con `_` en el id no encuentra su átomo explícito en el navegador. spec2viz tenía el mismo defecto.
   - En IR queda como xfail estricto: `test_label_key_of_sldb_splits_underscores_like_norm_key`.
2. `sldb/desk/inbox/20261115-215007-suggestion-ir13b-pide-exportar-desde-sldb-api-notations-...md`: pide reexportar desde `sldb.api.notations` lo siguiente:
   - `AmbiguousPathError`, `UnknownReferenceError` y `UnknownNotationError`;
   - `DEFAULT_NOTATIONS` y `builtin_notations`;
   - `resolve_catalog_path` y `split_fragment`.

   Mientras tanto, specIR los toma por `specir/visual/notation_style.py` (el único puente hacia `sldb.notations`) y por el submódulo `sldb.api.notations.catalog_paths`.

## Limpieza

- Borré todo lo que creé en /dev/shm: `ir13b-tmp/` (basetemps de todas mis corridas), los logs `ir13b-*.log` e `ir13b-implpath.txt`. No quedó ningún `specir-catalog-*`.
- No toqué `/dev/shm/pytest-of-robocop` ni nada ajeno.
- Los `sldb serve` de las pruebas se cerraron en `finally` y además corrían bajo `timeout`.

## Pendientes

1. **sldb:** las dos notas de arriba. Cuando se resuelvan, hay que quitar el xfail y cambiar los imports del puente.
2. **IR13d:** la CLI (`catalog build`, el alias `build` y la opción de anotaciones con `AnnotationsTarget`) y la exposición de `specir.visual.catalog` en la API pública.
3. **IR13:** marcar las filas como cumplidas. El catálogo no tiene goldens, así que tras retirar spec2viz la paridad queda acreditada por esta corrida (`2d28453`).
4. Nada pendiente sin commitear en IR: los cambios de `.scion/` y de `store_index.yaml` de otra sesión entraron en su commit `5b8ce32` y en el closeout.
