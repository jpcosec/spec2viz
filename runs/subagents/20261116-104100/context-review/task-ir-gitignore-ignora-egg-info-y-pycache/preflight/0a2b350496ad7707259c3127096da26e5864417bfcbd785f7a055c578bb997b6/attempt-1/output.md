## REFORMULACION

El encargo es una tarea ejecutable, no un agregado: modificar únicamente `IR/.gitignore` para que `git status` deje de listar `src/specir.egg-info/` y los directorios `__pycache__/`. El resultado esperado es añadir al final dos líneas exactas, `*.egg-info/` y `__pycache__/`, sin tocar las tres existentes. Límites: no borrar artefactos del disco, no cambiar otros archivos, no modificar el hook de scion y no ejecutar la suite. Repo: IR. La validación incluye comprobar que no haya archivos rastreados bajo esos patrones.

## AMBIGUEDADES

1. “git check-ignore -q tests/__pycache__ también (si ese directorio existe)”. El input no aclara si el ejecutor debe crear el directorio, omitir la comprobación o considerar ausencia como éxito; obligaría a inventar el procedimiento y el resultado esperado.
2. “agregar a IR/.gitignore dos líneas, *.egg-info/ y __pycache__/, al final”. No se especifica el orden entre ambas líneas; obligaría a elegir uno, aunque no cambia el resultado funcional.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, `IR/.gitignore`, y comprobaría el estado con `git status --porcelain` y `git ls-files`. Después añadiría exactamente las dos líneas al final de `.gitignore`. Dependencias: repositorio git en IR, archivo `.gitignore` existente y comandos git/deskops disponibles. Validaciones futuras: `git diff .gitignore` con solo dos líneas añadidas; `git check-ignore` para `src/specir.egg-info` y, condicionalmente, `tests/__pycache__`; `git status --porcelain` sin coincidencias; `git ls-files` sin archivos rastreados bajo esos patrones; `deskops graph missing --root .` con rc 0. No se ejecutará nada en este preflight.

## FUTURO

Un nodo ejecutor aplicará la edición y recogerá las salidas de validación. Un humano o nodo de cierre decidirá la aceptación de la tarea; el input no especifica commit, borrado de artefactos ni cambios en el hook.
