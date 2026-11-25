PASA

# Resultado del tester (intento 2): declarar el retiro de spec2viz en el acta

- Tarea: `task-declarar-el-retiro-de-spec2viz-en-el-acta-comprobador-en-rc-0-catalog-build-medido-y-cambios-del-mom`
- Commit final del ejecutor (el que devuelve `git log -1 --grep "Task-Id: ..."`): `8df3b9025b56cf23b8480173f25514b3c4786f5b` — *acta y matriz de spec2viz: sin frases que contradigan el retiro declarado (G1, G3, consumidores, resumen)*.
- El trabajo sustantivo de la tarea está en `e53879573e6e0a2388b930b2aed2d26b909c68a0` (acta declarada, medición, rc 0) y `8df3b90` corrige las contradicciones que detectó el tester del intento 1. Se valida el estado acumulado `e538795^..8df3b90`.
- Archivos del cambio: `docs/spec2viz/acta-de-retiro.md` y `docs/spec2viz/matriz-de-cobertura.md`. Solo documentación; el commit no toca `src/` ni `tests/`, así que no hay `tests/*.py` del commit ni `tests/test_<modulo>.py` que correr.
- Entorno: `/workspace/IR`, `.venv` del repo, `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-ca0f0e14eaaa-a2*`. No se modificaron los documentos ni el commit.

## Comprobaciones ejecutadas

| Comprobación | Resultado |
|---|---|
| `specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb` | **rc 0**: `dependencies: 0`, `rows not accredited: 0`, `gate: passed, the retirement can be declared`. |
| `grep -n 'no declarado' docs/spec2viz/acta-de-retiro.md` | Solo la línea 16, bajo «Historia, hasta la declaración» (historia fechada). PASS. |
| `pytest -q tests/visual/test_retirement_gate.py` | **7 passed**, rc 0 (incluye `test_the_real_universe_has_no_dependency_and_every_row_is_accredited` sobre el universo real). |
| `pytest -q tests/test_matriz_cobertura_spec2viz.py` | **5 passed**, rc 0. |
| Recuento de «Acreditación (IR13)» en la matriz | 105 filas, **105 cumplidas y 0 abiertas**. Coincide con el resumen nuevo. |
| `specir catalog build --config tests/visual/fixtures/catalog/examples/catalog/project.yml --out /tmp/...` | **rc 0**; 86 s en frío y 14,8 s con caché caliente; RSS máximo observado 0,82 GB en caliente. Confirma que termina; no reproduce exactamente el 55,8 s / 1,7 GB de la medición del coordinador que registra el acta, pero el hecho de que termine con rc 0 sí. |

Salida de la corrida real del comprobador:

```
audited repos: graph_ui, deskops, pron, sldb, IR
audited stores: -
dependencies: 0
rows not accredited: 0
gate: passed, the retirement can be declared
```

## Cumplimiento del encargo

1. La cabecera dice **«Retiro: declarado el 2026-11-23»**, con la decisión de JP y la medición nueva (55,8 s, rc 0, 1,7 GB) en la sección de `specir catalog build`.
2. La «Salida del comprobador» nueva muestra rc 0, 0 dependencias y 0 filas no acreditadas; la salida con rc 1 queda marcada como historia fechada.
3. Los puntos 1 a 8 de «Lo que falta para declarar el retiro» están marcados hechos con fecha y commit (`c377aff6`, `a918dfa`, `3d0a436`, `c47111d`, `109684f`, etc.); el punto 9 (archivar el repo en GitHub) queda como último paso del coordinador. El punto 6 registra que los oráculos de paridad se retiran al declarar porque ya comparan contra goldens congelados y no importan spec2viz.
4. G1 y G3 ya no contradicen su estado: el texto de gate abierto está marcado como «Historia fechada»; G4/G5 y las filas de `sldb`, `spec2viz/.sldb` e `IR` de «Consumidores» pasan a resueltas; el resumen de la matriz dice 105 cumplidas y 0 abiertas, con las 97/8 como historia fechada. Los cuatro hallazgos del tester del intento 1 están corregidos.
5. `docs/spec2viz/acta-de-retiro.md` no se contradice sobre el estado declarado. Las menciones restantes a «pendiente»/«abierto» son historia fechada de corridas anteriores, el pendiente real del punto 9 (archivar en GitHub, fuera de esta tarea) o el pendiente sin efecto en specir de `graph_ui/.github/workflows/ci.yml` que el propio comprobador no cuenta.

## Observaciones (no bloquean el cierre)

- La línea 52 («G4 de graph_ui sigue pendiente…») sigue en presente, pero está dentro de la narración fechada de la corrida del 2026-11-16 de IR13e y el acta resuelve graph_ui más adelante; no confunde el estado final.
- La fila G4 y la tabla «Consumidores» conservan los conteos históricos (63 dependencias, 43 importaciones de IR) como inventario fechado; el estado y la columna de resolución dicen cumplido/resuelto el 2026-11-23.
- El comando de `specir catalog build` que cita el acta omite `--out`, que la CLI exige; la verificación se hizo añadiendo `--out /tmp/...`. Es un detalle de redacción preexistente y no afecta a la declaración del retiro.

## Veredicto

**PASA.** El acta declara el retiro el 2026-11-23, el comprobador real sale con rc 0 y 0 filas no acreditadas, la medición de `specir catalog build` está registrada y confirmada (rc 0), los pendientes están marcados con sus commits y el punto 9 queda como último paso del coordinador. `no declarado` solo aparece en la historia fechada y no quedan frases que contradigan el estado declarado.
