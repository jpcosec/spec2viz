# ST-reflection: spec2viz reflection and enforcement

**Basado en:** UC-05

## Script

```bash
# 1. ¿El tipo reflection existe en help?
spec2viz validate --help 2>&1 | grep -i reflection || echo "reflection not mentioned in help"

# 2. Validar archivo reflection de ejemplo (si existe)
ls examples/reflection/ 2>/dev/null || echo "No reflection examples dir"
ls examples/fixtures/canonical.yml 2>/dev/null && echo "Canonical fixture exists"

# 3. Si existe el canonical.yml, validarlo
spec2viz validate examples/fixtures/canonical.yml 2>&1

# 4. Renderizar reflection a enforcement artifact
# (reflection usa renderer json por defecto)
spec2viz render examples/fixtures/canonical.yml --out /tmp/viz-reflection 2>&1

# 5. Si hay archivo de reflection en examples/
for f in examples/reflection/*.yml examples/reflection/*.yaml 2>/dev/null; do
    echo "=== $f ==="
    spec2viz validate "$f"
    spec2viz render "$f" --out /tmp/viz-reflection
done

# 6. Inspeccionar enforcement artifact generado
cat /tmp/viz-reflection/canonical.enforcement.json 2>/dev/null || cat /tmp/viz-reflection/*.json 2>/dev/null || echo "No enforcement files found"

# 7. Prove enforcement script (si existe)
python3 examples/prove_enforcement.py 2>&1 || echo "prove_enforcement not available"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Reflection es discoverable? |
| 2 | ¿Hay ejemplos de reflection? |
| 3-5 | ¿Validación y render funcionan? |
| 6 | ¿El enforcement artifact tiene estructura esperada? |
| 7 | ¿El script prove_enforcement funciona? |

## Modos de fracaso

- Reflection no aparece en --help ni en examples/
- Enforcement artifact no se genera o tiene formato incorrecto
- No hay documentación de qué es un enforcement artifact
- El pipeline reflection → enforcement no está conectado al CLI
