REFORMULACION  
Propósito: aislar las pruebas MCP de IR del store real de deskops para que escrituras externas no rompan la suite. Resultado: un fixture de sesión crea una copia temporal del store de deskops y las pruebas MCP enlazan y digieren esa copia, conservando cobertura federada. Repo: IR (`/mnt/ssd/proyectos/SLDB_1/IR`), limitado a `tests/conftest.py` y `tests/test_mcp_extension.py`. Límites: no cambiar deskops ni sldb; queda fuera la tarea de federación de spec2viz, que debe estar integrada primero. Nodo ejecutable (`task.code`), no agregado.

AMBIGUEDADES  
1. “el .sldb de deskops (sin la caché)”: no define qué entradas constituyen caché ni si se copia recursivamente todo lo demás; obligaría a inventar el criterio de exclusión.  
2. “los archivos que lista git -C <deskops> ls-files”: no fija directorio de trabajo, ref ni tratamiento de enlaces/submodules; obligaría a inventar el comando exacto.  
3. “Si sldb rechaza quitar un enlace porque un modelo de deskops depende de él”: no indica cómo detectar rechazo ni dependencia; obligaría a inventar código de error o mensaje.  
4. “el árbol .sldb más los .md listados por git ls-files del proyecto real, leídos en la copia”: “proyecto real” no aclara si es deskops o también los stores enlazados copiados; obligaría a inventar el alcance del digest.  
5. “pasada la ventana de la copia”: no define cómo delimitar esa ventana en `strace`; obligaría a inventar un marcador temporal.

DRY-RUN  
Un ejecutor leería el TaskDoc, `tests/conftest.py`, `tests/test_mcp_extension.py` y el closeout de la dependencia. Crearía `build_deskops_copy(tmp_path_factory)` y un fixture `scope="session"`; copiaría `.sldb` sin caché y archivos versionados; quitaría enlaces externos con `sldb stores remove` o copiaría stores enlazados a `<tmp>/<nombre>`; haría que `FEDERATED` reciba la copia; ajustaría `federated_digest` y `mount_copy`; no relajaría aserciones. Dependencias: closeout `4f1e108` integrado y CLI sldb compatible. Validaciones futuras: grep, pytest dirigido, `sldb stores list`, `strace`, suite completa con `flock` y `deskops graph missing`. Sin ejecutar nada.

FUTURO  
Otro nodo integra/verifica la dependencia; el ejecutor futuro reportará bloqueos si los enlaces no resuelven; validaciones y aceptación final corresponden a ejecución y revisión humana.
