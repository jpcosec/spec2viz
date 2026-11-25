REFORMULACION
Propósito: alinear spec2viz con `sldb notations validate` y retirar los comandos provisionales de specIR. Resultado: SV-K16, SV-K21, SV-K26 y SV-K29 quedan cumplidas como “usar sldb directamente” con equivalente `sldb notations validate`; SV-K09, K18 y K23 pasan a cumplidas si todas sus hijas lo están; se eliminan `specir diagram validate` y el alias `specir validate`; ayuda, docs, tests y CHANGELOG (si existe) quedan actualizados; retirement check deja solo SV-A17. Repo: SLDB_1/IR (`/mnt/ssd/proyectos/SLDB_1/IR`). Límites: dentro `docs/spec2viz/matriz-de-cobertura.md`, `docs/spec2viz/correspondencia-cli.md`, definiciones en `src/specir`, `tests/visual/test_cli.py` y tests que invoquen esos comandos, CHANGELOG; fuera SV-A17, tests de paridad que importan spec2viz y el acta de retiro.

AMBIGUEDADES
1. “specir diagram validate y el alias specir validate se retiran de specIR”: no precisa archivos ni si el alias es entry point separado; obligaría a inventar ubicaciones.
2. “los tests que llamen a esos comandos”: no los identifica; obligaría a inventar el inventario de tests.
3. “citando un test” / “citando el test”: no nombra la evidencia exacta; obligaría a inventar el test citado.
4. “correr specir retirement check con las rutas del inventario”: no define inventario, ruta ni formato; obligaría a inventar la invocación.
5. “CHANGELOG si existe”: no fija ruta ni formato; obligaría a inventar el archivo.

DRY-RUN
Lecturas: TaskDoc, rituales, matriz, correspondencia CLI, definiciones en `src/specir`, `tests/visual/test_cli.py`, tests de matriz y retirement gate, inventario y CHANGELOG. Cambios previstos: editar filas y subgrupos de la matriz; actualizar tabla de equivalentes y test de ayuda; borrar comandos y ajustar tests para comprobar su ausencia; actualizar documentación y CHANGELOG. Dependencias: `sldb notations validate` disponible; inventario y nombres de tests localizados; worktree para commit. Validaciones futuras: ejecutar el pytest indicado; comprobar que `sldb notations validate --help` responde; ejecutar retirement check y verificar que solo queda SV-A17; commit con trailer Task-Id. Sin ejecutar nada.

FUTURO
Otro nodo o humano debe aportar el inventario de rutas, confirmar archivos del alias y tests citados, y aprobar el commit. El ejecutor producirá los cambios, la salida de retirement check en el run dir y el commit; el cierre actualizará board y átomos.
