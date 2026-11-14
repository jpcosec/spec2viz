## REFORMULACION
**Propósito:** decidir el contrato de escritura de la superficie MCP de SpecIR: qué es una propuesta, qué precondición protege la aplicación, dónde se declara el nivel de escritura y si existe deshacer.  
**Resultado:** cuatro decisiones registradas como atoms, citando alternativas descartadas, motivo y operación de la API pública de SLDB que las sostiene —o carencia notificada—. El nodo es una tarea de decisión ejecutable, no un agregado.  
**Repo:** `SLDB_1/IR`; trabajo en `desk/tasks/` y entrega declarada en `docs/decisiones/contrato-de-escritura-mcp.md`.  
**Límites:** dentro, las cuatro decisiones y la actualización/complemento del atom de seguridad MCP; fuera, implementar y decidir permisos multiusuario. Ninguna decisión puede abrir escritura al store fuera de la API pública de SLDB.

## AMBIGUEDADES
1. «Cada decisión se registra como atom con deskops add atom»: no se dan sintaxis, esquema ni identificadores; obligaría a inventar comandos y formato de atoms.
2. «parte de la matriz de la tarea de auditoría de la API de SLDB»: la matriz no está en el input; obligaría a inventar el mapeo decisión→operación API.
3. «El atom de reglas de seguridad de la superficie MCP queda actualizado o complementado»: no se incluye su contenido ni se aclara si se edita o se crea otro; obligaría a inventar el cambio.
4. «nivel de escritura permitido (contenido, reglas y tipos de relación, modelos)»: «modelos» no se define; obligaría a interpretar si son modelos de datos, documentos o esquemas.
5. «la carencia notificada a SLDB»: no se especifica canal ni formato de notificación; obligaría a inventar el mecanismo.
6. `files: docs/decisiones/contrato-de-escritura-mcp.md`, frente a un Goal que solo exige atoms: no queda claro si ese documento debe crearse; obligaría a decidir el entregable documental.

## DRY-RUN
**Lecturas previstas:** taskdoc, tarea dependiente `task-ir01...`, matriz de auditoría, pill de guardrail, atoms existentes y documento destino si existe.  
**Cambios previstos, sin ejecutar:** crear cuatro atoms vía `deskops add atom`; actualizar/complementar el atom de seguridad; crear o actualizar `docs/decisiones/contrato-de-escritura-mcp.md` si se confirma su exigencia.  
**Dependencias:** matriz de IR01, disponibilidad de `deskops`, convención de atoms y contenido previo del atom de seguridad.  
**Validaciones futuras:** cuatro atoms con alternativa descartada y motivo; cada decisión ligada a operación API o carencia notificada; ausencia de escritura fuera de la API pública; atom de seguridad actualizado/complementado.

## FUTURO
IR01 debe aportar la matriz de auditoría. Un humano o nodo revisor debe confirmar el entregable documental y aprobar las decisiones. SLDB debe recibir y resolver las carencias de API notificadas. Un nodo posterior diseñará la escritura MCP citando estos atoms.
