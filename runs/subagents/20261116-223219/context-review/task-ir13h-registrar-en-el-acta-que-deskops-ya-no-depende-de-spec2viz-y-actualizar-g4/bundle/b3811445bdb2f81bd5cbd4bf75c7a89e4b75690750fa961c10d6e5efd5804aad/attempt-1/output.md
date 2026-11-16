REFORMULACION

Propósito: actualizar el acta de retiro y la línea G4 de la matriz para registrar que deskops ya no depende de spec2viz, con evidencia de commits en `origin/main` y una corrida nueva del comprobador. Resultado: fila de deskops resuelta, G4 y «Lo que falta» sin deskops pendiente, bloque fechado con la corrida y matriz con G4 actualizado. Repo: specIR; solo `docs/spec2viz/acta-de-retiro.md` y `docs/spec2viz/matriz-de-cobertura.md`. Límites: no tocar código, pruebas ni otros repos; no editar deskops; no declarar el retiro; no cambiar otras filas ni el resumen de la matriz. No es agregado ni paquete.

AMBIGUEDADES

1. «su columna Dependencias sigue el precedente de pron y graph_ui»: no fija el texto exacto ni cuánta historia conservar; obligaría a inventar la redacción final de esa celda.
2. «La fila G4 del gate y el punto de Consumidores de Lo que falta dejan de nombrar a deskops como pendiente»: no aclara si además hay que reemplazar los recuentos de G4 por los de la corrida nueva o solo retirar nombres; obligaría a inventar el alcance de la edición.
3. «deskops graph missing --root .»: no indica desde qué directorio ni repo se ejecuta ni qué salida exacta se espera; obligaría a inventar el contexto de validación.

DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout, pills, acta completa (fila deskops, G4, «Lo que falta», bloque IR13g) y línea G4 de la matriz. Comprobaciones previas: `merge-base --is-ancestor` de 2421ca29, 74ffdb63 y b716bf85 contra `origin/main` de deskops; `grep` en `store_index.yaml`. Cambios previstos: marcar deskops resuelto citando los tres pares de commits; ajustar G4 y «Lo que falta»; añadir bloque fechado con la corrida de cinco rutas; actualizar solo G4 en la matriz. Dependencias: deskops con esos commits en origin, venv de specIR, `TMPDIR=/dev/shm` y matriz con 9 filas abiertas. Validaciones futuras: `git diff --stat`, corrida de `specir retirement check`, coincidencia de filas no acreditadas con la matriz, pytest de matriz/retirement gate y `deskops graph missing`. Sin ejecutar nada.

FUTURO

El nodo ejecutor hará las ediciones y la corrida, y el closeout actualizará el board y preparará el commit. JP decide el archivo de spec2viz cuando el gate llegue a cero.
