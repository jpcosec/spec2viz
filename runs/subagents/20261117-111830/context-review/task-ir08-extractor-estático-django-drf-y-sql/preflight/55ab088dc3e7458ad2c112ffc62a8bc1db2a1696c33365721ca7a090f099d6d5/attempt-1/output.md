REFORMULACION

El nodo debe implementar en el repo specIR (`/mnt/ssd/proyectos/SLDB_1/IR`) el extractor estático de backend y datos para `tests/fixtures/blog_app`. Propósito: poblar el grafo de dominio desde código existente usando solo la API pública de sldb. Resultado: módulo `specir.extract` que, sobre `code_facts`, interpreta convenciones Django/DRF y hechos constraint SQL y escribe documentos y relaciones con anclas, procedencia observada/derivada, `source_hash` e idempotencia. Límites: no leer ni parsear fuentes (tree-sitter, ast, regex, pglast), no otros dialectos, no frontend, runtime ni impacto; no tocar el fixture salvo copia temporal; si falta un fact, detenerse y pedirlo al desk de sldb.

AMBIGUEDADES

1. “check_anchors (o check_doc_anchors)”: obliga a elegir una API concreta; inventar criterio de selección.
2. “lo informa como cambiado” y “el informe de la extracción lista…”: no define formato, canal ni esquema del informe; obliga a inventarlos.
3. “la regla usa solo la llamada y lo dice en la descripción”: no fija texto ni ubicación exacta; obliga a inventar redacción.
4. “salvo lo que pida la Validation 5”: las validaciones son viñetas sin numerar; obliga a inventar la correspondencia.
5. “con su evidencia de origen” frente a “El campo evidencia queda vacío”: obliga a decidir si “evidencia” es campo o ancla.

DRY-RUN

Lecturas: task doc, `domain.py`, `relation_types.yaml`, decisión de procedencia, fixture, `pyproject.toml`, pruebas y API de sldb. Cambios previstos: crear `src/specir/extract`, pruebas nuevas, actualizar extra `structuredLanguageDB[mcp,code,postgres]` y `.venv`. Dependencias: commits de sldb, extras instalados, IR05/IR06 y espejos B2/C1–C5. Validaciones futuras: nodos de la cadena, constraints SQL, anclas y procedencia, doble ejecución idempotente, copia temporal, RelationTypeDoc/RuleDoc, grep y pytest, `deskops graph missing`. Nada se ejecuta aquí.

FUTURO

Otro nodo o humano debe: entregar facts faltantes desde sldb; fijar tipos y taxonomía desde IR05/IR06; resolver espejos B2/C1–C5; adjudicar anclas cambiadas, informes y validaciones; confirmar el dialecto SQL y la actualización del entorno.
