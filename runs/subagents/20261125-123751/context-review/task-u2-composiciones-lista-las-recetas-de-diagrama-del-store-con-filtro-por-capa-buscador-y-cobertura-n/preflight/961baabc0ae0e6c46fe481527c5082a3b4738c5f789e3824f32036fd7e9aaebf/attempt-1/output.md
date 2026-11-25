# REFORMULACION

**Propósito:** construir en la pestaña Composiciones de la UI de specIR la lista de recetas de diagrama que sirve sldb, con filtro por capa, buscador por título y cobertura n/m cuando exista.

**Resultado:** componente `RecipeList` en `IR/ui/src/compositions/` más su test, que lista recetas desde el payload del endpoint que corresponda (`/notations`, o `/views` si trae specs), filtra, busca y muestra n/m o `—`.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`, app en `IR/ui/`; no tocar `sldb/`. React+TSX (D10), copia desde `sldb/surface` con cabecera de origen (D7), vitest + testing-library, accesibilidad (D3), la UI no calcula.

**Límites:** fuera vista previa (U3), BPMN (U4), notas (U5). Validación: `npx tsc --noEmit && npx vitest run src/compositions/RecipeList.test.tsx`.

# AMBIGUEDADES

1. "la lista sale de /notations (o de ambos); verificar con sldb serve ... cual devuelve sus 15 specs y usar ese" — obliga a decidir entre `/notations`, `/views` o ambos, y a ejecutar `sldb serve` contra pron para elegir; el input no fija el criterio final.
2. "con filtro por capa" — no define qué es "capa" ni el campo del payload que la contiene; obligaría a inventar campo y valores.
3. "buscador por titulo" — no nombra el campo de título del SpecDoc; obligaría a inventar la clave.
4. "usar el campo que el payload de vistas traiga; si no lo trae, mostrar '—'" frente a "La cobertura n/m no esta en views_payloads.py ni notations_payloads.py: saldra '—'" — no queda claro si hay que buscar un campo alternativo o asumir siempre `—`.
5. "cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit)" — no se da el commit concreto; obligaría a elegirlo.
6. Referencias a "D7", "D10", "D3", `PROPUESTA-UI.md` y maqueta: son fuentes externas al input; sin ellas habría que inferir contrato y estética.

# DRY-RUN

**Lecturas:** este TaskDoc; `PROPUESTA-UI.md` y `maqueta-ui.html`; `sldb/surface/src/core/client.ts`, `views_routes.py`, `notations_payloads.py`; salida de `sldb serve` sobre `/mnt/ssd/proyectos/SLDB_1/pron/.sldb`; esqueleto de U1.

**Cambios previstos:** `ui/src/compositions/RecipeList.tsx` (o equivalente), fixture del payload real, `RecipeList.test.tsx`, nota en `result-summary.md`.

**Dependencias:** U1 (esqueleto/pestañas); endpoint y forma del payload; disponibilidad del store de pron.

**Validaciones futuras:** `tsc --noEmit`, `vitest` del test, prueba manual con captura/salida anotada.

# FUTURO

Johanes revisa en frío el resultado; sldb responde por inbox con la cobertura n/m; U3 consume la selección de receta. La elección definitiva de endpoint y el criterio de "capa" requieren decisión humana si persisten las ambigüedades 1–2.
