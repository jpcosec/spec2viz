# Drawer Board

This board routes deferred work only. Todo lo que aparece aquí queda diferido: ninguna candidata está activa, ninguna figura en `desk/tasks/Board.md` y ninguna tiene `task_type` asignado.

Propuesta para revisión, 2026-11-11. Backlog inicial de specIR: repo periférico sobre SLDB, hoy MCP y modelado semántico, más adelante la capa visual de spec2viz hasta poder retirarlo.

## Remaining

### Rama MCP y modelado

- `task-ir01-auditor-a-de-la-api-p-blica-de-sldb-frente-a-la-superficie-mcp` — IR01 Auditoría de la API pública de SLDB frente a la superficie MCP. Matriz de qué necesita el MCP y si la API pública de SLDB ya lo ofrece. Depende de: nada.
- `task-ir02-decisi-n-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp` — IR02 Decisión: contrato de escritura y nivel de mutabilidad del MCP. Qué es una propuesta de cambio, qué precondición protege la aplicación, dónde se declara el nivel de escritura, si existe deshacer. Depende de: IR01.
- `task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real` — IR03 Servidor MCP de solo lectura sobre un store SLDB real. Descubrir modelos, leer documentos, recorrer relaciones y resolver vistas. Depende de: IR01.
- `task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar` — IR04 Escritura validada por MCP: proponer, validar, aplicar. Documentos, aristas, tipos de relación y reglas como datos del store; el MCP no edita clases Python. Depende de: IR02, IR03.
- `task-ir05-decisi-n-procedencia-y-divergencia-entre-c-digo-y-modelo` — IR05 Decisión: procedencia y divergencia entre código y modelo. Taxonomía canónica de procedencia y regla para cuando el código fuente cambia. Depende de: IR01.
- `task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog` — IR06 Tipos de dominio transversales y cadena de prueba del blog. Modelos, tipos de relación y reglas de specIR, y la cadena de publicar un post recorrible por MCP. Depende de: IR04, IR05.
- `task-ir08-extractor-estatico-django-drf-y-sql` — IR08 Extractor estático Django/DRF y SQL. Rutas, serializers, modelos y esquema SQL al grafo, con archivo, línea y hash de origen. Depende de: IR05, IR06.
- `task-ir09-extractor-estatico-react-tsx-y-contratos-api` — IR09 Extractor estático React/TSX y contratos de API. Componentes, acciones, estados y llamadas a la API, vinculados a operaciones de backend; lo dinámico se marca, no se afirma. Depende de: IR05, IR06.
- `task-ir10-reglas-semanticas-y-analisis-de-impacto` — IR10 Reglas semánticas y análisis de impacto. Reglas que detectan cadenas interfaz, API, operación y datos rotas, y una operación de impacto con evidencia y severidad; no propone parches. Depende de: IR06, IR08, IR09.

### Rama cobertura y retiro de spec2viz

- `task-ir07-matriz-de-cobertura-de-spec2viz-para-su-retiro` — IR07 Cobertura completa de spec2viz: matriz, fuente de verdad del diagrama y gate de retiro. Una fila por capacidad con modo y condición de retiro; decisión sobre el YAML de spec frente al grafo. No declara nada como migrado. Depende de: IR03, IR06.
- `task-ir11-compiladores-y-proyecciones-de-spec2viz` — IR11 Compiladores y proyecciones de spec2viz. Modelos de spec, compiladores de todos los tipos y materialización de proyecciones, con paridad por fixtures. Depende de: IR07, IR06.
- `task-ir12-renderers-linter-y-recursos-estaticos-de-spec2viz` — IR12 Renderers, linter y recursos estáticos de spec2viz. Todos los formatos de salida, linter de Mermaid, JSON Schema y recursos empaquetados. Depende de: IR11.
- `task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz` — IR13 Sync, generación, catálogos, consumidores y retiro de spec2viz. Sincronización al store, generación de specs, catálogos, notaciones, migración de graph_ui y deskops, y gate final de retiro. Depende de: IR07, IR11, IR12.

## Dependencias

```text
IR01 ─┬─ IR02 ─┐
      ├─ IR03 ─┴─ IR04 ─┐
      └─ IR05 ──────────┴─ IR06 ─┬─ IR08 ─┐
                                 ├─ IR09 ─┴─ IR10
                                 ├─ IR07 (también IR03) ─┬─ IR11 (también IR06) ── IR12 ─┐
                                 │                       └──────────────────────────────┴─ IR13
```

La fuente de las dependencias es el campo `depends_on` de cada candidata, con ids completos; este dibujo es solo un resumen.

## Rule

Nothing in `desk/drawer/` executes. Cuando una candidata esté lista, se autora una tarea completa con `deskops add task --from-drawer <item>`, momento en que se le asigna su tipo; la candidata se retira después con `deskops drawer remove`. No hay promoción directa del drawer a tarea activa. El store no rastrea `desk/drawer/`: estos archivos se resuelven en disco.
