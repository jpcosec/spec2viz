## REFORMULACION
Propósito: implementar en IR/ui la vista previa de una receta usando el lienzo copiado de surface, con zoom, arrastre, reinicio y apertura del documento del nodo en el panel derecho. Resultado: `RecipePreview` funcional y su test. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`, app `IR/ui/`. Límites: no tocar `sldb/`; fuera BPMN y notas; no calcular ni inventar datos; toda escritura mediante operación nombrada de `sldb serve`; copiar solo lo necesario de `sldb/surface`, citando origen y commit.

## AMBIGUEDADES
1. “Vista previa de la receta elegida”: no se define qué selecciona la receta ni dónde reside esa selección. Obligaría a inventar estado, evento y fuente de selección.
2. “reiniciar vuelve”: no se especifica a qué estado vuelve. Obligaría a inventar si restaura escala 1, ajuste inicial, posición cero o ambos.
3. “clic en un nodo pide /document y lo muestra en el panel”: no se fija el identificador enviado ni el contrato de actualización del panel. Obligaría a inventar parámetros y evento, salvo que U1 los determine.
4. “una captura en Chrome real… guardada en el run dir”: no se identifica el run dir ni el procedimiento concreto. Obligaría a inventar ruta y método de captura.
5. “commit” del origen copiado: no se indica cuál. Obligaría a determinar el commit vigente en ejecución, no a inventarlo.

## DRY-RUN
Un ejecutor leería el TaskDoc, U1, `PROPUESTA-UI.md`, `maqueta-ui.html`, `NotationSvgCanvas.tsx` y contratos de `/notations/view` y `/document`. Copiaría el lienzo con cabecera de procedencia, crearía `RecipePreview` y su test con payloads fijos, cablearía zoom/arrastre/reinicio y la apertura del documento en el panel. Dependencias: U1, endpoints y surface. Validaría con `cd ui && npx tsc --noEmit && npx vitest run src/compositions/RecipePreview.test.tsx`; después, prueba manual con store de pron y captura.

## FUTURO
U1 debe aportar el panel/cliente y sus contratos; U4 y U5 cubren BPMN y notas. Un humano decidirá la aceptación visual y verificará la captura; el cierre/commit corresponde al ritual de closeout.
