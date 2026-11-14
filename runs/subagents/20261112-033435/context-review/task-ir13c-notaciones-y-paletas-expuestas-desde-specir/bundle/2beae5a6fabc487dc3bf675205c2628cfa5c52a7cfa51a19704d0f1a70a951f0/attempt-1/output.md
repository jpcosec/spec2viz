REFORMULACION
El nodo es una tarea de código ejecutable en el repo specIR. Propósito: cerrar la migración de spec2viz permitiendo que specIR exponga las operaciones de notaciones y paletas que spec2viz ofrece por CLI. Resultado: `src/specir/visual/notations.py` como envoltorio de la API pública de SLDB para listar, validar, sincronizar y resolver notaciones, y listar, validar y sincronizar paletas con comprobación de contraste; pruebas portadas en `tests/visual/test_notations.py` y `tests/visual/test_palettes.py`. Límites: no redefinir modelos de vocabulario visual, no reimplementar el resolvedor, no tocar catálogos, CLI general ni consumidores.

AMBIGUEDADES
1. “las pruebas de spec2viz de notación, vista de notación y paleta”: no se nombran rutas ni versión; obligaría a inventar qué pruebas, fixtures y golden se portan.
2. “llama a las operaciones de notaciones y vistas de la API pública de SLDB”: no se nombran funciones, firmas ni contrato de retorno; obligaría a inventar el mapeo entre operaciones de spec2viz y símbolos de `sldb.api`.
3. “Listar notaciones y paletas desde specIR devuelve las builtin”: no se define la interfaz pública de specIR ni la forma de salida; obligaría a inventar funciones y estructura de datos.
4. “incluido el contraste insuficiente”: no se fija umbral ni regla; si SLDB no la expone, obligaría a inventar el criterio.

DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout, pills, átomos; los tres archivos nombrados; como solo lectura, pruebas/fixtures/golden de spec2viz y la matriz. Cambios previstos: implementar envoltorios en `notations.py`; portar pruebas y fixtures reales a `tests/visual/`; no importar spec2viz ni módulos internos de SLDB. Dependencias: operaciones públicas de SLDB para notaciones, paletas, contraste y vista; store de prueba real; pruebas de spec2viz; `task-ir07`. Si falta una operación, detenerse y reportar. Validaciones futuras: las cinco condiciones de Validation, más `tests/test_imports.py`; ejecutar primero pruebas visuales focalizadas y luego cobertura más amplia.

FUTURO
Otro nodo o un humano debe aportar la selección exacta de pruebas/golden de spec2viz, confirmar el mapeo de API pública disponible y actualizar las filas de la matriz de cobertura; `task-ir07` y el gate de retiro dependen de este resultado.
