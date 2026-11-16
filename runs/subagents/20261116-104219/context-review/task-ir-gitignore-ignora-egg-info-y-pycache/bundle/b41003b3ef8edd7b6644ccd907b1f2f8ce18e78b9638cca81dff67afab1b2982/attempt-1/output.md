## REFORMULACION

Encargo: en el repo IR, añadir a `IR/.gitignore` dos líneas al final, `*.egg-info/` y `__pycache__/`, para que `git status` deje de listar `src/specir.egg-info/` y los `__pycache__/`. Nodo ejecutable `task.code`, no agregado; ritual activo `ritual-execution`. Límites: solo `.gitignore`; no borrar artefactos del disco, no tocar otros archivos ni el hook de scion, no ejecutar la suite. Resultado: dos líneas agregadas, ningún archivo rastreado oculto y validaciones del TaskDoc en verde.

## AMBIGUEDADES

1. `"status: draft"` frente a `"implement only the active task for IR"`: no se define si una tarea en draft está autorizada para ejecutarse; obligaría a inventar la regla de autorización.
2. `"git check-ignore -q tests/__pycache__ también (si ese directorio existe)"`: no se especifica si la validación se omite o se considera cumplida cuando el directorio no existe; obligaría a inventar el criterio de pase.
3. `"los directorios __pycache__/"` frente a la validación limitada a `tests/__pycache__`: no queda claro si debe comprobarse cualquier `__pycache__` (por ejemplo, bajo `src/specir/`); obligaría a inventar la cobertura real.
4. `"git check-ignore -q src/specir.egg-info sale con rc 0"`: no indica si la ruta debe existir previamente; obligaría a inventar esa precondición.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout/phase, pill de guardrail y `.gitignore`. Cambio previsto: agregar exactamente dos líneas al final, sin tocar las tres existentes. Dependencias: raíz IR, `git` y `deskops` disponibles; artefactos pueden o no existir. Validaciones futuras: `git diff .gitignore`; `git check-ignore` para egg-info y tests/__pycache__; `git status --porcelain` filtrado; `git ls-files` filtrado; `deskops graph missing --root .`. Si falta una dependencia real, detenerse y reportar el bloqueo, conforme a la pill. No hay código que probar: la suite no aplica.

## FUTURO

Un humano decide si el draft está autorizado y realiza el commit. El ritual de closeout actualiza el board y enlaza conocimiento durable; la fase valida la integración del cambio con el resto de tareas.
