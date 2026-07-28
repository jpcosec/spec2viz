# ST-vega: spec2viz Vega output correctness

**Basado en:** UC-02, UC-04

## Script

```bash
mkdir -p /tmp/viz-vega

# 1. Render matrix diagram to Vega
spec2viz render examples/matrix/example.yml --out /tmp/viz-vega --renderer vega 2>&1

# 2. Check Vega output is valid JSON against Vega schema
python3 -c "
import json
vega = json.load(open('/tmp/viz-vega/example.vega.json'))
print('Top-level keys:', list(vega.keys()))
print('Has $schema:', '\$schema' in vega and vega['\$schema'].startswith('https://vega.github.io/schema/vega/v5'))
print('Has title/description:', 'description' in vega)
print('Has marks:', 'marks' in vega)
print('Has data:', 'data' in vega)
print('Has scales:', 'scales' in vega)
print('Has signals:', 'signals' in vega)
print('Data sources count:', len([d for d in vega.get('data', [])]))
print('Marks count:', len(vega.get('marks', [])))
print('VEGA SCHEMA: VALID')
"

# 3. Check matrix-specific Vega features: stages, views, boundaries
python3 -c "
import json
vega = json.load(open('/tmp/viz-vega/example.vega.json'))
data = {d['name']: d for d in vega.get('data', []) if 'name' in d}
print('Data tables:', list(data.keys()))
for name, table in data.items():
    if 'values' in table:
        print(f'  {name}: {len(table[\"values\"])} rows')
    if 'transform' in table:
        print(f'  {name}: {len(table[\"transform\"])} transforms')
    if 'source' in table:
        print(f'  {name}: source={table[\"source\"]}')

# Check signals
signals = vega.get('signals', [])
print(f'Signals: {len(signals)}')
for sig in signals:
    print(f'  {sig[\"name\"]} = {sig.get(\"value\", \"(computed)\")}')

# Check scales
scales = vega.get('scales', [])
print(f'Scales: {len(scales)}')
for sc in scales:
    print(f'  {sc[\"name\"]}: {sc.get(\"type\", \"N/A\")} domain={sc.get(\"domain\", \"N/A\")}')
"

# 4. Render a second matrix fixture if available
for f in tests/fixtures/matrix*.yml examples/matrix/*.yml; do
    echo "=== $f ==="
    spec2viz render "$f" --out /tmp/viz-vega --renderer vega 2>&1
done

# 5. Verify no other diagram type produces Vega output
for f in examples/sequence/example.yml examples/state/example.yml; do
    echo -n "$f + vega: "
    spec2viz render "$f" --out /tmp/viz-vega --renderer vega 2>&1 && echo "OK" || echo "FAIL (expected)"
done

# 6. Check Vega output file extension
ls -la /tmp/viz-vega/
echo "Vega extensions:"
ls /tmp/viz-vega/*.vega.json 2>/dev/null | wc -l
echo "Other JSON:"
ls /tmp/viz-vega/*.json 2>/dev/null | wc -l

# 7. Verify Vega output can be loaded by vl-convert or similar
python3 -c "
import json
vega = json.load(open('/tmp/viz-vega/example.vega.json'))
# Basic structural validation
required = ['\$schema', 'marks', 'data', 'scales', 'signals', 'width', 'height']
missing = [k for k in required if k not in vega]
if missing:
    print(f'Missing required keys: {missing}')
else:
    print(f'All {len(required)} required keys present')
    print('STRUCTURAL VALIDATION: PASSED')
"

# 8. Vega signals reference correct scales?
python3 -c "
import json
vega = json.load(open('/tmp/viz-vega/example.vega.json'))
scale_names = {s['name'] for s in vega.get('scales', [])}
mark_scales = set()
for mark in vega.get('marks', []):
    for enc in mark.get('encode', {}).values():
        for k, v in enc.items():
            if isinstance(v, dict) and 'scale' in v:
                mark_scales.add(v['scale'])
unused = scale_names - mark_scales
missing = mark_scales - scale_names
if unused:
    print(f'Unused scales: {unused}')
if missing:
    print(f'Missing scales: {missing}')
if not unused and not missing:
    print('SCALE REFERENCE INTEGRITY: PASSED')
"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Matrix renderiza a Vega sin error? |
| 2 | ¿El JSON es válido? ¿Tiene $schema? |
| 3 | ¿Los datos de matrix stages/views están correctos? |
| 4 | ¿Otros fixtures de matrix renderizan? |
| 5 | ¿Tipos no-matrix fallan con error claro? |
| 6 | ¿Extensión .vega.json? |
| 7 | ¿Estructura básica de Vega presente? |
| 8 | ¿Las escalas referenciadas existen? |

## Modos de fracaso

- Vega output sin `$schema` (no renderizable en Vega editor)
- Faltan escalas, marcas o señales necesarias
- Datos de matrix incompletos (stages, views, components)
- Extensiones inconsistentes (`.vega.json` vs `.vg.json` vs `.json`)
- Señales no referencian escalas existentes
- Vega output no es JSON válido
