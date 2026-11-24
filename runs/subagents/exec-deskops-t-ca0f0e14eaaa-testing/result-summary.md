FALLA

# Resultado del tester: declarar el retiro de spec2viz en el acta

- Tarea: `task-declarar-el-retiro-de-spec2viz-en-el-acta-comprobador-en-rc-0-catalog-build-medido-y-cambios-del-mom`
- Commit del ejecutor: `e53879573e6e0a2388b930b2aed2d26b909c68a0` — *acta de retiro de spec2viz: retiro declarado el 2026-11-23, comprobador rc 0, catalog build medido*
- Archivos del commit: `docs/spec2viz/acta-de-retiro.md` (+79/-29) y `docs/spec2viz/matriz-de-cobertura.md` (+20/-20).
- Entorno: `/workspace/IR` (checkout principal), `TMPDIR=/tmp`, `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-ca0f0e14eaaa`, `.venv` del repo. No se modificó el commit ni los documentos.

## Comprobaciones ejecutadas

| Comprobación | Resultado |
|---|---|
| `specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb` | **rc 0**: `dependencies: 0`, `rows not accredited: 0`, `gate: passed, the retirement can be declared`. |
| `grep -n 'no declarado' docs/spec2viz/acta-de-retiro.md` | Solo la línea 16, dentro de «Historia, hasta la declaración». PASS. |
| `pytest -q tests/test_matriz_cobertura_spec2viz.py` | **5 passed**, rc 0. |
| `pytest -q tests/visual/test_retirement_gate.py` | **7 passed**, rc 0 (incluye el test del universo real). |
| `specir catalog build --config tests/visual/fixtures/catalog/examples/catalog/project.yml --out /tmp/...` | **rc 0**; 66,9 s en frío y 10,9 s con caché caliente; RSS máximo observado 0,82 GB en caliente. Confirma que termina; no reproduce exactamente el 55,8 s / 1,7 GB del acta (medición del coordinador). |

Las validaciones automáticas del encargo pasan: el comprobador sale en rc 0 y `no declarado` solo queda en la historia fechada.

## Hallazgos que impiden el cierre

El Done When pide el acta «sin frases que lo contradigan», y el commit deja varias frases que contradicen el retiro declarado:

1. **`docs/spec2viz/acta-de-retiro.md:131` (G3).** La columna Estado dice `cumplido el 2026-11-23 (sldb notations validate cubre SV-K16, K21, K26 y K29; 3d0a436)`, pero la misma fila, en Evidencia, sigue diciendo: «**Faltan** los comandos de sldb para validar notación y paleta (SV-K21, SV-K26) y el de validar un spec…». Es una contradicción directa dentro de la misma fila.
2. **`docs/spec2viz/acta-de-retiro.md:129` (G1).** El Estado dice `cumplido el 2026-11-23 (0 filas no acreditadas)`, pero la Evidencia arranca con «97 cumplidas y **8 abiertas** en «Acreditación (IR13)» de la matriz». La acreditación real tiene 105 filas, todas `cumplida`, y el comprobador da 0 filas no acreditadas.
3. **`docs/spec2viz/acta-de-retiro.md:144-146` (tabla «Consumidores»).** Las filas de `sldb`, del store `spec2viz/.sldb` y de `IR (specIR)` siguen con `pendiente` en «Cambio que lo resolvió», cuando el mismo acta declara hechos los puntos 1, 2 y 6 y G4/G5 cumplidos. En particular, la fila de IR sigue afirmando que los oráculos de paridad importan spec2viz y «se saltan sin spec2viz», pero el punto 6 registra que desde `c47111d` comparan contra goldens congelados y ya no lo importan.
4. **`docs/spec2viz/matriz-de-cobertura.md:339`.** El resumen de «Acreditación (IR13)» sigue diciendo «97 cumplidas, 8 abiertas (tras IR13j)», mientras que las 105 filas de esa misma sección están en `cumplida` y el nuevo estado de G1-G5 declara el gate cumplido. El commit tocó esa matriz para marcar G1-G5, pero no actualizó el resumen.

Estos puntos son corregibles solo con edición documental (marcar las evidencias antiguas como historia fechada o actualizarlas, y corregir las filas de consumidores y el resumen de la matriz), pero en el estado entregado el acta se contradice sobre si el retiro y los gates están hechos.

## Veredicto

**FALLA.** El núcleo del encargo está hecho (cabecera «declarado el 2026-11-23», medición nueva, salida rc 0, puntos 1-9 actualizados, punto 9 como último paso y oráculos de paridad registrados en el punto 6), y las validaciones automáticas pasan. Sin embargo, no se cumple el Done When de que el acta no tenga frases que lo contradigan: G1 y G3 conservan texto de gate abierto, la tabla de consumidores deja tres consumidores como pendientes y el resumen de la matriz sigue dando 8 filas abiertas.
