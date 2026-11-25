## REFORMULACION
El encargo es crear en `/mnt/ssd/proyectos/SLDB_1/IR/ui/` el esqueleto de una app Vite + React TSX para specIR: arranque, cascarón con explorador, pestañas Grafo/Anclajes/Composiciones, panel de documento, lentes Lectura/Fierros y cliente de `sldb serve`. Debe copiar de `sldb/surface` —con cabecera de origen y commit— `client.ts`, `paper-tokens.css` y `contract.ts`, configurar `VITE_SLDB_URL` con default `/sldb` y proxy a `SLDB_TARGET` (default `http://127.0.0.1:8085`), y añadir tests. Límites: solo `IR/ui`; no tocar `sldb/`; no implementar contenido de pestañas (U2-U9); la UI no calcula ni inventa datos. Resultado observable: `tsc --noEmit` y `vitest` de `src/Shell.test.tsx` pasan.

## AMBIGUEDADES
1. “commit 39c51f6e de sldb origin/main o el HEAD que leas, citandolo”: no fija si debe usarse ese commit o el HEAD disponible. Obliga a decidir el criterio de fallback y qué commit citar.
2. “el lienzo importa tipos de surface/src/core/contract.ts”: “lienzo” no está definido en el encargo. Obliga a inventar si se refiere al panel de documento, al grafo o a otro componente.
3. “el cliente copiado tiene un test minimo con fetch mockeado”, pero la validación solo ejecuta `src/Shell.test.tsx`: no queda claro si el test del cliente es obligatorio y si debe ejecutarse. Obliga a decidir el alcance real de la validación.
4. “la app COPIA de sldb/surface lo que necesita”: además de los archivos nombrados, no se enumeran todas las dependencias copiadas. Obliga a descubrir imports y decidir qué más copiar.

## DRY-RUN
Un ejecutor futuro leería `PROPUESTA-UI.md`, `maqueta-ui.html`, `surface/vite.config.ts`, `surface/DESIGN.md`, `client.ts`, `contract.ts` y `paper-tokens.css` en el commit elegido. Crearía `ui/package.json`, `vite.config.ts`, `tsconfig`, `index.html`, `src/` y copiaría archivos con cabecera de origen. Implementaría `Shell` con tres pestañas accesibles, dos lentes, panel vacío honesto y cliente configurable. Añadiría `Shell.test.tsx` y el test del cliente. Dependencias: archivos fuente, toolchain Node/Vite/Vitest y decisiones D7/D10. Validaciones futuras: `cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx`; comprobar cabeceras y ausencia de cambios en `sldb/`. No se ejecuta nada.

## FUTURO
Otros nodos U2-U9 aportarán contenido de pestañas y selección de nodos. Un humano o revisor confirmará el commit fuente si HEAD difiere y decidirá si el test del cliente entra en la validación.
