REFORMULACION
Propósito: que specir.extract deje de leer bytes del fuente para recalcular `source_hash` en `checked_blocks` y lo obtenga por la API pública de sldb. Resultado: `src/specir/extract/write.py` sin `read_bytes`/`read_text`/`open` sobre fuentes, con comparación vía `sldb.api` y `ValueError` con ref si el ancla no coincide, más una prueba en `tests/extract` que detecte lecturas de fuente. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: solo `write.py` (`checked_blocks`) y `tests/extract`; no otros cambios del extractor; si `sldb.api` no aporta el dato, pedir por el desk de sldb y detener la tarea.

AMBIGUEDADES
1. "por ejemplo, un code_facts de la ruta justo antes de escribir, comparado con el fact del plan", "o se pide a sldb que record_anchor lo devuelva": dos alternativas sin criterio de elección; la segunda implicaría tocar sldb. Obliga a inventar la decisión.
2. "el source_hash del fact recién leído para esa ruta debe coincidir con el del plan": no se da firma de code_facts, parámetros, ni cómo localizar el fact de la ruta o el del plan. Obliga a inventar llamadas y selección.
3. "una prueba ... que falle si el extractor abre o lee un archivo fuente del fixture (por ejemplo, vigilando open y Path.read_bytes durante la extracción)": no define fixture ni cómo distinguir fuentes de otras lecturas. Obliga a inventar el mecanismo.
4. "grep ... no devuelve nada" frente a "no contiene ... open sobre fuentes": el grep no distingue lecturas de fuentes. Obliga a inventar si vale grep vacío o filtrado.
5. "Si hace falta un dato que sldb.api no da, se pide ... y la tarea se detiene": no define cómo comprobarlo ni quién decide. Obliga a inventar el criterio de parada.

DRY-RUN
Lecturas: `write.py`/`checked_blocks`, API `sldb.api.code`, fixtures de `tests/extract`, `tests/models/test_blog_chain.py`. Cambios previstos: sustituir `hashlib.sha256` sobre `read_bytes` por consulta y comparación de `source_hash`; añadir prueba que intercepte `open`/`read_bytes`. Dependencias: task-ir08, disponibilidad de `source_hash` en la API, `.venv` y deskops. Validaciones futuras: grep indicado, pytest con `TMPDIR=/dev/shm` y `deskops graph missing --root .`, sin ejecutar.

FUTURO
Un nodo/API de sldb debe confirmar si `code_facts` o `record_anchor` exponen `source_hash`; un humano decide la parada y la petición al desk de sldb; el coordinador acepta el cierre.
