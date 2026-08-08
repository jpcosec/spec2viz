---
name: deskops-task-lifecycle
description: Guía estricta para la preparación de contexto cero (Task + Pills + Atoms), despacho obligatorio de subagentes independientes (Executor y Tester), ejecución aislada y cierre atómico en deskops. Usar siempre que se trabaje en tareas de desk/tasks/ o desk/drawer/tasks/.
---

# Deskops Task Lifecycle & Subagent Delegation

Este skill define el procedimiento obligatorio para gestionar el ciclo de vida de una tarea en `deskops`. Enforza la **autonomía de contexto cero** de los subagentes y la **delegación estricta por subagentes**.

---

## 🚨 MANDATOS CRÍTICOS E INNEGOCIABLES

### 1. Autonomía Absoluta y Contexto Cero (Zero-Context Subagent Bundle)
* La implementación **NUNCA** la realiza el agente principal basándose en el historial conversacional del chat.
* El trío de artefactos **TaskDoc + Pills + Atoms** debe contener el 100% de la información, contratos, guardarraíles, rutas y dependencias necesarias.
* Un nuevo subagente sin contexto previo (*zero-context subagent*) debe ser capaz de tomar este paquete de contexto y completar la tarea de forma autónoma sin requerir memoria previa ni preguntas aclaratorias.

### 2. Delegación Estricta por Subagentes (NUNCA Ejecutar Individualmente)
* **SIEMPRE** se deben invocar subagentes independientes (vía `invoke_subagent` o runners de subagentes) para ejecutar los roles de **Executor** y **Tester**.
* **NUNCA** el Supervisor ni la sesión del chat principal debe asumir e implementar individualmente los cambios de código o la ejecución de pruebas.

---

## 📋 Flujo Operacional Paso a Paso

### Paso 1: Diseño y Preparación del Paquete de Contexto Cero
1. Crear/Escribir la tarea en `desk/drawer/tasks/task-<id>.md`.
2. **Ambiguity Review:** Verificar que la tarea sea autosuficiente. Si un agente nuevo tuviera que adivinar una ruta, variable, comando o contrato, la tarea está incompleta.
3. Vincular explícitamente en la tarea:
   - **`pills`**: Todas las cápsulas de guardarraíles operacionales aplicables.
   - **`atoms`**: Todos los átomos de conocimiento y arquitectura necesarios.
   - **`files`**: La lista exacta de archivos que se esperan modificar.

### Paso 2: Promoción y Commit de Preparación
1. Hacer commit de la creación en el drawer.
2. Promover la tarea a activa:
   ```bash
   deskops promote drawer-task-to-active-task task-<id>
   ```

### Paso 3: Despacho Obligatorio del Subagente Executor
1. El Supervisor **invoca un subagente independiente** (Executor) entregándole únicamente su paquete de contexto:
   - Contenido completo de `task-<id>.md`
   - Contenido de las `Pills` vinculadas
   - Contenido de los `Atoms` vinculados
2. El subagente Executor trabaja en su propia sesión aislada, realiza las modificaciones dentro del `Scope` y ejecuta las comprobaciones locales.

### Paso 4: Despacho Obligatorio del Subagente Tester
1. El Supervisor **invoca un subagente independiente** (Tester) para validar los contratos de forma imparcial.
2. El subagente Tester ejecuta la validación y emite las evidencias en `runs/subagents/<run-dir>/`:
   - `validation.log` (salida completa de pruebas)
   - `result-summary.md` (resumen de resultados)

### Paso 5: Cierre Atómico y Ritual de Fase
1. Una vez verificadas las evidencias por el Supervisor, se ejecuta el commit de cierre oficial:
   ```bash
   deskops closeout commit --task task-<id> --run-dir runs/subagents/<run-dir>
   ```
2. Al completar todas las tareas de la fase activa, ejecutar el **Ritual de Fase** (`desk/rituals/phase.md`).

---

## 🚫 Anti-patrones Prohibidos
- ❌ **Implementar inline:** Modificar archivos de código directamente desde el agente Supervisor o en la conversación principal.
- ❌ **Paquetes de contexto incompletos:** Lanzar un subagente con una tarea vaga esperando que "adivine" la implementación.
- ❌ **Saltarse al Tester:** Validar la tarea uno mismo sin lanzar un subagente de pruebas independiente y sin evidencias.
- ❌ **Git commit manual:** Usar `git commit` simple en lugar del comando de cierre oficial `deskops closeout commit`.
