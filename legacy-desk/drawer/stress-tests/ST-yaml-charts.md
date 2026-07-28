# ST-yaml-charts: Legacy yaml_charts compatibility

**Basado en:** UC-06

## Script

```bash
# 1. Import legacy module directly
python3 -c "
try:
    import yaml_charts
    print('yaml_charts imported successfully')
except ModuleNotFoundError as e:
    print(f'ModuleNotFoundError: {e}')
except Exception as e:
    print(f'Import error: {type(e).__name__}: {e}')
" 2>&1

# 2. Import specific public functions from legacy namespace
python3 -c "
try:
    from yaml_charts import load, validate, compile_ir, render, render_to_file
    print('All functions importable from yaml_charts')
except Exception as e:
    print(f'Import error: {type(e).__name__}: {e}')
" 2>&1

# 3. Check if top-level yaml_charts module exists in site-packages
python3 -c "
import importlib.util
spec = importlib.util.find_spec('yaml_charts')
print(f'Module spec: {spec}')
" 2>&1

# 4. Check if yaml_charts is in sys.modules after spec2viz import
python3 -c "
import sys
import spec2viz
print(f'yaml_charts in sys.modules: {\"yaml_charts\" in sys.modules}')
print(f'spec2viz.spec2vix in sys.modules: {\"spec2viz.spec2vix\" in sys.modules}')
# Show what spec2vix registered
for k in sorted(sys.modules.keys()):
    if 'spec2vix' in k:
        print(f'  {k}')
" 2>&1

# 5. Check if spec2vix.__init__.py registers yaml_charts as a top-level alias
python3 -c "
import spec2viz.spec2vix
print(f'spec2vix loaded')
import sys
print(f'yaml_charts alias in sys: {\"yaml_charts\" in sys.modules}')
" 2>&1

# 6. Test the legacy CLI entry point if it exists
which yaml-charts 2>/dev/null && yaml-charts --help 2>&1 || echo "yaml-charts CLI not found"

# 7. Check CHANGELOG mentions of backward compatibility
grep -A3 "compatibility\|shim\|legacy\|deprecat" CHANGELOG.md 2>/dev/null || echo "No compatibility mentions in CHANGELOG"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Import legacy module funciona? |
| 2 | ¿Import legacy functions funciona? |
| 3 | ¿Hay módulo físico? |
| 4 | ¿spec2viz registra alias automáticamente? |
| 5 | ¿spec2vix crea top-level alias? |
| 6 | ¿Existe comando `yaml-charts`? |
| 7 | ¿CHANGELOG menciona compatibilidad? |

## Modos de fracaso

- `import yaml_charts` no funciona (ModuleNotFoundError)
- Compatibilidad documentada pero no implementada
- Alias parcial (algunas funciones sí, otras no)
- Sin deprecation warning al importar
- README/atoms documentan compatibilidad que no existe
