## REFORMULACION
**Propósito:** IR13a conecta specIR con lo ya migrado a sldb: sincronizar specs al store (D1) y generar specs de componentes desde grafo, snapshot y AST de Python (D2), sin reimplementar nada. **Resultado:** pruebas de paridad y de store real en `tests/visual/test_sync_generation_parity.py`, ajustes en `tests/test_imports.py` y `tests/visual/test_visual_names.py`, docstring de `src/specir/visual/__init__.py` y filas de la matriz de cobertura actualizadas. **Repo:** specIR (`/mnt/ssd/proyectos/SLDB_1/IR`). **Límites:** fuera escribir SpecSync/generador, catálogos, notaciones y paletas, CLI, consumidores y retiro de spec2viz.

## AMBIGUEDADES
1. «o su reemplazo por proyección tiene la prueba equivalente declarada en la matriz»: no define qué reemplazo por proyección admite ni qué prueba lo acreditaría; obligaría a inventar el criterio de aceptación del caso desde grafo.
2. «los fixtures de sincronización son los specs válidos del corpus de IR11 … más los specs ARQ y FLOW»: no enumera el conjunto exacto; obligaría a inventar qué specs entran si el corpus cambia.
3. «Si el resultado de sldb difiere de spec2viz, la diferencia se declara en la matriz … o se pide el arreglo por el desk de sldb»: no fija cuándo declarar y cuándo bloquear; obligaría a inventar el umbral.
4. «portando a specIR solo lo que sldb no traiga ya con sus propias pruebas»: no dice cómo verificar qué traen D1/D2; obligaría a inventar un inventario de cobertura ajena.
5. «las filas de sincronización, importación de grafo y generación de la matriz» frente a «filas SV-E01, SV-F01 y SV-F02»: no aclara si SV-E02 queda incluida; obligaría a inventar el alcance de la actualización.

## DRY-RUN
**Lecturas:** TaskDoc, rituales, pills, átomos, tests citados, `pyproject.toml` y matriz. **Cambios previstos:** completar/ajustar las pruebas de sincronización, borrado, RelationTypeDoc, grafo, AST y paridad; actualizar comprobaciones de imports y nombres; documentar el uso directo de `sldb.api.notations` en `specir.visual`; actualizar filas SV-E01, SV-F01 y SV-F02. **Dependencias:** exportaciones de D1/D2/D3 en `sldb.api.notations`, `structuredLanguageDB[code]`, spec2viz instalado solo para paridad. **Validaciones futuras:** primero `tests/test_imports.py`; luego pruebas de store real sin spec2viz; después marcadas `parity`; finalmente revisión de la matriz y del gate. Sin ejecutar.

## FUTURO
D1 y D2 deben entregar la API en sldb; el desk de sldb puede recibir el pedido por imports anidados de SV-F02. IR13 decide el cierre de filas y el retiro de spec2viz; JP decide la fuente de verdad del diagrama.
