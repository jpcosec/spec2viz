## REFORMULACION
**Propósito:** ejecutar el punto 8 del acta de retiro de spec2viz dentro de IR. **Resultado:** el BPMN emitido por specir usa `exporter='specir'` y un `targetNamespace` propio; el catálogo usa una clave nueva de `localStorage` y migra las anotaciones de `spec2viz.catalog.annotations.v1`; los goldens afectados se regeneran y revisan; los tests pasan. **Repo:** IR, incluyendo emisor BPMN, página del catálogo, tests y goldens. **Límites:** no declarar el retiro ni archivar spec2viz, ni tocar inventario/SV-A17; depende de `task-specir-retirement-check...`; este nodo no ejecuta nada.

## AMBIGUEDADES
1. «un targetNamespace de specir»: no fija el URI exacto; obliga a inventar el valor normativo.
2. «una clave de localStorage de specir»: no nombra la clave nueva; obliga a inventar su identificador.
3. «migra al cargar las anotaciones guardadas [...] sin perderlas y sin volver a escribir la clave vieja»: no aclara si debe borrar la clave antigua, conservarla o migrar solo una vez; obliga a inventar la semántica.
4. «se regeneran con el comando del repo»: no indica el comando; obliga a inventarlo o buscarlo fuera del input.
5. «pytest -q de los tests de BPMN, catalogo y goldens tocados»: no fija rutas ni selectores; obliga a inventar el alcance exacto.

## DRY-RUN
Un ejecutor futuro leería el TaskDoc, el acta y los ficheros localizados por grep; modificaría el emisor BPMN y su test, la JS del catálogo y su test, y regeneraría goldens. Depende de la tarea previa de comprobación del retiro. Validaría con `TMPDIR=/dev/shm pytest -q`, grep de la clave antigua limitado a la migración y revisión del diff de goldens. No se ejecuta ahora.

## FUTURO
La dependencia debe aportar su resultado antes de cerrar. Un humano revisa los valores exactos y el diff de goldens, y autoriza el commit. El coordinador ejecutará después el punto 3 —declarar el retiro y archivar spec2viz— tras `attach_atom_edges`; el punto 1 sigue abierto.
