## REFORMULACION
Propósito: añadir a `specir` un comando CLI que ejecute la extracción frontend de un árbol y avise de los archivos que `code_facts` omitió; con `--strict`, debe fallar con rc 1 si hubo saltados. Resultado: grupo click `ux` con subcomando `extract ROOT [--store PATH] [--path P ...]`, propagación de `skipped` en `ExtractionReport`, resumen de nodos creados/actualizados/no derivados, aviso por stderr y test nuevo. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: solo `src/specir/cli.py`, `src/specir/extract/__init__.py` si hace falta y `tests/extract/test_ux_extract_cli.py`; fuera: dictionary/coverage (T8/T9), localizador y cambios en sldb. Validación: pytest sobre el test nuevo y `tests/extract/test_frontend_extraction.py`.

## AMBIGUEDADES
1. «siguiendo como estan declarados catalog y retirement»: no se adjunta el patrón; obligaría a inventar la estructura exacta del grupo click.
2. «extract ROOT [--store PATH] [--path P ...] que llama a specir.extract.extract_frontend»: no se define la firma ni el mapeo de `--store`/`--path`; obligaría a inventar esa traducción.
3. «escribe un resumen (nodos creados/actualizados, no derivados)»: no se fija formato ni origen de los contadores; obligaría a inventar campos o contrato.
4. «con el motivo si sldb lo da»: no se especifica si cada saltado es texto o dict; obligaría a inventar el esquema de `skipped`.
5. «los primeros 10»: no se indica orden ni formato; obligaría a inventar la presentación.
6. «Plan desk/drawer/plans/graph-ui-diccionario-de-componentes/README.md»: no se incluye el plan; si se requiere como fuente, obligaría a asumir su contenido.

## DRY-RUN
Hipotéticamente, un ejecutor leería `cli.py`, `extract/__init__.py`, los tests existentes y la firma de `code_facts`. Añadiría el grupo `ux` y el comando `extract`, llamaría a `extract_frontend`, imprimiría el resumen y los saltados en stderr (cuenta, primeros 10 y motivo si existe), y aplicaría rc 1 solo con `--strict`. Añadiría `skipped: list` con default vacío al reporte y lo poblaría desde `code_facts`. Crearía el test con `CliRunner`: árbol `.tsx` con rc 0, y saltados simulados por monkeypatch con aviso y `--strict` rc 1. Dependencias: `code_facts` de sldb y el nodo de nombres de relación. Validación futura: ejecutar el comando pytest indicado; no se ejecuta ahora.

## FUTURO
El nodo dependiente debe entregar el comportamiento de nombres de relación acotados a 255 bytes; T8/T9 producirán dictionary y coverage. Un humano decidirá si el README del plan es fuente vinculante y aceptará el formato final del resumen y del aviso.
