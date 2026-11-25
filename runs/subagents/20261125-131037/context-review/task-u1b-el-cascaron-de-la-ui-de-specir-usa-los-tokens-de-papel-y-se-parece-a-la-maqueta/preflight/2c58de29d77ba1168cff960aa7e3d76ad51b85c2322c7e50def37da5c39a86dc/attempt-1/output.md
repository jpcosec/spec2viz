## REFORMULACION

El nodo es una tarea de código ejecutable, no un agregado ni paquete. Propósito: cerrar la brecha visual detectada en U1, cuyo contrato funcional pasa pruebas pero en Chrome no respeta la forma. Resultado: que el cascarón de `IR/ui` use los tokens `--wb-*` de `src/styles/paper-tokens.css` y se parezca a `maqueta-ui.html#grafo`: pestañas y lentes monoespaciadas, borde de 2 px y activa en piedra; explorador y panel de documento con fondo/borde; títulos serif Newsreader; rail inferior; miga con nombre del store. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`, app `IR/ui`. Límites: solo estilos del cascarón y componentes del Shell y su test; queda fuera el contenido de las pestañas (U2-U9).

## AMBIGUEDADES

1. “Ajustar src/Shell.test.tsx solo si cambian roles o nombres”: no define qué roles/nombres ni el estado base; obligaría a inventar el criterio para tocar o no el test.
2. “se puede copiar en lo necesario citando origen”: no fija alcance de copia ni formato de cita; obligaría a inventar cuánto reutilizar y cómo atribuirlo.
3. “guardar dos capturas en el run dir”: no indica ruta ni nombres; obligaría a inventar ubicación y convención.
4. “las diferencias que queden”: admite diferencias residuales sin umbral; obligaría a inventar qué diferencia visual es aceptable frente a la maqueta.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, la dependencia U1, `paper-tokens.css`, `sldb/surface/DESIGN.md`, `sldb/surface/src/styles/app.css`, `maqueta-ui.html#grafo`, `Shell.tsx`, `shell.css` y `Shell.test.tsx`. Cambiaría estilos del cascarón para consumir `--wb-*`, eliminar apariencias nativas, aplicar fondos/bordes, títulos serif, rail y miga; tocaría el test solo bajo la condición indicada. Dependencias: U1 disponible, app arrancable en Chrome, maqueta accesible y tokens existentes. Validaciones futuras: `npx tsc --noEmit`, `npx vitest run src/Shell.test.tsx`, comparación visual lado a lado y capturas citadas en `result-summary.md`. Sin ejecutar nada.

## FUTURO

Un humano —previsiblemente johanes— decide si la equivalencia visual y las diferencias residuales son aceptables. Otros nodos U2-U9 aportan el contenido de pestañas.
