# ST-spec-consistency: spec.md vs implementation

**Basado en:** UC-01, UC-02, UC-03, UC-04, UC-05, UC-06

## Script

```bash
# 1. Check spec.md mentions of CLI commands — do they all exist?
python3 -c "
import re
spec = open('spec.md').read()
# Find all code-block commands that look like CLI invocations
commands = set()
for line in spec.split('\n'):
    if line.startswith('spec2viz ') or line.startswith('$ spec2viz '):
        cmd = line.replace('$ ', '').strip().split()[1] if ' ' in line else ''
        if cmd:
            commands.add(cmd)
print('CLI commands mentioned in spec.md:')
for c in sorted(commands):
    print(f'  spec2viz {c}')
# Check which exist
import subprocess
for c in sorted(commands):
    r = subprocess.run(['spec2viz', c, '--help'], capture_output=True, text=True)
    print(f'  spec2viz {c}: {\"EXISTS\" if r.returncode == 0 else \"NOT FOUND\"}')
"

# 2. Check spec.md mentions of diagram types — all enum values covered?
python3 -c "
import re
spec = open('spec.md').read()
types_spec = set(re.findall(r'type:\s*(\w+)', spec))
from spec2viz.models.base import DiagramType
types_code = {t.value for t in DiagramType}
print('Diagram types in spec.md:', sorted(types_spec))
print('Diagram types in code:', sorted(types_code))
missing_from_spec = types_code - types_spec
missing_from_code = types_spec - types_code
if missing_from_spec:
    print(f'In code but not in spec.md: {missing_from_spec}')
if missing_from_code:
    print(f'In spec.md but not in code: {missing_from_code}')
if not missing_from_spec and not missing_from_code:
    print('All diagram types documented in spec.md')
"

# 3. Check spec.md mentions of render formats — do they match?
python3 -c "
spec = open('spec.md').read()
renderers_in_spec = []
for line in spec.split('\n'):
    if 'PlantUML' in line or 'Mermaid' in line or 'Vega' in line or 'D2' in line or 'SVG' in line or 'PNG' in line:
        if 'render' in line.lower() or 'format' in line.lower() or 'output' in line.lower() or 'artifact' in line.lower():
            renderers_in_spec.append(line.strip())
print('Render formats mentioned in spec.md context:')
for r in renderers_in_spec[:10]:
    print(f'  {r}')
print()
print('Note: spec.md mentions D2, SVG, PNG as future targets')
print('Implemented: PlantUML, Mermaid, Vega')
print('Not implemented: D2, SVG, PNG')
"

# 4. Check that all example fixtures validate against the documented schema
python3 -c "
from spec2viz import load, validate, json_schema
import subprocess, json
schema = json_schema()
for path in ['examples/sequence/example.yml', 'examples/state/example.yml',
             'examples/component/example.yml', 'examples/activity/example.yml',
             'examples/deployment/example.yml', 'examples/matrix/example.yml']:
    result = subprocess.run(['spec2viz', 'validate', path], capture_output=True, text=True)
    status = 'OK' if result.returncode == 0 else 'FAIL'
    print(f'{path}: {status}')
"

# 5. Check that spec.md pipeline matches actual CLI pipeline
python3 -c "
spec = open('spec.md').read()
# Pipeline keywords
pipeline_spec = []
for line in spec.split('\n'):
    if 'pipeline' in line.lower() or 'step' in line.lower() or 'phase' in line.lower():
        pipeline_spec.append(line.strip())
print('Pipeline described in spec.md:')
for l in pipeline_spec[:5]:
    print(f'  {l}')
print()
print('Actual CLI pipeline:')
print('  1. spec2viz validate <file>')
print('  2. spec2viz render <file> --renderer <fmt>')
print('  3. (external) plantuml/mermaid/vega tools for SVG/PNG')
print()
print('Gap: spec.md promises SVG/PNG output; actual CLI produces textual diagrams only')
"

# 6. Check spec.md version matches package version
python3 -c "
spec = open('spec.md').read()
import re
version_spec = re.search(r'v?(\d+\.\d+)', spec)
print(f'Version mentioned in spec.md: {version_spec.group(1) if version_spec else \"Not found\"}')
import importlib.metadata
try:
    pkg_ver = importlib.metadata.version('spec2viz')
    print(f'Package version: {pkg_ver}')
except:
    # Check pyproject.toml
    pp = open('pyproject.toml').read()
    ver = re.search(r'version\s*=\s*\"([^\"]+)\"', pp)
    print(f'pyproject.toml version: {ver.group(1) if ver else \"Not found\"}')
"

# 7. Check CLI --help mentions all subcommands that spec.md references
python3 -c "
import subprocess
r = subprocess.run(['spec2viz', '--help'], capture_output=True, text=True)
help_text = r.stdout
print('CLI subcommands from --help:')
for line in help_text.split('\n'):
    if line.strip().startswith('render') or line.strip().startswith('validate') or line.strip().startswith('schema'):
        print(f'  spec2viz {line.strip()}')
print()
spec = open('spec.md').read()
for cmd in ['validate', 'render', 'schema']:
    in_help = cmd in help_text
    in_spec = cmd in spec
    print(f'{cmd}: help={\"YES\" if in_help else \"NO\"}, spec={\"YES\" if in_spec else \"NO\"}')
"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Todos los comandos del spec existen en el CLI? |
| 2 | ¿Tipos de diagrama documentados coinciden con enum? |
| 3 | ¿Formatos de render documentados coinciden con implementación? |
| 4 | ¿Ejemplos del spec se validan correctamente? |
| 5 | ¿Pipeline documentado coincide con pipeline real? |
| 6 | ¿La versión del spec coincide con el paquete? |
| 7 | ¿Subcomandos en spec existen en --help? |

## Modos de fracaso

- spec.md promete formatos (D2, SVG, PNG) no implementados
- Tipos documentados que no existen en el código
- Pipeline documentado no coincide con UX real
- Versión desactualizada en spec.md
- Ejemplos en spec.md no validan con el schema actual
