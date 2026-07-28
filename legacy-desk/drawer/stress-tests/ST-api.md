# ST-api: spec2viz Python API

**Basado en:** UC-06

## Script

```bash
# 1. Import API pública
python3 -c "
from spec2viz import load, validate, compile_ir, render, render_to_file, json_schema, write_json_schema
print('All functions importable')
"

# 2. load + validate + compile_ir + render pipeline
python3 -c "
from spec2viz import load, validate, compile_ir, render

# Load
diagram = load('examples/sequence/example.yml')
print(f'Loaded: {diagram.id} ({diagram.type})')
print(f'Type: {type(diagram).__name__}')

# Validate
validate(diagram)
print('Validated: OK')

# Compile
ir = compile_ir(diagram)
print(f'IR type: {type(ir).__name__}')
print(f'IR: {ir}')

# Render (PlantUML)
output = render(ir, renderer='plantuml')
print(f'PlantUML output ({len(output)} chars)')
print(output[:200])

# Render (Mermaid)
output = render(ir, renderer='mermaid')
print(f'Mermaid output ({len(output)} chars)')
print(output[:200])
"

# 3. render_to_file
python3 -c "
from spec2viz import render_to_file
path = render_to_file('examples/state/example.yml', out='/tmp/viz-api', renderer='plantuml')
print(f'Wrote to: {path}')
import os
print(f'File size: {os.path.getsize(path)} bytes')
"

# 4. json_schema
python3 -c "
from spec2viz import json_schema, write_json_schema
schema = json_schema()
print(f'Full schema: {len(schema)} keys')
schema_seq = json_schema('sequence')
print(f'Sequence schema: {len(schema_seq)} keys')
schema_state = json_schema('state')
print(f'State schema: {len(schema_state)} keys')
write_json_schema('/tmp/viz-schema-api.json')
print('Schema written to file')
"

# 5. load con archivo inválido
python3 -c "
from spec2viz import load
try:
    load('/tmp/nonexistent.yml')
except Exception as e:
    print(f'Load error type: {type(e).__name__}')
    print(f'Load error msg: {e}')
"

# 6. validate con diagram inválido
python3 -c "
from spec2viz import load, validate
diagram = load('tests/fixtures/invalid/bad_sequence.yml')
try:
    validate(diagram)
except Exception as e:
    print(f'Validate error type: {type(e).__name__}')
    print(f'Validate error msg: {e}')
"

# 7. compile_ir con tipo desconocido
python3 -c "
from spec2viz import compile_ir
# ...

# 8. load de todos los tipos
for f in examples/sequence/example.yml examples/state/example.yml \
         examples/component/example.yml examples/activity/example.yml \
         examples/deployment/example.yml examples/matrix/example.yml; do
    python3 -c \"
from spec2viz import load, validate, compile_ir
d = load('$f')
validate(d)
ir = compile_ir(d)
print(f'$f: {d.type} -> {type(ir).__name__}')
\"
done

# 9. Type hints disponibles?
python3 -c "
from spec2viz import load, validate, compile_ir, render, render_to_file
import inspect
for fn in [load, validate, compile_ir, render, render_to_file]:
    sig = inspect.signature(fn)
    hints = fn.__annotations__ if hasattr(fn, '__annotations__') else {}
    print(f'{fn.__name__}{sig} -> {hints.get(\"return\", \"?\")}')"

# 10. Import de modelos directamente
python3 -c "
from spec2viz.models.sequence import SequenceDiagram, SequenceData, ParticipantModel, MessageModel
from spec2viz.models.state import StateDiagram, StateData, StateModel, TransitionModel
from spec2viz.models.component import ComponentDiagram, ComponentData, NodeModel, EdgeModel
from spec2viz.models.activity import ActivityDiagram, ActivityData, StepModel
from spec2viz.models.deployment import DeploymentDiagram, DeploymentData, DeploymentNodeModel, ArtifactModel, ConnectionModel
from spec2viz.models.matrix import MatrixDiagram, MatrixData, MatrixViewModel, MatrixStageModel, MatrixComponentModel
from spec2viz.models.base import DiagramType, BaseDiagram, Metadata, Style
print('All models importable')
print(f'Diagram types: {[t.value for t in DiagramType]}')
"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Import paths son intuitivos? |
| 2 | ¿Pipeline load → validate → compile → render funciona? |
| 3 | ¿render_to_file produce archivo en ubicación esperada? |
| 4 | ¿json_schema produce schemas correctos? |
| 5 | ¿Load con archivo inválido lanza ParseError o Exception genérica? |
| 6 | ¿Validate con diagram inválido lanza ValidationError? |
| 7 | ¿compile_ir con tipo desconocido lanza CompileError? |
| 8 | ¿Todos los tipos compilean a IR? |
| 9 | ¿Hay type hints? |
| 10 | ¿Los modelos Pydantic son construibles programáticamente? |

## Modos de fracaso

- Exception hierarchy plana (todo Exception, nada específico)
- Sin type hints en funciones públicas
- `load()` no acepta `pathlib.Path`
- `render_to_file` escribe en ubicación inesperada
- Modelos de IR no exportados desde spec2viz top-level
