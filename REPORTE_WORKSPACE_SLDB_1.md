# Reporte Común del Workspace `SLDB_1` — Knowledge Workspace & Multi-Proyección

**Fecha de corte:** Noviembre 2026  
**Alcance:** Ecosistema `/home/jp/proyectos/SLDB_1` (`sldb`, `deskops`, `pron`, `spec2viz`, `UIs/graph_ui`) y su alineación con `/home/jp/proyectos/softfactory_spec`.

---

## 1. Resumen Ejecutivo (Contexto General)

En `SLDB_1`, toda la información de ingeniería de un repositorio (tareas, decisiones/átomos, contratos de materialización, especificaciones de arquitectura, símbolos de código Python, comandos CLI y relaciones entre ellos) vive dentro de una base de conocimiento verificable en el directorio `.sldb/` de cada repositorio, gobernada por:

1. **`sldb` (`/home/jp/proyectos/SLDB_1/sldb`)**: El motor y store documental/relacional. Valida modelos tipados (vía `pron`), calcula versiones de contenido (`doc_version`), construye el Intermediate Representation (`document_ir`) de documentos Markdown y mantiene el grafo de aristas (`document_edges` / `load_edge_index`).
2. **`deskops` (`/home/jp/proyectos/SLDB_1/deskops`)**: La capa operativa de flujo de trabajo (`Board.md`, ciclo de vida de tareas, gates de cierre `deskops closeout verify|commit`, y orquestación de workers vivos vía `deskops runtime workers` / Herdr).
3. **`spec2viz` (`/home/jp/proyectos/SLDB_1/spec2viz`)**: El motor de resolución de notaciones diagramáticas (`resolve_view`).
4. **`UIs/graph_ui` (`/home/jp/proyectos/SLDB_1/UIs/graph_ui`)**: La capa visual web que proyecta el store `.sldb` y el estado de `deskops` en el navegador.

### ¿Qué problema se resolvió?
Originalmente, la UI existente (`frontends/mindmap/serve.py`, puerto `8088`) estaba diseñada como un editor/canvas de mapas mentales y diagramas con pestañas acopladas (`Documents`, `Draft`, `Models`, `Specs`, `Views`, `Deskops`). Al agregar la vista multiproyección como una 7ª pestaña dentro de ese shell (`/workspace/node`), la experiencia quedaba encajonada en la barra superior antigua y mostraba estructuras crudas en vez de un entorno de lectura e inspección integrado.

