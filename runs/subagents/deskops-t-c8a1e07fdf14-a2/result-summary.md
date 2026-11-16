# Resultado del tester deskops-t-c8a1e07fdf14-a2 (IR13e, intento 2)

- Tarea: `task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb`
- Rol: tester. Run id: `run-deskops-t-c8a1e07fdf14-a2`. Session: `scion://agent/deskops-t-c8a1e07fdf14-a2`. session_sha256: no disponible (el runtime no expone el transcript).
- Contrato: `e14875086fa0666d1167e68b0083e15177e1d0395ce85f862640f6c6aafca8c8` (preflight-3 y bundle-2 aceptados).
- Estado verificado: IR `8940470` más los cambios sin commitear de la tarea. sldb `3c2186de` (instalado editable). spec2viz HEAD `91ba1d0`; las fuentes se leyeron con `git show b624b75:…`.
- Evidencia: `validation.log` (cada comando, su salida y su rc), `suite.log`, `retirement-check.txt`, `graph.txt`, `git-status.txt`, `acred-rows.txt`, `abiertas-matriz.txt`, `acta-deps.txt` y `check-deps.txt`.

## Veredicto por verificación

| # | Verificación | Veredicto | Evidencia |
|---|---|---|---|
| 1a | `tests/visual/test_notations_parity.py -rxXs` | **PASS** | 88 passed, 1 xfailed, 0 skipped, rc 0. El único xfail es `test_invalid_notations_are_rejected[changes1-not a spec2viz diagram type]`. |
| 1b | `tests/test_imports.py` | **PASS** | 9 passed, rc 0 |
| 1c | `tests/test_matriz_cobertura_spec2viz.py` | **PASS** | 5 passed, rc 0 |
| 1d | `tests/visual/test_retirement_gate.py` | **PASS** | 6 passed y 1 xfailed, rc 0. El xfail es el estricto del universo real, previo y esperado mientras el gate siga abierto. |
| 1e | `tests/visual/test_catalog.py -rxX` con `SPECIR_MMDC` | **PASS** | 68 passed, 0 xfailed, 0 xpassed, rc 0. Las pruebas de label_key pasan sin xfail. |
| 2 | Suite completa bajo flock, una vez (`free -g`: 14 GB disponibles) | **PASS** | 747 passed, 4 xfailed, rc 0, 311 s. Los 4 xfail son estrictos y conocidos: 2 de `test_blog_chain` (IR04), el de mindmap y el del gate real. No hay xpass ni fallos. |
| 3 | Greps de imports prohibidos | **PASS** | Los dos greps dan rc 1, sin coincidencias. De sldb, el archivo importa solo `sldb.api` y `sldb.api.notations`. El resto lo toma de `specir.visual.notation_style`. |
| 4 | `specir retirement check` | **PASS** | rc 1, el esperado. Lista 11 filas no acreditadas: SV-A17, H01, H03, K09, K16, K18, K21, K22, K23, K26 y K29. Son exactamente las 11 «abierta» de «Acreditación (IR13)» (diff vacío). No aparece ninguna fila cumplida. |
| 5 | `deskops graph missing --root .` | **PASS** | rc 0 |
| 6a | 42 portadas, cada una con su prueba de origen | **PASS** | 44 `def test_`: 42 portadas y 2 de comparación. Cuadra así: 3 (view_doc) + 12 de 14 (notation) + 10 de 11 (notation_view) + 2 (view_contract) + 15 de 16 (style_palette, contando e1 y e2) = 42. Las 6 excluidas son las CLI del scope. Cada docstring cita `spec2viz tests/<archivo>::<prueba>`. |
| 6b | 9 comparaciones «valida igual» | **PASS** | `test_spec2viz_notation_validates_the_same_as_the_sldb_builtin` cubre 8 notaciones con parametrize. `test_spec2viz_default_palette_validates_the_same_as_the_sldb_builtin` cubre la paleta. Las 9 comparan `model_dump()` con la builtin de sldb. |
| 6c | Expectativas sin suavizar; xfail estricto y con motivo real | **PASS** | Comparé las 42 una por una con `b624b75` y las aserciones son textualmente iguales. Solo cambian los imports. En `test_class_view_picks_glyphs…` queda únicamente la rama `relation_doc_has_attributes()`, la más exigente, y pasa. El xfail es `strict=True`. Reproduje el mensaje real de sldb: «diagram_type 'mindmap' is not a valid diagram type» (`sldb/src/sldb/notations/notation_spec.py:47`). La nota a sldb existe: `sldb/desk/inbox/20261116-022332-…`. |
| 6d | e1 y e2 | **PASS** | `test_notation_load_gives_typed_errors` tiene los 7 casos de `test_notation_validate_gives_typed_errors`, con las mismas mutaciones y clases y `pytest.raises(error)` sobre `load_notation`. `test_palette_check_is_typed` tiene los 6 casos de `test_palette_validation_is_typed`, con las mismas mutaciones, clases y patrones y `check_palette(PaletteSpec.model_validate(raw))` sobre la copia idéntica de `default.yml`. Ninguna usa CliRunner. Los docstrings dicen «parte no CLI». Pasan los 13 casos. |
| 6e | Fixtures idénticas a `b624b75` | **PASS** | `cmp` sin diferencias para las 8 notaciones y `palettes/default.yml`. El README es de una línea, con la revisión y la ruta. Las fixtures que ya existían y que usan las pruebas (`component.kinds/styled`, `deployment.*`, `activity.lanes`, `matrix.quotation-view` y 4 specs de `docs/architecture/spec2viz/`) también son idénticas a `b624b75`. |
| 6f | `notation_style.py` solo agrega reexportaciones | **PASS** | El diff solo agrega nombres al import de `sldb.notations` y a `__all__`, más un párrafo de docstring. No define nada nuevo. |
| 6g | Las 18 filas y la precisión (g) | **PASS** | Hay 12 cumplidas: E02, H02, H04, H05, H06, J06, K19, K20, K24, K25, G08 e I02. Todas sus pruebas pasan sin xfail. SV-H04 suma `test_palette_check_is_typed`. Hay 6 abiertas, cada una con su motivo: A17 (solo G5); H01 (suma `test_notation_load_gives_typed_errors`, pero la frena el xfail; nota 20261116-022332); H03 (solo G4: el HEAD `b868673` de graph_ui aún importa `spec2viz.notation_view`); K18 (falta K21 y K22); K22 (falta H03); K23 (falta K26). Las K dependientes siguen la precisión (c). El resumen da 94 cumplidas y 11 abiertas, lo mismo que el recuento de la tabla. |
| 6h | SV-H06 se sostiene con el contrato | **PASS** | Según la precisión (b), SV-H06 se acredita con 5 pruebas exactas, y las 5 pasan. La precisión (g) agrega pruebas solo a H01 y H04, no a H06. Las dos de mermaid corren contra `specir.visual.renderers.mermaid`, como autoriza (b). |
| 6i | El acta refleja la salida actual del comprobador | **PASS** | El bloque «Salida del comprobador (dependencias)» del acta coincide línea a línea con la salida actual (85 líneas, diff vacío). La cabecera dice rc 1, 85 dependencias y las mismas 11 filas. También es cierto que graph_ui tiene 48 rutas sin commitear y que su HEAD `b868673` importa spec2viz en `sldb_adapter.py:245`. |
| 6j | No se tocó nada fuera de los 5 del scope | **PASS** | Archivos con cambios: `notation_style.py`, la matriz, el acta, `test_notations_parity.py` y `fixtures/spec2viz-notations/`. El resto está en `desk/`, `.sldb/` y `runs/` (del coordinador), más `__pycache__/` y `src/specir.egg-info/`, que son artefactos de build sin rastrear. |

