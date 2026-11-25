## REFORMULACION
Propósito: añadir a `specir` una vía CLI que ejecute la extracción frontend existente y haga visible lo que hoy se pierde en silencio: los archivos que `code_facts` salta por gramática ausente (206 TS/JS en la medición citada). Resultado: grupo click `ux` con comando `extract ROOT [--store PATH] [--path P ...]`, que llama a `extract_frontend`, imprime un resumen, propaga `skipped` al `ExtractionReport` y avisa por stderr; con `--strict`, rc 1 si hay saltados. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`, tocando `src/specir/cli.py`, posiblemente `src/specir/extract/__init__.py` y un test nuevo. Límites: fuera dictionary/coverage (T8/T9), localizador y cambios en sldb.

## AMBIGUEDADES
1. «con el motivo si sldb lo da»: no se especifica la forma de cada elemento de `skipped` (cadena, dict, campos). Obligaría a inventar cómo extraer e imprimir el motivo y qué hacer si falta.
2. «escribe un resumen (nodos creados/actualizados, no derivados)»: no dice destino (stdout/stderr), formato ni qué significa exactamente «no derivados». Obligaría a inventar el contrato de salida.
3. «[--store PATH]»: no define semántica, valor por defecto ni relación con la extracción. Obligaría a inventar el comportamiento del flag.
4. «los primeros 10»: no fija orden ni si son 10 archivos o 10 líneas. Obligaría a inventar el criterio de truncado.
5. «siguiendo como estan declarados catalog y retirement»: exige inferir convenciones no incluidas en el input. Obligaría a inventar la estructura del grupo click si no se inspecciona el repo.

## DRY-RUN
Un ejecutor futuro leería `src/specir/cli.py`, `src/specir/extract/__init__.py`, `src/specir/extract/extract_frontend` (o módulo equivalente), `tests/extract/test_frontend_extraction.py` y la firma de `code_facts` en sldb. Cambios previstos: declarar grupo `ux` y comando `extract`; añadir `skipped: list` con default vacío al `ExtractionReport`; poblar desde `code_facts`; imprimir resumen y aviso stderr; implementar `--strict`; crear `tests/extract/test_ux_extract_cli.py` con los dos casos indicados. Dependencias: tarea de nombres de relación (255 bytes), API de sldb que ya devuelve `skipped`, entorno `.venv`. Validación futura: el comando pytest indicado, sin ejecutarlo ahora.

## FUTURO
T8/T9 consumirán dictionary/coverage; el propietario de sldb decidirá si `skipped` incorpora motivos estructurados; un humano decidirá formato exacto del resumen y política de `--strict` si el dry-run revela conflicto.
