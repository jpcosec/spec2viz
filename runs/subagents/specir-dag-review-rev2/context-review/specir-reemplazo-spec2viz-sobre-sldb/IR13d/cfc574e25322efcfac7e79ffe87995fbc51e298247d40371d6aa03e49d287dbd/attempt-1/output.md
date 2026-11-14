REFORMULACION
Nodo ejecutable de entrega (`kind: code`), no agregado. Propósito: que specIR exponga la capa visual de spec2viz mediante un comando, una API Python pública y una habilidad de agente, con tabla de correspondencia. Resultado: entradas públicas equivalentes, pruebas que las invocan y filas CLI/API/habilidad de la matriz con condición de retiro cumplida. Repo: specIR. Límites: no implementa capacidades (IR12, IR13a/b/c), no instala la habilidad en otros repos ni migra consumidores.

AMBIGUEDADES
1. “equivalentes de todos los comandos y subgrupos de spec2viz” no fija nombre del ejecutable, sintaxis, opciones, salida, códigos de salida ni semántica de alias. Obligaría a inventar el contrato del CLI.
2. “API Python pública equivalente a la que exporta el paquete spec2viz” no enumera símbolos, firmas, módulos, tipos ni errores. Obligaría a inventar la superficie pública.
3. “habilidad de agente que reemplaza a la de uso de spec2viz” no define formato, disparadores, contenido ni grado de conservación. Obligaría a inventar el contrato de la skill.
4. “Las pruebas anteriores pasan” y “las filas de CLI, API Python y habilidad de la matriz de cobertura” no identifican suite base, filas ni condición de retiro. Obligaría a inventar el baseline y los criterios.
5. “Cada comando y subgrupo que lista la ayuda de spec2viz” no fija versión ni fuente de esa ayuda. Obligaría a inventar la autoridad y versión.
6. “entorno limpio” no define Python, SO, gestor ni red. Obligaría a inventar el entorno de instalación.

DRY-RUN
Un ejecutor leería la ayuda y API exportada de spec2viz, la matriz de cobertura, tests y fixtures, el CLI y módulos visuales de specIR y la skill existente. Crearía o ajustaría `src/specir/cli.py`, `src/specir/visual/__init__.py`, `skills/use-specir/SKILL.md`, `docs/spec2viz/correspondencia-cli.md` y tests visuales. Depende de IR13a, IR13b, IR13c e IR12. Validaría tabla comando a comando, pruebas de API portadas, extracción de comandos de la skill contra ayuda, e instalación limpia sin spec2viz. No ejecuta nada.

FUTURO
IR13 consume la tabla y las filas de cobertura para el gate de retiro; los dueños de otros repos deciden instalar la skill y migrar consumidores; el dueño de spec2viz decide archivarlo. Las capacidades las producen IR13a/b/c e IR12.
