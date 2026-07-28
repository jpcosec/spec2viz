# UC-01: Validate a diagram spec

El usuario escribió un archivo YAML describiendo un diagrama de secuencia y quiere verificar que es semánticamente válido antes de renderizarlo.

## Pasos

1. Ejecutar `spec2viz validate <file>` sobre un YAML de sequence válido
2. Ejecutar `spec2viz validate` sobre un YAML con errores (participante faltante, mensaje a destino inexistente)
3. Ejecutar `spec2viz validate` sobre múltiples archivos

## Preguntas de estrés

- ¿El mensaje de éxito es claro? (¿"OK"? ¿Silencio?)
- ¿El mensaje de error es accionable? (¿línea, columna, sugerencia?)
- ¿Validate corre validación sintáctica (YAML parse) y semántica (referencias)?
- ¿Los exit codes discriminan error sintáctico vs semántico?
- ¿Validate acepta directorios o solo archivos individuales?
- ¿Qué pasa con archivos que no son diagram specs válidos?
