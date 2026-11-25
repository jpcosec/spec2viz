## REFORMULACION
Encargo de implementación (`task.code`): en el repo `/mnt/ssd/proyectos/SLDB_1/IR`, app `IR/ui/`, construir `RecipePreview` para dibujar la receta elegida con el payload de `/notations/view`, usando una copia de `NotationSvgCanvas.tsx` con cabecera de origen, y permitir zoom, arrastre, reinicio y clic en nodo para abrir su documento en el panel derecho. Entregable: composición, lienzo copiado, test `src/compositions/RecipePreview.test.tsx`, `tsc` y `vitest` en verde, más captura real en Chrome de una spec de pron citada en `result-summary.md`. Límites: no tocar `sldb/`, fuera BPMN y notas, React/TSX, sin datos inventados, toda escritura vía `sldb serve`.

## AMBIGUEDADES
1. “la receta elegida”: no se define cómo se elige ni dónde vive la selección; obligaría a inventar estado, ruta o selector.
2. “el payload de /notations/view”: faltan parámetros, forma de petición y esquema de respuesta; obligaría a inventar el contrato.
3. “El documento del nodo sale de /document”: no se indica cómo obtener el id del nodo ni la forma de respuesta; obligaría a inventar el mapeo y el render.
4. “cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit)”: no se da el commit; obligaría a inventarlo.
5. “Zoom y reinicio como botones” y “arrastre”: no se fijan incrementos, límites, base de reinicio ni semántica del arrastre; obligaría a inventarlos.
6. “el lienzo copiado y su test”: solo se nombra `NotationSvgCanvas.tsx`; no queda claro si también se copia su test; obligaría a decidir/inventar.
7. “una captura en Chrome real ... guardada en el run dir”: no se especifica ruta del run dir ni qué spec de pron usar; obligaría a inventarlas.
8. “abre su documento en el panel derecho”: no se define la API del panel ni qué elementos SVG son nodos clicables; obligaría a inventar ambos.

## DRY-RUN
Lecturas hipotéticas: TaskDoc, `PROPUESTA-UI.md`, `maqueta-ui.html`, `NotationSvgCanvas.tsx`, configuración de `ui/`, tests y cliente existentes. Cambios previstos: copiar el lienzo con cabecera, crear `RecipePreview`, estilos mínimos y test con payloads fijos. Dependencias: U1 (esqueleto, panel, tokens, cliente), endpoints `/notations/view` y `/document`, y `sldb serve` contra el store de pron para la prueba manual. Validaciones futuras: `npx tsc --noEmit`, `npx vitest run src/compositions/RecipePreview.test.tsx`, y captura manual en Chrome.

## FUTURO
U1 debe aportar el panel derecho, tokens y cliente. Un humano debe fijar el commit citado, confirmar contratos de endpoints y elegir la spec de pron para la captura. El entorno debe proporcionar Chrome y el run dir.
