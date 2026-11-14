REFORMULACION
El nodo (task.code ejecutable) debe completar la migración de las superficies de consumo de spec2viz a specIR: CLI, API Python y habilidad de agente. Resultado: comando specIR con equivalentes de todos los comandos/subgrupos de spec2viz (diagram, notation, palette, catalog, alias render/validate/lint/schema/build, about), API pública equivalente, skills/use-specir/SKILL.md, docs/spec2viz/correspondencia-cli.md y pruebas portadas en tests/visual/. Repo: paths relativos a /home/jp/proyectos/SLDB_1/IR; el input no lo nombra. Límites: no implementar capacidades (IR13a/b/c y renderers), no instalar la habilidad ni migrar consumidores; extender src/specir/visual/__init__.py sin recrearlo ni quitar exportaciones (lo crea IR11).

AMBIGUEDADES
1. “API Python pública equivalente a la que exporta el paquete spec2viz”: no enumera símbolos, firmas ni criterio; obligaría a inventarlos.
2. “portando a tests/visual/ las pruebas de spec2viz de CLI, API y empaquetado”: no indica ubicación, versión ni selección; obligaría a inventar fuente y conjunto.
3. “Cada comando y subgrupo que lista la ayuda de spec2viz”: no se aporta esa ayuda ni versión; obligaría a inventar el inventario.
4. “una habilidad de agente que reemplaza a la de uso de spec2viz”: no define contenido, ubicación de la original ni criterio; obligaría a inventarlos.
5. “las filas de CLI, API Python y habilidad de la matriz de cobertura”: matriz no incluida; obligaría a inventar formato y condición de retiro.
6. “entorno limpio”: no se especifica; obligaría a inventar su definición.

DRY-RUN
Un ejecutor futuro leería el documento, pills, archivos listados, salidas de IR13a/b/c/IR12 y API pública de SLDB. Cambios previstos: editar cli.py; extender __init__.py; crear SKILL.md, correspondencia-cli.md y tests. Dependencias: capacidades previas, __init__ de IR11, pruebas/ayuda de spec2viz, prohibición de mocks. Validaciones futuras: cobertura de ayuda, pruebas API portadas, comandos de la skill extraídos e invocados, instalación limpia sin spec2viz. Sin ejecutar.

FUTURO
IR13a/b/c/IR12 producen capacidades y paridad; IR11 produce __init__. Un humano decide la aceptación final y el retiro de filas de la matriz; otro nodo puede aportar la superficie pública/pruebas de spec2viz.
