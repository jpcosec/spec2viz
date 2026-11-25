## REFORMULACION
El encargo es crear en el repo `/mnt/ssd/proyectos/SLDB_1/IR`, bajo `IR/ui/`, una app Vite + React TSX que arranque con el cascarón de specIR: explorador, pestañas Grafo/Anclajes/Composiciones, panel de documento y lentes Lectura/Fierros. Debe copiar de `sldb/surface` el cliente de `sldb serve`, los tokens de papel y los tipos de contrato, citando origen y commit. Resultado esperado: app mínima operativa, Shell con pestañas y lentes, cliente con URL/proxy correctos y tests que pasan. Límites: solo `IR/ui`; no tocar `sldb/`; no importar `@sldb/surface`; no implementar contenido de pestañas (U2-U9); la UI no calcula y no inventa datos.

## AMBIGUEDADES
1. “commit 39c51f6e de sldb origin/main o el HEAD que leas”: no fija qué commit usar; obliga a decidir y podría inventar la procedencia citada.
2. “paridad minima con la pagina de spec2viz (U1-U5)”: no define qué es “mínima”; obliga a inventar criterios de paridad.
3. “estructura del prototipo de Kimun, estetica del SLDB Workbench”: los archivos de contrato no están en el bundle; obliga a interpretarlos o inventar detalle visual.
4. “cd ui && npx tsc --noEmit…”: no indica desde qué directorio se ejecuta; obliga a asumir que es desde `IR/`.
5. “el cliente copiado tiene un test minimo con fetch mockeado”: no fija archivo ni comando; obliga a inventar su ubicación y si entra en la validación.

## DRY-RUN
Lecturas futuras: TaskDoc, `PROPUESTA-UI.md`, `maqueta-ui.html`, `surface/src/core/client.ts`, `surface/src/styles/paper-tokens.css`, `surface/src/core/contract.ts`, `surface/vite.config.ts` y `DESIGN.md`. Cambios previstos: crear `package.json`, `vite.config.ts`, `tsconfig`, `index.html`, `src/Shell.tsx`, estilos y tests; copiar archivos con cabecera de origen; configurar `VITE_SLDB_URL` con default `/sldb` y proxy a `SLDB_TARGET`. Dependencias: acceso al repo `sldb`, Node/npm, `sldb serve` futuro en `8085`. Validaciones futuras: `npx tsc --noEmit` y `npx vitest run src/Shell.test.tsx`; verificar cabeceras y que no se modifica `sldb/`.

## FUTURO
U2-U9 aportarán contenido de pestañas; un humano decidirá commit exacto de `sldb` si procede, revisará la estética y aprobará el cierre. La ejecución real y el arranque de `sldb serve` quedan fuera de este nodo.
