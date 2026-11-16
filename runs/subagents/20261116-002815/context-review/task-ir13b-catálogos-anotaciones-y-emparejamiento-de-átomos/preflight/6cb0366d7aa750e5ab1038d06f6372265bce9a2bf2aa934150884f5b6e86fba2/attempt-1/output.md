## REFORMULACION

Encargo ejecutable de tipo `task.code` en el repo **specIR**. Propósito: completar la migración de spec2viz construyendo la capa visual de catálogos de diagramas y su emparejamiento de átomos mediante `sldb.api.matching` (D4). Resultado: `specir.visual` registra vistas (`vistas.yml`) y stores jerárquicos, construye/sincroniza/valida un catálogo HTML autocontenido con los renderers de IR12, sirve catálogo y anotaciones con `sldb serve` si alcanza, y reporta emparejamiento y cobertura por vista llamando a SLDB. Límites: no implementar matching en specIR, no sincronizar specs individuales, no definir notaciones/paletas, CLI ni migrar consumidores. Depende de IR13a, IR12 y la tarea espejo D4; usa solo API pública de SLDB, sin mocks, y demuestra paridad con pruebas/fixtures de spec2viz.

## AMBIGUEDADES

1. «el catálogo se sirve con sldb serve si alcanza»: no define «alcanza»; obligaría a inventar criterio, umbral y fallback.
2. «si sldb serve no alcanza para las anotaciones, se pide por el desk de sldb»: no indica formato, responsable ni evidencia; obligaría a inventar el procedimiento.
3. «specIR conserva solo la parte visual del catálogo»: no separa visual de servidor/anotaciones; obligaría a inventar el límite.
4. «los mismos errores tipados que spec2viz»: no enumera tipos ni esquema; obligaría a inventar el mapeo.
5. «el mismo contenido», «las mismas vistas»: no fija normalización, orden ni rutas comparadas; obligaría a inventar equivalencia.
6. «advertencia, o error en modo estricto»: no define activación de modo estricto; obligaría a inventarla.
7. «su condición de retiro cumplida»: no incluye la matriz ni la condición; obligaría a inventar el criterio.

## DRY-RUN

Un ejecutor futuro leería esta TaskDoc, sus pills, IR13a, IR12, la API pública de `sldb.api.matching`, `sldb serve` y pruebas/fixtures de catálogo y átomos de spec2viz. Prevén cambios en `specir.visual`: registro de vistas, sincronización/validación, construcción offline del catálogo, integración de anotaciones y llamada delgada a matching. Dependencias: D4 publicada, renderers IR12, sincronización IR13a y capacidad de `sldb serve`. Validaría paridad de errores, contenido de store, catálogo sin recursos externos, persistencia de anotaciones, cobertura/átomos y ausencia de import de spec2viz. Sin ejecutar nada.

## FUTURO

La tarea espejo D4 entrega `sldb.api.matching`; IR13a e IR12 entregan sincronización y renderers. El desk de SLDB o un humano decide si `sldb serve` cubre anotaciones, aprueba el modo estricto si aplica y confirma la matriz de retiro.