Siguiendo el diseño objetivo de [`/home/jp/proyectos/softfactory_spec/SPEC.md`](file:///home/jp/proyectos/softfactory_spec/SPEC.md) y [`/home/jp/proyectos/softfactory_spec/mockup.html`](file:///home/jp/proyectos/softfactory_spec/mockup.html), se implementaron y dejaron conviviendo **dos servidores en paralelo**:

| Servidor | Entrypoint | Puerto por defecto | Propósito |
| :--- | :--- | :---: | :--- |
| **Mindmap UI (Clásico)** | `frontends/mindmap/serve.py` | `8088` | Mantiene intacta la UI existente de edición de mapas, modelos, specs, views, deskops y la pestaña `/workspace/node`. |
| **Knowledge Workspace IDE (Paralelo)** | `frontends/workspace/serve.py` | `8090` | Visor IDE standalone de 3 columnas (`◈ KIMUN · Knowledge Workspace`) conectado 100% a datos reales de `.sldb`, `deskops` y Git. |

---

## 2. Lo que se ha hecho (Entregables Completados)

### 2.1. En `/home/jp/proyectos/SLDB_1/UIs/graph_ui`
1. **Backend de Rutas Multi-proyección (`frontends/mindmap/workspace_routes.py`)**:
   - Resolución canónica `Model:name` sin ambigüedad entre documentos con el mismo slug en distintos modelos (ej. `TaskDoc` vs `PillDoc`).
   - Proyección **Document** (`document_ir` + `payload` + `semantic_tags`).
   - Proyección **Graph** a `1 hop` y `2 hops` sobre aristas reales de `sldb.api.edges.document_edges` en una sola lectura, soportando grafos con ciclos sin duplicar nodos ni aristas.
   - Proyección **Code** confinada a `repo_root`: soporte de referencias `ruta/archivo.py:linea` con ventana de contexto (`fragment_span`), bloqueo de *path traversal* (`..`, rutas absolutas externas), bloqueo de symlinks que escapen del repo (`fuera_del_repo`) y bloqueo *fail-closed* de rutas en `.git` o ignoradas por `.gitignore` (`protegido`).
   - **Resiliencia ante documentos degradados**: Si un documento en disco falla validación de modelo, `workspace_routes.py` usa la API pública `load_edge_index` para preservar la identidad del nodo (`is_degraded: true`) y mantener vivas sus proyecciones de Grafo y Contexto.
   - **Contexto e Integridad**: Cálculo separado de `content_hash` (`doc_version` de SLDB) y `file_revision` (SHA-256 en disco), relaciones entrantes y salientes, y cruce con `idx.problems` del store.

2. **Cierre Canónico de `task-workspace-multiproyeccion-documento-grafo-local-codigo-y-contexto`**:
   - Revisado y aprobado en par con Claude (`w43:p1`).
   - Verificado con `deskops closeout verify` (`ok: true` en los 4 gates declarados: `tests`, `commit`, `document`, `atom|materialization`).
   - Cerrado y archivado mediante `deskops closeout commit` en `desk/tasks/archive/2026-10/task-workspace-multiproyeccion-documento-grafo-local-codigo-y-contexto.md`.

3. **Servidor Paralelo Standalone — Knowledge Workspace IDE (`frontends/workspace/`)**:
   - [`frontends/workspace/serve.py`](file:///home/jp/proyectos/SLDB_1/UIs/graph_ui/frontends/workspace/serve.py):
     - `WorkspaceService`: Enriquecimiento en tiempo real sobre `WorkspaceRoutes` y `DeskRoutes`:
       - Extracción de prosa real por sección (`sections_prose`) desde los archivos Markdown del repositorio usando los spans de línea del IR (`line_start`..`line_end`) o los campos semánticos del payload (`why`, `goal`, `scope`, `implementation_path`, `validation`, `done_when`, `answer`, `what`, `how`, etc.).
       - Inspección de referencias adicionales de código (`spec_path`, `target_identity`, `source_path` + `source_span` y el propio archivo del nodo).
       - Proyección `changes` (Merkle / staleness / impacto a 1–2 saltos + estado `git status --porcelain`).
       - Endpoint `GET /api/workspace/overview` con estadísticas globales del store (`4,571` nodos y `7,820` aristas en `graph_ui/.sldb`), tareas del `Board.md`, workers vivos de `deskops`, historial de subagentes (`runs/subagents/index.jsonl`) e historial Git (`git log`).
   - [`frontends/workspace/index.html`](file:///home/jp/proyectos/SLDB_1/UIs/graph_ui/frontends/workspace/index.html), [`frontends/workspace/app.js`](file:///home/jp/proyectos/SLDB_1/UIs/graph_ui/frontends/workspace/app.js), [`frontends/workspace/styles.css`](file:///home/jp/proyectos/SLDB_1/UIs/graph_ui/frontends/workspace/styles.css):
     - Interfaz de 3 columnas fiel a `softfactory_spec/mockup.html`:
       - **Columna Izquierda:** Navegación por categorías (`Overview`, `Tasks`, `Documents`, `Atoms / Contracts`, `Code / Symbols`, `Graph / Schema`, `Agents`, `Runs`, `Changes`, `History`) + catálogo filtrable de los 4,571 nodos reales del store.
       - **Columna Central:** Pestañas `Document` (con prosa legible y chips clicables `@mention` y `<code>`), `Graph` (canvas visual 2D en SVG con anillos concéntricos de 1 y 2 hops y chips de filtro por modelo y arista), `Code` (visor numerado con resaltado de líneas) y `Changes (Merkle)` (comparación de hashes e impacto en nodos vecinos).
       - **Columna Derecha (`Context`):** Metadatos canónicos, hashes, relaciones entrantes/salientes clicables e integridad.

---

## 3. Estado Actual por Componente en `SLDB_1`

| Componente | Ruta en `SLDB_1` | Estado Actual | Notas / Relación con el Workspace |
| :--- | :--- | :--- | :--- |
| **`UIs/graph_ui`** | `/home/jp/proyectos/SLDB_1/UIs/graph_ui` | En `master`, limpio y con tests en verde | Commits `a1b2b22`, `f16fcd1`, `134a665`, `20e5797`. Servidores `8088` y `8090` activos. |
| **`sldb`** | `/home/jp/proyectos/SLDB_1/sldb` | Operativo; con sugerencia en `desk/inbox/` | Se dejó documentada en [`desk/inbox/20261031-033714-suggestion-resiliencia-en-carga-de-store-ante-documentos-invalidos-y-problems-estructurados.md`](file:///home/jp/proyectos/SLDB_1/sldb/desk/inbox/20261031-033714-suggestion-resiliencia-en-carga-de-store-ante-documentos-invalidos-y-problems-estructurados.md) la mejora para que `documents()` soporte carga parcial resiliente ante un documento inválido y estructure `idx.problems` por nodo. |
| **`deskops`** | `/home/jp/proyectos/SLDB_1/deskops` | Operativo (con paquete `workspace-documental` en curso) | Consumido en modo lectura desde `graph_ui` (`DeskRoutes` y `deskops runtime workers`). |
| **`spec2viz` / `pron`** | `/home/jp/proyectos/SLDB_1/spec2viz`, `pron` | Operativos | Provee esquemas y vistas de notación consumidos por `EditorStore`. |

---

## 4. Cómo Ejecutar y Ver Ambos Servidores en Paralelo

Desde `/home/jp/proyectos/SLDB_1/UIs/graph_ui`:

```bash
# Terminal 1: UI existente de Mindmap (puerto 8088)
PYTHONPATH=$PWD/frontends python frontends/mindmap/serve.py 8088

# Terminal 2: Nuevo visor paralelo Knowledge Workspace IDE (puerto 8090)
PYTHONPATH=$PWD/frontends python frontends/workspace/serve.py 8090
```

- **Visor Paralelo (Knowledge Workspace IDE):**
  - `http://127.0.0.1:8090/`
  - Ejemplo directo sobre una tarea activa:  
    `http://127.0.0.1:8090/?id=TaskDoc:task-vista-changes-arbol-de-hashes-staleness-e-impacto-en-conocimiento`
- **UI Mindmap Existente:**
  - `http://127.0.0.1:8088/`
  - Vista integrada en Mindmap:  
    `http://127.0.0.1:8088/workspace/node?id=TaskDoc:task-vista-changes-arbol-de-hashes-staleness-e-impacto-en-conocimiento`

### Ejecución de Pruebas en `UIs/graph_ui`
```bash
cd /home/jp/proyectos/SLDB_1/UIs/graph_ui
pytest -q tests/test_mindmap_workspace.py tests/test_parallel_workspace_serve.py
node --test tests/mindmap-workspace.test.mjs
pytest -q tests/e2e_mindmap_workspace.py
```

---

## 5. Próximas Tareas Enrutadas en el `Board.md` de `graph_ui`

1. **[`task-vista-changes-arbol-de-hashes-staleness-e-impacto-en-conocimiento`](file:///home/jp/proyectos/SLDB_1/UIs/graph_ui/desk/tasks/task-vista-changes-arbol-de-hashes-staleness-e-impacto-en-conocimiento.md)**:
   - Formalizar los tests específicos (`tests/test_mindmap_changes.py`) y el cálculo de staleness/árbol de hashes ante mutaciones en tiendas temporales reales (el servidor paralelo `frontends/workspace/serve.py` ya incluye la primera versión operativa de la pestaña `Changes (Merkle)` sobre hashes reales y vecindad a 1–2 hops).
2. **[`task-edicion-contextual-de-relaciones-y-campos-con-control-de-concurrencia`](file:///home/jp/proyectos/SLDB_1/UIs/graph_ui/desk/tasks/task-edicion-contextual-de-relaciones-y-campos-con-control-de-concurrencia.md)**:
   - Añadir edición acotada de campos/relaciones desde el panel de contexto con control optimista de concurrencia (`expected_revision` / `409 Conflict`).
