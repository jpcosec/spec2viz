## REFORMULACION
IR05 es un nodo de decisión (no ejecutable) del repo specIR: debe fijar una taxonomía canónica de procedencia y una regla de divergencia entre modelo y código. El resultado es `docs/decisiones/procedencia-y-divergencia.md` con tres atoms: taxonomía y equivalencias; representación de lo desconocido y paso de inferencia a validada; y divergencia ante fuente cambiada. Límites: elegir entre tres listas dadas, definir equivalencias y anclas, decidir prevalencia y desconocido; queda fuera implementar extractores. Depende de IR01 y lo consumen IR06, IR08 e IR09.

## AMBIGUEDADES
1. «definir las equivalencias»: las listas no son isomorfas (tres, cuatro y cinco categorías); obligaría a inventar correspondencias y semántica de categorías no descritas.
2. «decidir qué prevalece cuando modelo y código discrepan»: no se indica criterio ni autoridad; obligaría a inventar la regla de prevalencia.
3. «cómo una inferencia pasa a validada, y por acción de quién»: no se nombra actor ni evidencia exigida; obligaría a inventar el rol validador.
4. «qué ocurre con un nodo cuya fuente cambió»: no se define política (marcar, invalidar, conservar); obligaría a inventar el tratamiento.
5. «la fila correspondiente de la matriz de auditoría»: la matriz es salida de IR01 y no está en el input; obligaría a inventar sus filas.
6. «las anclas de código de SLDB»: no se describen en el input; obligaría a inventar su forma y alcance.

## DRY-RUN
Un ejecutor futuro leería: `fundamentos_modelado_semantico_mcp.md` §7, `Plan_IR.md` fase 5, `sldb/src/sldb/models/provenance.py`, la matriz de IR01 y este DAG. Produciría un único documento con tres atoms y tabla de equivalencias. Dependencia bloqueante: IR01. Validaciones futuras: existencia de los tres atoms, equivalencias completas, regla de desconocido/validación con actor, política de divergencia y, si falta capacidad en SLDB, fila de auditoría identificada. No ejecuta código ni modifica SLDB.

## FUTURO
IR01 entrega la matriz de auditoría; un humano ratifica la taxonomía y el actor validador; IR06, IR08 e IR09 citan la taxonomía decidida; IR13 verifica la cobertura global.
