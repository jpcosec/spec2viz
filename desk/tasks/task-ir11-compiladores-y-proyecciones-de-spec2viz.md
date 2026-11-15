---
sldb:
  by: agent
  at: '2026-11-15T22:36:05Z'
  authority: generated
  via: save_document_payload
id: task-ir11-compiladores-y-proyecciones-de-spec2viz
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
- task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
- task-espejo-sldb-modelos-de-spec-por-tipo-de-diagrama-d3
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/visual/__init__.py
- src/specir/visual/ir.py
- src/specir/visual/compilers/__init__.py
- src/specir/visual/exceptions.py
- src/specir/visual/normalize.py
- src/specir/visual/projections.py
- src/specir/visual/spec_models.py
- tests/test_imports.py
- tests/visual/parity.py
- tests/visual/test_visual_compilers.py
- tests/visual/test_visual_ir.py
- tests/visual/test_visual_names.py
- tests/visual/test_visual_normalize.py
- tests/visual/test_visual_parity.py
- tests/visual/test_visual_projections.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
from_drawer: desk/drawer/tasks/task-ir11-compiladores-y-proyecciones-de-spec2viz.md
---

# IR11 Compiladores y proyecciones de spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

Los compiladores son el centro de spec2viz: convierten un spec en una representación lista para dibujar. Sin cubrirlos, ninguna otra parte de la capa visual puede migrar, y es donde se aplica la decisión sobre el YAML de spec frente al grafo.

## Goal

_Describe the concrete result this task must produce._

specIR compila todos los tipos de diagrama que compila spec2viz y produce diagramas tanto desde un spec autorado como desde una proyección del grafo, según el contrato decidido en la tarea de cobertura.

## Scope

_State what is in scope and what is out of scope._

Dentro: los modelos de spec, su carga y su validación para clase, secuencia, estado, componente, actividad, despliegue, matriz y reflexión se toman de sldb (D3, tarea espejo de sldb) y no se redefinen en specIR; representación intermedia visual propia de specIR y un compilador por tipo; materialización de proyecciones: de un ViewDoc evaluado por la API de SLDB sobre su grafo y de un SpecDoc con sus SpecNodeDoc a la misma representación intermedia. specIR puede transformar esos resultados en nodos y aristas específicos del dominio/diagrama, pero la consulta del store, el índice, las aristas autoradas y los recorridos genéricos siguen siendo de SLDB y se consumen mediante su API pública. Los modelos de vocabulario visual se usan desde SLDB y no se redefinen. Fuera: índice o backend genérico de grafo, renderizado a formatos de salida, linter y recursos empaquetados; sincronización al store, catálogos y consumidores; retirar spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Los modelos de spec, su carga y su validación vienen de sldb (D3): specIR los importa de su API pública y no define ninguno; los compiladores y las proyecciones consumen esos modelos. Módulos de compilación en el paquete specIR; resolución de vistas por la API pública de SLDB. Paridad: los fixtures y pruebas de compiladores de spec2viz se portan a tests/visual/ de specIR y se comparan por equivalencia estructural normalizada de la representación intermedia: mismos tipos de elemento, mismos campos con los mismos valores, mismos nodos y aristas con los mismos extremos y atributos, comparados tras ordenar de forma determinista las colecciones cuyo orden no es significativo (nodos y aristas por id) y conservando el orden donde sí lo es (pasos de actividad, mensajes de secuencia, miembros de clase). Solo se excluye de la comparación la metadata de procedencia (origen, marcas de tiempo, rutas absolutas); cualquier otra diferencia es un fallo o una diferencia declarada en la matriz. El código de specIR bajo src/ no importa spec2viz. Las pruebas de paridad bajo tests/ sí pueden importar spec2viz como oráculo de desarrollo para producir el valor esperado, marcadas como pruebas de paridad y omitidas si spec2viz no está instalado; cuando spec2viz se retire, el oráculo se sustituye por los resultados guardados de su última ejecución. Propiedad de archivos compartidos: esta tarea crea src/specir/visual/__init__.py con las exportaciones de modelos de spec, compiladores y proyecciones; la tarea IR13d lo extiende después con la API pública completa, y corre siempre después de esta porque depende de ella por la cadena IR13a e IR12. `projections.py` obtiene datos del store mediante la API pública de SLDB: `run_view` para ViewDoc compuesto, `evaluate_projection_view` para ViewDoc de proyección y `resolve_view` para SpecDoc; luego los transforma a la representación visual específica. No consulta archivos/índices internos ni reproduce recorridos genéricos.

