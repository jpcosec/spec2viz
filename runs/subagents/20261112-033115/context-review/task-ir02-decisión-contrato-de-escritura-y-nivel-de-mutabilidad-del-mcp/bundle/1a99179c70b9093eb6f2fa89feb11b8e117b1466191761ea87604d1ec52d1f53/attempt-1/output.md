REFORMULACION
Propósito: decidir el contrato de escritura y el nivel de mutabilidad de la superficie MCP de specIR para que la escritura por MCP pueda diseñarse. Resultado: un registro en docs/decisiones/contrato-de-escritura-mcp.md con cuatro decisiones —propuesta, precondición, nivel de escritura y deshacer—, cuatro atoms con provenance al registro, el atom de seguridad actualizado y los ids anotados en registro y referencias. Repo: specIR; los cambios en SLDB, deskops u otros repos se piden por su desk. Límites: no implementar ni decidir permisos multiusuario. No es un agregado ejecutable: es una tarea de decisión con compuerta humana; no tiene hijos.

AMBIGUEDADES
1. "el recibo owner que exige la activación de una tarea de decisión acredita que la decisión es suya": no define el recibo, quién lo emite ni cómo se obtiene; obligaría a inventar identidad y forma de acreditación.
2. "o la carencia notificada a SLDB": no aclara si basta el mensaje enviado o hace falta respuesta o evidencia; obligaría a inventar el criterio de aceptación.
3. "dónde se declara el nivel de escritura permitido (contenido, reglas y tipos de relación, modelos)": el paréntesis no dice si son ámbitos, opciones o capas; obligaría a inventar la taxonomía.
4. "la operación de la API pública de SLDB que sostiene la alternativa elegida": asume una operación única por alternativa; si combina varias o no existe, obligaría a inventar la correspondencia.
5. "se anotan en el registro y en las referencias de la tarea": no fija formato ni si agrega o reemplaza; obligaría a inventar el esquema.

DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout/phase, pill, ambos atoms, matriz de ir01 y el registro si ya existe. Cambios previstos: redactar las cuatro secciones con alternativas y recomendación; recoger la elección del dueño; crear cuatro atoms con deskops add atom --provenance; editar el atom de seguridad; anotar ids. Dependencias: matriz de auditoría, elección del dueño, CLI deskops y API pública de SLDB. Validaciones futuras: las seis de la sección del TaskDoc, sin ejecutar.

FUTURO
El dueño elige y acredita; ir01 entrega la matriz; el desk de SLDB responde carencias; la tarea de escritura por MCP consumirá los mecanismos; deskops y SLDB cambian por su desk.
