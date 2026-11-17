REFORMULACION
El nodo debe implementar en specIR un extractor estático de backend y datos que interprete los facts genéricos de `sldb.api.code.code_facts` para una app Django REST Framework y su SQL Postgres, sin leer código. Resultado: documentos y relaciones de los tipos de dominio de specIR —operaciones, handlers, entidades, estados y tablas— con anclas de archivo, línea y `source_hash`, procedencia observada o derivada, verificación `sin_verificar` e idempotencia. Repo: specIR (`/mnt/ssd/proyectos/SLDB_1/IR`), usando solo la API pública de sldb. Límites: fuera tree-sitter, ast, pglast, regex sobre fuentes, otros dialectos SQL, frontend, runtime, reglas no deducibles, análisis de impacto y cambios permanentes en el fixture; si falta un fact, detenerse y pedirlo al desk de sldb.

AMBIGUEDADES
1. “el informe de la extracción lista los nodos y relaciones cuyas anclas da como changed” y “el informe que devuelve la extracción la lista como no derivada”: no se fija formato, canal ni esquema del informe; obligaría a inventar API/CLI y estructura de salida.
2. “Las relaciones extraídas pasan la validación de sus RelationTypeDoc y de los RuleDoc vigentes”: no se nombra validador, contrato de error ni si bloquea `apply_batch`; obligaría a inventar integración y semántica de fallo.
3. “las pruebas nuevas del extractor”: no se dan nombres, rutas ni granularidad; obligaría a inventar organización de tests.
4. “los mismos tipos y relaciones” respecto de “tests/models/test_blog_chain.py”: no se enumera el conjunto exacto ni si cubre solo publicar o todo el fixture; obligaría a inventar el golden esperado.
5. “si el ancla escrita no coincide con él el extractor falla”: no se especifica excepción, mensaje ni estado parcial; obligaría a inventar el contrato de error.

DRY-RUN
No ejecuto nada. Un ejecutor futuro leería TaskDoc, rituales phase/execution/testing/closeout, pills, átomos, `domain.py`, `relation_types.yaml`, decisión de procedencia, fixture `blog_app`, `test_blog_chain.py`, `pyproject.toml` y API de sldb. Cambios previstos: módulo `specir.extract`, pruebas nuevas y extra postgres en pyproject/.venv. Dependencias: commits de sldb, fixture `ad51a0f`, facts C1–C5 y hechos constraint. Validaría extracción contra golden, SQL/PK/FK, anclas y procedencia, doble ejecución idéntica, cambiados en copia temporal sin sobrescribir verificados, ausencia de inferido/declarado, RelationType/Rule, grep prohibido, pytest y `deskops graph missing`. No es agregado: es `task.code` ejecutable.

FUTURO
IR05/IR06 y los espejos B2/C1–C5 entregan tipos, procedencia y facts; un humano adjudica verificados/refutados, decide paradas por facts faltantes y autoriza cierre/commit; el ritual de fase integra las validaciones tras las tareas.
