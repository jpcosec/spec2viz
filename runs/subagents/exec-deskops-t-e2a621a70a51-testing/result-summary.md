FALLA

# Resultado del tester (IR09: extractor React/TSX y contratos de API)

- task: `task-ir09-extractor-estático-react-tsx-y-contratos-de-api`
- commit del ejecutor: `6a9bbdd0bc07a22bbff1bd7df7f781dbd8fa5f76` — *IR09: extractor estático React/TSX y contratos de API sobre facts de sldb*
- archivos del commit: `src/specir/extract/react_tsx.py` (nuevo), `src/specir/extract/__init__.py`, `src/specir/extract/plan.py`, `tests/extract/test_frontend_extraction.py` y los fixtures `tests/fixtures/blog_frontend/` y `tests/fixtures/blog_frontend_gaps/`.
- Las pruebas se corrieron en un worktree limpio en `6a9bbdd` (`/tmp/ir09-clean`, `PYTHONPATH=/tmp/ir09-clean/src`), no sobre el árbol de trabajo sucio, para no mezclar cambios ajenos en curso.

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/extract tests/models/test_blog_chain.py tests/test_imports.py` | **43 passed, 2 xfailed**, rc 0 (101,11 s). Incluye las 11 pruebas nuevas y las 16 de IR08. |
| `TMPDIR=/tmp ... tests/extract/test_frontend_extraction.py` de a uno | **11 passed**, rc 0. |
| `grep -rnE "tree_sitter\\|import ast\\|from ast\\|pglast\\|read_bytes\\|read_text\\|sldb\\.code\\b\\|spec2viz" src/specir/extract` | rc 1: sin coincidencias. specIR no trae analizador propio. |
| `deskops graph missing --root .` | rc 0: «No missing graph references found.». |
| Fixture con `.ts`, `.tsx` y `.js` mapeados por el mismo código, anclas, procedencia, idempotencia, `edges check` y `rules check` | Cubierto por las 11 pruebas y en verde. El fixture principal produce `PublishButton`, `PublishAction`, `triggers` e `invokes` a `POST /posts/{id}/publish`. |

## Discrepancia bloqueante: `fetch` canónico con URL literal no va a `not_derived`

La precisión (c) del encargo dice: «fetch(...) va a not_derived porque el método no está en los facts». La implementación no lo cumple cuando `fetch` lleva una URL literal:

- `src/specir/extract/react_tsx.py:40-45` (`_is_hole`) solo considera hueco a `fetch` si **además** la llamada no es canónica o su `first_arg` no es un literal que empieza por `/`:
  ```python
  return (verb or last(call["name"]) == "fetch") and not (
      call.get("canonical") and isinstance(first, str) and first.startswith("/")
  )
  ```
- Para `{name: "fetch", first_arg: "/posts/{id}/publish", canonical: true}` la segunda condición es `False`, así que `_is_hole` devuelve `False`. En `_call`, al no ser una llamada HTTP (el método no está en los facts) y estar en profundidad 1, la llamada se descarta **sin añadir nada a `not_derived`**.

Reproducción con facts reales de sldb, sobre una copia temporal del fixture real (`blog_app` + `blog_frontend`): se añadió un `src/api/probe.js` con

```js
export function probePublish() {
  return fetch("/posts/{id}/publish");
}
```

y un `ProbeButton.tsx` cuyo handler llama a `probePublish` (el mismo patrón de seguimiento de un nivel de la precisión (d)). `extract_frontend` devolvió `not_derived` vacío, creó la `InterfaceActionDoc` de `handleProbe` sin `invokes` y `sldb rules check` salió con rc 1:

```
error rules/rule-specir-action-invokes-an-api-operation InterfaceActionDoc:action-frontend-src-probebutton-probebutton-handleprobe
```

Es decir: el caso más habitual de `fetch` (URL literal dentro de una función de cliente del proyecto) se pierde en silencio, en vez de quedar como hueco declarado «fetch no da el método en los facts». El fixture entregado no tiene ningún `fetch`, por eso las 11 pruebas no lo detectan.

**Corrección esperada:** tratar cualquier llamada cuyo último segmento sea `fetch` como hueco (siempre true en `_is_hole`), con su motivo, y añadir una prueba con un `fetch` de URL literal (por ejemplo en `blog_frontend_gaps` o en la prueba de comparación de la ruta).

## Nota sobre el árbol de trabajo actual

En `/workspace/IR` hay cambios no commitados ajenos a IR09 (`src/specir/mcp_extension.py`, `tests/test_mcp_extension.py`, `tests/test_mcp_undo.py` y documentación de desk). Con ellos, `tests/models/test_blog_chain.py::test_an_agent_does_not_verify_through_the_mcp` falla porque el test antiguo espera `is_error` y la implementación en curso devuelve un rechazo `domain`. En el commit `6a9bbdd` esa prueba pasa; no es un defecto del trabajo del ejecutor.

## Veredicto

**FALLA** por la precisión (c): el extractor no declara como `not_derived` un `fetch` canónico con URL literal y puede dejar una acción sin `invokes` (y una regla de nivel error). Las demás validaciones del encargo, incluidas las 43 pruebas, pasan.
