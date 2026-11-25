## REFORMULACION

Corregir el acta de retiro de spec2viz en `/mnt/ssd/proyectos/SLDB_1/IR` para reflejar la decisión de JP del 2026-11-24: spec2viz no quedó archivado, sino que continúa como IR en `jpcosec/specir`; `main` es IR y `legacy` conserva la historia de spec2viz. Resultado: tres ediciones en `docs/spec2viz/acta-de-retiro.md`: sustituir el punto 9 por su versión hecha con salvedad, actualizar la frase de cabecera y actualizar la línea de estado al 2026-11-24. Límites: solo documentación, sin código ni borrado de historia; `gate-de-retiro.md` no se toca.

## AMBIGUEDADES

1. Alcance contradictorio. Cita: «Solo docs/spec2viz/acta-de-retiro.md (y gate-de-retiro.md si nombra el archivo)» frente a «Solo docs/spec2viz/acta-de-retiro.md (gate-de-retiro.md no se toca)». Obliga a inventar si `gate-de-retiro.md` debe modificarse cuando nombre el archivo.
2. Texto de partida incompleto. Cita: «hoy empieza con '9. **Pendiente, último paso (coordinador, en GitHub).** Archivar spec2viz'». Solo da el inicio del punto 9, no la línea completa; obliga a decidir si basta localizarlo por prefijo o si hay que reconstruir el resto.
3. Condición de alcance no verificable sin lectura. Cita: «y gate-de-retiro.md si nombra el archivo». Obliga a inventar qué significa exactamente “nombra el archivo” y qué edición correspondería.

## DRY-RUN

Lecturas previstas: `docs/spec2viz/acta-de-retiro.md`; opcionalmente `gate-de-retiro.md` solo para comprobar si nombra el archivo, sin modificarlo. Cambios previstos: tres reemplazos literales en el acta —punto 9, frase de cabecera y línea de estado— conservando el resto del contenido. Dependencias: ninguna declarada. Validaciones futuras: `grep -n "jpcosec/specir" docs/spec2viz/acta-de-retiro.md` y comprobar ausencia de «Lo único que queda es archivar» mediante `! grep`. No se ejecuta nada.

## FUTURO

Un ejecutor aplicará las tres ediciones y las validaciones. Un validador o humano confirmará que el acta refleja la decisión de JP, que no se alteró la historia y que `gate-de-retiro.md` quedó fuera de alcance salvo decisión expresa.
