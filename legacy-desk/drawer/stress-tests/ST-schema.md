# ST-schema: spec2viz schema — JSON Schema export

**Basado en:** UC-03

## Script

```bash
# 1. Help
spec2viz schema --help

# 2. Export schema completo a stdout
spec2viz schema > /tmp/viz-schema-complete.json
python3 -c "
import json
s = json.load(open('/tmp/viz-schema-complete.json'))
print('Schema title:', s.get('title', 'N/A'))
print('Schema type:', s.get('type', 'N/A'))
print('Defs count:', len(s.get('defs', s.get('$defs', {}))))
"

# 3. Export schema de tipo sequence
spec2viz schema --type sequence > /tmp/viz-schema-sequence.json
python3 -c "
import json
s = json.load(open('/tmp/viz-schema-sequence.json'))
print('Title:', s.get('title', 'N/A'))
print('Properties:', list(s.get('properties', {}).keys()))
"

# 4. Export schema de tipo state
spec2viz schema --type state > /tmp/viz-schema-state.json

# 5. Export schema de tipo component
spec2viz schema --type component > /tmp/viz-schema-component.json

# 6. Export schema con --type desconocido
spec2viz schema --type nonexistent 2>&1

# 7. Export schema a archivo con --out
spec2viz schema --out /tmp/viz-schema-file.json
ls -la /tmp/viz-schema-file.json

# 8. Export schema completo y validar un fixture contra él
python3 -c "
import json
schema = json.load(open('/tmp/viz-schema-complete.json'))
data = json.load(open('examples/sequence/example.yml'))
import jsonschema
try:
    jsonschema.validate(data, schema)
    print('example.yml: valid against full schema')
except jsonschema.ValidationError as e:
    print(f'Validation error: {e.message}')
"

# 9. Todos los tipos tienen schema?
for t in sequence state component activity deployment matrix; do
    spec2viz schema --type "$t" > /dev/null 2>&1 && echo "$t: OK" || echo "$t: FAIL"
done

# 10. Schema incluye descriptions?
python3 -c "
import json
s = json.load(open('/tmp/viz-schema-sequence.json'))
# Check if any property has a description
props = s.get('properties', {})
has_desc = any('description' in v for v in props.values())
print(f'Has descriptions: {has_desc}')
"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help documenta --type y --out? |
| 2 | ¿Schema completo es discriminated union válido? |
| 3-5 | ¿Schemas de tipo específico son correctos? |
| 6 | ¿Error: unknown type? |
| 7 | ¿--out funciona? |
| 8 | ¿Los fixtures se validan contra el schema? |
| 9 | ¿Todos los tipos tienen schema exportable? |
| 10 | ¿Hay descriptions para autocompletado? |

## Modos de fracaso

- Schema sin `$defs` ni `defs` (no reutiliza definiciones)
- Schema de tipo específico no es válido (missing required fields)
- Schema completo no matchea los fixtures existentes
- Sin descriptions (útil para IDE autocompletion)
- Schema con errores de sintaxis JSON
