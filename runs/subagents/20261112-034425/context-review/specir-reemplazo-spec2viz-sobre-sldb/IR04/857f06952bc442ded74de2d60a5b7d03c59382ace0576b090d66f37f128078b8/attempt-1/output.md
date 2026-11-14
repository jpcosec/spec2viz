REFORMULACION
IR04 es un nodo de código (delivery) del repo specIR, no un agregado. Propósito: construir las tools MCP de escritura para que un agente proponga, valide y aplique cambios al store, con el mecanismo que fije IR02. Resultado: src/specir/mcp/write_tools.py, changes.py y mutability.py, más tres suites de pruebas; el ciclo proponer-validar-aplicar funciona sobre un documento y una arista. Límites: solo documentos de modelos ya registrados, aristas, RelationTypeDoc y RuleDoc; excluye crear o editar clases Python de modelos por MCP y síntesis de código de aplicación.

AMBIGUEDADES
1. "Una tool por encima del nivel de escritura permitido": no se define la jerarquía ni los niveles; obligaría a inventar su orden y semántica.
2. "según la severidad de la regla": faltan los valores de severidad y qué severidad rechaza o solo reporta; obligaría a inventar esa taxonomía.
3. "lleva en su procedencia quién": no se dice de dónde sale la identidad del actor; obligaría a inventar el modelo de identidad.
4. "la condición de su RelationTypeDoc": "condición" no está definida; obligaría a inventar su lenguaje y evaluación.
5. "contra un store de prueba": no se especifica si es la copia aislada de IR03 o un fixture nuevo; obligaría a inventar su origen.

DRY-RUN
Un ejecutor futuro leería el registro y atoms de IR02, el servidor y tools de IR03, la API pública de SLDB para mutación y procedencia, y tests/conftest. Cambios previstos: los tres módulos MCP y las tres suites. Dependencias: IR02 debe fijar propuesta, precondición, nivel y deshacer; IR03 debe aportar servidor, direcciones y paginación; SLDB debe soportar escritura y procedencia. Validaciones futuras: pruebas contra store de prueba, comparación de archivos antes/después en seco, rechazo por cambio posterior a la validación, aristas inválidas, reglas por severidad, argumentos tipados, procedencia, nivel excedido y ausencia de tools de módulos Python.

FUTURO
IR02 produce las cuatro decisiones y sus atoms; sin ellas no hay mecanismo que implementar. IR03 entrega servidor de lectura, direcciones, paginación y arnés de pruebas. IR06 consume estas tools para poblar la cadena del blog. El dueño del proyecto decide nivel de escritura, precondición y deshacer; SLDB debe notificar carencias de su API pública.
