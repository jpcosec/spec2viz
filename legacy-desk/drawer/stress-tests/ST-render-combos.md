# ST-render-combos: spec2viz render — all type+renderer combinations

**Basado en:** UC-02, UC-04

## Script

```bash
# 1. Enumerar todas las combinaciones posibles type + renderer
# y verificar cuáles funcionan y cuáles no

mkdir -p /tmp/viz-combos

COMBOS=(
    "examples/sequence/example.yml:plantuml"
    "examples/sequence/example.yml:mermaid"
    "examples/sequence/example.yml:vega"
    "examples/state/example.yml:plantuml"
    "examples/state/example.yml:mermaid"
    "examples/state/example.yml:vega"
    "examples/component/example.yml:plantuml"
    "examples/component/example.yml:mermaid"
    "examples/component/example.yml:vega"
    "examples/activity/example.yml:plantuml"
    "examples/activity/example.yml:mermaid"
    "examples/activity/example.yml:vega"
    "examples/deployment/example.yml:plantuml"
    "examples/deployment/example.yml:mermaid"
    "examples/deployment/example.yml:vega"
    "examples/matrix/example.yml:plantuml"
    "examples/matrix/example.yml:mermaid"
    "examples/matrix/example.yml:vega"
)

for combo in "${COMBOS[@]}"; do
    IFS=":" read -r file renderer <<< "$combo"
    echo -n "$file + $renderer: "
    spec2viz render "$file" --out /tmp/viz-combos --renderer "$renderer" 2>&1 && echo "OK" || echo "FAIL"
done

# 2. Verificar archivos generados
ls -la /tmp/viz-combos/

# 3. Extensión de archivo por renderer
echo "---"
echo "PlantUML files:"
ls /tmp/viz-combos/*.puml 2>/dev/null | wc -l
echo "Mermaid files:"
ls /tmp/viz-combos/*.mmd 2>/dev/null | wc -l
echo "Vega files:"
ls /tmp/viz-combos/*.vega.json 2>/dev/null | wc -l

# 4. ¿El renderer default (sin --renderer) funciona para cada tipo?
# Default debería ser plantuml para sequence/state/component/activity/deployment,
# vega para matrix
for file in examples/sequence/example.yml examples/state/example.yml \
            examples/component/example.yml examples/activity/example.yml \
            examples/deployment/example.yml examples/matrix/example.yml; do
    echo -n "$file (default): "
    spec2viz render "$file" --out /tmp/viz-defaults 2>&1 && echo "OK" || echo "FAIL"
done
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Qué combinaciones fallan? ¿El error es claro? |
| 2 | ¿Archivos generados tienen nombres predecibles? |
| 3 | ¿Extensiones correctas según renderer? |
| 4 | ¿Renderer default funciona para cada tipo? |

## Modos de fracaso

- Matriz de compatibilidad no documentada (usuario no sabe qué funciona)
- Default renderer no está definido para algún tipo
- Error en combinaciones no soportadas no es claro ("RenderError" vs "no soportado")
- Extensiones inconsistentes (`.puml` vs `.plantuml`? `.vega.json` vs `.vg.json`?)