## Contexto del intento 2

- El XPASS de label_key está resuelto. `4dc8946` existe en IR y `test_catalog.py` da 0 xfail y 0 xpass. sldb `06dbcf02` es el arreglo.
- SV-H04 ya no se acredita sin la validación tipada no CLI, porque e2 está portada y pasa. SV-H01 la incorpora con e1 y sigue abierta solo por el caso mindmap.

## Discrepancias con el informe del ejecutor

No encontré ninguna de fondo. Todos los números del ejecutor coinciden con los míos: 88/1, 68 sin xfail, 94/11, 85 dependencias, las 11 filas y las 18 filas con su estado. Hay tres observaciones menores que no bloquean:
- La matriz cita «sldb `9307d485`» como revisión de la corrida de IR13e, mientras que el acta y la corrida actual usan sldb `3c2186de`. Es una inconsistencia de texto sin efecto: las pruebas pasan contra `3c2186de`.
- `src/specir.egg-info/` y los `__pycache__/` no están en `.gitignore` y aparecen en `git status`. Hay una tarea de gitignore en el inbox (8775c05). No hay que commitearlos.
- El ejecutor no corrió la suite completa, como estaba previsto. La corrí yo: rc 0.

## Pruebas obsoletas o faltantes

No hay. El único xfail nuevo es estricto, tiene motivo real y se reportó a sldb.

## Seguimiento antes del closeout

No hace falta nada en IR. SV-H01 espera la respuesta de sldb (nota 20261116-022332). SV-H03 y SV-K22 esperan el commit de graph_ui. SV-A17 espera G5.

## Veredicto final: **PASS**
