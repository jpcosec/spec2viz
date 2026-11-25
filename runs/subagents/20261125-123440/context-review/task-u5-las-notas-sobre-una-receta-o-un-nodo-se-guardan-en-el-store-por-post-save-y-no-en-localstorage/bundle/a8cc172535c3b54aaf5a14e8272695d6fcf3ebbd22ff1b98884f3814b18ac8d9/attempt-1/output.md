## REFORMULACION
El nodo U5 debe implementar en `/mnt/ssd/proyectos/SLDB_1/IR`, app `IR/ui/`, el módulo `src/notes/` y `Notes.test.tsx`: listar, dar de alta y editar notas sobre la receta o el nodo, guardándolas en el store de sldb mediante `POST /save` con `expected` (control optimista), sin `localStorage`. Usará `CatalogAnnotationsDoc`, ya existente y registrado; no creará modelos ni tocará `sldb/`. La UI no calcula ni inventa datos; si falta un dato, lo indica. Podrá copiar de `sldb/surface` con cabecera de origen, sin importar `@sldb/surface`. Límite: solo `src/notes/` y su test.

## AMBIGUEDADES
1. “Notas sobre la receta o el nodo”: no define cómo se elige o vincula la receta/nodo activo ni dónde vive la UI; obligaría a inventar el mecanismo de selección/contexto.
2. “con lista, alta y edición” frente a “lista, alta manda POST /save con el payload esperado, un 409 muestra el conflicto”: no aclara si edición entra en test y aceptación; obligaría a inventar cobertura y criterio de cierre para edición.
3. “un 409 muestra el conflicto”: no fija texto, componente ni recuperación; obligaría a inventar el mensaje y comportamiento.
4. “cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit)”: no da commit ni lista de archivos; obligaría a elegir procedencia no especificada.

## DRY-RUN
Nodo ejecutable (`task.code`), no agregado. Sin ejecutar: leería el TaskDoc, rituales, `PROPUESTA-UI.md`, `maqueta-ui.html`, `src/specir/visual/catalog/annotations.py:25-28` y su registro `add_model`, la implementación de `POST /save` con `expected` en `sldb/surface`, y el esquema de `CatalogAnnotationsDoc`. Crearía/cambiaría `IR/ui/src/notes/` —componentes, cliente de guardado, estados de carga/error/conflicto— y `Notes.test.tsx` con `fetch` mockeado; si copia archivos, añadiría cabecera con ruta y commit. Depende de U3 para el contexto receta/nodo y de `sldb serve`. Validaría con `cd ui && npx tsc --noEmit && npx vitest run src/notes/Notes.test.tsx`, además de roles/nombres accesibles y ausencia de `localStorage`.

## FUTURO
U3 debe aportar la receta/nodo seleccionado. Johanes/JP validan UX y copy de conflicto; closeout decide commit y enlace de conocimiento. La fase integra U1–U5 y valida el conjunto.
