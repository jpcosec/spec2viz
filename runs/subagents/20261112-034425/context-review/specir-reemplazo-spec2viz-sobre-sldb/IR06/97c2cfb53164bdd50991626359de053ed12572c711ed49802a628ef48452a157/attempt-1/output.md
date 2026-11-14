REFORMULACION
IR06 encarga, en el repo specIR, definir los tipos de dominio transversales como clases Python subclases del documento base de SLDB, distribuir RelationTypeDoc y RuleDoc al store y dejar un store de prueba poblado por MCP con la cadena de publicar un post (React, DRF, PostgreSQL). Resultado: paquete de modelos, YAML de relaciones y reglas, instalador, fixture y pruebas. Límites: sin extractores, análisis de impacto ni síntesis; el MCP escribe datos, no clases; no redefine vocabulario visual de SLDB.

AMBIGUEDADES
1. «subclases del documento base de SLDB»: no nombra clase base, registro ni campos; obliga a inventar jerarquía y API de registro.
2. «control de interfaz, acción, operación de API, handler, operación de dominio, política, estado, entidad de dominio y tabla»: no fija nombres, campos ni identidad; obliga a inventar el esquema estable que IR08-IR10 citarán.
3. «triggers, invokes, handled_by, executes, governed_by, transitions, writes, persisted_in» y «relación entre tipos no permitidos»: no da matriz origen-destino, cardinalidad ni condición; obliga a inventar qué pares son válidos.
4. «invariantes entre capas ... por ejemplo que toda acción de interfaz invoque una operación de API existente»: «por ejemplo» deja abierto el conjunto; obliga a inventar cuántas RuleDoc, su texto y severidad.
5. «la cadena de publicar un post» y «PublishButton, PublishAction, endpoint, handler, PublishPost y tabla»: no define propiedades, nombres de endpoint/handler/tabla ni estados/política; obliga a inventar el contenido del fixture.
6. «specIR distribuye e instala en un store»: no define formato, idempotencia, conflicto ni procedencia de instalación; obliga a inventar la semántica de install.py.
7. «store de prueba reutilizable por las tareas posteriores»: no fija ubicación, limpieza ni IDs estables; obliga a inventar el contrato de reutilización.

DRY-RUN
Un ejecutor leería alcance, acceptance, output_scope y contratos de IR04 (tools MCP, dry-run, RelationTypeDoc/RuleDoc como datos) e IR05 (taxonomía de procedencia), además del documento base y registro de modelos de SLDB y las tools MCP de lectura. Crearía src/specir/models/{__init__,domain}.py, data/relation_types.yaml, data/rules.yaml, install.py, fixture blog_chain.yaml y las tres pruebas. Dependería de IR04/IR05, del registro de SLDB y de MCP lectura/escritura. Validaría: tests de modelos; recorrido MCP bidireccional PublishButton→…→tabla; rechazo de relación no permitida; retirada de operación API y reporte de RuleDoc; un solo documento Post en dos vistas; procedencia por nodo/relación; ausencia de modelos visuales redefinidos y de extractores/impacto/síntesis. No ejecutaría nada.

FUTURO
IR05 decidirá taxonomía canónica y divergencia; IR04 fijará firmas MCP; IR02/IR03 aportarán lectura; IR07/IR11 darán semántica de vistas; IR08-IR11 consumirán los tipos. Un humano aprobará nombres y esquema si se promueven como contrato estable.
