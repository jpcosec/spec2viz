# ST-test-suite-health: spec2viz test suite health

**Basado en:** UC-01, UC-02, UC-03, UC-04, UC-05, UC-06

## Script

```bash
# 1. Run full test suite with verbose output
python -m pytest tests/ -v --no-header 2>&1 | head -60

# 2. Run full test suite — summary only
python -m pytest tests/ --tb=no --no-header -q 2>&1

# 3. Run with warnings as errors
python -m pytest tests/ -W error::UserWarning --no-header -q 2>&1

# 4. Check for skipped tests
python -m pytest tests/ -v --no-header -rs 2>&1 | tail -20

# 5. Check for xfailed tests
python -m pytest tests/ -v --no-header -rx 2>&1 | tail -20

# 6. Collect only (dry run, check discovery)
python -m pytest tests/ --collect-only --no-header -q 2>&1

# 7. Run specific test modules
python -m pytest tests/test_cli.py --no-header -q 2>&1
python -m pytest tests/test_api.py --no-header -q 2>&1
python -m pytest tests/test_validator.py --no-header -q 2>&1
python -m pytest tests/test_compilers.py --no-header -q 2>&1
python -m pytest tests/test_renderers.py --no-header -q 2>&1
python -m pytest tests/test_base_model.py --no-header -q 2>&1

# 8. Check test isolation: each test creates and cleans up its own files
python -m pytest tests/ --basetemp=/tmp/pytest-tmp --no-header -q 2>&1

# 9. Are there asyncio tests?
python -m pytest tests/ --co -q 2>&1 | grep -c "async" || echo "No async tests"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿Todos los tests pasan? ¿Hay warnings de deprecación? |
| 2 | ¿Conteo total de tests? |
| 3 | ¿Hay warnings que serían errores en CI estricto? |
| 4-5 | ¿Tests skipped o xfailed? ¿Razones claras? |
| 6 | ¿Discovery encuentra todos los tests esperados? |
| 7 | ¿Cada módulo corre independientemente? |
| 8 | ¿Los tests contaminan el sistema de archivos? |
| 9 | ¿Hay tests asyncio? (sugiere async API) |

## Modos de fracaso

- Tests que pasan en desarrollo pero fallarían en CI (warnings → errors)
- Dependencia entre tests (orden-dependentes)
- Tests que dejan archivos temporales sin limpiar
- Coverage gaps entre módulos
