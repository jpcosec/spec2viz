PASA

# Resultado del tester (retiro de spec2viz, punto 8: BPMN/TargetNamespace, clave de localStorage y goldens)

- task: `task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo`
- commit del ejecutor: `109684fde25e6df9aef79ebe4729ae59ba0b660a` — *retiro de spec2viz, punto 8: BPMN con exporter y targetNamespace de specir, clave de localStorage de specir con migracion*
- archivos del commit:
  - `src/specir/visual/renderers/bpmn.py`
  - `src/specir/visual/templates/default.html`
  - `tests/visual/test_catalog_annotations.py`
  - `tests/visual/goldens/spec2viz-2de1056-renders.json`
  - `tests/visual/goldens/spec2viz-2de1056-oracle.json`
  - `docs/spec2viz/acta-de-retiro.md`
- entorno: `/workspace/IR` (sin cambios locales en `src/`, `tests/` ni `docs/`), `.venv/bin/python` (3.13.18), `TMPDIR=/tmp`, `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-97635c2c4cce*`, tests de a uno y en serie.

## Comprobaciones ejecutadas

| Comprobación | Resultado |
|---|---|
| `python -m pytest -q tests/visual/test_bpmn.py` | **26 passed**, rc 0 |
| `python -m pytest -q tests/visual/test_catalog_annotations.py` | **8 passed**, rc 0 |
| `python -m pytest -q tests/visual/test_render_parity.py` | **45 passed**, rc 0 |
| `python -m pytest -q tests/visual/test_resources.py` | **6 passed, 1 skipped**, rc 0 |
| `python -m pytest -q tests/visual/test_catalog.py` | **68 passed**, rc 0 |
| `python -m pytest -q tests/visual/test_catalog_parity.py` | **29 passed**, rc 0 |
| `python -m pytest -q tests/visual/test_render_commands.py` | **33 passed**, rc 0 |
| `python -m pytest -q tests/visual/test_schema.py tests/visual/test_lint_mermaid.py` | **19 passed, 7 skipped**, rc 0 |

Los 7 skips de `test_schema.py`/`test_lint_mermaid.py` son los preexistentes por dependencias opcionales ausentes (`mmdc`/herramientas), ajenos a este cambio. `test_resources.py` salta solo el build de la wheel por falta de `uv`.

## Cumplimiento del encargo

1. **BPMN con exporter y targetNamespace de specir.** El emisor raíz queda con `targetNamespace="http://specir/bpmn"` y `exporter="specir"` (`src/specir/visual/renderers/bpmn.py:725-726`). Verificado además renderizando en vivo `activity.validation.yml`: ambos atributos presentes y sin rastros de `spec2viz`; el XML y el digest de `bpmn.html` coinciden con los goldens nuevos.
2. **Clave de localStorage de specir con migración.** La página usa `specir.catalog.annotations.v1` y la única aparición de `spec2viz.catalog.annotations.v1` en código de producción está en `annoMigrateLegacy()` (`default.html:898`). La migración copia la clave vieja a la nueva solo si la nueva no existe, elimina la vieja, y si ambas existen gana la nueva; un valor viejo inválido se deja intacto. Los tres tests nuevos lo cubren (migración, ambas claves, JSON inválido) y pasan.
3. **Goldens nuevos revisados.** `spec2viz-2de1056-renders.json` actualiza las 8 salidas BPMN (exporter/targetNamespace) y sus 8 digests `bpmn.html`; `spec2viz-2de1056-oracle.json` actualiza los 4 digests de página de catálogo y el digest de `templates/default.html`. El diff se revisó: no hay cambios ajenos al retiro y los tests de paridad/render pasan contra los goldens nuevos.
4. **Acta.** El punto 8 de `docs/spec2viz/acta-de-retiro.md` registra el hecho con fecha 2026-11-23, valores concretos y remisión a `git log --grep Task-Id`.
5. **Grep de la clave vieja.** En producción solo aparece en la migración; las demás apariciones son tests, acta/desk y artefactos históricos de `runs/`, no código ejecutable del catálogo.

## Observaciones no bloqueantes

- Los goldens no se regrabaron con el recorder de spec2viz (retirado); se parchearon y se validaron contra la salida viva de specir. La alternativa habría vuelto a fijar la salida vieja de spec2viz, contraria al objetivo del punto 8.
- `test_resources_are_spec2viz_bytes` conserva su nombre/docstring, pero su digest de `templates/default.html` ya corresponde a la plantilla modificada de specir. El test pasa porque el golden se actualizó; convendría renombrar/reformular esa expectativa en una limpieza futura, sin afectar la aceptación de esta tarea.
- `test_bpmn.py` no añade una aserción explícita de `exporter`/`targetNamespace`; la cobertura efectiva viene de los goldens de paridad y de la verificación manual anterior.
- `test_catalog_parity.py` debe correrse en serie (el propio ejecutor documentó fallos bajo `xdist -n 4`); en serie pasa completo.

## Veredicto

**PASA.** El BPMN emitido es de specir, el catálogo migra sin perder anotaciones ni reescribir la clave vieja, los goldens afectados están actualizados y revisados, el acta registra el punto 8 y todos los tests de BPMN, catálogo y goldens pasan de a uno con `TMPDIR=/tmp`.
