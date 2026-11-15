# Gate de retiro de spec2viz: procedimiento

La lista comprobable del gate (G1 a G7) está en la sección «Gate de retiro» de
`docs/spec2viz/matriz-de-cobertura.md`; este documento no la repite, solo fija quién la evalúa, en qué
orden y qué pasa si falla.

## Quién y cuándo

- Lo evalúa la tarea IR13 (`task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz`), una
  vez cerradas IR11, IR12, IR13a, IR13b, IR13d y las tareas de sldb D1 a D4.
- IR13 es la única que escribe evidencia en la matriz (la prueba que acredita cada fila) y el acta de
  retiro `docs/spec2viz/acta-de-retiro.md`.
- Archivar o borrar el repo spec2viz es decisión de su dueño una vez cumplido el gate; ni IR07 ni IR13 lo
  hacen.

## Orden de evaluación

1. **G7** primero: si la decisión del YAML no está aceptada por JP, el gate no se evalúa.
2. **G6** (specIR limpio): prueba de imports de specIR.
3. **G1, G2 y G3** (filas, suite y CLI): por cada fila, ejecutar la prueba citada; la tabla «Pruebas de
   spec2viz por fila» no puede dejar un archivo de `spec2viz/tests/` sin fila ni un caso sin portar o sin
   prueba equivalente declarada.
4. **G4 y G5** (consumidores y stores): el comprobador de IR13 recorre en solo lectura exactamente el
   universo del «Inventario de consumidores» de la matriz más el repo de specIR, y lista cada dependencia
   remanente con repo o store, ruta, línea y clase.

## Si falla

- Cualquier ítem en falso: el comprobador sale con código distinto de cero y el retiro no se declara.
- Una dependencia remanente en otro repo no se corrige desde specIR: se pide al desk de ese repo
  (`deskops message send --to <repo>`) y se registra como evidencia pendiente.
- Una fila cuya condición resulta imposible se reescribe en la matriz con aprobación de JP; nunca se
  marca como descartada sin prueba.
