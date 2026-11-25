REFORMULACION
Propósito: corregir la resolución del workspace en las pruebas de IR para que usen `SPECIR_WORKSPACE` cuando exista. Resultado: `tests/conftest.py` resuelve el workspace mediante una función `workspace_root()` —variable de entorno si está definida; si no, `REPO.parent`— y un test nuevo verifica ambos casos. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: solo `tests/conftest.py` y un test chico; fuera el resto de fixtures. Es una tarea ejecutable de código, no un agregado.

AMBIGUEDADES
1. “Revisar que todo uso de WORKSPACE (l.~96 deskops, otros hermanos) pase por esa constante.” No se identifican “otros hermanos” ni si su ajuste pertenece al alcance; obligaría a inventar qué rutas hermanas revisar y si modificarlas.
2. “con monkeypatch de la variable y reimportando o leyendo la funcion que la resuelve” deja abierto el mecanismo del test; obligaría a elegir entre reimportar el módulo o probar `workspace_root()` directamente.
3. “los tests que usan el store de deskops encuentran el workspace desde una copia fuera de SLDB_1” no enumera esos tests; obligaría a inventar el conjunto de aceptación, ya que la validación solo nombra dos archivos.

DRY-RUN
Lecturas previstas: `tests/conftest.py` completo, especialmente la línea 29 y todos los usos de `WORKSPACE`; `tests/test_mcp_extension.py` como referencia; configuración relevante del repo. Cambios previstos: extraer `workspace_root()` con fallback `REPO.parent`, asignar `WORKSPACE = workspace_root()` y hacer que los usos existentes pasen por esa constante; crear `tests/test_workspace_env.py` con monkeypatch para cubrir variable presente y ausente. Dependencias: `os`, `pathlib`, `pytest` y `SPECIR_WORKSPACE`. Validaciones futuras: ejecutar el comando de Validación con `TMPDIR`, `PYTHONPATH` y el intérprete indicados; comprobar además que no se alteraron fixtures fuera de alcance. Nada se ejecuta en esta revisión.

FUTURO
El closeout decide y añade los trailers del commit, actualiza el Board y enlaza conocimiento durable si corresponde. Un humano revisa/aprueba el cambio. El ritual de fase integra la tarea con las demás y valida el conjunto; otro nodo puede ejecutar la validación ampliada.
