## REFORMULACION

El nodo es una tarea ejecutable (`task.code`), no un agregado. Su propósito es corregir el contrato visual del cascarón de `IR/ui` tras la revisión de johanes, haciendo que use los tokens de papel y se parezca a la maqueta. El resultado esperado es un cascarón con pestañas y lentes monoespaciadas, borde de 2 px y activa en piedra; explorador con fondo piedra y borde; panel de documento con borde; títulos serif; rail inferior; miga con el nombre del store. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`, app `IR/ui`. Límites: solo estilos del cascarón y componentes del Shell en `IR/ui/src` y su test; queda fuera el contenido de pestañas (U2-U9); usar variables `--wb-*`, sin colores a mano.

## AMBIGUEDADES

1. “guardar dos capturas en el run dir”: no define cuál es el run dir ni nombres/formato; obligaría a inventar ruta y convención.
2. “se parece a la maqueta” / “muestran el mismo cascaron”: no fija tolerancia visual ni diferencias aceptables; obligaría a inventar un criterio de fidelidad.
3. “que se puede copiar en lo necesario citando origen”: no delimita qué partes de `app.css` copiar ni cómo citar; obligaría a inventar alcance y formato.
4. “miga con el nombre del store en la cabecera”: no indica de dónde obtener ese nombre; obligaría a inventar la fuente.
5. “las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra”: el TaskDoc los declara vacíos; obligaría a inventar contenido vinculado.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, rituales, `paper-tokens.css`, `DESIGN.md`, `app.css` de surface, componentes del Shell, `Shell.test.tsx` y la maqueta. Cambiaría `shell.css` para consumir `--wb-*`; estilizaría botones de pestaña/lente sin apariencia nativa; añadiría fondos/bordes al explorador y panel; títulos serif; rail y miga. Depende de U1 y de los tokens copiados. Validaría con `cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx`, comparación en Chrome y capturas citadas. No se ejecuta nada.

## FUTURO

U1 entrega la base; U2-U9 aportan contenido. Un humano decide la aceptación visual y las diferencias residuales; otro nodo/cierre registra capturas, actualiza el board y prepara el commit.
