## REFORMULACION

Propósito: producir el plan que demuestre que specIR puede cubrir todas las capacidades de spec2viz antes de retirarlo. Resultado: una matriz por capacidad con modo y condición verificable de retiro; la decisión sobre el YAML de spec frente al grafo; y un gate comprobable. Repo: el de specIR, con salidas en `docs/spec2viz/matriz-de-cobertura.md`, `docs/spec2viz/gate-de-retiro.md` y `docs/decisiones/fuente-de-verdad-del-diagrama.md`. Límites: no migra ni implementa ninguna fila, no analiza impacto ni extracutores de otras tecnologías, y no declara nada como ya migrado. Es una tarea documental, no un agregado ejecutable.

## AMBIGUEDADES

1. «spec2viz/spec2viz/cli.py y los módulos del paquete; spec2viz/tests/ como definición de paridad»: no fija rama, commit ni versión de spec2viz; obligaría a inventar qué revisión se inventaría.
2. «el plan absorber-spec2viz-y-modelos-ui de SLDB»: no da ruta ni identificador; obligaría a inventar su ubicación y contenido.
3. «cita la tarea de sldb que la migra (SpecSync, generador de spec desde grafo y AST, modelos de spec o emparejamiento de átomos)»: no enumera identificadores de tareas de SLDB; obligaría a inventarlos.
4. «qué pasa con los specs YAML existentes en los repos que usan spec2viz»: no delimita qué repos cuentan; obligaría a inventar el universo de búsqueda.
5. «Existe un atom con la decisión sobre el YAML de spec frente al grafo»: no indica archivo, formato ni relación con los átomos ya listados; obligaría a inventar su ubicación y esquema.

## DRY-RUN

Un ejecutor futuro leería el CLI, módulos y pruebas de spec2viz; el plan de SLDB; la API pública de SLDB; los consumidores citados; y los índices de stores. Después redactaría la matriz completa, la decisión y el gate; no tocaría código ni migraría piezas. Dependencias: revisión concreta de spec2viz, plan de SLDB e identificadores de tareas de migración. Validaría que todos los comandos y módulos aparezcan, que cada modo cite su respaldo, que los consumidores citen archivo, que exista el átomo de decisión y que el gate sea una lista comprobable. Sin ejecutar nada.

## FUTURO

IR13 añadirá a la matriz la prueba que acredita cada cobertura tras cerrar IR13a–IR13d. De la matriz se derivarán tareas de migración; otras tareas de SLDB migrarán piezas; los consumidores dejarán de invocar spec2viz y los stores de registrar sus modelos. La aprobación de la decisión sobre el YAML y del gate, y el retiro efectivo, corresponden a revisión humana y a nodos posteriores.
