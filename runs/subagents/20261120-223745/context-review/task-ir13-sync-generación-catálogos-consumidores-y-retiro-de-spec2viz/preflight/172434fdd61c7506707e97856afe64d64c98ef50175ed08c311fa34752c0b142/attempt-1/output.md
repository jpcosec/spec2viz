## REFORMULACION
Cierre de la migración spec2viz→specIR. Propósito: demostrar con evidencia que toda capacidad de spec2viz queda cubierta y que ningún consumidor depende de ella. Resultado: comprobador `specir retirement check` (src/specir/visual/retirement.py y subcomando añadido a src/specir/cli.py), acta `docs/spec2viz/acta-de-retiro.md` y matriz actualizada con acreditación por fila; el gate exige rc 0 sobre el universo auditado (inventario de la matriz + repo specIR). Repo: specIR. Límites: auditoría de solo lectura; no implementar capacidades (IR07, IR13a/b/d/e); no editar otros repos, solo pedir cambios con `deskops message send`; no archivar spec2viz. Es un agregado funcional: `task_type: task.code`, pero las dependencias hacen de agregación.

## AMBIGUEDADES
1. «los modos ni las condiciones de retiro que fijó IR07» y «una fila en modo reemplazar»: el input no define qué modos existen ni sus reglas. Obligaría a inventarlos.
2. «G6 cumplido; G1, G2, G3, G4, G5 y G7 abiertos»: no se define qué son G1–G7. Obligaría a inventar su contenido y criterio.
3. «las tareas de compiladores, renderers, IR13a, IR13b, IR13c e IR13d» frente a «IR13c se retiró»: contradicción. Obligaría a decidir si IR13c existe.
4. «122 dependencias y 30 filas abiertas» frente a «122 dependencias y 23 filas abiertas»: dos estados. Obligaría a elegir el vigente (por orden, el segundo).

## DRY-RUN
Lecturas: matriz (inventario y «Acreditación (IR13)»), cli.py creado por IR13d, acta, pruebas de IR13a/b/d/e, modos de IR07.

Cambios hipotéticos: retirement.py; subcomando en cli.py; sección de acreditación por fila; acta con salidas y mensajes enviados.

Dependencias: IR07, IR13a, IR13b, IR13d e IR13e cerradas.

Validaciones futuras: fixture con fila sin prueba; detección de import, dependencia, llamada y modelo; solo-documentación no reportado; error 2 por inventario; rc 1 con pendientes; rc 0 real; suite de spec2viz.

Hijos→transferencias: IR07 entrega matriz con modos y condiciones; IR13a, specs sincronizadas/generadas; IR13b, catálogos y emparejamiento de átomos; IR13d, cli.py base y habilidad; IR13e, pruebas portadas como evidencia. IR13 consume todo, añade gate y acta. Validación conjunta: cada fila acreditada con prueba citada y rc 0; si no, retiro no declarado.

## FUTURO
Aceptación del gate y decisión de archivar spec2viz: dueño de spec2viz. Cambios en graph_ui, deskops, pron, sldb y spec2viz: sus desks. Declarar el retiro en el acta: humano (JP). Portar pruebas restantes «usar sldb directamente»: IR13 o tarea derivada.
