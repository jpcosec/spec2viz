## REFORMULACION

El encargo es implementar en el repositorio specIR, paquete `specir.extract`, un mapeo de dominio que consuma exclusivamente la API pública de sldb: facts y anclas del reader de frontend (TS, TSX y JS, React incluido) y operaciones de escritura. Debe producir nodos de interfaz —componentes, controles, acciones, estados— y relaciones `triggers` e `invokes` hacia operaciones de API ya presentes en el grafo, con evidencia de archivo, línea y hash. Debe resolver llamadas HTTP contra contratos de API disponibles y registrar brechas sin inventar operaciones. Límites: no analizar TS/TSX/JSX/JS, no observar DOM ni comportamiento dinámico, no generar UI, no usar mocks ni datos fabricados, no reimplementar readers ausentes. Resultado: extractor idempotente validado sobre el frontend React del blog de ejemplo, sin analizador propio.

## AMBIGUEDADES

1. «los contratos de API disponibles (por ejemplo OpenAPI)»: no se indica ubicación, formato ni fuente autorizada; obligaría a inventar dónde leerlos.
2. «operaciones de API que ya están en el grafo (pobladas a mano o por el mapeo de backend)»: no queda claro si el extractor solo enlaza o también crea operaciones ausentes; obligaría a inventar la política.
3. «marcada como inferida o un hueco declarado»: la elección entre ambas no está reglada; obligaría a inventar el criterio.
4. «archivo, línea y hash»: no se especifica algoritmo ni canonicalización del fragmento; obligaría a inventar la evidencia.
5. «mitad de interfaz de la cadena de publicar un post»: no define el grafo esperado exacto; obligaría a inventar nodos y relaciones adicionales.
6. «el frontend React del blog de ejemplo»: no se da ruta, versión ni composición; obligaría a inventar el fixture.

## DRY-RUN

Un ejecutor leería el TaskDoc, sus dependencias IR05, IR06 y B2, las pills, la API pública de sldb, el fixture y los contratos de API. Crearía el módulo de mapeo, constructores de nodos/relaciones, evidencia, resolución de llamadas y registro de brechas, más pruebas. Dependería de los facts/anclas del reader de frontend, las operaciones del grafo, los tipos de dominio y `RelationTypeDoc`. Validaría después: PublishButton/PublishAction enlazados, mismo código para `.ts/.tsx/.js`, evidencia completa, inferidos/huecos declarados, brechas registradas, doble ejecución idéntica y validación de RelationTypeDoc. No se ejecuta nada.

## FUTURO

B2/sldb produce los facts y anclas; el desk de sldb atiende readers o facts faltantes; un humano decide fuente de contratos, política de inferencia, fixture y criterio exacto de aceptación.
