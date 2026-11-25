## REFORMULACION
Propósito: actualizar el acta de retiro de spec2viz para reflejar la decisión de JP del 2026-11-24: spec2viz no queda archivado, continúa como IR en `jpcosec/specir` (`main` = IR; `legacy` = historia de spec2viz) y el punto 9 queda hecho.

Resultado: tres ediciones en `docs/spec2viz/acta-de-retiro.md`: (1) reemplazar el ítem 9 por el texto indicado; (2) sustituir la frase de cabecera sobre archivar el repo; (3) cambiar la línea de estado al 2026-11-24.

Repo: `/mnt/ssd/proyectos/SLDB_1/IR`.

Límites: solo ese archivo; `gate-de-retiro.md` no se toca; nada de código; se conserva la historia reemplazando el estado.

## AMBIGUEDADES
1. Cita: «se reemplaza el item entero (sus dos lineas)» y «hoy empieza con "9. **Pendiente, último paso (coordinador, en GitHub).** Archivar spec2viz"». Obligaría a inventar el texto exacto de la segunda línea y el límite del ítem si el ajuste de línea o el contenido real no coinciden literalmente.

## DRY-RUN
Lecturas: abrir `docs/spec2viz/acta-de-retiro.md` y localizar el ítem 9 por su prefijo, la frase de cabecera y la línea de estado.

Cambios previstos: reemplazar el ítem 9 completo por el texto nuevo; sustituir la frase de cabecera por «El punto 9 quedó hecho el 2026-11-24: spec2viz continúa como IR en jpcosec/specir, con su historia en la rama legacy.»; cambiar la línea de estado por «Estado al 2026-11-24: el retiro está declarado y los nueve puntos están hechos.»

Dependencias: que el archivo exista y contenga las cadenas citadas; acceso al repo indicado.

Validaciones futuras: ejecutar los dos `grep` indicados y comprobar que el punto 9 menciona `jpcosec/specir`, `legacy` y la fecha 2026-11-24.

## FUTURO
Un nodo ejecutor aplicará las tres ediciones y correrá las validaciones. Un humano —JP o revisor— confirma la decisión y acepta el acta. Si el archivo real no coincide literalmente con lo citado, un humano decide cómo reconciliarlo. No hay nodos hijos ni artefactos de código.
