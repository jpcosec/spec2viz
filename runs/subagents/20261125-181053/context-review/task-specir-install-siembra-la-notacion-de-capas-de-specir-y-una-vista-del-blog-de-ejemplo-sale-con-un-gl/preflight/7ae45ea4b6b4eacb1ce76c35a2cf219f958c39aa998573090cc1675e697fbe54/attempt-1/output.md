## REFORMULACION
**Propósito:** sembrar en el store la notación de capas de specIR al ejecutar `specir install`, para que graph_ui pueda dibujar los tipos de dominio extraídos. Nodo ejecutable `task.code`; no es agregado.

**Resultado:** datos de notación instalables y `src/specir/install.py` modificado; una vista del blog de ejemplo resuelve cada documento de dominio con glifo y cada relación con link.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`.

**Límites:** dentro, datos de notación de specIR e `install.py`; fuera, carriles por capa, ORCA e IFML.

## AMBIGUEDADES
1. «La notación es dato sembrado, igual que relation_types.yaml y rules.yaml.» No indica ruta destino, esquema ni idempotencia de la siembra. Obligaría a inventar ubicación, formato y comportamiento ante datos existentes.
2. «el blog de ejemplo extraído» no identifica fixture, comando de extracción ni ViewDoc concreta. Obligaría a inventar el origen del ejemplo y la definición de la vista.
3. «cada documento de dominio con su glifo y cada relación con su link, sin huecos.» No define correspondencia tipo→glifo, dirección/tipo de link ni criterio de «sin huecos». Obligaría a inventar expectativas y aserciones.

## DRY-RUN
**Lecturas:** TaskDoc, `docs/decisiones/paridad-por-capacidades.md`, `desk/drawer/plans/paridad-por-capacidades/specir-layers.yml`, `src/specir/install.py`, ejemplos `relation_types.yaml`/`rules.yaml`, tests citados.

**Cambios previstos:** convertir el borrador en dato de notación versionado; hacer que `install` lo siembre; añadir o ajustar `tests/test_install.py` y `tests/test_layers_notation.py`; preparar el caso del blog y la vista para la comprobación final.

**Dependencias:** borrador válido con 11 glifos y 11 links; resolución de vistas existente; fixture del blog disponible.

**Validaciones futuras:** `python -m pytest -q tests/test_install.py tests/test_layers_notation.py`; store nuevo con `specir install`; extracción del blog; `sldb notations validate`; resolución de la vista sin huecos.

## FUTURO
Un ejecutor posterior implementará y ejecutará los cambios. Un humano deberá confirmar el fixture/vista del blog y la aceptación. La tarea de graph_ui aportará los carriles por capa; ORCA e IFML quedan fuera.
