## REFORMULACION
Nodo ejecutable de edición documental, no agregado. Propósito: corregir en `docs/spec2viz/acta-de-retiro.md` afirmaciones obsoletas sobre G5 y la fila de IR. Resultado: la fila G5, el punto G5 de «Lo que falta» y la fila IR en «Consumidores» reflejan que la federación de las pruebas está cerrada (`b16aab7`, `4f1e108`) y que queda retirar `spec2viz/.sldb` del universo del comprobador y archivar el store. Repo: IR. Límites: solo ese archivo; fuera matriz, nueva corrida del comprobador, declaración del retiro, código y pruebas.

## AMBIGUEDADES
1. «Si algo falla, no se corrige el acta: se anota y se reporta»: no indica dónde ni con qué formato se anota/reporta. Obligaría a inventar destino y plantilla.
2. «los informes de IR13h citados en Why»: solo se dan directorios (`runs/subagents/deskops-e-...` y `deskops-t-...`), no nombres de archivo. Obligaría a inventar qué informe leer.
3. «grep -nE 'spec2viz' tests/conftest.py no muestra ninguna ruta al store real de spec2viz»: no fija el patrón exacto que cuenta como «store real». Obligaría a inventar el criterio.
4. «git diff --stat muestra, fuera de desk/, .sldb/ y runs/, solo docs/...»: no aclara si cambios preexistentes ajenos invalidan la tarea. Obligaría a inventar tolerancia.

## DRY-RUN
Lecturas hipotéticas: TaskDoc, acta completa e informes de IR13h; `git status`/`git diff`. Cambios previstos: editar únicamente los tres lugares del acta; no tocar código ni pruebas. Dependencias: commits presentes, `.venv` y `deskops` disponibles. Validaciones futuras: `git merge-base --is-ancestor 4f1e108 HEAD` con rc 0; `grep` sin ruta al store; diff limitado al acta; `pytest` de los dos archivos indicados con rc 0; `deskops graph missing --root .` con rc 0. Si una verificación falla, detenerse. Nada de esto se ejecuta aquí.

## FUTURO
Otro nodo registrará el cierre/commit y actualizará el estado de la tarea. Un humano decide si una verificación falla o si la redacción exacta no puede inferirse. La matriz, la declaración del retiro y el archivado del store corresponden a otros nodos o responsables.
