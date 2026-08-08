---
name: deskops-health-and-drift
description: Skill especializado en diagnosticar la salud de desk/, detectar deriva (drift) entre modelos SLDB y agentes materializados, y verificar enlaces en el grafo KGDB. Usar al auditar o reparar repositorios deskops.
---

# Deskops Health, Repair & Drift Management

Este skill guía la inspección de la salud del espacio de trabajo `desk/`, la reparación segura de estados inconsistentes y la detección de deriva de artefactos.

---

## 🚨 MANDATOS CRÍTICOS E INNEGOCIABLES

### 1. Diagnóstico previo a cualquier edición de recuperación
* NUNCA asumir que el estado de `desk/` está limpio o corrupto sin ejecutar `deskops status` y `deskops doctor`.
* NUNCA modificar manualmente archivos en `desk/` para reparar un estado roto si existe un comando oficial de `deskops`.

### 2. Detección de Deriva de Agentes y Modelos
* Los archivos instalados de agentes (ej. en `~/.pi/agent/agents/` o `.opencode/`) son **materializaciones** de documentos fuente `RoleDoc`/`Atom`.
* Si un agente instalado difiere de su fuente, el archivo instalado NO se edita a mano; se edita la fuente y se ejecuta `deskops materialize`.

---

## 📋 Comandos y Procedimientos de Diagnóstico

### Paso 1: Verificación de Salud del Workspace
```bash
deskops status --root .
deskops doctor --root .
```

### Paso 2: Detección de Enlaces Faltantes en el Grafo (KGDB)
```bash
deskops graph build --root .
deskops graph missing --root .
```

### Paso 3: Verificación de Deriva (Drift Check)
```bash
deskops drift check --root .
```

### Paso 4: Re-materialización de Agentes
Si se detecta deriva en los agentes instalados:
```bash
deskops materialize --root .
```

---

## 🚫 Anti-patrones Prohibidos
- ❌ Editar archivos en `~/.pi/agent/agents/` manualmente.
- ❌ Saltearse `deskops doctor` cuando hay inconsistencias en `Board.md`.
