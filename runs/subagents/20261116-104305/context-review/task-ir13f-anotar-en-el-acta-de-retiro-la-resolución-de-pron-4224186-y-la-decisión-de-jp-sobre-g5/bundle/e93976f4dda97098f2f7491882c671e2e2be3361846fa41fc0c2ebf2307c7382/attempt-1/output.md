REFORMULACION
Propósito: actualizar `docs/spec2viz/acta-de-retiro.md` (repo IR) para reflejar que pron resolvió su pedido con el commit 4224186 y que JP decidió G5 por la opción A. Resultado: fila de pron «resuelto» con commit y evidencia del tester; fila G5 «decidido; pendiente de ejecución en IR» con atom, task.decision y pendientes de IR; lista final sin pron en G4 y con la decisión en G5; nueva salida resumida de `specir retirement check`. Límites: solo ese archivo; no matriz, retiro, universo del store, pruebas, pron ni spec2viz.

AMBIGUEDADES
1. «Leer primero las dos notas de desk/inbox citadas en Why y el acta completa.» Las notas no están en el bundle; si se exigiera cita literal de la evidencia, habría que inventarla o depender del resumen del Rationale.
2. «se corre de nuevo specir retirement check y se anota su salida resumida (filas abiertas, número de dependencias y rc), igual que las corridas anteriores del acta.» No aclara si sustituye o añade la corrida anterior ni si «filas abiertas» es lista o recuento; obligaría a inventar el formato/posición.
3. «Para verificar el atom y la task.decision de spec2viz: ls ../spec2viz/desk/atoms/ | grep g5 y ls ../spec2viz/desk/tasks/ | grep g5.» No define qué hacer si no aparecen; obligaría a inventar si bloquear, anotar ausencia o citar solo lo hallado.

DRY-RUN
Sin ejecutar: leer acta, notas referenciadas, `../pron/docs/spec2viz/build.py` y listar atom/task de spec2viz. Comprobar `git -C ../pron merge-base --is-ancestor 4224186 HEAD`; si falla, no marcar pron y reportar. Editar solo el acta en cuatro puntos. Luego correr `specir retirement check` con el comando indicado y anotar rc, dependencias y filas abiertas. Validaciones previstas: diff stat, ancestor pron, ausencia de filas pron, pytest de matriz/gate, greps de pron/G5 y `deskops graph missing --root .`.

FUTURO
IR13 deberá quitar `spec2viz/.sldb` del universo al declarar el retiro; otra tarea dejará de federar ese store en pruebas; el desk de spec2viz es dueño del atom/task.decision. Si la verificación de pron o de los identificadores falla, decide un humano/desk; este nodo no lo resuelve.
