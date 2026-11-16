## REFORMULACION

Encargo ejecutable, no agregado: actualizar el acta de retiro de spec2viz en el repo IR, únicamente `docs/spec2viz/acta-de-retiro.md`. Propósito: reflejar dos hechos ya decididos/verificados fuera del acta. Resultado: (1) fila de pron como resuelta, citando el commit `4224186` y la evidencia del tester; (2) fila G5 con la decisión de JP del 2026-11-16 (opción A: archivar `spec2viz/.sldb` con el repo, sin reapuntar sus 7 modelos), citando atom y task.decision, y listando lo pendiente en IR; (3) ajustar la lista final de pasos (quitar pron de G4 y sustituir la alternativa de G5 por la decisión); (4) repetir `specir retirement check` y anotar salida resumida. Límites: no tocar matriz de cobertura, declaración de retiro, universo del store, pruebas, pron ni spec2viz.

## AMBIGUEDADES

1. “las dos notas de desk/inbox citadas en **Why**” — el documento no tiene sección `Why`, sino `Rationale`; obliga a inferir que Why = Rationale.
2. “grep -n specir ../pron/docs/spec2viz/build.py muestra las llamadas de las líneas 22 a 24” — no fija el contenido exacto esperado; si el grep devuelve líneas distintas pero equivalentes, el ejecutor debe inventar el criterio de aceptación.
3. “se anota su salida resumida (filas abiertas, número de dependencias y rc), igual que las corridas anteriores del acta” — no define formato; obliga a deducirlo del acta, y si las corridas previas difieren, a elegir uno.
4. “el atom de spec2viz atom-decisión-de-jp-2026-11-16-g5-... y la task.decision task-decisión-de-jp-g5-...” — la verificación propuesta (`ls | grep g5`) no garantiza que esos identificadores exactos existan; si no coinciden, obliga a decidir si se citan igual, se corrigen o se reporta bloqueo.

## DRY-RUN

Lecturas: las dos notas de `desk/inbox`, el acta completa y, si aplica, las pills citadas. Comprobaciones: `grep` de `specir` en `../pron/docs/spec2viz/build.py`; `git -C ../pron merge-base --is-ancestor 4224186 HEAD`; listado de atoms/tasks G5 en `../spec2viz/desk`. Cambios previstos: solo el acta, conservando tablas y formato. Dependencias: repos hermanos pron/spec2viz, `.venv`, `TMPDIR=/dev/shm`. Validaciones futuras: `git diff --stat`, merge-base rc 0, ausencia de filas pron en retirement check, pytest de matriz y gate, `deskops graph missing --root .` rc 0.

## FUTURO

IR13 debe quitar `spec2viz/.sldb` del universo al declarar el retiro; otra tarea debe dejar de federar ese store en las pruebas; un humano/JP cierra G5 tras ejecutarse lo pendiente. Si falla la verificación de pron, decide un humano.
