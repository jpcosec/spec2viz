# Result summary
run_id: exec-deskops-e-4b15df05b312
session: (Claude Code session, no child session file)
session_sha256: n/a

Commit en la rama deskops/deskops-e-4b15df05b312 (Task-Id incluido). Archivos:
- src/specir/extract/routes.py (nuevo): read_routes + extract_routes(yaml_path, store); valida method/route con ValueError que nombra la entrada; choque con ApiOperationDoc de otro origen -> ValueError sin escribir; campo stale_declared.
- src/specir/extract/plan.py: docstring de Planned.payload admite 'declarado' solo para ApiOperationDoc sin facts de extract_routes; asserts lo imponen (y prohiben inferido).
- src/specir/extract/write.py: ExtractionReport.stale_declared (campo nuevo; write_plan sin cambio de comportamiento).
- src/specir/extract/__init__.py: exporta extract_routes.
- tests/extract/test_declared_routes.py: (a)-(f).

Validacion: pytest de test_declared_routes.py + test_frontend_extraction.py: 20 passed (validation.log, exit 0; con -n 4).
Notas: (d) axios.post('/api/x') enlaza invokes; fetch(...) queda en not_derived (sin method en los facts). No se hizo el comando 'specir ux routes' (solo la funcion).
