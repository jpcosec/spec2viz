REFORMULACION
IR02 es una decisión del repo specIR, hija de ROOT y dependiente de IR01. Busca que el dueño del proyecto registre el contrato de escritura del MCP: qué es una propuesta de cambio, qué precondición protege la aplicación, dónde se declara el nivel de escritura permitido y si existe deshacer. El resultado es `docs/decisiones/contrato-de-escritura-mcp.md`, con alternativas, elección, motivo, fecha y responsable, más un atom durable por decisión, citando la API pública de SLDB o su carencia. Límites: no implementa, no decide permisos multiusuario y no admite escrituras fuera de la API pública. No es un agregado: no tiene hijos.

AMBIGUEDADES
1. “cuatro decisiones tomadas por el dueño del proyecto”: no se identifica al dueño ni la fuente de la fecha. Obliga a inventar autoridad y fecha.
2. “un atom durable por cada decisión”: no se define formato, store, esquema ni ubicación; `output_scope` solo lista el documento. Obliga a inventar el mecanismo de atoms.
3. “El atom de principios de seguridad de la superficie MCP”: la validación parece exigir un atom adicional o distinto de los cuatro, sin enumerar principios. Obliga a inventar la lista y si son cuatro o cinco.
4. “las referencias de la tarea los incluyen”: no dice qué tarea ni cómo se referencia. Obliga a inventar el enlace, probablemente en IR04.
5. “la carencia notificada a SLDB”: no indica canal, formato ni responsable. Obliga a inventar la notificación.

DRY-RUN
Un ejecutor futuro leería la matriz de IR01, la API pública de SLDB, el registro existente y el esquema de atoms. Crearía el documento con cuatro secciones y cuatro atoms; listaría sus ids y dejaría las referencias para IR04. Depende de la decisión del dueño, de IR01 y del store de atoms. Validaría: secciones completas, citas a la API o carencia, provenance de atoms, coincidencia texto-decisión, cuatro ids listados, ausencia de rutas privadas y atom de seguridad actualizado.

FUTURO
El dueño elige cada alternativa y aporta autor y fecha; IR01 entrega la matriz; IR04 cita los mecanismos decididos y referencia los atoms; un humano valida el registro.
