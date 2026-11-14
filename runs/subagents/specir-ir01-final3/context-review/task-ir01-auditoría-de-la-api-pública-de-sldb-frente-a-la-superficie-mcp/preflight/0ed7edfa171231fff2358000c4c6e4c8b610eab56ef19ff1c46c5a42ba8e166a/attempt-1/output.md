REFORMULACION
Propósito: auditar la API pública de SLDB frente a las necesidades de la futura superficie MCP de specIR. Resultado: un informe en `docs/auditoria/sldb-api-frente-a-mcp.md` con una matriz de exactamente once capacidades, cada una con necesidad, estado, evidencia, brecha, acción y referencia handoff. Repo: trabajar desde `/home/jp/proyectos/SLDB_1/IR`, inspeccionando `../sldb` y leyendo solo `../pron/source/spec/14-superficie-mcp.md` como contrato externo. Límites: no diseñar tools, escribir código, editar otros repos ni decidir el contrato final de escritura; no leer módulos internos de SLDB ni importar/ejecutar pron. Si hay filas no disponibles, enviar una única nota a `sldb` y registrar su ID o el fallo.

AMBIGUEDADES
1. “Si no basta para decidir equivalencia, anotar la ambigüedad y preguntar al desk SLDB.” No aclara si esa fila debe clasificarse como `faltante` o `requiere-extensión-en-SLDB`, ni si entra en la nota; obligaría a inventar la regla de clasificación.
2. “contrastar conducta con create_model, add_model, validate_model_draft y promote_model_draft” no indica si son símbolos públicos literales o nombres conceptuales; obligaría a inventar su correspondencia con la API real.
3. “La referencia handoff es el carácter EM DASH literal — en disponible y sldb:<note-id> en no disponible, referidas a una sola nota.” No fija si cada fila no disponible repite el mismo ID ni cómo representarlo si la nota falla; obligaría a inventar el formato exacto.
4. “El informe tiene sección Resumen con el ID o ausencia de nota.” No especifica el texto exacto para declarar ausencia; obligaría a inventar una fórmula.

DRY-RUN
Un ejecutor futuro capturaría commit, rama, estado y hashes de `../sldb`; listaría recursivamente `src/sldb/api/*.py`, los documentos indicados y la spec de pron; leería sin importar ni ejecutar. Construiría la matriz de once filas, citando símbolos y rutas reales, y escribiría únicamente el informe, creando `docs/auditoria` si falta. Si alguna fila resulta no disponible, redactaría y enviaría una sola nota con el título y contenido exigidos, registraría comando/resultado/fecha y el ID. Validaría número de filas, estados/acciones cerrados, evidencia, snapshot, ausencia de lecturas internas y coherencia de la nota.

FUTURO
El propietario de SLDB responde aclaraciones y decide extensiones o el contrato de undo; otro nodo puede ejecutar la auditoría y enviar la nota. Un humano valida el cierre y la aceptación del informe.
