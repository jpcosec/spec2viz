REFORMULACION

IR02 es un nodo de decisión no ejecutable y sin hijos: no produce código, sino un registro en `docs/decisiones/contrato-de-escritura-mcp.md` con cuatro decisiones del dueño sobre el contrato de escritura del MCP —propuesta de cambio, precondición de aplicación, nivel de escritura permitido y deshacer— y cuatro atoms durables que las dejan disponibles. El resultado esperado es ese documento más los atoms con `provenance` al registro. Repo: `specIR`. Límites: no implementar y no decidir permisos multiusuario; el único `output_scope` es el documento. Depende de IR01 y alimenta a IR04.

AMBIGUEDADES

1. «un atom durable por cada decisión»: no se define formato, ubicación, esquema ni identificador del atom; obligaría a inventar dónde y cómo se persiste.
2. «El atom de principios de seguridad de la superficie MCP»: se cita un atom que no forma parte de los cuatro ni tiene ubicación definida; obligaría a inventar si es un quinto atom y cuál es.
3. «según la matriz de auditoría, o la carencia notificada a SLDB»: no se indica cómo se referencia una carencia notificada; obligaría a inventar su identificador o ruta.
4. «tomadas por el dueño del proyecto» y «quién decidió»: no se nombra al dueño ni el formato de autoría; obligaría a inventar una identidad o rol.
5. «o por actor»: no se define qué es un actor ni cómo se identifica; obligaría a inventar un modelo de actores.
6. «las referencias de la tarea los incluyen»: no se explicita qué tarea ni qué campo de referencia; obligaría a inventar el destino y el mecanismo de cita.

DRY-RUN

Un ejecutor futuro leería la matriz de IR01, la API pública de SLDB, el formato existente de atoms y los requisitos de IR04. Redactaría el documento con cuatro secciones —alternativas, elegida, motivo, fecha y quién decide—, citaría la operación pública o la carencia, crearía cuatro atoms con `provenance` y comprobaría que ningún camino de escritura evita la API pública. Validaría además que el atom de seguridad ya cita mecanismos decididos. Sin ejecutar nada.

FUTURO

El dueño del proyecto toma las cuatro decisiones; IR01 entrega la matriz y las carencias; IR04 consume los atoms para implementar las tools; SLDB recibe las notas de faltantes; un humano valida el registro y su coherencia con IR04.
