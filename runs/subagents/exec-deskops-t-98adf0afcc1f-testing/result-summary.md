PASA

# Veredicto

El trabajo del commit `7314305e75895593732758da8489c449256f920d` cumple el encargo: una
capacidad es un `CapabilityDoc` de specIR con `audience`, su prueba de aceptación es un
`MaterializationContractDoc` enlazado por `accepted_by`, una regla de severidad `error` reporta
las capacidades sin prueba, y una `ViewDoc` sembrada lista capacidad, audiencia y test. Las ocho
capacidades de `docs/decisiones/paridad-por-capacidades.md` están en el store de specIR; 7 y 8
enlazan su test y sus anclas están intactas; 1 a 6 quedan reportadas como hallazgo (sin inventar
tests). El commit no lleva `Task-Id`, como pedía el encargo, y el plan de drawer marca el trabajo
anterior como reemplazado (con `deskops`, sin borrarlo).

# Pruebas ejecutadas

Se corrieron en un worktree limpio en el commit exacto del ejecutor, porque el árbol principal
está contaminado por el ciclo de vida de deskops posterior al commit (cambios en
`.sldb/core/models/TaskCodeDoc.yaml` y en el índice) que hacen fallar el fixture `check_store`
por `data_mutation` en cuatro `TaskCodeDoc` ajenos al cambio. Ese fallo no se reproduce en el
commit.

| Archivo | Resultado |
|---|---|
| `tests/test_capabilities_as_nodes.py` (validación exigida) | **8 passed** |
| `tests/models/test_domain_models.py` (módulo tocado) | **7 passed** |
| `tests/test_mcp_undo.py` (test tocado) | **8 passed** |
| `tests/test_mcp_extension.py` (test tocado) | 8 passed, **3 failed** por deriva del entorno |

Los 3 fallos de `tests/test_mcp_extension.py` son ajenos a este commit: el `sldb` actual expone
el tool `anchors_resolve`, que el test no incluye en `SLDB_READ`. Se reprodujo el mismo fallo en
el commit padre `1952fc6` (`test_the_write_tools_are_sldbs_own_and_the_extension_adds_a_validator_not_a_tool`).

# Evidencia de aceptación (cubierta por el test exigido)

- `CapabilityDoc` exige `audience` no vacía; `DomainOperationDoc` sigue sirviendo para operaciones
  extraídas de código.
- Las 8 capacidades de la tabla están en `.sldb` (`CapabilityDoc`), cada una con `audience`.
- La regla `rule-specir-capability-has-an-acceptance-test` reporta exactamente las 6 sin prueba,
  con severidad `error`.
- Las capacidades 7 y 8 tienen `accepted_by` a una materialización con
  `target_identity = tests/visual/test_api.py::test_validate_passes` y
  `tests/visual/test_cli.py::test_render_each_type`, respectivamente; `sldb anchors check`
  confirma sus anclas intactas.
- `view-specir-capabilities` lista las 8 con su audiencia y, cuando existe, su test; se siembra
  desde `src/specir/data/views.yaml` con `specir.install`.

# Observaciones

- El plan `desk/drawer/plans/paridad-por-capacidades/` quedó con el trabajo anterior en estado
  `replaced` y `replaced_by` apuntando a esta tarea, tanto en `README.md` como en `dag.yaml`.
- No se modificó código ni datos del repositorio durante la prueba; solo se crearon este resumen
  y `validation.log` en el directorio del tester.
