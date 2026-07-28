# ST-plantuml: spec2viz PlantUML output correctness

**Basado en:** UC-02, UC-04

## Script

```bash
mkdir -p /tmp/viz-puml

# 1. Render todos los tipos a PlantUML
spec2viz render examples/sequence/example.yml --out /tmp/viz-puml --renderer plantuml
spec2viz render examples/state/example.yml --out /tmp/viz-puml --renderer plantuml
spec2viz render examples/component/example.yml --out /tmp/viz-puml --renderer plantuml
spec2viz render examples/activity/example.yml --out /tmp/viz-puml --renderer plantuml
spec2viz render examples/deployment/example.yml --out /tmp/viz-puml --renderer plantuml

# 2. Verificar que los .puml tienen sintaxis PlantUML básica
for f in /tmp/viz-puml/*.puml; do
    echo "=== $(basename $f) ==="
    head -3 "$f"
    # Debería empezar con @startuml
    grep -q "^@startuml" "$f" && echo "  @startuml: YES" || echo "  @startuml: NO"
    # Debería terminar con @enduml
    tail -1 "$f" | grep -q "^@enduml" && echo "  @enduml: YES" || echo "  @enduml: NO"
done

# 3. Verificar que el ejemplo styled de component tiene estilos
spec2viz render tests/fixtures/component.styled.yml --out /tmp/viz-puml --renderer plantuml
head -20 /tmp/viz-puml/component.styled.puml

# 4. Matrix a PlantUML (no debería funcionar)
spec2viz render examples/matrix/example.yml --out /tmp/viz-puml --renderer plantuml 2>&1

# 5. Comparar con outputs esperados (golden files)
# Si existen ejemplos .puml en examples/
for f in examples/**/*.puml; do
    base=$(basename "$f" .puml)
    generated="/tmp/viz-puml/${base}.puml"
    if [ -f "$generated" ]; then
        diff <(grep -v '^@startuml\|^@enduml' "$f") <(grep -v '^@startuml\|^@enduml' "$generated") \
            && echo "$base: MATCH" || echo "$base: DIFFERS"
    fi
done
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Todos los tipos producen PlantUML? |
| 2 | ¿Cada archivo tiene @startuml/@enduml? |
| 3 | ¿Los estilos se reflejan en el PlantUML? |
| 4 | ¿Matrix falla con error claro? |
| 5 | ¿Los outputs coinciden con golden files? |

## Modos de fracaso

- PlantUML sin @startuml (invisible para renderers)
- Sintaxis inválida (arrows mal formados, tipos incorrectos)
- Golden files desactualizados vs código actual
- Estilos (theme, kinds) no se reflejan en output
