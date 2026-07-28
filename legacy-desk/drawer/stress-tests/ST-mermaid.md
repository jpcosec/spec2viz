# ST-mermaid: spec2viz Mermaid output correctness

**Basado en:** UC-02, UC-04

## Script

```bash
mkdir -p /tmp/viz-mmd

# 1. Render todos los tipos a Mermaid
spec2viz render examples/sequence/example.yml --out /tmp/viz-mmd --renderer mermaid
spec2viz render examples/state/example.yml --out /tmp/viz-mmd --renderer mermaid
spec2viz render examples/component/example.yml --out /tmp/viz-mmd --renderer mermaid
spec2viz render examples/activity/example.yml --out /tmp/viz-mmd --renderer mermaid
spec2viz render examples/deployment/example.yml --out /tmp/viz-mmd --renderer mermaid

# 2. Verificar sintaxis Mermaid básica
for f in /tmp/viz-mmd/*.mmd; do
    echo "=== $(basename $f) ==="
    head -3 "$f"
    # Sequence: debería empezar con sequenceDiagram
    # State: debería empezar con stateDiagram-v2
    # Component/Activity/Deployment: debería empezar con graph
done

# 3. Cada tipo produce el tipo de diagrama Mermaid correcto?
python3 -c "
for f, expected_type in [
    ('/tmp/viz-mmd/example.mmd', 'sequenceDiagram'),
    ('/tmp/viz-mmd/example-state.mmd', 'stateDiagram-v2'),
]:
    content = open(f).read()
    has = expected_type in content
    print(f'{f}: expected {expected_type} -> {\"YES\" if has else \"NO\"}')
"

# 4. Matrix a Mermaid (no debería funcionar, usa Vega)
spec2viz render examples/matrix/example.yml --out /tmp/viz-mmd --renderer mermaid 2>&1

# 5. Validar Mermaid con mmdc si está instalado
which mmdc 2>/dev/null && echo "mmdc available" || echo "mmdc not available (no local validation possible)"

# 6. Output de Mermaid vs PlantUML: consistencia de contenido
# ¿Ambos renderers producen el mismo diagrama lógico?
diff <(spec2viz render examples/sequence/example.yml --renderer plantuml 2>/dev/null | grep -v '^@') \
     <(spec2viz render examples/sequence/example.yml --renderer mermaid 2>/dev/null) \
     2>&1 | head -20 || echo "Different formats (expected)"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Todos los tipos producen Mermaid? |
| 2 | ¿Sintaxis correcta por tipo? |
| 3 | ¿Sequence → sequenceDiagram, State → stateDiagram-v2? |
| 4 | ¿Matrix falla con error claro? |
| 5 | ¿Se puede validar localmente? |
| 6 | ¿Mismo diagrama lógico en ambos renderers? |

## Modos de fracaso

- Mermaid inválido sintácticamente
- Tipo de diagrama Mermaid incorrecto (sequence produce graph en vez de sequenceDiagram)
- Nodos sin IDs únicos
- Labels con caracteres especiales no escapados
- Matrix a Mermaid produce archivo corrupto en vez de error claro
