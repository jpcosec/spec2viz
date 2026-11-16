# REFORMULACION

**Propósito:** completar la migración de spec2viz a specIR en su cara de consumo: que specIR tenga un comando, una API Python pública y una habilidad de agente equivalentes a los de spec2viz.

**Resultado:** `src/specir/cli.py` con todos los comandos/subgrupos (diagram, notation, palette, catalog; alias render, validate, lint, schema, build; about); exportaciones públicas añadidas en `src/specir/visual/__init__.py` (sin recrear ni borrar las existentes); `skills/use-specir/SKILL.md`; `docs/spec2viz/correspondencia-cli.md` con tabla comando por comando; pruebas portadas en `tests/visual/` (CLI, API, empaquetado).

**Repo:** el propio monorepo, workspace `desk`.

**Límites:** fuera implementar capacidades (vienen de IR11/IR12/IR13a/IR13b/IR13c), instalar la habilidad en otros repos y migrar consumidores.

# AMBIGUEDADES

1. "API Python pública equivalente a la que exporta el paquete spec2viz": el input no enumera esos símbolos; obligaría a inventar la lista de exportaciones en vez de derivarla de spec2viz.
2. "habilidad de agente que reemplaza a la de uso de spec2viz": no se fija formato, secciones ni nivel de detalle; obligaría a inventar su estructura.
3. "Cada comando y subgrupo que lista la ayuda de spec2viz": la fuente de verdad (ayuda de spec2viz) no está en el input; obligaría a inventar el inventario de comandos.
4. "las filas de CLI, API Python y habilidad de la matriz de cobertura": no se indica dónde vive ni su esquema; obligaría a inventar ubicación y formato.
5. "se instala en un entorno limpio": no se define el entorno; obligaría a inventar el procedimiento de verificación.

# DRY-RUN

**Lecturas:** `src/specir/cli.py`, `src/specir/visual/__init__.py`, `skills/use-specir/SKILL.md`, `docs/spec2viz/correspondencia-cli.md`, `tests/visual/test_cli.py|test_api.py|test_packaging.py` y las tres pills. Referencia externa: ayuda y `__all__` de spec2viz.

**Cambios previstos:** crear/editar los cinco archivos listados y portar pruebas de CLI, API y empaquetado.

**Dependencias:** IR13a, IR13b, IR12 (cadena IR11) ya entregadas; spec2viz disponible solo como referencia.

**Validaciones futuras:** tabla completa con prueba por equivalente; pruebas de API portadas en verde; prueba que extrae comandos de la habilidad y los invoca con `--help`; instalación en entorno limpio sin spec2viz.

# FUTURO

Un humano decide las ambigüedades 1–5 (lista de API, formato de habilidad, ubicación de la matriz, definición de entorno limpio). Otro nodo retira spec2viz y migra consumidores.
