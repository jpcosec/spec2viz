## REFORMULACION
Encargo ejecutable, no agregado. Propósito: que specIR derive la interfaz React del blog sin leer código, interpretando los facts genéricos de `sldb.api.code.code_facts`. Resultado: un módulo en `specir.extract` que produzca `InterfaceControlDoc`, `InterfaceActionDoc`, `triggers` e `invokes` hacia las `ApiOperationDoc` de IR08, con anclas por fact, procedencia observada/derivada, `not_derived` motivado e idempotencia. Repo: `/mnt/ssd/proyectos/SLDB_1/IR` (`specir`). Límites: no parsear fuentes, no observar DOM, no usar OpenAPI, no generar interfaz; solo API pública de sldb; si falta un fact genérico, detenerse y pedirlo al desk de sldb.

## AMBIGUEDADES
1. “al menos un .ts y un .js si el caso lo pide”: no define qué caso lo pide; obliga a inventar el criterio de extensiones del fixture.
2. “o un cliente de API”: no concreta forma, nombre ni patrón de llamada; obliga a inventar cómo reconocerlo en los facts.
3. “los helpers de anclas, procedencia y escritura (write_anchor, apply_batch, el informe creados, sin cambios, cambiados y no derivados de IR08)”: no fija rutas, firmas ni disponibilidad; obliga a inventar su interfaz.
4. “una URL que no casa con ninguna ApiOperationDoc”: no explicita normalización de rutas ni comparación con parámetros; obliga a inventar esas reglas.
5. “van a not_derived con su motivo”: no define estructura ni valores admitidos; obliga a inventar el esquema.

## DRY-RUN
Un ejecutor futuro leería la TaskDoc, IR05, `src/specir/models/domain.py`, el extractor/pruebas de IR08, las pills, los fixtures `blog_app` y `blog_frontend`, y la superficie pública de sldb. Previsto: añadir el módulo de frontend en `src/specir/extract`, reutilizar helpers, mapear handlers y llamadas, crear nodos/relaciones/anclas, registrar `not_derived`, añadir fixture y pruebas. Dependencias: IR05, IR06, espejos B2/C1–C5, C3 TS, IR08 y sldb en `origin main`. Validaciones futuras: pytest indicado, `grep` prohibido, `sldb edges/rules check`, idempotencia y `deskops graph missing`. Sin ejecución.

## FUTURO
Otros nodos deben aportar los facts C3, los espejos y el grafo backend de IR08; la tarea D1 ajusta helpers. Un humano decide ante un fact ausente, un bloqueo o la aceptación final.
