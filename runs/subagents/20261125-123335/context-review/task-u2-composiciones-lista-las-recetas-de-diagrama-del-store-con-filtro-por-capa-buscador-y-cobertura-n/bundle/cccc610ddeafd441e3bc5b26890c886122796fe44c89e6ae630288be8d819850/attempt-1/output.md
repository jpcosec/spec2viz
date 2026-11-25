## REFORMULACION
**Propósito:** construir en `IR/ui/` la pestaña Composiciones con una lista de recetas de diagrama del store, filtro por capa, buscador y cobertura n/m cuando sldb la entregue, manteniendo paridad mínima con spec2viz (D7/D10).
**Resultado:** `src/compositions/RecipeList` y `RecipeList.test.tsx`; controles accesibles; sin cálculos en la UI; datos faltantes visibles como `—`.
**Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`, app en `IR/ui/`; no tocar `sldb/`.
**Límites:** fuera vista previa (U3), BPMN (U4) y notas (U5). La app copia de `sldb/surface` lo necesario con cabecera de origen/commit, sin importar `@sldb/surface`.

Nodo ejecutable de código, no agregado.

## AMBIGUEDADES
1. **Fuente de la lista:** el Goal pide “la lista de recetas (los diagramas/vistas del store de IR)” y Done When exige “desde el payload de /views”; la revisión dice “la lista sale de /notations (o de ambos)”. Elegir uno u otro obliga a inventar la fuente canónica y el contrato del payload.
2. **Forma del payload:** se ordena “usar el campo que el payload de vistas traiga”, pero no se define ningún campo de capa, título ni cobertura. Implementar exige inventar nombres y estructura.
3. **Filtro por capa:** “filtro por capa” no especifica valores, campo ni comportamiento ante capa ausente. Obliga a inventar semántica.
4. **Buscador:** “busca por titulo” no define coincidencia exacta/parcial, mayúsculas ni campos indexados. Obliga a inventar criterio.
5. **Store de aceptación:** el Goal habla del “store de IR”, pero la aceptación usa el store de pron porque IR “no tiene SpecDoc ni ViewDoc”. Obliga a decidir si la prueba funcional sustituye al store objetivo.

## DRY-RUN
**Lecturas previstas:** TaskDoc; `PROPUESTA-UI.md`; `maqueta-ui.html`; `surface/src/core/client.ts`; `src/sldb/cli/serve/views_routes.py`; payloads de views/notations; test de U1.
**Cambios previstos:** crear `RecipeList.tsx`, su test con payload fijo y, si hace falta, tipos/cliente copiados con cabecera; anotar en `result-summary.md` la fuente elegida, la ausencia de cobertura y la evidencia manual.
**Dependencias:** U1 (esqueleto, tokens, pestañas, cliente); `sldb serve` con `/views` y/o `/notations`.
**Validaciones futuras:** `cd ui && npx tsc --noEmit && npx vitest run src/compositions/RecipeList.test.tsx`; prueba manual contra store de pron mostrando sus 15 SpecDoc.

## FUTURO
U1 entrega el cascarón y cliente; sldb debe aclarar endpoint canónico y campo de cobertura; johanes/humano valida la evidencia manual y decide si el store de pron satisface la aceptación; U3 consumirá la selección para vista previa.
