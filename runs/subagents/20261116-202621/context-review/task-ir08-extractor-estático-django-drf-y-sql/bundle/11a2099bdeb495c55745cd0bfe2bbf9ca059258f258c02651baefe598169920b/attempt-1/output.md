# REFORMULACION

**Propósito:** que el grafo de backend y datos de specIR se pueble desde código real en vez de a mano, fijando el formato de procedencia que usarán el resto de extractores.

**Resultado:** un módulo de mapeo (`specir.extract`) que, consumiendo solo facts y anclas que sldb extrae de una app Django REST Framework y de su esquema SQL Postgres, produce documentos y relaciones de los tipos de dominio de specIR, cada uno con evidencia de origen (archivo, línea, hash) y su procedencia; idempotente.

**Repo:** specIR; fixture = app Django DRF pequeña del blog, versionada en el repo.

**Límites:** specIR no lee ni analiza código (sin tree-sitter, ast ni parsers propios); solo Postgres; sin frontend; sin análisis en tiempo de ejecución; sin reglas de negocio no deducibles (quedan desconocidas o inferidas); sin parches al código; solo `sldb.api`; si falta un fact, se pide al desk de sldb.

# AMBIGUEDADES

1. "los readers de la tarea espejo B2": su TaskDoc no está en el bundle → inventar qué facts y anclas concretos expone.
2. "traducida a la taxonomía de la tarea de procedencia" / "taxonomía canónica": no se aporta → inventar ejes y valores de origen/verificación.
3. "los nodos de backend y datos de la cadena de publicar un post que la tarea de tipos de dominio pobló a mano": no hay inventario → inventar el conjunto esperado y sus relaciones.
4. "los RuleDoc vigentes": no se listan → inventar qué reglas validan las relaciones.
5. "el hash del fragmento": algoritmo y normalización no definidos → inventar forma de cálculo.
6. "señala los nodos anclados a ese archivo como cambiados, sin borrar hechos validados": no se define el mecanismo ni el criterio de detección → inventar la divergencia según origen.

# DRY-RUN

**Lecturas:** `sldb.api` para facts/anclas del fixture (rutas, vistas, serializers, modelos, SQL Postgres) y para el store de prueba real.
**Cambios previstos:** `src/specir/extract/` (mapeo facts→tipos de dominio), tests y fixture del blog; sin parsers.
**Dependencias:** task-ir05 (procedencia), task-ir06 (tipos y cadena manual), task-espejo B2 (readers SQL/TS/TSX).
**Validaciones futuras:** equivalencia con la cadena manual; anclas completas; doble ejecución → árbol idéntico; mutación de archivo → nodos marcados; no inferido como observado; RelationTypeDoc/RuleDoc; `tests/test_imports.py` sin `pron`, `spec2viz` ni módulos internos de sldb.

# FUTURO

- B2 entrega readers y facts; sin ellos el ejecutor se detiene y reporta el bloqueo.
- ir05 fija la taxonomía de procedencia; ir06, los tipos y la cadena manual de referencia.
- Un humano/JP decide dialecto (ya indicado: Postgres) y resuelve carencias vía desk de sldb.
