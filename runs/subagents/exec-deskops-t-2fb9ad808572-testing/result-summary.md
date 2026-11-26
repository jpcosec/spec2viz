PASA

# Resultado del tester (intento 2): dependencia entre piezas como dato de specIR y regla sembrada

- Tarea: `task-un-invariante-entre-piezas-se-escribe-como-regla-sobre-los-nodos-de-specir-y-la-regla-graph-ui-no-de`.
- Commit del ejecutor (intento 2): `d06e5a575d5c215dfaaeb582adcd8c41790c1d44` — *feat: depends_on between pieces, its extractor and the rule graph_ui does not depend on pron*. La rama `deskops/deskops-e-b747fa3581d8` fue publicada por el reap en `main` como `d1648af` (padre `2b6f546`); el contenido de código y tests es idéntico (`git diff --stat d06e5a5 d1648af` solo cambia run docs). Se valida el árbol final en `main`.
- Composición: `git cherry-pick 4256522` sobre `main` (que ya tenía `7314305`/CapabilityDoc); los dos conflictos se resolvieron conservando ambas entradas, en el orden main y después 4256522.
- El commit no lleva trailer `Task-Id` (`git log -1 --format=%B d1648af`): solo el asunto.
- Archivos: `src/specir/cli.py`, `src/specir/data/relation_types.yaml`, `src/specir/data/rules.yaml`, `src/specir/extract/{__init__.py,dependencies.py,plan.py,write.py}`, `src/specir/models/{__init__.py,domain.py}`, `tests/fixtures/dep_pieces/**`, `tests/models/test_domain_models.py`, `tests/test_dependency_invariants.py`.
- Entorno: `/workspace` (IR en `main` = `d1648af`), `.venv` del repo, Python 3.13.18, `PYTHONPATH=/workspace/IR/src:/workspace/deskops`, `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-2fb9ad808572*`.

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `pytest -q tests/test_dependency_invariants.py` en el árbol final de `main` | **5 passed**, rc 0 (62,7 s). |
| `pytest -q tests/models/test_domain_models.py` en el árbol final de `main` | **7 passed**, rc 0 (24,4 s). |
| Ambos archivos juntos sobre el commit del ejecutor (`d06e5a5`, worktree) | **12 passed**, rc 0 (49,0 s). |
| `pytest -q tests/extract/test_edge_name_bounded.py tests/test_cli_mcp.py tests/test_imports.py` | **17 passed**, rc 0 (24,6 s). |
| `pytest -q tests/test_extract_python_cli.py` | 6 failed, 3 passed; **idéntico en `7bd8595` sin el commit** (6 failed, 3 passed). Preexistente de entorno, no del cambio. |
| `pytest -q tests/extract/test_blog_extraction.py` | 8 failed; `interpret` produce exactamente los mismos nodos en `d06e5a5` y en `7bd8595` (StateDoc 2, TableDoc 1, DomainEntityDoc 1): faltan los hechos de rutas en este entorno, ajeno al commit. |
| `pytest -q tests/test_capabilities_as_nodes.py` | 5 errors en el fixture `check_store` (alertas de anclas de ReviewDocs); **los mismos errores en `7bd8595` sin el commit**: store del repo, no regresión. |

## Qué queda verificado

- `depends_on` en `src/specir/data/relation_types.yaml`: `PieceDoc -> PieceDoc`, `many_to_many`, `axis: WHAT`; la relación de procedencia de aristas (`rule-specir-edges-carry-their-provenance`) incluye `depends_on`.
- Conflicto resuelto conservando ambos: `relation_types.yaml` tiene `accepted_by` y después `depends_on`; `tests/models/test_domain_models.py` tiene `KINDS` con `CapabilityDoc` y `PieceDoc`, los tipos con `accepted_by` y `depends_on`, y `present == 23` (12 tipos + 10 reglas + 1 vista, comprobado por la prueba).
- Extractores: `specir.extract.extract_dependencies` y `specir extract dependencies ROOT` salen de `attrs.imports` y `attrs.nested_imports` de los hechos de módulo de sldb; solo imports absolutos, los relativos quedan dentro, los anidados/condicionales cuentan; la arista es `origen: observado`, `verificacion: sin_verificar` y `attributes.sitios` lista el archivo de cada import; si el import desaparece, `write_plan(..., retire="depends_on")` borra la arista observada no verificada.
- Regla sembrada `rule-specir-graph-ui-does-not-depend-on-pron` (`on_check`, `error`, `subject: model <= PieceDoc`, `where: title = "graph_ui"`, `condition: none(rel:depends_on: title = "pron")`).
- Las cinco pruebas de `tests/test_dependency_invariants.py` cubren el Done When: sin import no hay arista y la regla pasa; con import la arista queda observada con su sitio y la regla reporta `error` con sujeto `PieceDoc:piece-graph-ui`; quitando el import la arista se retira y la regla pasa; relativos no generan arista; anidados/condicionales sí; una dependencia no prohibida no se reporta.

Comprobación manual independiente sobre `tests/fixtures/dep_pieces` con el import añadido:

```
RelationDoc:edge-piece-graph-ui--depends_on--piece-pron
  PieceDoc:piece-graph-ui -> PieceDoc:piece-pron
  sitios: ['graph_ui/view.py (línea desconocida)']
  origen: observado, verificacion: sin_verificar
  anchors: ['code:graph_ui/view.py::']
rules check:
  level: error
  code: rules/rule-specir-graph-ui-does-not-depend-on-pron
  subject: PieceDoc:piece-graph-ui
  what: graph_ui depends on pron, ... | none(rel:depends_on: title = "pron") (seen: {"title":"pron"})
```

## Pendiente autorizado por la tarea

El hallazgo nombra la pieza y la prohibición, y la arista lleva el archivo, pero **no la línea** (`desconocida`) y el `what` del hallazgo no incluye `attributes.sitios`. La tarea lo autoriza si falta un predicado, pidiéndolo al inbox de sldb. Las dos carencias están pedidas por inbox y siguen abiertas:

- `sldb/desk/inbox/20261125-213716-suggestion-facts-de-import-sin-l-nea-y-reglas-on-check-sobre-aristas-sin-atributos.md`: los hechos de import no traen línea y una regla `on_check` no puede leer los atributos de la arista en el cuantificador.
- `sldb/desk/inbox/20261125-215901-suggestion-correcci-n-specir-no-lee-el-archivo-para-la-l-nea-del-import.md`: corrección de que specIR no lee código, así que no puede sacar la línea por su cuenta.

## Veredicto

**PASA.** El intento 2 parte de `main`, conserva ambas entradas en los dos archivos en conflicto, publica el trabajo sin `Task-Id` y las dos validaciones pedidas pasan en el árbol final (`5 passed` y `7 passed`; `12 passed` juntos sobre el commit). El único hueco frente al Done When —archivo y línea del import en el hallazgo— es el pendiente que la propia tarea permite dejar explicado cuando falta un predicado; está explicado y pedido al inbox de sldb.
