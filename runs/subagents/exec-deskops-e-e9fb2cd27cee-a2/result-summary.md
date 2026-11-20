# Intento 2 — IR09 (fetch como hueco declarado)
run_id: exec-deskops-e-e9fb2cd27cee-a2
session: (claude, sesión del ejecutor; sin archivo de sesión hijo)
session_sha256: n/a

- `src/specir/extract/react_tsx.py`: `_is_hole` es true para toda llamada cuyo último segmento es `fetch` (también con URL literal); su motivo va a not_derived ("fetch no da el método en los facts (hueco declarado)").
- Fixture nuevo en `tests/fixtures/blog_frontend_gaps`: `src/FetchButton.tsx` y `src/api/fetcher.ts` (`fetch("/posts")`).
- `tests/extract/test_frontend_extraction.py`: prueba que el fetch literal va a not_derived y que su acción (handleLoad) existe sin invokes.
- Validación: pytest tests/extract tests/models/test_blog_chain.py tests/test_imports.py -> 44 passed, 2 xfailed, rc 0 (validation.log). El grep de prohibidos no devuelve nada.
