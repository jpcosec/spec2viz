## REFORMULACION
Encargo ejecutable: implementar en `IR/ui/src/compositions/` la lista de recetas de diagrama del store para la pestaña Composiciones, con filtro por capa, buscador por título y cobertura de átomos `n/m` cuando el payload la aporte; si no, mostrar `—` sin calcularla. Resultado: componente y `RecipeList.test.tsx` que pasen `tsc` y `vitest`. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`, app en `IR/ui/`. Límites: no tocar `sldb/`; fuera vista previa (U3), BPMN (U4) y notas (U5); no calcular datos ni inventarlos; copiar de `sldb/surface` solo lo necesario, con cabecera de origen y commit; controles con rol y nombre accesible.

## AMBIGUEDADES
1. Endpoint contradictorio: «Las recetas salen de sldb serve: /views» frente a «la lista sale de /notations (o de ambos); verificar con sldb serve sobre el store de pron cual devuelve sus 15 specs y usar ese». Obligaría a inventar si se usa `/views`, `/notations` o una unión.
2. Criterio de aceptación: «RecipeList muestra, filtra y busca recetas desde el payload de /views» frente a la verificación real con 15 `SpecDoc` de pron. Obligaría a inventar una fusión o fallback no especificado.
3. Forma del payload de prueba: solo se pide «un payload fijo», sin esquema ni campos de capa, título y cobertura. Obligaría a inventar nombres de campos y fixture.
4. Filtro por capa: no se define qué campo del payload representa la capa ni si los valores son fijos. Obligaría a inventar el criterio de filtrado.
5. Cobertura: «cuando sldb la da» y luego «saldrá '—'». No se nombra el campo exacto que, si existiera, debería leerse. Obligaría a inventar su ruta.

## DRY-RUN
Un ejecutor leería `PROPUESTA-UI.md`, `maqueta-ui.html`, `surface/src/core/client.ts`, `views_routes.py`, las rutas de notaciones y la UI de U1. Cambiaría la lista en `IR/ui/src/compositions/` y añadiría `RecipeList.test.tsx`; anotaría en `result-summary.md` la ausencia de cobertura. Depende de U1, de `sldb serve`, React/TSX, vitest y Testing Library. Validaría con `npx tsc --noEmit` y `npx vitest run src/compositions/RecipeList.test.tsx`; después levantaría `sldb serve --store /mnt/ssd/proyectos/SLDB_1/pron/.sldb` y comprobaría 15 specs y `—` en cobertura.

## FUTURO
Johanes hará la revisión en frío. sldb podría añadir el campo de cobertura pedido por inbox. U3, U4 y U5 consumirán la lista o su selección. Un humano anotará la captura o salida manual en `result-summary.md`.
