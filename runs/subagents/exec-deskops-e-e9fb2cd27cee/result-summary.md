# Resultado IR09 (exec-deskops-e-e9fb2cd27cee)

run_id: exec-deskops-e-e9fb2cd27cee
session: no disponible (sin ruta de sesión hija expuesta al ejecutor)
session_sha256: no disponible

Commit en la rama deskops/deskops-e-e9fb2cd27cee (sin push). Archivos:
- src/specir/extract/react_tsx.py (nuevo): reglas React/HTTP sobre facts; un solo mapeo para .ts/.tsx/.js/.jsx.
- src/specir/extract/__init__.py: `extract_frontend(root, store)`.
- src/specir/extract/plan.py: prefijos de nombre para InterfaceControlDoc/InterfaceActionDoc (firma sin cambios).
- tests/extract/test_frontend_extraction.py (nuevo, 11 pruebas).
- tests/fixtures/blog_frontend/ (PublishButton.tsx, api/client.ts openapi-fetch, api/legacy.js) y tests/fixtures/blog_frontend_gaps/ (huecos: template URL con axios.get, DELETE /posts/archive ausente).

Validación (validation.log): pytest tests/extract tests/models/test_blog_chain.py tests/test_imports.py rc 0 (43 passed, 2 xfailed); grep prohibido rc 1 (nada); deskops graph missing rc 0.

Para revisar:
- La regla `sldb rules check` marca error a una acción sin invokes, por eso los huecos/brechas viven en un fixture aparte (blog_frontend_gaps), copiado solo en esa prueba; el fixture principal pasa edges/rules sin errores.
- handlePublish (nested arrow) no es fact: sldb incluye sus llamadas en el componente; se usa eso solo si el componente tiene un único handler que no es fact; si no, not_derived.
- handlePublish llama además a publishLegacy (.js, POST literal) para que el .js se mapee; ambos llevan a la misma arista (dedupe; anclas de la primera llamada).
- Llamada no-HTTP sin nombre único en los facts del frontend va a not_derived (literal del punto d); puede dar ruido.
- El venv necesitó tree-sitter-* y mcp instalados a mano (extras de sldb).
