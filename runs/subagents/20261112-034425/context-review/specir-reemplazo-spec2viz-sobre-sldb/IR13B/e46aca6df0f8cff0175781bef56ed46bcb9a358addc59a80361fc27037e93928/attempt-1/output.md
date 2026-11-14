REFORMULACION
Propósito: que specIR cubra catálogos, anotaciones y emparejamiento de átomos de spec2viz. Resultado: `catalog.py`, `catalog_serve.py`, `atoms.py` y sus pruebas; registro `vistas.yml`, construcción/sincronización/validación de catálogo, servidor local con autoguardado, matching explícito/difuso y cobertura por vista. Repo: `specIR`. Límites: dentro, lo listado en el alcance; fuera, sincronización de specs individuales, notaciones/paletas, CLI y migración de consumidores; depende de IR13A e IR12. Es un nodo de entrega de código, no un agregado.

AMBIGUEDADES
1. “stores jerárquicos de diagramas”: no define esquema, claves ni jerarquía; obligaría a inventar el layout de almacenamiento.
2. “servidor local con autoguardado de anotaciones”: no fija disparador, formato, concurrencia ni resolución de conflictos; obligaría a inventar persistencia y política de guardado.
3. “emparejamiento de átomos con elementos de diagrama (explícito y difuso)”: no define normalización, umbral ni desempate; obligaría a inventar el algoritmo difuso.
4. “cobertura por vista”: no define métrica, denominador ni agregación; obligaría a inventar el cálculo.
5. “los mismos errores tipados que spec2viz”: no enumera tipos ni códigos; obligaría a inventar taxonomía si los fixtures no la fijan.
6. “no escribe nada si alguna vista falla”: no aclara si exige transacción, temporal y reemplazo, o validación previa; obligaría a inventar la semántica atómica.

DRY-RUN
Lecturas: contrato IR13B, filas de catálogo/átomos de la matriz, fixtures de spec2viz, `vistas.yml` y APIs entregadas por IR13A/IR12. Cambios previstos: crear o ajustar solo los seis archivos de `output_scope`. Dependencias: IR13A para sincronización/store y IR12 para renderers/recursos. Validaciones futuras: pruebas de paridad de errores, catálogo y átomos; no escritura ante vista fallida; recarga de anotación; catálogo sin recursos externos faltantes; ausencia de import de spec2viz. Sin ejecutar nada.

FUTURO
IR13A e IR12 producen piezas y fixtures consumidos. IR13D expone CLI/API. IR13 audita matriz y consumidores. Un humano decide migraciones, retiro y archivo de spec2viz.
