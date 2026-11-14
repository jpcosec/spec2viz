## REFORMULACION

El nodo debe producir en el repo specIR tres documentos: `docs/spec2viz/matriz-de-cobertura.md`, `docs/spec2viz/gate-de-retiro.md` y `docs/decisiones/fuente-de-verdad-del-diagrama.md`. Propósito: inventariar toda capacidad de spec2viz con modo de cobertura y condición verificable de retiro; fijar la relación entre YAML de spec y grafo SLDB; escribir un gate comprobable. Resultado: una matriz que permita derivar tareas de migración sin re-inventariar spec2viz, sin declarar nada migrado. Límites: no migra ni implementa filas, no extrae otras tecnologías, no analiza impacto. Es `task.docs`; no es agregado ni paquete ejecutable.

## AMBIGUEDADES

1. «el plan absorber-spec2viz-y-modelos-ui de SLDB»: no da ruta ni ID; obligaría a inventar su ubicación y vigencia.
2. «la tarea final IR13 la actualiza después… una vez cerradas IR13a, IR13b, IR13c e IR13d»: no define esas tareas; obligaría a inventar alcance y dependencias.
3. «Todos los comandos y subgrupos que lista la ayuda del CLI de spec2viz»: no fija versión ni snapshot; obligaría a inventar el universo auditado.
4. «prueba equivalente declarada por fila reemplazada»: no da criterio de equivalencia; obligaría a inventar qué cuenta como prueba.
5. «los stores cuyo índice registra modelos spec2viz.sldb_models»: no da censo ni método de descubrimiento; obligaría a inventar el universo de stores.
6. «migrar tal cual; reemplazar…; exponer desde specIR lo que ya vive en SLDB»: los modos pueden solaparse; obligaría a inventar la regla de asignación.
7. «Ninguna fila dice descartado, fuera de alcance o ya implementado sin una prueba citada» frente a «no declara nada como ya migrado»: obligaría a inventar si se permite descartar y con qué evidencia.

## DRY-RUN

Lecturas previstas: `spec2viz/spec2viz/cli.py`, módulos del paquete, `spec2viz/tests/`, el plan SLDB citado, las pills y los archivos de consumidores. Cambios previstos: crear los tres documentos; poblar filas con modo y condición; redactar la decisión y el gate; asegurar el atom de decisión. Dependencias: IR03 (API SLDB), IR06 (tipos/pruebas), plan SLDB y consumidores externos. Validaciones futuras: cobertura de ayuda CLI y módulos, citas por fila, sustituto y prueba en modo reemplazar, operación SLDB en modo exponer, archivo por consumidor, atom de decisión y checklist del gate. Sin ejecutar nada.

## FUTURO

IR13/IR13a-d añadirán evidencia por fila; otro nodo derivará las tareas de migración; la suite de spec2viz se ejecutará contra specIR; los repos consumidores cambiarán mediante su desk; un humano aprobará la decisión y el gate.
