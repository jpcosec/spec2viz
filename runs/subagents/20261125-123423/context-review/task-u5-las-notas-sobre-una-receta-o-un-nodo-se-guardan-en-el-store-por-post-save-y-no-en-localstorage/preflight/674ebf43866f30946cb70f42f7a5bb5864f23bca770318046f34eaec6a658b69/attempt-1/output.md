## REFORMULACION
No es un agregado: es una tarea `task.code` ejecutable. **Propósito:** añadir notas sobre una receta o un nodo en la UI nueva de specIR, persistidas en el store mediante `POST /save`, nunca en `localStorage`. **Resultado:** notas con lista, alta y edición usando `CatalogAnnotationsDoc`; test `src/notes/Notes.test.tsx` con fetch mockeado (lista, alta con payload esperado, 409 muestra conflicto). **Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`, app en `IR/ui/`. **Límites:** trabajar en `IR/ui/src/notes/` y su test; no tocar `sldb/`; no crear modelos nuevos en sldb/specIR; copiar de `sldb/surface` lo necesario, con cabecera de origen; toda escritura por operación nombrada de sldb serve; sin datos inventados.

## AMBIGUEDADES
1. «Notas sobre la receta o el nodo»: no define campos ni cómo se asocia la nota a receta/nodo; obligaría a inventar esquema y payload.
2. «lista, alta y edición»: no describe el flujo de edición ni qué se actualiza; obligaría a inventar UI y semántica.
3. «POST /save de sldb serve con expected (control optimista) como hace surface»: no da endpoint base, forma del payload ni origen/valor de `expected`; obligaría a inspeccionar surface o inventar contrato.
4. «un 409 muestra el conflicto»: no define mensaje, estado ni recuperación; obligaría a inventar comportamiento UX.
5. «cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit)»: no indica commit ni archivos concretos; obligaría a inventar procedencia.
6. «IR/ui/src/notes/ y su test»: no fija nombres/estructura interna; obligaría a inventar organización de archivos.

## DRY-RUN
Lecturas hipotéticas: TaskDoc, `PROPUESTA-UI.md`, `maqueta-ui.html`, `CatalogAnnotationsDoc` y `annotations.py`, implementación de `POST /save` en surface, configuración de vitest/tsc. Cambios previstos: componentes/estado en `ui/src/notes/`, cabeceras de origen y `Notes.test.tsx` con fetch mockeado. Dependencia: U3. Validaciones futuras: `cd ui && npx tsc --noEmit && npx vitest run src/notes/Notes.test.tsx`, más revisión de que no hay `localStorage` ni escrituras fuera de `/save`.

## FUTURO
Un humano debe resolver las ambigüedades 1–5 o aportar el contrato de surface. Otro nodo (U3) entrega la superficie de receta/nodo. La página de catalog build (D9) comparte `CatalogAnnotationsDoc`. Johanes hará revisión en frío.
