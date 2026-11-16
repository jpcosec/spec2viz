# Informe del worker: decisiones de JP sobre el gate de retiro de spec2viz (IR13)

Fecha: 2026-11-15. Trabajé directo en IR main, sin push. No toqué otros repos; solo instalé mermaid-cli en
`/mnt/ssd/herramientas/mermaid-cli`. **El retiro sigue sin declararse**: `specir retirement check` sale con
rc 1, aunque ahora quedan 23 filas abiertas (antes 30). G7 quedó cumplido.

## Commits (IR main)

| sha | Qué |
|---|---|
| `bc671ad` | Código y documentos: ids de estado que acepta mermaid (`src/specir/visual/renderers/mermaid.py`); pruebas de motor real que respetan `SPECIR_MMDC` (`tests/visual/test_render_cases.py`); prueba nueva de ids con guion y expectativa de la proyección de estados (`tests/visual/test_render_parity.py`); matriz, acta, documento de decisión y habilidad `use-specir`. |
| `7c9e29e` | desk (con `deskops`): atom de la decisión aceptada, la propuesta queda como redirección y estado de IR13 en el Implementation Path. Incluye los `.sldb` que escribió deskops. |
| (último) | runs: este informe. |

## 1. Cómo quedó registrada G7

- `deskops add atom` creó
  `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`,
  con título «Decisión de JP (2026-11-15): …». La respuesta empieza con «ESTADO: DECISIÓN ACEPTADA POR JP
  el 2026-11-15 (transmitida por el supervisor con autorización explícita)». Los tags y la procedencia
  (`docs/decisiones/fuente-de-verdad-del-diagrama.md`) son los mismos de antes.
- `deskops atoms merge atom-propuesta-pendiente-de-jp-… --into atom-decisión-de-jp-…` fusionó la propuesta.
  No había referencias entrantes desde el desk (0 reescritas), y la propuesta quedó como redirección. Con
  `deskops edit atom` le cambié el título a «Redirección: la propuesta fue aceptada por JP el
  2026-11-15; …». También reescribí la respuesta del atom aceptado para quitar el texto de la propuesta
  que el merge había agregado al final.
- **task.decision: no hay ninguna asociada a G7.** Las únicas tareas task.decision del desk son las
  candidatas IR02 e IR05 del drawer, que no tienen relación con G7. Por eso no registré owner ni
  disposición. La decisión queda en el atom y en los documentos.
- `docs/decisiones/fuente-de-verdad-del-diagrama.md`: el estado pasa a «aceptada por JP el 2026-11-15» y la
  sección «Recomendación» pasa a llamarse «Decisión».
- Matriz: G7 queda `[x]` como **cumplido**, con la cita del documento y del atom. Las filas marcadas con †
  (regla de rutas de deskops y specs existentes) quedan alineadas con la decisión.

## 2. mmdc con motor real

- Instalación: `npm install @mermaid-js/mermaid-cli` (12.2.x) con `PUPPETEER_SKIP_DOWNLOAD=1` en
  `/mnt/ssd/herramientas/mermaid-cli`, sin instalación global.
- Envoltorio `/mnt/ssd/herramientas/mermaid-cli/mmdc`:
  - usa `PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome` y `puppeteer-config.json` (headless);
  - pone el perfil de Chrome en `mktemp -d /dev/shm/irjp-mmdc.XXXXXX` y lo borra con `trap` al salir;
  - corre bajo `timeout --kill-after=5 ${MMDC_TIMEOUT:-55}`.
- Cómo apuntar `SPECIR_MMDC` a ese mmdc: está documentado en `skills/use-specir/SKILL.md`, sección «Real
  mermaid engine (mmdc)». IR no tiene README.

Lo que arreglé en specIR:

- **Ids con guion en la proyección de estados.** El motor real rechazaba `[*] --> post-draft` en
  `stateDiagram-v2` (un `-` dentro del id se lee como el comienzo de una flecha). El renderer mermaid de
  estados ahora escribe los ids con solo letras, dígitos y `_` (`post_draft`), con un sufijo numérico si
  dos ids chocan. Los ids que ya eran válidos no cambian, así que la paridad con spec2viz se mantiene
  (`test_render_parity.py`, 82 passed). El pseudoestado `*` (`__any_state`) el motor lo acepta tal cual.
  PlantUML y D2 no cambian.
- **Dos pruebas de motor real ignoraban `SPECIR_MMDC`.** `test_real_mermaid_engine_accepts_the_packages`
  y `test_view_to_mermaid_is_accepted_by_the_real_engine` llamaban a `mmdc` del PATH. Ahora usan
  `mmdc_path()`, igual que las demás.

