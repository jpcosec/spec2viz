## REFORMULACION

El nodo U2 es una tarea de código ejecutable (no agregado). **Propósito:** añadir la pestaña Composiciones con la lista de recetas de diagrama desde `sldb serve`, con filtro por capa, buscador por título y cobertura n/m cuando exista. **Resultado:** `RecipeList` y `RecipeList.test.tsx` en `IR/ui/src/compositions/`, con fixture de pron y aceptación manual anotada en `result-summary.md`. **Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`, app en `IR/ui/`. **Límites:** solo lista y su test; fuera vista previa (U3), BPMN (U4) y notas (U5); no tocar `sldb/`; la UI no calcula; copias de `sldb/surface` llevan cabecera con origen.

## AMBIGUEDADES

1. **Origen de recetas.** Cita: «la lista sale de /notations (o de ambos)». Obliga a inventar política de unión, deduplicación y orden si `/views` también trae specs.
2. **Qué es «capa».** Cita: «filtro por capa». No define campo, valores, coincidencia exacta/múltiple ni comportamiento vacío; obliga a inventar el modelo.
3. **Campo de título.** Cita: «buscador por titulo (parcial, sin distinguir mayusculas)». No fija clave (`title`/`titulo`/`name`) ni normalización de acentos; obliga a inventarlas.
4. **Cabecera de copia.** Cita: «ruta en sldb y commit». No hay commit fijado ni lista de archivos a copiar; obliga a inventar la procedencia.
5. **Fixture.** Cita: «fixture tomado de sldb serve sobre el store de pron». No indica ruta, nombre, tamaño ni si se versiona; obliga a inventar su ubicación.
6. **Interfaz con U1.** Cita: «depends_on: task-u1-esqueleto…». El bundle no incluye U1; obliga a inventar tokens, API de componentes y setup de test.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, rituales, `PROPUESTA-UI.md`, `maqueta-ui.html`, `surface/src/core/client.ts`, rutas/payloads de `/views` y `/notations`, código de U1 y configuración vitest. Crearía `RecipeList.tsx`, `RecipeList.test.tsx`, probablemente un fixture y tipos copiados con cabecera. Dependería de U1, de `sldb serve` sobre pron, del endpoint elegido y de la ausencia del campo de cobertura. Validaría con `npx tsc --noEmit`, `npx vitest run src/compositions/RecipeList.test.tsx`, y prueba manual con `sldb serve --store` de pron anotada en `result-summary.md`. Sin ejecutar.

## FUTURO

U3/U4/U5 consumirán la lista y su selección. sldb responderá por inbox sobre la cobertura. Johanes/JP confirmarán el endpoint si la verificación no basta. Un humano ejecutará la aceptación real, el cierre y el commit; la fase integrará la capa.
