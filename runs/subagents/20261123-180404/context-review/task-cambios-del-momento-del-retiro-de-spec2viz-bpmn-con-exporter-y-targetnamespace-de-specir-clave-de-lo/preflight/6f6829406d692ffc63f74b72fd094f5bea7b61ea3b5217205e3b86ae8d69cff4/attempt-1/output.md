## REFORMULACION

Propósito: ejecutar en IR los cambios del momento del retiro de spec2viz ordenados por JP (acta, punto 8, decisión 3): adaptar el emisor BPMN de specir y la clave de localStorage del catálogo, con migración, y actualizar goldens y tests. Resultado: BPMN con `exporter='specir'` y targetNamespace propio; página de catálogo con clave nueva y migración desde `spec2viz.catalog.annotations.v1` al cargar, sin pérdida ni reescritura de la vieja; goldens regenerados y revisados; acta con el punto 8 hecho. Repo: IR. El nodo es un `task.code` draft, no un agregado. Límites: fuera declarar el retiro y archivar spec2viz (punto 3, coordinador tras `attach_atom_edges`) y sacar `spec2viz/.sldb` del inventario y SV-A17 (punto 1, abierto).

## AMBIGUEDADES

1. «un targetNamespace de specir»: no da la URI; obliga a inventar el valor.
2. «una clave de localStorage de specir»: no da el nombre exacto; obliga a inventar clave y versionado.
3. «sin perderlas y sin volver a escribir la clave vieja»: no fija qué hacer si coexisten ambas claves, el JSON es inválido o falla la escritura; obliga a inventar la política.
4. «el comando del repo»: no lo nombra; obliga a descubrirlo o inventarlo.
5. «Marcar el punto 8 como hecho en el acta» frente a «Fuera: declarar el retiro en el acta»: no aclara si editar el acta está permitido; obliga a decidir el alcance.
6. «lleva exporter='specir'»: no indica el elemento ni la ubicación exacta del atributo; obliga a inventarlos.
7. «depends_on: ... task-specir-retirement-check...»: no declara si la dependencia está cumplida; obliga a asumir el desbloqueo.
8. «test (de JS o de la pagina generada)»: no fija framework ni ruta; obliga a elegir.

## DRY-RUN

Leería el TaskDoc, el acta (punto 8) y haría grep de `exporter=`, `targetNamespace` y la clave vieja. Cambiaría el emisor BPMN y su test; añadiría clave nueva, migración y test; regeneraría goldens con el comando del repo; anotaría el punto 8 con fecha y commit. Dependencias: la tarea `depends_on` y el comando de regeneración. Validaría con `TMPDIR=/dev/shm pytest -q`, el test de migración, grep de la clave vieja solo en la migración y revisión del diff. Sin ejecutar nada.

## FUTURO

El coordinador declara el retiro y archiva spec2viz tras `attach_atom_edges`; se resuelve el punto 1 (inventario/SV-A17); un humano revisa goldens y acta; la tarea dependiente acredita su condición.
