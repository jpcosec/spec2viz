## REFORMULACION

Propósito: fijar una única taxonomía de procedencia para specIR y una regla de divergencia entre el modelo y el código fuente del que se extrajo, para que una inferencia no se trate como hecho. Resultado: tres atoms (taxonomía canónica + tabla de equivalencias; representación de lo desconocido y promoción de inferencia a validada con actor; regla de divergencia) y, si falta capacidad en SLDB, la fila correspondiente de la matriz de auditoría. Repo: solo specIR (`docs/decisiones/procedencia-y-divergencia.md` y atoms en desk). Límites: no implementar extractores; cualquier cambio en SLDB se pide por su desk (pill). No es un agregado ni paquete ejecutable: es un nodo de decisión documental; su "ejecución" es redactar y registrar decisiones.

## AMBIGUEDADES

1. "elegir la taxonomía canónica entre (1)… (2)… (3)…": el input no da criterio de elección ni declara jerarquía entre las tres listas; obliga a inventar el criterio (¿cobertura, autoridad del documento, compatibilidad con SLDB?).
2. "definir las equivalencias": no se aporta el contenido de las listas (1) y (2) —solo su ubicación—; mapear exige inventar correspondencias.
3. "decidir si la relación entre un nodo extraído y su fuente se expresa con las anclas de código de SLDB": `anchoring.md` no está en el bundle; su semántica tendría que inventarse.
4. "qué prevalece cuando modelo y código discrepan": no hay regla previa ni actor decisor; hay que inventar precedencia.
5. "la fila correspondiente de la matriz de auditoría": la matriz no está en el bundle; depende de task-ir01 y su formato es desconocido.
6. "Cada decisión se registra como atom" frente a `files: docs/decisiones/procedencia-y-divergencia.md`: no se aclara si el .md es entregable o solo contenedor.
7. "por acción de quién": no se nombra el rol que promueve inferencia a validada.

## DRY-RUN

Lecturas previstas: las tres listas citadas, `sldb/docs/architecture/provenance.md` y `anchoring.md` (fuera del bundle: habría que obtenerlos), la matriz de auditoría de IR01, el atom de seguridad MCP. Cambios previstos: crear tres atoms y el documento de decisiones; ninguno fuera de specIR. Dependencias: IR01 (matriz), disponibilidad de docs de SLDB (lectura, no edición). Validaciones futuras: existencia y contenido de los tres atoms, tabla de equivalencias completa, fila de auditoría citada, y que tipos de dominio y extractores puedan citar una sola taxonomía.

## FUTURO

Corresponde a un humano o a otro nodo: aprobar la taxonomía elegida, resolver las ambigüedades 1–7, entregar los documentos de SLDB y la matriz de IR01, y ejecutar en el desk de SLDB cualquier carencia detectada.
