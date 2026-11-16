# Drawer Board

This board routes deferred work only. Todo lo que aparece aquí queda diferido: ninguna candidata está activa, ninguna figura en `desk/tasks/Board.md` y ninguna tiene `task_type` asignado.

Propuesta para revisión, 2026-11-11. Backlog inicial de specIR: repo periférico sobre SLDB, hoy MCP y modelado semántico, más adelante la capa visual de spec2viz hasta poder retirarlo.

## Remaining

### Rama MCP y modelado


### Rama cobertura y retiro de spec2viz


## Dependencias

```text
IR01 ─┬─ IR02 ─┐
      ├─ IR03 ─┴─ IR04 ─┐
      └─ IR05 ──────────┴─ IR06 ─┬─ IR08 ─┐
                                 ├─ IR09 ─┴─ IR10
                                 ├─ IR07 (también IR03) ─┬─ IR11 (también IR06) ── IR12 ─┐
                                 │                       └──────────────────────────────┴─ IR13
```

La fuente de las dependencias es el campo `depends_on` de cada candidata, con ids completos; este dibujo es solo un resumen.

## Rule

Nothing in `desk/drawer/` executes. Cuando una candidata esté lista, se autora una tarea completa con `deskops add task --from-drawer <item>`, momento en que se le asigna su tipo; la candidata se retira después con `deskops drawer remove`. No hay promoción directa del drawer a tarea activa. El store no rastrea `desk/drawer/`: estos archivos se resuelven en disco.
