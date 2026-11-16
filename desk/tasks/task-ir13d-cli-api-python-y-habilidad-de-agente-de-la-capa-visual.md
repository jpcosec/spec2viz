---
sldb:
  by: agent
  at: '2026-11-16T01:21:03Z'
  authority: generated
  via: save_document_payload
id: task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs
- task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos
- task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/cli.py
- src/specir/visual/__init__.py
- src/specir/visual/commands.py
- pyproject.toml
- skills/use-specir/SKILL.md
- docs/spec2viz/correspondencia-cli.md
- docs/spec2viz/matriz-de-cobertura.md
- tests/visual/test_cli.py
- tests/visual/test_api.py
- tests/visual/test_packaging.py
- tests/visual/test_render_commands.py
- tests/visual/test_schema.py
- tests/visual/test_lint_mermaid.py
- tests/visual/test_render_cases.py
- tests/visual/test_bpmn.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13d CLI, API Python y habilidad de agente de la capa visual

## Rationale

_Explain why this task exists or the business driver behind it._

Parte de la migración final de spec2viz, separada de IR13 para que cada tarea tenga un solo entregable. Los consumidores de spec2viz lo usan por su comando, por su API Python y por una habilidad de agente; sin equivalentes en specIR no tienen a dónde migrar.

## Goal

_Describe the concrete result this task must produce._

specIR ofrece un comando, una API Python pública y una habilidad de agente que cubren cada entrada pública de spec2viz.

## Scope

_State what is in scope and what is out of scope._

Dentro: comando de specIR con equivalentes de todos los comandos y subgrupos de spec2viz (diagram, notation, palette, catalog, y los alias de primer nivel render, validate, lint, schema y build, y about); API Python pública equivalente a la que exporta el paquete spec2viz; habilidad de agente que reemplaza a la de uso de spec2viz; tabla de correspondencia comando por comando.
Fuera: implementar las capacidades, que vienen de las tareas de compiladores, renderers, IR13a, IR13b e IR13c; instalar la habilidad en otros repos; migrar consumidores.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo src/specir/cli.py y exportaciones públicas en src/specir/visual/__init__.py que conectan las capacidades ya implementadas; habilidad en skills/use-specir/SKILL.md; correspondencia en docs/spec2viz/correspondencia-cli.md. Paridad medida portando a tests/visual/ las pruebas de spec2viz de CLI, API y empaquetado. Propiedad de archivos compartidos: src/specir/visual/__init__.py ya existe cuando esta tarea empieza: lo crea la tarea de compiladores y proyecciones (IR11), de la que esta depende por la cadena IR13a e IR12. Aquí solo se extiende con las exportaciones públicas que faltan; no se recrea ni se quitan las exportaciones existentes.

Precisiones (preflight-2, resueltas por el worker de IR13d):
1. API pública: la lista sale de los nombres públicos del `__init__` del paquete spec2viz en la revisión 2de1056 (load, validate, compile_ir, render, json_schema, write_json_schema, render_to_file, with_provenance, provenance_header, provenance_text, EXT_MAP, DEFAULT_RENDERER, BaseDiagram). load y validate son de sldb (SV-J01, D3): se usan como `sldb.api.notations.load_spec` y `validate_spec`, sin reexportarlos en specIR. El resto lo exporta `specir.visual`, junto con el linter de mermaid y el catálogo (build_catalog, render_catalog, AnnotationsTarget). tests/visual/test_api.py porta el test_api de spec2viz y comprueba que cada nombre público de spec2viz tiene su equivalente (en specir.visual o en sldb).
2. Habilidad: mismo formato que las habilidades de agente existentes (frontmatter con name y description, orientación, ruta de lectura, taxonomía, contrato de renderers, flujo y validación). Nombra solo comandos que existen; lo que es de sldb lo enseña con el comando de sldb (regla de JP: nada de envoltorios sobre la CLI o la API de sldb).
3. Inventario de comandos: el árbol de comandos de la CLI de spec2viz (el mismo que comprueba tests/test_matriz_cobertura_spec2viz.py), filas SV-K01 a SV-K30 de la matriz. Los subgrupos notation y palette y los comandos sync, from-graph, generate, catalog sync, catalog validate y catalog serve no tienen equivalente en specIR: la correspondencia remite al comando de sldb y specIR no lo duplica.
4. Matriz: docs/spec2viz/matriz-de-cobertura.md (filas SV-J02, SV-J03, SV-J07 a SV-J09 y SV-K*). IR13d cita sus pruebas sin marcar filas cumplidas; marcarlas es de IR13.
5. Entorno limpio: un venv nuevo en /dev/shm con sldb y la wheel de specIR (sin spec2viz), donde `specir --help` y `specir about` arrancan y `import spec2viz` falla.
6. SV-K16 (validar un spec por CLI): sldb aún no tiene el comando (pedido en su inbox). Mientras tanto `specir diagram validate` y el alias `validate` llaman a `load_spec` y `validate_spec` de sldb sin redefinir nada; cuando sldb publique su comando, el de specIR se retira y la cabecera de procedencia pasa a nombrar el de sldb. Registrado en la matriz.
7. El script `specir` pasa a `specir.cli:main`; el módulo de comandos de IR12 conserva los grupos diagram y catalog, que cli.py monta y extiende con catalog build, los alias y about.

Precisiones (bundle-2):
1. "Equivalentes de todos los comandos y subgrupos" se cumple con una fila por comando en docs/spec2viz/correspondencia-cli.md: los de specIR son comandos de `specir`; notation, palette y los demás genéricos tienen como equivalente el comando de sldb (o su función pública mientras sldb no tenga comando) y specIR no crea grupos que los envuelvan (regla de JP). Una prueba invoca cada equivalente y otra comprueba que specIR no define ninguno de los que la tabla da a sldb.
2. La habilidad puede nombrar comandos de `specir` y de `sldb`; la prueba invoca con `--help` cada uno de los dos, con las opciones que nombra. Lo que no puede nombrar es un comando de spec2viz.
3. Entorno limpio: el venv se crea bajo el tmp_path de pytest, que con TMPDIR=/dev/shm está en /dev/shm. Instala primero desde la caché de uv (--offline) y, si falta algo, desde la red; si no hay ni caché ni red la prueba se salta con el motivo. Sin uv o sin las fuentes de sldb también se salta.

## Validation

_List the checks required before this task can close._

- Cada comando y subgrupo que lista la ayuda de spec2viz tiene una fila en la tabla de correspondencia con su equivalente en specIR, y una prueba invoca cada equivalente.
- Las pruebas de API de spec2viz portadas pasan contra la API pública de specIR.
- La habilidad de agente nombra solo comandos que existen en el comando de specIR (comprobado por una prueba que los extrae y los invoca con ayuda).
- El paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y las filas de CLI, API Python y habilidad de la matriz de cobertura tienen su condición de retiro cumplida.
