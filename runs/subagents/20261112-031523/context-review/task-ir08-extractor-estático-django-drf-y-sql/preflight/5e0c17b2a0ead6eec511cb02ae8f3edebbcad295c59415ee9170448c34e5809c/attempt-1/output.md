REFORMULACION
Propósito: construir en specIR un extractor estático de una aplicación Django REST Framework y su esquema SQL para poblar el grafo de tipos de dominio desde código existente. Resultado: módulo extractor que produce documentos y relaciones de los tipos de dominio de specIR, con procedencia por nodo y relación (archivo, línea, hash y taxonomía), cubriendo rutas/vistas, serializers, modelos, tablas/columnas/claves y relaciones; idempotente. Repo: specIR, según las rutas `src/specir/extract/...`, `tests/extract/...` y el fixture `tests/fixtures/blog_backend/manage.py`. Límites: lectura estática por AST/metadatos, sin ejecutar la aplicación; fuera frontend, runtime, reglas no deducibles —quedan desconocidas o inferidas—, análisis de impacto y parches; escritura solo por API pública de SLDB (`sldb.api`), sin `pron` ni `spec2viz`. Fixture: app Django REST Framework real y pequeña del blog.

AMBIGUEDADES
1. “en la taxonomía decidida en la tarea de procedencia”: no se da la taxonomía; obliga a inventar valores y criterios de clasificación.
2. “las mismas operaciones validadas que la superficie MCP de escritura”: no se enumeran; obliga a inventar qué operaciones y firmas usar.
3. “si la tarea de procedencia lo decide así”: decisión condicional ausente; obliga a inventar si se usan anclas de código.
4. “los tipos de dominio de specIR” y “mismos tipos y relaciones”: no se listan; obliga a inventar nombres y esquema esperados.
5. “señala los nodos anclados a ese archivo como cambiados”: no define cómo; obliga a inventar estado o metadatos de cambio.
6. “hash del fragmento fuente”: no fija algoritmo, normalización ni límites del fragmento; obliga a inventar esos criterios.

DRY-RUN
Nodo ejecutable `task.code`, no agregado. Lecturas: TaskDoc, pills, dependencias ir05/ir06 y archivos listados. Cambios previstos: crear/ajustar `extract/__init__.py`, `provenance.py`, `django_drf.py`, `sql_schema.py`; añadir tests y fixture. Dependencias: taxonomía/procedencia y tipos de ir05/ir06; operaciones de la API SLDB. Validaciones futuras: comparación con la cadena poblada a mano, procedencia completa, doble extracción idempotente, detección de archivo modificado, ausencia de inferidos como observados/validados, RelationTypeDoc/RuleDoc e imports permitidos. Sin ejecutar.

FUTURO
Otro nodo o humano debe resolver ir05/ir06: taxonomía, tipos, reglas vigentes y decisión sobre anclas; también aportar operaciones MCP/API y criterios de “cambiado” y hash. La aceptación final corresponde a validación humana.
