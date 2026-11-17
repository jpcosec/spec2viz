## REFORMULACION

**Propósito:** eliminar de `specir.extract` la lectura de bytes del fuente para recalcular `source_hash`, sustituyéndola por una comprobación vía API pública de sldb. **Resultado:** `src/specir/extract/write.py` (`checked_blocks`) valida el ancla contra el `source_hash` obtenido de `sldb.api` —menciona `code_facts` o `record_anchor`—, conserva el `ValueError` con el ref y no escribe si un ancla falla; además, una prueba en `tests/extract/` falla si el extractor abre o lee archivos fuente del fixture. **Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`. **Límites:** solo `write.py` (`checked_blocks`) y la prueba nueva; “Fuera: cualquier otro cambio del extractor”. Si falta un dato en `sldb.api`, se pide por el desk de sldb y la tarea se detiene.

## AMBIGUEDADES

1. “por ejemplo, un code_facts de la ruta justo antes de escribir, comparado con el fact del plan), o se pide a sldb que record_anchor lo devuelva”. Dos alternativas sin elección; obligaría a inventar qué API usar y su contrato.
2. “una prueba en tests/extract/ que falle si el extractor abre o lee un archivo fuente del fixture (por ejemplo, vigilando open y Path.read_bytes”. No se identifica el fixture ni su ruta; obligaría a inventarlos.
3. “manteniendo el ValueError con el ref si no coinciden”. No define qué es “el ref” ni su formato; obligaría a inferirlo.
4. “grep -rnE 'read_bytes|read_text|open\(' src/specir/extract no devuelve nada”. No distingue lecturas de fuentes frente a otros usos de `open`; obligaría a decidir el alcance exacto del grep.

## DRY-RUN

**Lecturas previstas:** TaskDoc, `src/specir/extract/write.py` (función `checked_blocks`), contrato de `sldb.api` (`code_facts`/`record_anchor`), pruebas existentes en `tests/extract/` y fixture usado. **Cambios previstos:** reemplazar el cálculo con `hashlib.sha256(...read_bytes())` por consulta API; añadir prueba que vigile `open`/`Path.read_bytes`; conservar `ValueError` y la regla de no escribir. **Dependencias:** disponibilidad y semántica del dato en `sldb.api`; fixture identificable; `task-ir08-extractor-estático-django-drf-y-sql` como antecedente. **Validaciones futuras:** grep indicado, pytest indicado con rc 0, `deskops graph missing --root .` con rc 0. Nada se ejecuta en esta revisión.

## FUTURO

Decisión entre `code_facts` y `record_anchor`, y petición al desk de sldb si falta el dato: corresponde a otro nodo o a un humano. La aceptación final del cierre y del commit queda fuera de esta revisión.
