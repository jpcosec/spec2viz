# ST-styled-diagrams: spec2viz styled diagrams (theme, kinds)

**Basado en:** UC-02

## Script

```bash
mkdir -p /tmp/viz-styled

# 1. Validate styled component fixture
spec2viz validate tests/fixtures/component.styled.yml 2>&1

# 2. Render styled component to PlantUML
spec2viz render tests/fixtures/component.styled.yml --out /tmp/viz-styled --renderer plantuml 2>&1

# 3. Check skinparam styling in PlantUML output
python3 -c "
content = open('/tmp/viz-styled/component.styled.puml').read()
# Check for skinparam definitions
import re
skinparams = re.findall(r'skinparam\s+\S+', content)
print(f'Skinparam directives: {len(skinparams)}')
for sp in skinparams:
    print(f'  {sp}')
print()
print('Has @startuml:', content.startswith('@startuml'))
print('Has @enduml:', content.strip().endswith('@enduml'))
print('Has styling:', 'BackgroundColor' in content or 'FontColor' in content)
"

# 4. Render styled component to Mermaid
spec2viz render tests/fixtures/component.styled.yml --out /tmp/viz-styled --renderer mermaid 2>&1

# 5. Check CSS styling in Mermaid output
python3 -c "
content = open('/tmp/viz-styled/component.styled.mmd').read()
print('Mermaid output:')
print(content[:500])
print()
print('Has graph keyword:', 'graph' in content)
print('Has subgraph:', 'subgraph' in content)
print('Has classDef:', 'classDef' in content or 'style' in content.lower())
"

# 6. Check that kinds (boundary, core, etc.) are reflected in output
python3 -c "
puml = open('/tmp/viz-styled/component.styled.puml').read()
print('PlantUML kind markers:')
for kind in ['boundary', 'core', 'actor', 'system', 'component']:
    count = puml.lower().count(f'<<{kind}>>')
    print(f'  <<{kind}>>: {count} occurrences')
"

# 7. Test all fixture types with style
for f in tests/fixtures/*.yml; do
    echo "=== $(basename $f) ==="
    spec2viz validate "$f" 2>&1
    spec2viz render "$f" --out /tmp/viz-styled --renderer plantuml 2>&1
done

# 8. Check if other fixtures also produce styling
python3 -c "
import os
for f in os.listdir('/tmp/viz-styled'):
    if f.endswith('.puml'):
        content = open(f'/tmp/viz-styled/{f}').read()
        has_style = 'skinparam' in content or '<<' in content
        print(f'{f}: styling={\"YES\" if has_style else \"NO\"}')
"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Styled fixture valida correctamente? |
| 2-3 | ¿Los skinparam se reflejan en PlantUML? |
| 4-5 | ¿Los estilos se reflejan en Mermaid? |
| 6 | ¿Los `<<kinds>>` aparecen en output? |
| 7 | ¿Todos los fixtures de test funcionan? |
| 8 | ¿Qué fixtures producen styling? |

## Modos de fracaso

- Styling en YAML no se refleja en output PlantUML/Mermaid
- Los `<<kinds>>` no aparecen en el diagrama renderizado
- Skinparam directives están ausentes o incorrectas
- Mermaid no soporta classDef/styles (cae silenciosamente)
- styled fixture falla validación
- Los temas no se aplican consistentemente entre renderers
