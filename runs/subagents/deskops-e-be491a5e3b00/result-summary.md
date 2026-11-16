# IR13g: resultado del ejecutor deskops-e-be491a5e3b00 (intento 1)

Cambios solo en `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md` (`diff.patch`). Sin commit.

## Verificaciones de graph_ui
- `git -C ../UIs/graph_ui merge-base --is-ancestor 79d63ee HEAD`: rc 0 (HEAD `824c135`); `c9b09f7` también es ancestro.
- `git -C ../UIs/graph_ui grep -nE 'from spec2viz|import spec2viz|spec2viz>=' HEAD`: rc 0, pero todas las coincidencias están en `desk/` (notas, reviews, materializations) y `runs/` (evidencia de sus subagentes). Fuera de `desk/` y `runs/`: ninguna coincidencia. `pyproject.toml` y `.github/requirements-suite.txt` no mencionan spec2viz.
- `ci.yml` líneas 47 y 112 pasan `--src` a pip (el pendiente sin efecto que menciona la nota).

## Estados nuevos
- SV-H03: **cumplida**. Su único faltante era G4 de graph_ui, ya resuelto en `79d63ee`. `tests/visual/test_notations_parity.py` da 88 passed y 1 xfailed, y ese xfail es el de mindmap de SV-H01. Sus 13 pruebas (las 10 no CLI de test_notation_view, las 2 de view_contract_resolved y test_resolve_documents_is_public_and_filters_relations, 19 casos) dan 19 passed, sin xfail.
- SV-K22: **cumplida**. Solo dependía de SV-H03.
- SV-K18: **sigue abierta**. Depende de SV-K21; SV-K19, SV-K20 y SV-K22 ya están cumplidas.

## Resumen recontado
- Hay 96 cumplidas y 9 abiertas, de 105 filas.
- Las abiertas son SV-A17, H01, K09, K16, K18, K21, K23, K26 y K29.
- G1 sigue abierto y pasa a 9 filas. G2 no cambia.

## Matriz
- Tabla principal, filas de SV-H03, K18 y K22: nota «IR13g: …» al final de la columna Condición, con el formato de IR13d. La condición de IR07 no cambia.
- Acreditación: hay un párrafo nuevo de IR13g. Las filas de SV-H03 y K22 pasan a cumplidas y la Falta de SV-K18 queda «Depende de SV-K21». El resumen pasa a 96 y 9, y el estado de G1 también.
- El inventario de consumidores no se tocó.

## Acta
- La cabecera «Retiro: no declarado» pasa a 9 filas e incluye la historia de IR13g.
- Hay un bloque nuevo con la corrida de IR13g, con el formato del bloque de IR13f.
- G1: 96 cumplidas y 9 abiertas; IR13g acreditó SV-H03 y SV-K22.
- G4: ya no nombra a graph_ui como pendiente. Da el reparto de dependencias por repo y deja graph_ui y pron como resueltos.
- Consumidores, fila de graph_ui:
  - Dependencias: sigue el precedente de pron, «… (corrida del 2026-11-15); 0 desde la del 2026-11-16», precisando que en las de IR13e e IR13f era solo por su árbol sin commitear.
  - Cambio que lo resolvió: «resuelto», citando `79d63ee`, `c9b09f7` y la nota 20261116-131509, con la comprobación desde IR. Incluye el pendiente de `ci.yml` `--src`, que no cuenta como dependencia.
- Lo que falta: el punto 1 ya no nombra a graph_ui y el punto 3 quita SV-H03 y SV-K22.

## Corrida del comprobador
- Comando: `timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb`.
- Antes de editar (`retirement-check-antes.txt`): rc 1, 85 dependencias y 11 filas.
- Tras editar la matriz (`retirement-check.txt`): rc 1, 85 dependencias y 9 filas no acreditadas.
  - Las 9 filas son SV-A17, H01, K09, K16, K18, K21, K23, K26 y K29, y coinciden con las 9 abiertas de la matriz.
  - Dependencias por repo: IR 43, deskops 22, spec2viz/.sldb 19, sldb 1, graph_ui 0 y pron 0.
  - Las líneas de dependencia son idénticas a la salida del acta.
- HEADs: IR `3ec37f2`, sldb `b0e4f649`, graph_ui `824c135` (39 rutas sin commitear), deskops `aa25fdb0`, pron `39ea972` y spec2viz `91ba1d0`.

## Validación (validation.log)
- `git diff --stat` fuera de desk/, .sldb/ y runs/ muestra los dos documentos y, además, `tests/conftest.py` y `tests/test_mcp_extension.py`. Esos dos son cambios ajenos previos que el brief anuncia y no se tocaron.
- `pytest tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py` sale con rc 0: 11 passed y 1 xfailed. El xfail es el estricto del universo real, que es lo esperado.
- `deskops graph missing --root .` sale con rc 0.

## Pendiente
- La línea de G4 de la matriz («lista dependencias en graph_ui, deskops, pron, sldb…») está desactualizada para graph_ui y pron. El contrato solo pedía G1 y G2 en la matriz y IR13f tampoco la tocó, así que no la edité. Queda para quien lo decida.
- En el acta, los dos bloques anteriores de la corrida (IR13e e IR13f) se conservan como historia.
- El cierre, el commit y el tester independiente corresponden al coordinador.
