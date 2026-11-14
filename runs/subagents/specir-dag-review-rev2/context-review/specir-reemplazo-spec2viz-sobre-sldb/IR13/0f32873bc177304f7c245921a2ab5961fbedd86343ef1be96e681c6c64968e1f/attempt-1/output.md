REFORMULACION
Propósito: cerrar la migración de consumidores de spec2viz y demostrar con evidencia que specIR cubre toda capacidad y que ningún consumidor depende de spec2viz. Resultado: comprobador de retiro, pruebas, acta de retiro y matriz actualizada. Repo: specIR. Límites: audita solo el inventario de `docs/spec2viz/matriz-de-cobertura.md` más specIR; no implementa capacidades de IR13a-d ni compiladores/renderers, no edita otros repos y no archiva ni borra spec2viz. Es un nodo de entrega, no un agregado ejecutable.

AMBIGUEDADES
1. “archivos de CI” y “scripts” no definen extensiones, rutas ni herramientas; obligaría a inventar el conjunto exacto de configuración ejecutable.
2. “puntos de entrada y llamadas al comando spec2viz” no aclara invocaciones dinámicas, alias o cadenas construidas; obligaría a inventar reglas de detección.
3. “modelos spec2viz.sldb_models registrados en un índice de store” no da ruta, formato ni esquema del índice; obligaría a inventar cómo leerlo.
4. “prueba citada” no define formato de cita; obligaría a inventar una convención.
5. “clase de dependencia” no enumera etiquetas exactas; obligaría a inventar la taxonomía.
6. “mensaje enviado a su desk” y “referencia del cambio que lo resolvió” no definen canal, formato ni momento de envío; obligaría a inventar la evidencia.
7. “sin que ningún repo del workspace falle” contradice “un repo o store que no esté en ese inventario no se audita”; obligaría a decidir si workspace equivale al inventario o es más amplio.
8. “La suite de spec2viz pasa contra specIR” no identifica versión, comando ni entorno; obligaría a inventar el procedimiento.

DRY-RUN
Un ejecutor leería IR07 —matriz, gate e inventario—, IR13a-d —capacidades, CLI y API— y el repo specIR. Implementaría `retirement.py`, su CLI y pruebas con fixtures: matriz con fila sin prueba; repo con import, dependencia, script y modelo de store; repo con solo documentación; inventario inválido o incompleto. Generaría el acta y actualizaría la matriz. Validaría códigos de salida, reporte de repo/ruta/línea/clase, no escritura, auditoría exacta del inventario, suite o equivalencias declaradas y contenido del acta. Sin ejecutar.

FUTURO
IR13a-d aportan capacidades, CLI/API y pruebas; IR07 aporta matriz, inventario y gate. Los desks de graph_ui, deskops y stores confirman migraciones; el dueño de spec2viz decide archivarlo tras el gate.