Precisiones (preflight): el contrato es el de la tarea de cobertura (IR07): filas SV-B01 a SV-B10 y SV-A14 de docs/spec2viz/matriz-de-cobertura.md (modo migrar tal cual) y la propuesta docs/decisiones/fuente-de-verdad-del-diagrama.md (pendiente de JP; no cambia IR11: spec autorado y proyección compilan a la misma representación intermedia). Oráculo: spec2viz en la revisión 2de1056, instalado editable en .venv; el corpus son los 44 specs de spec2viz (tests/fixtures con invalid/, examples/, docs/architecture/spec2viz/) copiados a tests/visual/fixtures/spec2viz/, y los resultados guardados de su última ejecución van en tests/visual/goldens/spec2viz-2de1056.json (tests/visual/parity.py los regenera). Errores tipados: misma clase y mismo texto al cargar y validar con sldb.api.notations.load_spec/validate_spec que con spec2viz, sobre ese corpus. Blog: el de IR06 (tests/models/blog.py y tests/fixtures/blog_chain.yaml); Post es DomainEntityDoc:post y las proyecciones son ViewDoc:post-states y ViewDoc:publish-components. Firmas de sldb 641ecdfa: sldb.api.run_view(store, name, params), sldb.api.notations.evaluate_projection_view(store, view_or_ref, pythonpath) y resolve_view(store, spec_ref, pythonpath).
 Carencia de sldb (pedida a su desk el 2026-11-15): sldb.api.notations exporta load_spec y validate_spec pero no las clases de los modelos de spec; hasta que las exporte, un único módulo de specIR (src/specir/visual/spec_models.py) las importa de sldb.models.notation.diagram_specs, con una excepción acotada a ese módulo en tests/test_imports.py; ningún otro módulo alcanza internos de sldb.

Precisiones (bundle): la representación intermedia es la de spec2viz migrada tal cual (spec2viz/ir.py, filas SV-B01 a SV-B10): mismas dataclasses y campos, así que la comparación es campo a campo tras normalizar. La partición válidos/inválidos del corpus la da el oráculo: lo que spec2viz carga y valida debe compilar en specIR a la IR equivalente, y lo que spec2viz rechaza debe rechazarse con la misma clase y el mismo texto de error (queda en los goldens). La equivalencia spec autorado frente a proyección se exige para lo que specIR proyecta: componentes (ViewDoc de proyección y compuesto del blog) y SpecDoc de componentes y de estados; los otros seis tipos no tienen proyección del grafo en specIR (solo compilan desde spec). La lista autoritativa de archivos es files de esta tarea, actualizada con los que crea.

## Validation

_List the checks required before this task can close._

- Los ocho tipos de diagrama compilan en specIR, y cada fixture de compilador de spec2viz produce en specIR una representación intermedia estructuralmente equivalente a la de spec2viz según la normalización definida en el camino de implementación, o la diferencia está declarada en la fila correspondiente de la matriz de cobertura con su prueba equivalente.
- La función de normalización tiene su propia prueba: dos representaciones que difieren solo en el orden de nodos o en metadata de procedencia resultan iguales, y dos que difieren en un campo, un nodo o una arista resultan distintas.
- Los specs YAML existentes validan en specIR con los mismos errores tipados que en spec2viz, salvo que la decisión de la tarea de cobertura diga otra cosa.
- Un diagrama de componentes y uno de estados generados desde proyecciones del grafo del blog muestran la entidad Post y el store sigue teniendo un solo documento para ella.
- Compilar desde un spec autorado y desde la proyección equivalente del grafo da representaciones intermedias estructuralmente equivalentes según la misma normalización.
- specIR no define ninguna clase con el nombre de un modelo de vocabulario visual de SLDB.
- Ningún módulo bajo src/specir/ importa spec2viz (prueba de imports); spec2viz solo aparece importado en pruebas de paridad bajo tests/.
- specIR no define ninguna clase de modelo de spec por tipo de diagrama: los ocho se importan de sldb (prueba de imports y de nombres).

## Done When

_Name the observable condition that makes the task complete._

Las pruebas de paridad de compiladores pasan en specIR y las filas de compiladores y proyecciones de la matriz de cobertura tienen su condición de retiro cumplida.
