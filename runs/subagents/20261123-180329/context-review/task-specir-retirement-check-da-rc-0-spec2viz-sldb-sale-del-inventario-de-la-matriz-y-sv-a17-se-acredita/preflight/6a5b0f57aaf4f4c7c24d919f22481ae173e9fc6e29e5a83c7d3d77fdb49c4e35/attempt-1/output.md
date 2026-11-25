## REFORMULACION

**Propósito:** ejecutar el encargo `task.code` para que `specir retirement check` termine con rc 0 sacando `spec2viz/.sldb` del inventario/universo del comprobador y acreditando `SV-A17` con la decisión G5 opción A.

**Resultado:** comprobador en rc 0; `docs/spec2viz/matriz-de-cobertura.md` con `SV-A17` acreditada citando G5 opción A (16-nov); acta con el punto 2 hecho, fecha y commit.

**Repo:** no se declara raíz única; el TaskDoc vive en `SLDB_1/IR` y el alcance nombra `deskops`, `UIs/graph_ui`, `pron`, `sldb` y `spec2viz`.

**Límites:** dentro, inventario/universo del comprobador, matriz, acta y tests. Fuera, cambios del momento del retiro y declarar/archivar `spec2viz` (punto 3). No es agregado ni paquete: es una tarea ejecutable.

## AMBIGUEDADES

1. “la declaracion del inventario o universo del comprobador en IR (donde specir retirement check toma sus --path)”: no fija archivo, formato ni clave; obliga a inventar dónde y cómo se declara.
2. “el resto del universo”: no enumera los `--path` restantes; obliga a inventar la lista.
3. “acredita SV-A17 citando G5 opcion A (16-nov)”: no da texto ni formato exacto de cita; obliga a inventar la redacción.
4. “el acta registra el punto 2 hecho con fecha y commit”: no identifica el acta ni qué commit; obliga a inventar ruta y criterio.
5. “su salida queda en el informe”: no define informe, ruta ni formato; obliga a inventar destino.
6. “los tests del comprobador”: no nombra suite ni comando; obliga a inventar selección.

## DRY-RUN

Hipotéticamente: leer TaskDoc, configuración/argumentos del comprobador, matriz, acta y tests; ejecutar línea base y registrar 19 dependencias y `SV-A17`. Cambiar inventario quitando `spec2viz/.sldb`; editar `SV-A17`; actualizar acta. Depende de la decisión JP, G5 del 16-nov y del comprobador instalado. Validaciones futuras: `specir retirement check` con rc 0 y `TMPDIR=/dev/shm pytest -q` de tests. No se ejecuta nada.

## FUTURO

El coordinador ejecuta el punto 3: declarar el retiro y archivar `spec2viz`. La tarea de cambios del momento del retiro va después. Un humano valida el acta, el commit y el cierre.
