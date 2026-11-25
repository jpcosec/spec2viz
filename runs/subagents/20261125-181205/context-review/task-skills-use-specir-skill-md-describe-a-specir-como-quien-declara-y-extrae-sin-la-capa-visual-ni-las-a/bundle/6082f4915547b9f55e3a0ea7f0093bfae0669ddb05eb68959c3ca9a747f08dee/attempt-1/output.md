## REFORMULACION
Propósito: corregir `skills/use-specir/SKILL.md` para que describa specIR como capa que declara y extrae, sin presentarlo como capa visual ni documentar anotaciones retiradas del catálogo. Resultado: skill actualizada, comandos citados verificados y distinción explícita entre lo decidido y lo ya ejecutado. Repo: `SLDB_1/IR`. Límites: solo documentación de esa skill y sus referencias; fuera el código y `deskops-workflow`.

## AMBIGUEDADES
1. «Dentro: skills/use-specir/SKILL.md y sus referencias». No se enumeran esas referencias; habría que inventar qué archivos entran.
2. «Comprobar cada comando que la skill nombre corriendo su --help». El input no incluye la skill ni su inventario de comandos; habría que inventar comandos o asumir un entorno ejecutable.
3. «lo decidido y sin ejecutar está marcado como tal con la fecha». No se precisa qué afirmaciones son decisión y cuáles implementación; habría que inventar su estado.
4. «Que la skill diga qué hace specIR hoy y a dónde se va para ver o editar un diagrama». No se da el texto destino ni la ruta sustituta; habría que inventar la descripción.
5. El cold-bundle dice incluir «las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra», pero solo aporta TaskDoc y rituales; faltan `SKILL.md` y `docs/decisiones/paridad-por-capacidades.md`. Verificarlos obligaría a inventar su contenido.

## DRY-RUN
Lecturas previstas: `SKILL.md`, decisión de paridad, referencias alcanzadas, rituales execution/testing/closeout y Board. Cambios previstos: reescribir introducción; retirar sección de anotaciones del catálogo; indicar dónde ver/editar diagramas; marcar decisiones no ejecutadas con fecha. Dependencias: contenido real de la skill, decisión vigente y comandos disponibles. Validaciones futuras: `grep -nE 'the visual layer|same catalog page'` sin coincidencias; `--help` de cada comando citado; revisión de alcance y de la marca decisión/fecha. No se ejecuta nada.

## FUTURO
El nodo de ejecución editará la skill; un humano confirmará estado y fecha de lo decidido; otro nodo aportará el contenido íntegro de skill, decisión y referencias, ejecutará grep y `--help`, y closeout actualizará Board y commit.
