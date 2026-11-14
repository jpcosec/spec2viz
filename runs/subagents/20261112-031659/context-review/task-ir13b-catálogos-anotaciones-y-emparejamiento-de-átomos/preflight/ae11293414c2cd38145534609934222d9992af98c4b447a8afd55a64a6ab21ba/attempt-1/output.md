REFORMULACION
Propósito: completar la migración de spec2viz a specIR en catálogo, anotaciones y emparejamiento de átomos. Resultado: módulos `catalog.py`, `catalog_serve.py` y `atoms.py`, más pruebas en `tests/visual/`. Repo: `SLDB_1/IR`, paquete `src/specir`. Límites: dentro, registro de vistas, stores, catálogo HTML, sincronización, validación, servidor con autoguardado, emparejamiento explícito/difuso y cobertura; fuera, sincronización de specs, notaciones/paletas, CLI y consumidores. Depende de IR13a e IR12; no debe importar spec2viz.

AMBIGUEDADES
1. “según la matriz de cobertura”: no se adjunta matriz; obliga a inventar filas, condiciones de retiro y qué piezas se copian o reemplazan.
2. “los mismos errores tipados que spec2viz”: no se listan tipos, códigos ni fixtures; obliga a inventar contrato de errores y equivalencia.
3. “el mismo contenido que spec2viz”: falta versión/fuente y definición de contenido; obliga a inventar formato y comparación.
4. “emparejamiento de átomos con elementos de diagrama (explícito y difuso)”: no se define algoritmo difuso, umbral ni desempates; obliga a inventar reglas.
5. “servidor local con autoguardado de anotaciones”: no se define almacenamiento, formato, concurrencia ni recuperación; obliga a inventar persistencia.
6. “servidor local”: no se define puerto, autenticación, recarga ni fallos; obliga a inventar operación.
7. “advertencia, o error en modo estricto”: no se define cómo se activa el modo estricto sin CLI; obliga a inventar API/configuración.

DRY-RUN
Un ejecutor futuro leería el TaskDoc, las pills, los módulos listados y las salidas de IR13a/IR12; si faltan matriz, fixtures o referencia spec2viz, se detendría. Cambios previstos: crear/ajustar `catalog.py`, `catalog_serve.py`, `atoms.py` y portar pruebas. Dependencias: APIs de sincronización de IR13a y renderizadores de IR12. Validaciones futuras: ejecutar los seis checks de Validation, incluida la ausencia de import spec2viz. Nada ejecutado.

FUTURO
Humano u otro nodo aporta matriz de cobertura, fixtures y referencia spec2viz; decide criterios de retiro y activación estricta. IR13a/IR12 entregan APIs. Un nodo posterior ejecutará pruebas y verificará paridad.
