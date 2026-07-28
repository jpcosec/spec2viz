# ST-render: spec2viz render — diagram rendering

**Basado en:** UC-02

## Script

```bash
# 1. Help
spec2viz render --help

# 2. Render sequence a PlantUML
mkdir -p /tmp/viz-out
spec2viz render examples/sequence/example.yml --out /tmp/viz-out --renderer plantuml

# 3. Render sequence a Mermaid
spec2viz render examples/sequence/example.yml --out /tmp/viz-out --renderer mermaid

# 4. Render state a PlantUML
spec2viz render examples/state/example.yml --out /tmp/viz-out --renderer plantuml

# 5. Render component a Mermaid
spec2viz render examples/component/example.yml --out /tmp/viz-out --renderer mermaid

# 6. Render activity a PlantUML
spec2viz render examples/activity/example.yml --out /tmp/viz-out --renderer plantuml

# 7. Render deployment a Mermaid
spec2viz render examples/deployment/example.yml --out /tmp/viz-out --renderer mermaid

# 8. Render matrix a Vega
spec2viz render examples/matrix/example.yml --out /tmp/viz-out --renderer vega

# 9. Render con --backend (alias de --renderer)
spec2viz render examples/sequence/example.yml --out /tmp/viz-out --backend plantuml

# 10. Render sin --out
spec2viz render examples/sequence/example.yml --renderer plantuml
# ¿Escribe en CWD? ¿En .?

# 11. Render con --out que no existe
spec2viz render examples/sequence/example.yml --out /tmp/nonexistent-dir/viz --renderer plantuml

# 12. Render múltiples archivos
spec2viz render examples/sequence/example.yml examples/state/example.yml --out /tmp/viz-out --renderer mermaid

# 13. Verificar que los archivos generados son válidos
ls -la /tmp/viz-out/
head -5 /tmp/viz-out/example.puml 2>/dev/null || head -5 /tmp/viz-out/example.mmd 2>/dev/null

# 14. Render con renderer no soportado para el tipo
# (ej: Vega para sequence — no debería funcionar)
spec2viz render examples/sequence/example.yml --out /tmp/viz-out --renderer vega 2>&1
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Documenta renderers y tipos soportados? |
| 2-8 | ¿Cada combinación tipo+renderer funciona? |
| 9 | ¿`--backend` es idéntico a `--renderer`? |
| 10 | ¿Dónde escribe si no hay --out? |
| 11 | ¿Crea directorios o error? |
| 12 | ¿Batch render? ¿Nombres de output únicos? |
| 13 | ¿El output es sintácticamente válido? |
| 14 | ¿Error claro para combinación no soportada? |

## Modos de fracaso

- Archivos generados en ubicación inesperada sin --out
- Output inválido sintácticamente para el renderer target
- `--renderer` y `--backend` se comportan distinto
- Combinaciones no soportadas: error confuso o crash
- Múltiples archivos: collision de nombres si tienen mismo filename
