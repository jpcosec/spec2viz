# UX stress-test methodology (spec2viz)

## Qué es

Un UX stress-test es una exploración sistemática de la interfaz CLI desde la perspectiva de un usuario. No busca "encuentra bugs en el código" sino "encuentra dónde la experiencia se rompe, confunde o contradice el modelo mental que el usuario construyó".

## Principios

1. **Read-only.** No se edita ningún archivo. No se modifica el sistema bajo test. Solo se ejecutan comandos y se observa.
2. **El usuario no sabe lo que sabe el desarrollador.** El test asume que el usuario no leyó el código fuente. Solo conoce `--help`, la documentación superficial, y su intuición.
3. **Modelo mental primero.** Cada test se basa en una `use-case` narrativa (UC-XX) que describe qué quiere lograr el usuario. El test verifica si el sistema lo deja lograr eso sin fricción.
4. **Anchor en atoms.** Si `atom-spec2viz.md` dice "spec2viz transform semantic specs into diagrams", el test verifica: ¿la pipeline validate → compile → render es clara? ¿O hay gaps entre el modelo mental y los comandos?
5. **Fricción es el hallazgo.** Un error con traceback es un hallazgo. Un comando que existe pero se comporta distinto a lo esperado es un hallazgo. Un output silencioso donde debería haber feedback es un hallazgo. Una inconsistencia entre renderers es un hallazgo.

## Estructura de un test

Cada test vive en `desk/drawer/stress-tests/st-XX-nombre.md` y contiene:

```markdown
# ST-XX: Nombre

**Basado en:** UC-XX

## Script

Secuencia de comandos CLI que el usuario ejecuta. Textual, uno por línea.
Incluye casos felices, casos borde, y casos de error.

## Puntos de estrés

Tabla: por cada paso del script, qué observar.
No es "funciona o no funciona". Es "el output es claro?",
"el error sugiere qué hacer?", "el usuario queda en un estado conocido?".

## Modos de fracaso

Lista de formas en que la experiencia se rompe.
```

## Cómo se ejecuta

1. Elegir un ST basado en un UC
2. Preparar setup si hace falta (YAML spec files de prueba)
3. Ejecutar el script manualmente o mediante subagente
4. **Observar**, no juzgar. Anotar outputs textuales, exit codes, comportamientos sorprendentes
5. Escribir hallazgos en `findings/round-NN-descripcion.md`

## Qué observar en cada comando

| Dimensión | Preguntas |
|---|---|
| **Discoverability** | ¿El comando aparece en `--help`? ¿Su nombre es obvio? |
| **Error messages** | ¿El error es para un humano o para un desarrollador? ¿Muestra traceback interno? ¿Sugiere qué hacer? |
| **Exit codes** | ¿0 para éxito, 1 para error manejado, 2 para argparse? |
| **Silent failures** | ¿Hay comandos que devuelven 0 sin output cuando deberían haber fallado? |
| **Consistency** | ¿Validate/render/schema comparten convenciones de flags y output? |
| **Naming** | ¿`--renderer` y `--backend` hacen lo mismo? (son alias) |
| **State** | ¿El comando produce archivos? ¿En qué directorio? ¿Overwrite o append? |
| **Output** | ¿El output de render es correcto sintácticamente? ¿PlantUML/Mermaid válido? |
| **Edge cases** | ¿YAMLs malformados, diagram types inválidos, schemas inconsistentes, paths con espacios? |
| **CI readiness** | ¿Se puede pipear? ¿Hay `--format json` en validate? ¿Colores ANSI? |

## Cobertura esperada

Cada superficie del CLI debe tener al menos un ST:

| Superficie | ST asociado |
|---|---|
| `spec2viz validate` | ST-validate |
| `spec2viz render` | ST-render |
| `spec2viz schema` | ST-schema |
| Validate con cada diagram type | ST-validate-types |
| Render con cada diagram type + renderer | ST-render-combos |
| Render multiple files | ST-render-multi |
| PlantUML output correctness | ST-plantuml |
| Mermaid output correctness | ST-mermaid |
| Vega output correctness | ST-vega |
| Python API | ST-api |
| Edge cases (YAML malformed, missing files, unknown types) | ST-edge-cases |
| Reflection/enforcement pipeline | ST-reflection |
| Examples rendering | ST-examples |

## Lo que NO es un UX stress-test

- No es un test unitario
- No es un test de integración
- No es un test de regresión
- No es una auditoría de seguridad
- No es una revisión de código
