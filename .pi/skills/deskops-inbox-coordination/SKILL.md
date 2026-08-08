---
name: deskops-inbox-coordination
description: Skill para gestionar la comunicación inter-proyecto, envío de mensajes a inboxes de otros repositorios (sldb, spec2viz), triaje de notas entrantes y eliminación de fuentes procesadas.
---

# Deskops Inbox & Cross-Project Coordination

Este skill define el protocolo para enviar, recibir, triajar y consumir notas en `desk/inbox/` entre repositorios del `hum-ecosystem`.

---

## 🚨 MANDATOS CRÍTICOS E INNEGOCIABLES

### 1. Reporte Directo a Herramientas Hermanas (No parches sucios)
* Cuando un agente o usuario en un proyecto encuentra un fallo o limitación en una herramienta hermana (ej. `sldb` o `spec2viz`), **NUNCA** construye un parche sucio o desvío dentro de `deskops` sin antes registrar la nota en el `inbox` del repositorio destino.

### 2. Regla de Eliminación de Fuentes Procesadas (atom-used-source-artifacts-are-deleted)
* Cuando una nota de `inbox/` se triaja y promueve a una tarea activa en `desk/tasks/` o a un fix, **el archivo fuente del inbox DEBE eliminarse** para mantener el estado limpio y evitar duplicaciones.

---

## 📋 Procedimientos Operacionales

### Paso 1: Enviar una Nota a un Proyecto Hermano
```bash
deskops inbox "Mensaje o reporte con evidencia clara" \
  --repo <nombre-repo-destino> \
  --kind {unclear|suggestion} \
  --title "Título corto descriptivo"
```

### Paso 2: Listar e Inspeccionar la Bandeja del Proyecto Actual
```bash
deskops inbox --list --root .
deskops inbox --show <slug-fragmento> --root .
```

### Paso 3: Triaje de Notas de Inbox
1. Revisar la nota entrante.
2. Si requiere trabajo del proyecto:
   - Crear la tarea correspondiente en `desk/drawer/tasks/`.
   - Eliminar la nota procesada del inbox.

---

## 🚫 Anti-patrones Prohibidos
- ❌ Usar `inbox/` como borrador de tareas locales del propio agente (para eso se usa `drawer/`).
- ❌ Marcar notas del inbox como "procesadas" o "promovidas" sin borrar el archivo fuente.
