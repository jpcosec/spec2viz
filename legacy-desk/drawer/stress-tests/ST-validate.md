# ST-validate: spec2viz validate — diagram spec validation

**Basado en:** UC-01

## Script

```bash
# 1. Help
spec2viz validate --help

# 2. Validar sequence diagram válido
spec2viz validate examples/sequence/example.yml

# 3. Validar state diagram válido
spec2viz validate examples/state/example.yml

# 4. Validar component diagram válido
spec2viz validate examples/component/example.yml

# 5. Validar activity diagram válido
spec2viz validate examples/activity/example.yml

# 6. Validar deployment diagram válido
spec2viz validate examples/deployment/example.yml

# 7. Validar matrix diagram válido
spec2viz validate examples/matrix/example.yml

# 8. Validar archivo inexistente
spec2viz validate /tmp/nonexistent.yml

# 9. Validar archivo YAML inválido
echo "not: yaml: :" > /tmp/bad.yml
spec2viz validate /tmp/bad.yml

# 10. Validar archivo con schema inválido (tipo de diagrama desconocido)
echo "type: unknown_diagram" > /tmp/unknown-type.yml
spec2viz validate /tmp/unknown-type.yml

# 11. Validar archivo con error semántico (referencia a nodo inexistente)
spec2viz validate tests/fixtures/invalid/bad_sequence.yml
spec2viz validate tests/fixtures/invalid/bad_state.yml
spec2viz validate tests/fixtures/invalid/bad_activity.yml

# 12. Validar múltiples archivos
spec2viz validate examples/sequence/example.yml examples/state/example.yml examples/component/example.yml

# 13. Validar directorio (si soporta)
spec2viz validate examples/ 2>&1 || echo "Directory not supported"

# 14. Validar con output redirigido
spec2viz validate examples/sequence/example.yml > /tmp/viz-validate-output.txt 2>&1
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El help documenta el formato? |
| 2-7 | ¿Todos los tipos de diagrama se validan correctamente? |
| 8 | ¿Error: file not found? |
| 9 | ¿YAML parse error claro? |
| 10 | ¿Error: unknown diagram type? |
| 11 | ¿Errores semánticos claros? (¿línea? ¿detalle?) |
| 12 | ¿Batch validation? ¿Exit code? |
| 13 | ¿Soporta directorios? |
| 14 | ¿Output limpio? |

## Modos de fracaso

- Error "OK" para archivos inválidos
- Mensajes de error sin línea/columna
- Silent success para archivos que no son diagram specs
- No distingue error sintáctico vs semántico
