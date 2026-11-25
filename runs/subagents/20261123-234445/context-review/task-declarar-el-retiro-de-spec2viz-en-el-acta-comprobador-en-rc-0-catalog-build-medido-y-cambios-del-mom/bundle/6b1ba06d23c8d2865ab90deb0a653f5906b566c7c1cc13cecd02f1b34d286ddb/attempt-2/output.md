## REFORMULACION

**Propósito:** declarar formalmente el retiro de spec2viz en el acta, una vez cumplidas las condiciones decididas por JP el 2026-11-23.

**Resultado:** `docs/spec2viz/acta-de-retiro.md` actualizada: cabecera de “no declarado” a “declarado” con fecha 2026-11-23; medición de `specir catalog build` incorporada; salida del comprobador con rc 0; pendientes marcados como hechos con su commit; punto 9 (archivar repo en GitHub) registrado como último paso del coordinador; punto 6 sobre oráculos de paridad resuelto o motivado. Solo si hace falta, `matriz-de-cobertura.md`.

**Repo:** no se nombra explícitamente; las rutas del input apuntan al workspace SLDB.

**Límites:** solo documentación; fuera código y el archivado del repo en GitHub.

## AMBIGUEDADES

1. “Correr specir retirement check con el universo declarado”: no se define qué universo ni su configuración; obligaría a inventar el alcance exacto del comprobador.
2. “la seccion de medicion de catalog build trae la medicion nueva”: no se indica formato ni ubicación; solo la rationale aporta “55,8 s con rc 0 y 1,7 GB”. Obligaría a inventar la presentación.
3. “los items de 'Lo que falta para declarar el retiro' quedan marcados hechos con su commit”: no se mapea cada ítem a `c377aff6`, `e6e369d` o `109684f`; obligaría a inventar la correspondencia.
4. “el punto 9 ... queda como el ultimo paso, que hace el coordinador en GitHub”: no se aclara si debe cambiar su estado ni cómo representarlo; obligaría a inventar la redacción.
5. “los oraculos de paridad (punto 6) se retiran al declarar, o el motivo si no”: no se especifica qué oráculos ni qué motivo; obligaría a inventar la decisión.
6. “si hace falta, matriz-de-cobertura.md”: no se define el criterio de necesidad; obligaría a inventar cuándo editarla.

## DRY-RUN

Un ejecutor futuro leería el acta, la matriz si existe, los commits citados y la salida real del comprobador. Cambiaría cabecera, sección de medición, bloque de salida rc 0, lista de pendientes y punto 6; revisaría el punto 9 sin archivar nada. Depende de acceso al repo, al comando `specir` y a los hashes. Validaría con `specir retirement check` rc 0 y `grep -n 'no declarado'`, admitiéndolo solo en historia fechada. No se ejecuta aquí.

## FUTURO

El coordinador archiva `spec2viz` en GitHub; otro nodo o un humano confirma los commits, suministra la salida exacta del comprobador y valida el acta antes del cierre.
