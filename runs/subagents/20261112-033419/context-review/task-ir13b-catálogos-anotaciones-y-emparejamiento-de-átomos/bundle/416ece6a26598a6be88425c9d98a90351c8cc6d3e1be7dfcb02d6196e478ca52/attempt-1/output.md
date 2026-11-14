## REFORMULACION
Nodo ejecutable `task.code` (no agregado). Propósito: migrar a specIR las capacidades de catálogo de spec2viz. Resultado: `catalog.py`, `catalog_serve.py` y `atoms.py` con registro `vistas.yml`, stores jerárquicos, catálogo HTML autocontenido, sincronización, validación, servidor local con autoguardado de anotaciones, emparejamiento explícito/difuso de átomos y cobertura por vista. Repo: specIR; pruebas en `tests/visual/`. Límites: fuera sincronización de un spec individual, notaciones/paletas, CLI y migración de consumidores; no importar spec2viz; solo API pública `sldb.api`; sin mocks ni datos fabricados; paridad demostrada con pruebas/goldens de spec2viz. Depende de IR13a e IR12. TaskDoc en `draft`.

## AMBIGUEDADES
1. “Cada pieza se migra tal cual o se reemplaza, según la matriz de cobertura.” La matriz no está en el input; obliga a inventar qué piezas se migran y cuáles se reemplazan.
2. “los mismos errores tipados que spec2viz sobre los fixtures de catálogo.” No se dan rutas, fixtures ni taxonomía; obliga a inventar el contrato de errores.
3. “el mismo contenido que spec2viz” y “mismas vistas, categorías y navegación” no fijan formato, orden ni serialización; obliga a inventar el criterio de comparación.
4. “Una anotación hecha en el servidor local queda guardada y reaparece al recargar.” No define almacenamiento, concurrencia, autoguardado ni rutas; obliga a inventar el comportamiento del servidor.
5. “emparejamiento de átomos con elementos de diagrama (explícito y difuso)” no define algoritmo, umbral ni desempate; obliga a inventar la heurística. “advertencia, o error en modo estricto” no define el selector de modo; obliga a inventar su interfaz.

## DRY-RUN
Un ejecutor futuro leería el TaskDoc, rituales, pills, átomos y, como referencia de solo lectura, archivos fuente/pruebas nombrados, fixtures/goldens de spec2viz y matriz. Prevé crear/modificar los seis archivos listados, portando pruebas de catálogo, rutas, vistas resueltas y emparejamiento. Depende de IR13a (sincronización), IR12 (renderizadores), API pública SLDB y fixtures reales. Validaría primero pruebas pequeñas: validación, sincronización sin escritura parcial, HTML sin recursos externos, anotación persistente, emparejamiento/cobertura e import guard; luego `tests/test_imports.py`. No ejecuta nada.

## FUTURO
IR13a entrega la sincronización de specs; IR12, renderizadores y recursos. Un humano decide en la matriz las filas, el modo estricto y el gate de retiro; closeout actualiza el board y prepara el commit.
