REFORMULACION
Propósito: entregar specIR como paquete periférico que expone por MCP lectura/escritura y análisis sobre la API pública de SLDB y absorbe gradualmente la capa visual de spec2viz. Resultado: los 17 nodos cerrados con evidencia, matriz y gate de retiro demostrados por IR13, y G_SLDB_PRON_MCP satisfecho; solo entonces se propone retirar spec2viz. Repo: specIR. Límites: sin pron en ejecución, sin módulos internos de SLDB, absorción gradual y retiro solo con matriz completa y gate.

AMBIGUEDADES
1. "los consumidores migrados" frente a "Nuevo paquete periférico sobre la API pública de SLDB": no dice quién migra ni si el cierre espera otros repos o solo solicitudes; obliga a inventar el alcance cross-repo.
2. "sus contratos necesarios se incorporan como MCPs en SLDB": no enumera cuáles; el gate los llama "requeridas por specIR", circular; obliga a inventar el perímetro de G_SLDB_PRON_MCP.
3. "reemplazo funcional" y "absorbe de forma gradual": no fija si basta equivalencia declarada por fila o se exige paridad semántica; obliga a inventar el criterio de cierre.

DRY-RUN
Agregado no ejecutable. Recorrido hipotético: IR01 matriz → IR02 decisión → IR03 lectura → IR04 escritura → IR05 procedencia → IR06 tipos/blog → IR07 cobertura → IR08 backend → IR09 frontend → IR10 reglas → IR11 compiladores → IR12 renderers → IR13a sync → IR13b catálogos → IR13c notaciones → IR13d CLI → IR13 gate. Transferencias: IR01→IR02/03; IR02+03→IR04; IR04+05→IR06; IR03+06→IR07; IR05+06→IR08/09; IR06+08+09→IR10; IR06+07→IR11; IR11→IR12; IR07+11→IR13a; IR13a+12→IR13b; IR07→IR13c; IR13a-c+12→IR13d; IR13a-d+07→IR13. Validación conjunta: IR13 comprueba matriz completa, pruebas citadas y cero dependencias de spec2viz; ROOT añade 17 cierres y G_SLDB_PRON_MCP.

FUTURO
G_SLDB_PRON_MCP lo resuelve DeskOps de sldb. El dueño del proyecto decide IR02, IR05 e IR07. Los desks de graph_ui, deskops y stores ejecutan migraciones. El dueño de spec2viz decide archivar o borrar tras el gate; el desk de SLDB atiende faltantes de API.
