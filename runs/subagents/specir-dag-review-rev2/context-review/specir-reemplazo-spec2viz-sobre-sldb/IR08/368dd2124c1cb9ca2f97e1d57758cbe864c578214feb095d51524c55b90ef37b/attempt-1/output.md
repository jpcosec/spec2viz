REFORMULACION
IR08 es un nodo de código ejecutable, no un agregado. Propósito: construir en specIR un extractor estático de una aplicación Django REST Framework y su esquema SQL. Resultado: documentos y relaciones de los tipos de dominio de specIR, con procedencia por archivo, línea y hash, taxonomía de IR05 e idempotencia. Repo: specIR. Límites: sin ejecutar la aplicación; fuera frontend, runtime, reglas no deducibles, impacto y parches; no importar pron, spec2viz ni módulos de SLDB fuera de sldb.api.

AMBIGUEDADES
1. “Sobre el fixture de la aplicación del blog” y output_scope solo incluye “tests/fixtures/blog_backend/manage.py”. Obliga a inventar los demás archivos del fixture (settings, urls, views, serializers, models, SQL) y el subgrafo backend/datos exacto exigido.
2. “hash del fragmento fuente”: no define algoritmo, normalización ni límites del fragmento. Obliga a inventar el esquema de hash y qué texto exacto se hashea.
3. “señala los nodos anclados a ese archivo como cambiados”: no define representación del estado cambiado, criterio de anclaje ni cómo conservar hechos validados. Obliga a inventar ese mecanismo.
4. “su esquema SQL”: no especifica dialecto ni formato de entrada. Obliga a inventar si se parsea DDL, dump o metadatos, y con qué sintaxis.
5. “Las pruebas anteriores pasan”: no identifica cuáles pruebas previas. Obliga a inventar el conjunto de pruebas de referencia.

DRY-RUN
Un ejecutor futuro leería IR05 (taxonomía, equivalencias, divergencia), IR06 (clases, relation_types.yaml, rules.yaml, blog_chain.yaml), el fixture backend y la API pública sldb.api. Crearía src/specir/extract/{__init__,provenance,django_drf,sql_schema}.py, los tests extract y completaría el fixture blog_backend. Dependencias: IR05 e IR06; el fixture requerido excede el output_scope declarado. Validaría: equivalencia con la cadena manual de IR06, procedencia completa, doble extracción con árbol idéntico, mutación de fuente marcando cambios sin borrar validados, ausencia de inferidos con procedencia observada/validada, RelationTypeDoc/RuleDoc e frontera de imports. Sin ejecutar.

FUTURO
IR05 entrega taxonomía canónica, equivalencias y regla de divergencia. IR06 entrega clases de dominio, RelationTypeDoc, RuleDoc y store manual del blog. Un humano decide la validación de inferencias y la aceptación de cambios de fuente según IR05. IR08 consume esos artefactos; no los produce.
