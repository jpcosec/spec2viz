REFORMULACION
Propósito: sembrar en el store, al instalar specIR, la notación de capas que permita a una ViewDoc visualizar el grafo extraído del código. Resultado: en un store nuevo, tras `specir install` y extraer el blog de ejemplo, `sldb notations validate` acepta la notación y resolver una vista devuelve cada documento de dominio con su glifo y cada relación con su link, sin huecos. Repo: SLDB_1/IR; superficie `src/specir/install.py` y datos de notación. Límites: dentro, datos de notación de specIR e install; fuera, carriles por capa (tarea graph_ui), ORCA e IFML. Nodo ejecutable, no agregado.

AMBIGUEDADES
1. “La notación es dato sembrado, igual que relation_types.yaml y rules.yaml.” No define ubicación, esquema, formato ni política de copia/merge/idempotencia; obligaría a inventar cómo se siembra y cómo se resuelven conflictos.
2. “resolver una vista con ella devuelve cada documento de dominio con su glifo y cada relación con su link, sin huecos.” No identifica comando/API de resolución ni qué significa “sin huecos”; obligaría a inventar la prueba de aceptación y el formato de salida.
3. “el blog de ejemplo extraído” no indica comando, fuente ni fixture; obligaría a inventar la preparación del store de prueba.
4. “11 glifos, 11 links” no aclara si son 11 tipos de nodo y 11 de relación o 11 elementos totales; obligaría a inventar el mapeo.

DRY-RUN
Lecturas: TaskDoc y rituales; pills/átomos/archivos declarados (vacíos); borrador `desk/drawer/plans/paridad-por-capacidades/specir-layers.yml`; precedentes `relation_types.yaml` y `rules.yaml`; `src/specir/install.py`; tests `test_install.py`, `test_layers_notation.py`; fixture del blog. Cambios previstos: incorporar los glifos y links como dato sembrado; conectar install para sembrarlo de forma idempotente; añadir/ajustar pruebas. Dependencias: borrador validado, mecanismo de seed y CLI `sldb notations`. Validaciones futuras: ejecutar los dos pytest; `sldb notations validate`; crear store nuevo, instalar, extraer blog, resolver vista y comprobar glifo por nodo de dominio y link por relación sin huecos. Nada ejecutado.

FUTURO
Un nodo de ejecución implementará y probará el cambio y hará su commit; testing ampliará cobertura si toca comportamiento compartido; closeout actualizará el board y enlazará conocimiento durable; la fase integrará esta tarea. La tarea graph_ui consumirá la notación para carriles por capa; ORCA e IFML quedan para tareas posteriores.
