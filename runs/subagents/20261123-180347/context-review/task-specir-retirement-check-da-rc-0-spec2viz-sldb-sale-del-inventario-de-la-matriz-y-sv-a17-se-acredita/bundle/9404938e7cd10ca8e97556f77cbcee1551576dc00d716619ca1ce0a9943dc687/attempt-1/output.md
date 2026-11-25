## REFORMULACION
**Propósito:** retirar `spec2viz/.sldb` del universo del comprobador y acreditar SV-A17 con G5 opción A, para que `specir retirement check` dé rc 0.
**Resultado:** inventario sin ese store; fila SV-A17 actualizada en `docs/spec2viz/matriz-de-cobertura.md`; acta con el punto 2; comprobador en rc 0 y tests pasando.
**Repo:** el bundle vive en IR; se nombran superficies `deskops`, `UIs/graph_ui`, `pron` y `sldb`. No se declara rama ni commit.
**Límites:** fuera los cambios del momento del retiro y declarar el retiro/archivar spec2viz.

## AMBIGUEDADES
1. «Ubicar como se arma el universo del comprobador (config o argumentos)»: no se identifica archivo, formato ni clave; obligaría a inventar dónde declarar el inventario.
2. «con los --path de deskops, UIs/graph_ui, pron, sldb y el resto del universo»: «el resto» no está enumerado; obligaría a inventar rutas.
3. «acredita SV-A17 citando G5 opcion A (16-nov)»: no consta el texto exacto ni la ubicación de G5; obligaría a inventar la cita y su formato.
4. «el acta registra el punto 2 hecho con fecha y commit»: el commit aún no existe; obligaría a inventar hash o fecha.
5. «TMPDIR=/dev/shm pytest -q de los tests del comprobador»: no se da ruta ni selección; obligaría a inventar el target de pytest.
6. «Hoy quedan solo las 19 dependencias de ese store»: no se listan; obligaría a inventar la línea base esperada.

## DRY-RUN
**Lecturas:** TaskDoc, rituales, configuración/argumentos del comprobador, matriz, acta y tests del comprobador.
**Cambios previstos:** quitar `spec2viz/.sldb` del inventario; actualizar SV-A17 con la cita de G5; anotar el punto 2 en el acta; ajustar tests si fijan el inventario.
**Dependencias:** localizar la fuente única del universo, obtener la línea base y confirmar la redacción de G5.
**Validaciones futuras:** ejecutar `specir retirement check` con el universo declarado y comprobar rc 0; ejecutar `TMPDIR=/dev/shm pytest -q` sobre los tests del comprobador. Nada ejecutado.

## FUTURO
El closeout produce el commit y la fecha definitiva; la tarea de cambios del momento del retiro actúa después; el coordinador asume el punto 3 (declarar retiro y archivar spec2viz). La confirmación humana de la cita G5 corresponde a JP/owner.
