## REFORMULACION
Propósito: demostrar que specIR conecta interfaz, API, operación y datos mediante un grafo tipado sin duplicar objetos, usando la cadena de publicar un post. Resultado: clases Python de dominio; RelationTypeDoc y RuleDoc builtin; store de prueba poblado por MCP y recorrible; pruebas. Repo: `src/specir` (models, data, install.py) y `tests/models` con fixture. Límites: sin extractores, impacto ni síntesis; las clases son código de specIR, relaciones/reglas son datos del store; MCP solo escribe datos. El nodo es ejecutable, no agregado.

## AMBIGUEDADES
1. “un store de prueba poblado por MCP”: no se indica ubicación, identificador, configuración ni credenciales; obliga a inventar destino y conexión.
2. “subclases del documento base de SLDB”: no se nombra clase base, import ni contrato; obliga a inventar la API de herencia/registro.
3. “instalados por un comando de specIR”: no se define nombre, opciones ni idempotencia; obliga a inventar CLI e instalación.
4. “como hace deskops”: patrón externo no incluido; obliga a inventar el mecanismo de registro de modelos.
5. “con las tools de escritura”: no se listan tools, orden ni payloads; obliga a inventar la secuencia MCP.
6. “la procedencia de la taxonomía canónica decidida”: no se identifica taxonomía ni formato; obliga a inventar valores y representación.

## DRY-RUN
Lecturas: archivos listados y pills; API pública de SLDB y patrón deskops si están en el repo. Cambios previstos: modelos y registro; YAML de relation types/rules; comando de instalación; fixture `blog_chain`; tests de dominio y cadena. Dependencias: IR04 (escritura validada por MCP), IR05 (procedencia/divergencia), API SLDB y tools MCP. Validaciones futuras: pytest; recorrido bidireccional por MCP; rechazo de relación no permitida; regla incumplida al quitar endpoint; un único `Post` entre vistas; procedencia; no redefinir vocabulario visual. Sin ejecutar.

## FUTURO
IR04 entrega escritura validada por MCP; IR05 decide procedencia/divergencia; un humano confirma taxonomía canónica y acceso al store. Tareas posteriores reutilizan el store y el grafo para extractores/análisis.
