REFORMULACION
Propósito: migrar a specIR el núcleo de spec2viz —compiladores y proyecciones— para que todo spec o vista del grafo se convierta en una representación intermedia dibujable. Resultado: ocho tipos (clase, secuencia, estado, componente, actividad, despliegue, matriz, reflexión) compilando desde YAML autorado y desde proyecciones (ViewDoc evaluado y SpecDoc con SpecNodeDoc), con paridad estructural frente a spec2viz. Repo: /home/jp/proyectos/SLDB_1/IR; se crean src/specir/visual/{spec_models,loader,validator,ir,compilers,projections}.py y tests/visual/. Límites: no se redefinen modelos de vocabulario de SLDB ni se implementa índice/backend, renderizado, linter ni retirada de spec2viz; src/ no importa spec2viz, solo tests de paridad como oráculo. Depende de IR07 (contrato de cobertura) e IR06 (tipos transversales).

AMBIGUEDADES
1. «según el contrato decidido en la tarea de cobertura»: el contrato no está en el input; obligaría a inventar la decisión YAML-vs-grafo.
2. «salvo que la decisión de la tarea de cobertura diga otra cosa»: idem para errores tipados.
3. «la fila correspondiente de la matriz de cobertura» / «las filas de compiladores y proyecciones de la matriz»: la matriz no figura en files ni references; obligaría a inventar su ruta y esquema.
4. «generados desde proyecciones del grafo del blog»: no se define qué grafo, dónde vive ni cómo obtenerlo; obligaría a inventarlo.
5. «desde la proyección equivalente del grafo»: no se define qué hace equivaler un spec autorado con una proyección; obligaría a inventar el mapeo.
6. «los fixtures y pruebas de compiladores de spec2viz»: no se indica su ubicación ni versión; obligaría a suponerlas.
7. «prueba de imports»: no se especifica el mecanismo; obligaría a elegirlo.

FUTURO
IR07 entrega el contrato de cobertura y la matriz; IR06, los tipos transversales; IR13d extiende __init__.py después. Un humano valida el contrato y aprueba diferencias declaradas. No ejecutar nada.

DRY-RUN
Lecturas: los nueve archivos listados, las tres pills, IR06/IR07 y la matriz cuando exista. Cambios previstos: crear módulos y pruebas citados. Dependencias: IR06, IR07, API pública de SLDB. Validaciones futuras: paridad normalizada, prueba de normalización, errores tipados, proyecciones del blog, no redefinición, prueba de imports.
