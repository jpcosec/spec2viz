# ST-edge-cases: spec2viz edge cases

**Basado en:** UC-01, UC-02, UC-03, UC-04

## Script

```bash
# 1. YAML malformado
echo "not: yaml: :" > /tmp/viz-bad.yml
spec2viz validate /tmp/viz-bad.yml
spec2viz render /tmp/viz-bad.yml --out /tmp/viz-edge

# 2. Archivo no existente
spec2viz validate /tmp/nonexistent.yml
spec2viz render /tmp/nonexistent.yml --out /tmp/viz-edge

# 3. Archivo vacío
echo "" > /tmp/viz-empty.yml
spec2viz validate /tmp/viz-empty.yml

# 4. Directorio en vez de archivo
spec2viz validate examples/
spec2viz render examples/ --out /tmp/viz-edge

# 5. Path con espacios
mkdir -p "/tmp/viz test spaces"
spec2viz validate "examples/sequence/example.yml"  # archivo sin espacios, pero path con espacios en CWD

# 6. UTF-8 en diagrama (nombres con ñ, emojis)
cat > /tmp/viz-utf8.yml << 'EOF'
type: sequence
id: utf8-test
title: "Diagrama ñoño 🎉"
data:
  participants:
    - id: usuario
      kind: actor
    - id: sistema
      kind: system
  messages:
    - from_: usuario
      to: sistema
      message: "Petición ñoña 🎉"
      kind: request
EOF
spec2viz validate /tmp/viz-utf8.yml
spec2viz render /tmp/viz-utf8.yml --out /tmp/viz-edge --renderer plantuml
head -10 /tmp/viz-edge/utf8-test.puml 2>/dev/null

# 7. Múltiples --renderer
spec2viz render examples/sequence/example.yml --out /tmp/viz-edge --renderer plantuml --renderer mermaid 2>&1

# 8. Help consistency
spec2viz --help > /tmp/viz-help1.txt
spec2viz -h > /tmp/viz-help2.txt
diff /tmp/viz-help1.txt /tmp/viz-help2.txt && echo "-h and --help identical" || echo "DIFERENTES"
spec2viz 2>&1 | head -5

# 9. Error messages: stdout vs stderr
spec2viz validate /tmp/nonexistent.yml 2>/dev/null   # solo stdout
spec2viz validate /tmp/nonexistent.yml >/dev/null     # solo stderr

# 10. Flag desconocido
spec2viz validate --unknown-flag examples/sequence/example.yml 2>&1

# 11. Comando desconocido
spec2viz unknown-command 2>&1

# 12. Muy largo archivo de input
python3 -c "
# Generate a sequence diagram with 1000 messages
print('type: sequence')
print('id: large-test')
print('title: Large diagram')
print('data:')
print('  participants:')
for i in range(100):
    print(f'    - id: p{i:03d}')
    print(f'      kind: system')
print('  messages:')
for i in range(1000):
    print(f'    - from_: p{i%%100:03d}')
    print(f'      to: p{(i+1)%%100:03d}')
    print(f'      message: \"Message {i}\"')
    print(f'      kind: request')
" > /tmp/viz-large.yml
spec2viz validate /tmp/viz-large.yml 2>&1
time spec2viz render /tmp/viz-large.yml --out /tmp/viz-edge --renderer mermaid 2>&1

# 13. entry point: spec2viz vs python -m spec2viz
python -m spec2viz --help > /tmp/viz-py-help.txt 2>&1
diff /tmp/viz-help1.txt /tmp/viz-py-help.txt && echo "CLI and python -m identical" || echo "DIFERENTES"

# 14. spec2viz --version
spec2viz --version 2>&1 || echo "No --version flag"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1-4 | Errores claros para inputs inválidos |
| 5 | Espacios en paths |
| 6 | UTF-8 en diagramas |
| 7 | Múltiples flags iguales |
| 8 | -h vs --help idénticos |
| 9 | Errores a stderr |
| 10-11 | Errores argparse claros |
| 12 | Performance con diagramas grandes |
| 13 | spec2viz y python -m iguales |
| 14 | ¿--version? |

## Modos de fracaso

- UTF-8 produce error de encoding
- Performance pésima con 1000 mensajes
- Múltiples --renderer: crash o comportamiento inesperado
- Errores a stdout en vez de stderr
- Sin --version flag
- `python -m spec2viz` distinto de `spec2viz`
