# ST-render-multi: spec2viz render multiples y batch

**Basado en:** UC-04

## Script

```bash
mkdir -p /tmp/viz-batch

# 1. Render 3 archivos de distinto tipo a la vez
spec2viz render \
    examples/sequence/example.yml \
    examples/state/example.yml \
    examples/component/example.yml \
    --out /tmp/viz-batch \
    --renderer mermaid

# 2. Verificar que los 3 archivos se generaron
echo "Archivos generados:"
ls -la /tmp/viz-batch/
echo "Count: $(ls /tmp/viz-batch/ | wc -l)"

# 3. Render con --renderer plantuml, los archivos .puml deben ser distintos
spec2viz render \
    examples/sequence/example.yml \
    examples/state/example.yml \
    --out /tmp/viz-batch --renderer plantuml

ls /tmp/viz-batch/*.puml 2>/dev/null
echo "PlantUML files: $(ls /tmp/viz-batch/*.puml 2>/dev/null | wc -l)"

# 4. Batch con archivo que falla + archivo que funciona
# (crear archivo inválido)
echo "type: unknown" > /tmp/viz-bad.yml
spec2viz render \
    /tmp/viz-bad.yml \
    examples/sequence/example.yml \
    --out /tmp/viz-batch 2>&1
echo "Exit code: $?"

# 5. Render todos los ejemplos de una vez
spec2viz render examples/sequence/example.yml examples/state/example.yml \
    examples/component/example.yml examples/activity/example.yml \
    examples/deployment/example.yml examples/matrix/example.yml \
    --out /tmp/viz-all --renderer mermaid 2>&1
echo "Exit code: $?"
ls /tmp/viz-all/ 2>/dev/null | wc -l

# 6. ¿Render con glob pattern?
spec2viz render examples/**/*.yml --out /tmp/viz-glob 2>&1 || echo "No glob support"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1-3 | ¿Cada archivo produce su propio output? ¿Nombres únicos? |
| 4 | ¿Un fallo rompe todo el batch? ¿O skip con warning? |
| 5 | ¿6 archivos de distinto tipo se renderizan correctamente con Mermaid? |
| 6 | ¿Soporta glob patterns? |

## Modos de fracaso

- Batch: un fallo mata todo el grupo (no "skip and continue")
- Nombres de output colisionan (si 2 archivos se llaman example.yml)
- Sin resumen final ("3/3 rendered successfully, 1 failed")
- Sin flag `--continue-on-error`
