PASA

# Resultado del tester (IR09, intento 2: fetch literal como hueco declarado)

- task: `task-ir09-extractor-estático-react-tsx-y-contratos-de-api`
- commit del ejecutor: `6121f69f9da3b924875991a2f432886ad58e2a02` — *IR09: fetch con URL literal es hueco declarado en not_derived*
- archivos del commit: `src/specir/extract/react_tsx.py`, `tests/extract/test_frontend_extraction.py`, `tests/fixtures/blog_frontend_gaps/src/FetchButton.tsx` y `tests/fixtures/blog_frontend_gaps/src/api/fetcher.ts`.
- Las pruebas se corrieron en un worktree limpio en `6121f69` (`/tmp/ir09-clean`, `PYTHONPATH=/tmp/ir09-clean/src`), no sobre el árbol de trabajo sucio, para no mezclar los cambios ajenos en curso en `/workspace/IR`.

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `TMPDIR=/tmp ... pytest -q tests/extract/test_frontend_extraction.py` (de a uno) | **12 passed**, rc 0 (33 s). |
| `TMPDIR=/tmp ... pytest -q tests/extract` | **28 passed**, rc 0 (104 s). |
| `TMPDIR=/tmp ... pytest -q tests/models/test_blog_chain.py` | **7 passed, 2 xfailed**, rc 0 (14 s). |
| `TMPDIR=/tmp ... pytest -q tests/test_imports.py` | **9 passed**, rc 0. |
| Total de la validación (sin suite completa) | **44 passed, 2 xfailed**, rc 0. |
| `grep -rnE "tree_sitter\\|import ast\\|from ast\\|pglast\\|read_bytes\\|read_text\\|sldb\\.code\\b\\|spec2viz" src/specir/extract` | rc 1: sin coincidencias. specIR no incorpora analizador propio. |
| `deskops graph missing --root .` | rc 0: «No missing graph references found.». |

## Precisión (c) corregida

`_is_hole` ahora devuelve `True` para toda llamada cuyo último segmento es `fetch`, aunque `canonical` sea `true` y `first_arg` sea una URL literal; su motivo se añade a `not_derived`. La prueba nueva `test_a_fetch_with_a_literal_url_is_a_declared_gap_and_leaves_no_undeclared_action` usa `blog_frontend_gaps` y comprueba que el fetch literal (`src/api/fetcher.ts:2`) queda en `not_derived` con el motivo de hueco declarado y que la acción `handleLoad` existe sin `invokes` silenciosos.

Reproducción adicional del caso exacto que falló en el intento 1 (fetch canónico con URL literal que incluso casa con una operación existente): se añadieron a una copia temporal un `probe.js` con `fetch("/posts/{id}/publish")` y un `ProbeButton.tsx` cuyo handler llama a `probePublish`. `extract_frontend` devolvió:

```
frontend/src/api/probe.js:2 fetch: fetch no da el método en los facts (hueco declarado)
```

y no creó ningún `invokes` para `handleProbe`. El fallo original (llamada descartada en silencio) ya no ocurre.

## Nota sobre reglas y huecos declarados

En el store de huecos, una `InterfaceActionDoc` sin `invokes` sigue produciendo el hallazgo de nivel error `rule-specir-action-invokes-an-api-operation` si se ejecuta `sldb rules check` sobre ese store; es el comportamiento esperado de la regla y esos casos (fetch, URL no literal, endpoint ausente) quedan declarados en `not_derived`, que es lo exigido por el intento 2 («sin invokes sin declarar»). Sobre el fixture principal (`blog_frontend` + `blog_app`), la prueba `test_the_relations_pass_edges_and_rules_checks` pasa `sldb edges check` y `sldb rules check` sin hallazgos de nivel error.

## Veredicto

**PASA.** El caso que motivó el retorno a ejecución está corregido y cubierto por una prueba; las 44 pruebas de la validación pasan (2 xfailed), el grep de prohibidos no devuelve nada y `deskops graph missing` sale con rc 0.
