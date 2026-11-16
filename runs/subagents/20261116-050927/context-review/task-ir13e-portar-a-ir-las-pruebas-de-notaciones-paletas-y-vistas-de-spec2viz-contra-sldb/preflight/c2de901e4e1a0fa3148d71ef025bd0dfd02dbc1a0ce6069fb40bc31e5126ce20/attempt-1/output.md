## REFORMULACION

El nodo es una tarea ejecutable (`task.code`) del repo IR, no un agregado. Propósito: aportar evidencia para el retiro de spec2viz portando a IR, contra sldb, las pruebas de notaciones, paletas y vistas. Resultado: `tests/visual/test_notations_parity.py` con 40 pruebas portadas y 9 comparaciones «valida igual», fixtures copiados de spec2viz en b624b75, reexportaciones en `src/specir/visual/notation_style.py`, y matriz de cobertura y acta actualizadas. Límites: no modificar código de sldb ni de spec2viz, no implementar notaciones/paletas/vistas, no declarar el retiro, no tocar las filas excluidas y no ajustar expectativas para forzar verdes.

## AMBIGUEDADES

1. «dos comparaciones «valida igual» (las 8 notaciones y la paleta default…)» frente a «las 9 comparaciones «valida igual»»: ¿dos grupos o nueve casos? Obliga a inventar granularidad y recuento reportado.
2. «las filas K dependientes se acreditan citando tests/visual/test_cli.py cuando todas las filas de las que dependen quedan cumplidas»: no define qué filas son dependientes ni su conjunto (SV-K18 y SV-K23 no figuran en el Rationale); obliga a inventar el grafo.
3. «cada fila listada queda cumplida citando esas pruebas»: falta la tabla prueba→fila; obliga a inventar la trazabilidad de SV-A17, SV-E02, SV-H01..H06 y SV-J06.
4. «si no, la fila SV-A17 queda abierta diciendo que falta exportarlo»: no aclara si las demás pruebas siguen ejecutándose; obliga a decidir un alcance parcial.

## DRY-RUN

Lecturas: taskdoc, pills, bundle-2, matriz, acta, los cinco `test_*.py` de spec2viz en b624b75, exports de `sldb.api`, `notation_style.py`, `tests/test_imports.py` y `tests/visual/test_cli.py`. Cambios previstos: crear fixtures (8 yml, paleta, README), añadir reexportaciones y `__all__`, escribir el archivo de pruebas, actualizar 16 filas y el resumen, anotar el acta. Dependencias: revisión de spec2viz, API de sldb, `deskops`, `.venv`, `TMPDIR=/dev/shm` y `flock`. Validaciones futuras: pytest del archivo nuevo, tests de imports/matriz/gate, greps de imports, `specir retirement check`, suite completa y `deskops graph missing`; nada se ejecuta aquí.

## FUTURO

El desk de sldb decide y entrega exports faltantes (p. ej. `ViewDoc`) y responde notas; el desk de spec2viz conserva G5 y su store; IR07 o un humano decide el retiro; otro nodo/CI ejecuta la suite completa; `deskops` entrega los mensajes.
