# Resultado del tester deskops-t-5a39cc2dfbf8 (IR13e, intento 1)

- Tarea: `task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb` (contract_sha256 `5efb8cf1a77ffacdc67e55685465f67f4b64fabd59a2d004f7bc2043c7542b59`)
- Rol: tester. Run: `run-deskops-t-5a39cc2dfbf8`. Sesión: `scion://agent/deskops-t-5a39cc2dfbf8`. session_sha256: no disponible desde dentro de la sesión.
- Revisiones: IR `37f41ee` más los cambios del ejecutor sin commitear; sldb `9307d485`; spec2viz `91ba1d0`. Entre `b624b75` y `91ba1d0`, `git diff` sobre `spec2viz/`, `tests/` y `docs/architecture/` sale vacío.
- Evidencia: `validation.log` (cada comando con su salida y su rc), `full-suite.log`, `retirement.out`, `spec2viz-tests.txt`, `ported.txt`, `deps-check.txt`, `deps-acta.txt`, `board.txt`, `task.txt`, `next.txt`, `graph.txt` y `git-status.txt`.

## Veredicto por verificación

| # | Verificación | Veredicto | Evidencia |
|---|---|---|---|
| 1a | `tests/visual/test_notations_parity.py -rxXs` | **PASS** | 75 passed, 1 xfailed, rc 0. Ningún skipped. |
| 1b | `tests/test_imports.py` | **PASS** | 9 passed, rc 0. |
| 1c | `tests/test_matriz_cobertura_spec2viz.py` | **PASS** | 5 passed, rc 0. |
| 1d | `tests/visual/test_retirement_gate.py` | **PASS** | 6 passed, 1 xfailed (el xfail estricto previo del universo real), rc 0. |
| 2 | Suite completa bajo el lock (`free -g`: 20 GB disponibles) | **FAIL** | **728 passed, 5 xfailed, 5 errors, rc 1.** Ver la sección «Suite completa». |
| 3 | Greps de imports prohibidos | **PASS** | Los dos greps salen con rc 1 (sin coincidencias). De sldb solo se importan `sldb.api` y `sldb.api.notations`, y `ViewDoc` viene de `sldb.api`. |
| 4 | `specir retirement check` | **PASS** | rc 1 (gate abierto, lo esperado): 119 dependencias y 13 filas no acreditadas (SV-A17, G08, H01, H03, I02, K09, K16, K18, K21, K22, K23, K26 y K29), **idénticas** a las 13 «abierta» de «Acreditación (IR13)». Ninguna fila cumplida aparece. Las 119 líneas de dependencias del acta son iguales a las de la salida (`diff` vacío). |
| 5 | `deskops graph missing --root .` | **PASS** | «No missing graph references found.», rc 0. |
| 6a | 40 portadas, cada una con su prueba de origen en el docstring | **PASS** | En b624b75, los 5 archivos de spec2viz tienen 46 pruebas. 40 están citadas en docstrings, todas distintas y todas existentes. Las 6 no portadas son exactamente las 6 de CLI del scope. Por archivo: 3, 12/14, 10/11, 2 y 13/16. |
| 6b | 9 comparaciones «valida igual» | **PASS** | Son 8 casos parametrizados de `test_spec2viz_notation_validates_the_same_as_the_sldb_builtin` y 1 de `test_spec2viz_default_palette_validates_the_same_as_the_sldb_builtin`. Comparan con `model_dump()`, como dispuso bundle-1. |
| 6c | Expectativas sin suavizar; xfail estricto y con razón real | **PASS** | Comparé cada prueba portada con el original de b624b75. Las aserciones son las mismas y solo cambian los imports. Hay una única adaptación: en `test_class_view…` se aserta solo la rama `relation_doc_has_attributes()` verdadera, que es la más estricta, y está anotada en el docstring. Hay un solo xfail, con `strict=True`, en `test_invalid_notations_are_rejected[changes1]`. Lo reproduje: sldb da «diagram_type 'mindmap' is not a valid diagram type» (`sldb/src/sldb/notations/notation_spec.py:47`). La nota existe en `sldb/desk/inbox/20261116-022332-…`. |
| 6d | Fixtures idénticas a `git -C ../spec2viz show b624b75:<ruta>` | **PASS** | Las 9 dan `cmp` idéntico. Las fixtures preexistentes que usan las pruebas (10 specs en `fixtures/spec2viz/` y `vistas.yml` del catálogo) también son idénticas a b624b75. |
| 6e | `notation_style.py` solo reexporta | **PASS** | El diff solo agrega nombres a `from sldb.notations import (…)`, al docstring y a `__all__`. No define nada nuevo. |
| 6f | 16 filas: cumplida solo si todas sus pruebas pasan sin xfail | **PASS** | Cumplidas: E02, H02, H04, H05, H06, J06, K19, K20, K24 y K25. Sus pruebas pasan sin xfail y cada K depende solo de filas cumplidas. Abiertas con motivo: A17 (solo G5), H01 (xfail y nota 20261116-022332), H03 (solo G4 de graph_ui), K18 (K21 y K22), K22 (H03) y K23 (K26). Resumen 92/13 (antes 82+10 y 23−10). |
| 6g | Nada tocado fuera de los 5 archivos del scope | **PASS** | Fuera de `desk/`, `.sldb/` y `runs/` solo cambian los 5 archivos del scope. También aparecen sin seguimiento `src/specir.egg-info/` y los `__pycache__/`, que son artefactos de instalación y ejecución, no fuentes (ver discrepancias). |

