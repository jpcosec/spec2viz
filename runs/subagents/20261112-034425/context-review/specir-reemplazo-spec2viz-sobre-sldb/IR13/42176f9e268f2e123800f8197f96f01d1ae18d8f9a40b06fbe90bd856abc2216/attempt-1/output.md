REFORMULACION
Propósito: cerrar la migración de spec2viz con un gate verificable. Resultado: comprobador en `src/specir/visual/retirement.py` expuesto desde `src/specir/cli.py`, pruebas, acta de retiro y matriz actualizada; el gate solo pasa si toda fila de cobertura tiene condición cumplida y prueba citada, y ningún repo/store del inventario depende de spec2viz. Repo: specIR. Límites: no implementa capacidades (IR13A–D, compiladores/renderers), no edita otros repos, no archiva spec2viz.

AMBIGUEDADES
1. “recorre en solo lectura el universo auditado” y “los repos consumidores y los stores que lista el inventario”: no se define raíz/base para resolver rutas ni formato del inventario; obligaría a inventar resolución de rutas y parser.
2. “cada fila tiene su condición cumplida con una prueba citada”: no hay esquema de fila ni formato de cita; obligaría a inventar parser y criterio de “citada”.
3. “El comprobador falla […] y pasa cuando todas la tienen”: no se especifican códigos, mensajes ni interfaz CLI; obligaría a inventar el contrato de salida.
4. “pedidos de migración a los desks”: no se define canal, formato ni si los emite el comprobador o solo el acta; obligaría a inventar.
5. “La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente declarado”: no se dice cómo verificarlo ni dónde está la suite; obligaría a inventar ejecución o lectura.
6. “sin que ningún repo del workspace falle” frente al universo limitado al inventario: “workspace” es más amplio; obligaría a decidir si se audita todo o solo inventario más specIR.

DRY-RUN
Es ejecutable, pero actúa como agregado final. Leería matriz, inventario, filas y pruebas citadas; resolvería repos/stores; escanearía en solo lectura imports, `pyproject.toml`/requirements/CI/Makefile/scripts, comandos/API e índices de store; clasificaría y reportaría repo, ruta, línea y clase; fallaría si hay filas sin prueba o dependencias; escribiría acta y actualizaría matriz. Depende de IR07 (matriz, inventario, gate) e IR13A–D. Validaciones futuras: fixtures de fallo/paso, no modificación, universo exacto, universo real limpio, suite/equivalencias, acta completa. Consumo de hijos: IR13A aporta sincronización/grafo/AST; IR13B catálogos/átomos; IR13C notaciones/paletas; IR13D CLI/API/habilidad; IR07 matriz e inventario. El gate y el acta validan el conjunto.

FUTURO
Los desks ejecutan las migraciones pedidas; el dueño de spec2viz decide archivarlo o borrarlo; un humano revisa y declara el retiro; ROOT confirma el cierre.
