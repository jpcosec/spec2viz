PASA

# IR10 — resultado del tester (run-deskops-t-9ff404e7928e)

- Tarea: `task-ir10-reglas-semánticas-y-análisis-de-impacto`
- Commit del ejecutor: `c7f16bd520f99f32cbcf7ee452201a8986cdb64f` — *IR10: reglas semánticas entre capas y análisis de impacto (specir_rules, specir_impact)*
- Archivos: `src/specir/data/{relation_types.yaml,rules.yaml}`, `src/specir/impact.py`, `src/specir/mcp_extension.py`, `src/specir/models/{__init__.py,domain.py}`, `tests/models/{test_domain_models.py,test_rules_and_impact.py}`, `tests/test_mcp_extension.py`
- Entorno: worktree limpio detachado en `c7f16bd`; `PYTHONPATH` a su `src`, `TMPDIR=/tmp`. Evidencia en `validation.log`.

## Pruebas

| Archivo | Resultado |
|---|---|
| `tests/models/test_domain_models.py` | **7 passed** (10.41 s) |
| `tests/models/test_rules_and_impact.py` | **14 passed** (17.56 s) |
| `tests/test_mcp_extension.py` | **11 passed** (117.08 s) |
| `tests/models/test_domain_tools.py` (regresión) | **5 passed** (12.89 s) |
| `tests/models/test_blog_chain.py` (regresión) | **7 passed, 2 xfailed** (16.02 s) |

## Validation de la tarea

| Comprobación | Resultado |
|---|---|
| Cada regla tiene su brecha sembrada y se reporta con severidad, regla y documento | **PASS**. `test_a_seeded_gap_is_reported_with_its_severity_rule_and_document` cubre las seis brechas de cadena; `test_an_interface_field_the_serializer_lacks_is_reported` cubre el campo de interfaz. Cada hallazgo trae `severity`, `rule`, `subject`, `address`, `path` y `what`. |
| El grafo completo del blog no reporta hallazgos | **PASS**. `test_the_complete_chain_has_no_findings` exige `findings == []` y `total == 0`. |
| `TableDoc:posts` con `field=status` devuelve PublishButton con el camino completo | **PASS**. Devuelve `InterfaceControlDoc:publish-button` con la cadena `publish-button → publish-action → publish-post-endpoint → publish-handler → publish-post → posts` y las relaciones `triggers, invokes, handled_by, executes, writes`. |
| Cada tramo lleva procedencia y una relación inferida se señala | **PASS**. Cada arista trae `relation_doc`, `origen`, `verificacion` y `sldb_provenance`; `path.inferred` es `true` solo cuando la arista es `inferido`. |
| Las tools no escriben en el store | **PASS**. `test_rules_and_impact_write_nothing_and_propose_nothing` compara `tree_digest(blog_root)` antes y después de ambas tools. |
| Ninguna respuesta incluye parche ni modificación propuesta | **PASS**. La misma prueba recorre las respuestas y rechaza `fix`, `patch`, `diff`, `proposal`, `suggestion` y `changes`. |
| specIR no recorre el grafo por su cuenta | **PASS**. `impact.py` solo llama a `sldb.api.graph.graph_path(..., explain=True)`; la prueba no encuentra BFS/DFS/networkx/deque ni vecinos propios. |

## Alcance y guardrails

- El commit solo toca `src/specir/**` y sus pruebas; no modifica otros repos.
- Las reglas son `RuleDoc` sembrados desde `specir/data/rules.yaml` y evaluados con `sldb.api.rules_check`; el impacto usa solo API pública de sldb.
- `specir_rules` y `specir_impact` se registran con `server.add_tool(..., annotations=READ_ONLY)` y están disponibles desde nivel 0.
- No hay mocks ni documentos escritos a mano en las pruebas: usan el store temporal del blog creado por `tests/models/blog.py`.
- `git diff --check` del commit: limpio.

## Observación no bloqueante

El impacto usa `graph_path(..., explain=True)` y no `graph_paths`. La Validation pide *el camino* que justifica cada afectado (singular) y `graph_path` lo entrega explicado, con todos los tramos y su procedencia; por eso la verificación conductual queda cumplida. Si el coordinador exige literalmente el uso de `graph_paths`, sería una precisión de implementación, no un fallo de las comprobaciones de esta tarea.
