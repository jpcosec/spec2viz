REFORMULACION
Nodo ejecutable de código en specIR. Propósito: extraer la interfaz de la cadena de publicación desde facts genéricos de SLDB. Resultado: módulo en `src/specir/extract` que, sobre `sldb.api.code.code_facts` de TS/TSX/JS/JSX, crea `InterfaceControlDoc` e `InterfaceActionDoc`, triggers control→acción e invokes acción→`ApiOperationDoc` de IR08, con anclas archivo/línea/source_hash, procedencia observado/derivado, verificación `sin_verificar`, `not_derived` e idempotencia. Repo: specIR; superficies: `src/specir/extract`, `tests/extract`, `tests/fixtures/blog_frontend`. Límites: no leer/parsear fuentes, ni DOM, ni OpenAPI; solo API pública de `sldb.api`; reutilizar helpers sin cambiar firmas; si falta un fact, detenerse y pedirlo al desk de sldb.

AMBIGUEDADES
1. Extensiones del fixture. Scope: “con al menos un .ts y un .js si el caso lo pide”; precisión (a): “un .ts ... y un .js ..., los tres obligatorios”. Obliga a inventar si la ausencia de .ts o .js invalida la prueba.
2. Facts de funciones. “se sigue por su nombre canónico a la única función de los facts del frontend con ese nombre, un solo nivel”; el input solo describe `attrs.calls` y `attrs.handlers`, no el fact de definición de función. Obliga a inventar su forma y el emparejamiento.
3. Nombres de nodos. Validación: “produce PublishButton ... PublishAction”; precisión (a): “la prueba compara tipos y relaciones ... no los nombres”. Obliga a inventar si esos nombres son requisito o ejemplo.
4. Versión mínima de SLDB. “sldb mínimo en origin main: C3 TS en 0590ed11” frente a “Dependencias: ... espejos B2, C1–C5 y C3 TS”. Obliga a decidir si basta C3 TS o se exigen todos.

DRY-RUN
Lecturas: TaskDoc, IR05, `domain.py`, `plan.py`/`write.py`, `tests/models/blog.py`, fixtures `blog_app`/`blog_frontend`, `tests/extract` y `test_imports`. Cambios: módulo frontend en `src/specir/extract`; interpretación de handlers y llamadas; resolución contra `ApiOperationDoc`; anclas/procedencia/`not_derived` con helpers; fixture TSX/TS/JS y pruebas. Dependencias: grafo backend de IR08 en el mismo store, IR05/IR06, espejos SLDB C1–C5/C3 TS y D1. Validaciones: pytest indicado, `sldb edges/rules check`, doble ejecución idempotente, grep sin nuevas coincidencias y `deskops graph missing`. Sin ejecutar nada.

FUTURO
IR08 produce el grafo backend y sus `ApiOperationDoc`; IR05/IR06 producen decisión y tipos/pruebas; los espejos SLDB y D1 producen facts y source_hash por API. Si falta un fact, un humano o el desk de sldb decide/entrega. El cierre, commit y reconciliación de pills los decide el humano; la fase integrada valida el conjunto.
