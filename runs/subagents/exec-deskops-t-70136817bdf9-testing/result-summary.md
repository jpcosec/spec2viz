PASA

# Tester — task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita

## Alcance probado

- Commit del ejecutor en `main`: `b3e387b` (acta) sobre `a124562` (retirement check). El branch original del
  ejecutor tenía `a918dfa` + `37d7a5d`, con el mismo contenido de docs/tests.
- Archivos del cambio: `docs/spec2viz/matriz-de-cobertura.md`, `docs/spec2viz/acta-de-retiro.md` y
  `tests/visual/test_retirement_gate.py`. No se tocó código de `src/specir`, así que no aplica ningún
  `tests/test_<modulo>.py` adicional.
- Entorno: `/workspace/IR`, Python del `.venv` (`3.13.18`), `TMPDIR=/tmp` y
  `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-70136817bdf9*` (temporales dentro del contenedor).

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `specir retirement check` con el universo declarado (graph_ui, deskops, pron, sldb, IR; stores: ninguno) | **rc 0** — `dependencies: 0`, `rows not accredited: 0`, `gate: passed` |
| Línea base del ejecutor (`baseline-retirement-check.txt`) | rc 1 — 19 dependencias de `spec2viz/.sldb` y `SV-A17: abierta` |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/visual/test_retirement_gate.py` | **7 passed**, rc 0 |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/test_matriz_cobertura_spec2viz.py` (extra, matriz) | **5 passed**, rc 0 |

Salida de la corrida real:

```
audited repos: graph_ui, deskops, pron, sldb, IR
audited stores: -
dependencies: 0
rows not accredited: 0
gate: passed, the retirement can be declared
```

## Cumplimiento del encargo

1. `spec2viz/.sldb` ya no está en la tabla «Inventario de consumidores»: `inventory()` devuelve
   `(['graph_ui', 'deskops', 'pron', 'sldb', 'IR'], [])` y el comprobador sale con rc 0.
2. `SV-A17` figura `cumplida` en «Acreditación (IR13)», citando G5 opción A (JP, 2026-11-16) y la salida
   del store del inventario el 2026-11-23.
3. El acta registra G5 y el punto 2 como hechos el 2026-11-23, con fecha y commit.
4. La prueba real `test_the_real_universe_has_no_dependency_and_every_row_is_accredited` ya no es
   xfail estricto y pasa (7 passed en el archivo del comprobador).

## Observaciones (no bloquean este encargo)

- Quedan menciones históricas/estado en G1 y G4 del acta y en la prosa histórica de la matriz («63
  dependencias», «1 fila abierta, SV-A17», punto 3 de «Lo que falta»). El propio ejecutor las deja
  explícitamente para la tarea de declarar el retiro (punto 3, coordinador), fuera del alcance de este
  encargo.
- El acta cita el commit `a918dfa` del branch original del ejecutor; en `main` el contenido equivalente quedó
  como `a124562` (el objeto `a918dfa` existe localmente, pero no es alcanzable desde `main`). Conviene que el
  coordinador, al declarar el retiro, cite el commit de `main` o verifique que el hash sea alcanzable.

## Veredicto

**PASA.** El comprobador real sale con rc 0, `SV-A17` está acreditada con G5 opción A, el acta registra el
punto 2 con fecha y commit, y los tests del comprobador pasan de a uno.
