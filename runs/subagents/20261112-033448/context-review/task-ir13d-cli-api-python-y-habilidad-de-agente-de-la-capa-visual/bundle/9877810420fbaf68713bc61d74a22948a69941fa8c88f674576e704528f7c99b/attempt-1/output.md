## REFORMULACION

**Propósito:** completar la migración de la capa visual de spec2viz a specIR exponiendo sus superficies públicas: comando, API Python y habilidad de agente.

**Resultado:** un CLI de specIR con equivalentes de comandos/subgrupos y alias de spec2viz; una API pública en `src/specir/visual/__init__.py`; `skills/use-specir/SKILL.md`; la tabla `docs/spec2viz/correspondencia-cli.md`; y pruebas portadas en `tests/visual/`.

**Repo:** specIR, bajo `src/specir/`, `skills/`, `docs/` y `tests/`.

**Límites:** no implementar capacidades (vienen de compiladores, renderers, IR13a, IR13b e IR13c); no instalar la habilidad en otros repos; no migrar consumidores; solo extender `src/specir/visual/__init__.py`, sin recrearlo ni quitar exportaciones; sin mocks ni datos fabricados; sin depender de `spec2viz` ni de módulos internos de SLDB.

## AMBIGUEDADES

1. «equivalentes de todos los comandos y subgrupos de spec2viz (diagram, notation, palette, catalog, y los alias de primer nivel render, validate, lint, schema y build, y about)»: la enumeración parece exhaustiva pero dice «todos»; obligaría a inventar si faltan comandos de la ayuda de spec2viz.
2. «API Python pública equivalente a la que exporta el paquete spec2viz»: no enumera símbolos ni módulos; obligaría a inventar la superficie exportada.
3. «habilidad de agente que reemplaza a la de uso de spec2viz»: no fija contenido, fuente ni criterios; obligaría a inventar sus instrucciones.
4. «portando a tests/visual/ las pruebas de spec2viz de CLI, API y empaquetado»: no da rutas ni nombres; obligaría a inventar qué pruebas concretas portar y qué cubre «empaquetado».
5. «las filas de CLI, API Python y habilidad de la matriz de cobertura tienen su condición de retiro cumplida»: no cita la matriz ni el criterio; obligaría a inventar la condición de retiro por fila.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, rituales, pills, átomos; en solo lectura, ayuda/API/habilidad/pruebas de spec2viz y `docs/spec2viz/matriz-de-cobertura.md`; estado actual de `cli.py`, `visual/__init__.py` y pruebas. Cambios previstos: añadir comandos/alias en `cli.py`, exportaciones públicas, redactar la habilidad, la tabla de correspondencia y portar pruebas. Dependencias: capacidades de IR11/IR12/IR13a-c; propiedad de `visual/__init__.py`. Validaciones futuras: ejecutar `tests/visual/`, invocar cada equivalente, extraer comandos de la habilidad y comprobarlos con ayuda, instalar en entorno limpio sin spec2viz y verificar importaciones permitidas.

## FUTURO

IR13a-c y los renderers entregan las capacidades subyacentes; el ritual de fase integra la capa; un humano o el Board evalúa el gate de retiro de spec2viz; otro nodo decidirá la instalación de la habilidad en repos consumidores.
