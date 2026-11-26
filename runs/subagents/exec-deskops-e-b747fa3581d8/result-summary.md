# Result (intento 2)
run_id: exec-deskops-e-b747fa3581d8
session: n/a (executor Claude session, no child session file)
session_sha256: n/a

Cherry-pick de 4256522 sobre main (rama deskops/deskops-e-b747fa3581d8), commit d06e5a5, sin trailer Task-Id.
Conflictos resueltos conservando ambas entradas:
- src/specir/data/relation_types.yaml: accepted_by (CapabilityDoc) y depends_on.
- tests/models/test_domain_models.py: KINDS con CapabilityDoc y PieceDoc; tipos con accepted_by y depends_on; `present` pasa de 21 a 23 (depends_on + la regla sembrada).

Archivos del commit: src/specir/{cli.py,data/relation_types.yaml,data/rules.yaml,extract/__init__.py,extract/dependencies.py,extract/plan.py,extract/write.py,models/__init__.py,models/domain.py}, tests/fixtures/dep_pieces/**, tests/models/test_domain_models.py, tests/test_dependency_invariants.py.

Validación: tests/test_dependency_invariants.py + tests/models/test_domain_models.py: 12 passed.
Nota de entorno: el venv necesitó tree-sitter*, anyio, mcp, fastmcp y deskops además del indicado (sin ellos los hechos de código salen vacíos).
Pendiente conocido (del intento 1): los hechos de sldb no traen la línea del import; el hallazgo trae el archivo y "línea desconocida" (pedido a sldb por inbox).
