## REFORMULACION

**Propósito:** que specIR derive la mitad de interfaz del grafo (controles, acciones y sus vínculos con operaciones de API) sin analizar código, interpretando en specIR los facts genéricos que `sldb.api.code.code_facts` publica para TS, TSX, JS y JSX.

**Resultado:** un módulo de frontend dentro de `specir.extract` que, sobre el backend ya extraído por IR08 en el mismo store, produce `InterfaceControlDoc` e `InterfaceActionDoc`, `triggers` control→acción e `invokes` acción→`ApiOperationDoc`, con anclas por fact, procedencia observado/derivado, `sin_verificar`, idempotencia y lista `not_derived` con motivos. Fixture React mínimo del blog en `tests/fixtures/blog_frontend` y pruebas en `tests/extract/`.

**Repo:** specIR (`/mnt/ssd/proyectos/SLDB_1/IR`), consumiendo solo la API pública de sldb; sin leer bytes ni parsear fuentes.

**Límites:** fuera leer/parsear código, DOM/eventos en ejecución, OpenAPI y generación de interfaz; si falta un fact genérico, se pide a sldb y la tarea se detiene.

## AMBIGUEDADES

1. «al menos un .ts y un .js si el caso lo pide» (Scope) frente a «(a) … los tres obligatorios» (Precisiones). Obliga a inventar si `.ts`/`.js` son exigibles o condicionales.
2. «el extractor produce PublishButton … PublishAction» (Validation) frente a «la prueba compara tipos y relaciones con tests/models/blog.py, no los nombres» (a). Obliga a decidir si esos nombres son normativos.
3. «InterfaceActionDoc por handler, triggers control -> acción e invokes acción -> operación» no fija cardinalidad si varios controles comparten handler o si un handler lanza varias llamadas HTTP. Obliga a inventar la agregación.
4. «se sigue por su nombre canónico a la única función … un solo nivel» no dice qué pasa si esa función contiene varias llamadas HTTP ni cómo se reflejan. Obliga a inventar.
5. «salvo lo que el frontend comparta (helpers de anclas y escritura)» no delimita qué se puede tocar de `plan.py`/`write.py`. Obliga a inventar el alcance del cambio compartido.

## DRY-RUN

**Lecturas:** TaskDoc y pills; `docs/decisiones/procedencia-y-divergencia.md`; `src/specir/models/domain.py`; `src/specir/extract/plan.py` y `write.py`; extractor IR08; `tests/models/blog.py`; fixtures `blog_app`/`blog_frontend`; esquema de `code_facts` en sldb.

**Cambios previstos:** módulo frontend en `src/specir/extract`; fixture `.tsx`/`.ts`/`.js`; pruebas en `tests/extract/`.

**Dependencias:** IR05, IR06, IR08, espejos B2/C1–C5/C3 TS, `sldb.api`.

**Validaciones futuras:** pytest indicado; grep de prohibidos; idempotencia; `sldb edges check` y `rules check`; `deskops graph missing`.

## FUTURO

Un humano debe resolver las contradicciones 1 y 2. sldb debe exponer los facts C3 TS y atender huecos; IR08 debe poblar las `ApiOperationDoc` en el mismo store; la tarea D1 debe existir; y otro nodo valida la aceptación de motivos en `not_derived`.