Corridas con `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm`, cada archivo por separado:

| Archivo | rc | Resultado |
|---|---|---|
| tests/visual/test_lint_mermaid.py | 0 | 15 passed (antes 8 passed, 7 skipped) |
| tests/visual/test_render_cases.py | 0 | 30 passed, 0 skipped (antes 27 passed, 3 skipped). Antes del arreglo: 1 failed (FileNotFoundError `mmdc`) |
| tests/visual/test_render_parity.py | 0 | 82 passed. Antes del arreglo: 1 failed, el estado `post-draft` rechazado por mmdc |
| tests/visual/test_renderers.py | 0 | 56 passed |
| tests/visual/test_api.py | 0 | 31 passed |
| tests/visual/test_cli.py | 0 | 44 passed |
| tests/visual/test_visual_projections.py | 0 | 9 passed |
| tests/visual/test_catalog.py | 0 | 67 passed, 1 xfailed (`label_key`, SV-G08) |
| tests/visual/test_catalog_parity.py | 0 | 29 passed |
| tests/visual/test_visual_compilers.py | 0 | 28 passed |

**Filas acreditadas (de abiertas a cumplidas):** SV-B03, SV-C13, SV-C14, SV-D01, SV-G03, SV-K12 y SV-K17.
**SV-K09 sigue abierta** porque depende también de SV-K16 (`diagram validate` provisional). La matriz
queda con 82 cumplidas y 23 abiertas.

## 3. Exporter de BPMN y clave de localStorage

- En la matriz quedó registrado en la acreditación de SV-C06 (`exporter="spec2viz"`,
  `targetNamespace="http://spec2viz/bpmn"`) y de SV-G06 (clave `spec2viz.catalog.annotations.v1`), y como
  pendiente 8.
- En el acta quedó como paso 8 de «Lo que falta» (pasar a specir con goldens nuevos y migrar las
  anotaciones) y como decisión 3.
- No cambié el código: los valores se mantienen mientras dure la paridad.

## 4. Decisiones anotadas en el acta (nueva sección «Decisiones»)

1. G7 (JP).
2. mmdc con Chrome.
3. Exporter de BPMN y clave de `localStorage`.
4. deskops `deskops/graph/desk_graph.py:75`: la regla deja de nombrar spec2viz y reconoce los specs YAML
   como artefactos de autoría sincronizados con `sldb notations sync`. La ejecuta el desk de deskops.
5. sldb `docs/architecture/spec2viz`: los specs se quedan como fixtures durante la paridad; el catálogo se
   construye con `specir catalog build` y se sincroniza con `sldb notations sync --catalog`. La ejecuta el
   desk de sldb.
6. spec2viz se archiva cuando `specir retirement check` salga con 0.

Las decisiones 4 y 5 también quedaron en el inventario de consumidores de la matriz. Las de otros repos no
las implementé.

## 5. specir retirement check

```
cd IR && timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops \
  --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb
```

rc 1, en 4 s. Resumen de la salida:

```
audited repos: graph_ui, deskops, pron, sldb, IR
audited stores: spec2viz/.sldb
dependencies: 122
  (las mismas 122 del acta: graph_ui 34, deskops 22, pron 3, sldb 1, IR 43, store spec2viz/.sldb 19)
rows not accredited: 23
  SV-A17, SV-E02, SV-G08, SV-H01, SV-H02, SV-H03, SV-H04, SV-H05, SV-H06, SV-I02, SV-J06, SV-K09,
  SV-K16, SV-K18, SV-K19, SV-K20, SV-K21, SV-K22, SV-K23, SV-K24, SV-K25, SV-K26, SV-K29
gate: failed, the retirement is not declared
```

El acta y el Implementation Path de IR13 quedaron actualizados con estos números.

## Suite final

`SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm .venv/bin/python -m pytest -q -n 4 tests/ -rs -p no:cacheprovider`: **rc 0, 658 passed, 4 xfailed, 0 skipped** (7 min 06 s). Los 4 xfail son los estrictos conocidos: `label_key`, el universo real del gate y los dos de blog_chain. Mientras corría la suite no edité el desk.

## Verificación del desk

- `deskops graph missing --root .`: rc 0 («No missing graph references found»).

## Limpieza

- `/dev/shm/irjp-*`: borrado. Los perfiles temporales de Chrome los borra el envoltorio en cada llamada;
  después de la corrida no queda ningún `/dev/shm/irjp-mmdc.*` ni `puppeteer*`.
- No quedan procesos de Chrome ni de mmdc míos: cada render corre bajo `timeout` y termina con su llamada.
- `/mnt/ssd/herramientas/mermaid-cli` se conserva a propósito, porque es la instalación que hay que usar.