## Suite completa (verificación 2)

`SPECIR_MMDC=… TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/` terminó con **rc 1**: 728 passed, 5 xfailed y 5 errors. Los 5 errores son de setup, en todas las pruebas de `tests/test_mcp_extension.py`. El fixture `mount_copy` (`tests/conftest.py:70-83`) copia `.sldb`, `sldb` y `desk`, pero no `runs/`, y `sldb stores update` falla con:

```
Skipped missing documents: run-deskops-e-31500ac1cfa1, run-deskops-t-5a39cc2dfbf8
[warning] Sections rebuild: doc 'run-deskops-e-31500ac1cfa1' missing at …/IR/runs/subagents/deskops-e-31500ac1cfa1/run.md
```

Los dos RunDocs (`.sldb/core/documents/RunDoc/`, sin commitear) son del **coordinador**, de los despachos de ejecutor y tester. No vienen del trabajo del ejecutor.

Repro: copié `git archive HEAD` más solo los 5 archivos del ejecutor, sin el estado sin commitear de desk, `.sldb` y runs, a `/dev/shm`. Ahí `tests/test_mcp_extension.py` dio **5 passed, rc 0** (en `validation.log`). Un primer intento salió con rc 124 porque agotó el tope esperando el lock y nunca llegó a correr pytest. Borré la copia al terminar.

Conclusión: la entrega del ejecutor no rompe la suite. Aun así, la verificación tal como la pide el brief y la Validation de la tarea («la suite completa sale con rc 0» en el checkout) **no se cumple** en el estado actual del checkout.

## Discrepancias con el informe del ejecutor

1. El ejecutor no corrió la suite completa (lo declara: la deja al tester). Su informe no podía anticipar los 5 errores, que provienen de los RunDocs del coordinador.
2. Dice que `src/specir.egg-info/` «ya existía». El mtime del directorio es 2026-11-16 02:20:59 -0300 (05:20Z), dentro de la ventana de su ejecución. Pudo ser una reinstalación editable. No es una fuente, no está en el scope y no afecta al veredicto, pero el «ya existía» no se puede verificar.
3. Todo lo demás coincide con lo que verifiqué: los conteos (75/1, 40+9), las 16 filas, 13 no acreditadas y 119 dependencias, la nota a sldb, la revisión 91ba1d0 frente a b624b75 y las fixtures idénticas.

## Observaciones (no bloquean)

- `test_notation_validate_gives_typed_errors` y `test_palette_validation_is_typed` tienen, además de la parte de CLI, aserciones que no son de CLI (`load_notation` y `check_palette` lanzan errores tipados). El scope las excluye enteras, así que esas aserciones de validación tipada de paleta y notación no tienen hoy equivalente portado contra sldb. Puede afectar a la solidez de SV-H04 y SV-H06. Lo dejo para que IR13 lo decida.

## Seguimiento antes del closeout

- El coordinador debe conseguir que la suite completa salga con rc 0 en el checkout. Hay dos caminos: commitear o integrar sus `runs/` y RunDocs de forma que `mount_copy` no deje documentos colgando, o corregir el fixture (copiar `runs/` o tolerar RunDocs sin archivo) en otra tarea. Luego hay que volver a correr la suite bajo el lock. No hay nada que corregir en los 5 archivos del ejecutor.

## Veredicto final: **FAIL**

Por la regla del brief («FAIL si algo no se cumple»), la verificación 2 sale con rc 1. Las demás verificaciones pasan, y la causa del fallo está fuera del trabajo del ejecutor: son RunDocs del coordinador sin commitear. Con un árbol limpio, esas pruebas pasan.
