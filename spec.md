# Diagram-as-Data Spec v0.1

## 1. Objetivo

Definir un sistema donde cada diagrama arquitectónico se representa como un archivo YAML independiente, legible por humanos y por LLMs, y luego se renderiza a formatos gráficos como PlantUML, Mermaid, D2, SVG o PNG.

La idea central es:

```text
YAML = fuente semántica del diagrama
PUML/Mermaid/D2 = artefacto textual renderizable
SVG/PNG = artefacto visual final
```

El YAML es la fuente de verdad.
El PUML no se edita a mano salvo debugging.

---

# 2. Principios

## 2.1 Un YAML por grafo

Cada diagrama debe tener su propio archivo YAML.

Ejemplo:

```text
diagrams/
  component.quotation.yml
  sequence.create-quotation.yml
  state.quotation.yml
  activity.validation.yml
  matrix.quotation-view.yml
```

No se busca tener un mega YAML universal para todo el sistema.

---

## 2.2 El YAML describe intención, no layout

El YAML debe describir:

```text
qué entidades existen
cómo se relacionan
qué tipo de diagrama es
qué semántica tienen sus relaciones
```

No debería describir principalmente:

```text
posición X/Y
tamaño exacto de cajas
estilo visual de bajo nivel
```

Eso queda para templates/renderers.

---

## 2.3 El LLM opera sobre YAML

El LLM debe leer, modificar, validar y generar YAML.

No debería operar principalmente sobre PUML, porque PUML mezcla semántica con sintaxis de render.

---

## 2.4 Los renderers generan artefactos

Desde el YAML se pueden generar:

```text
.puml
.mmd
.d2
.svg
.png
```

Ejemplo:

```text
sequence.create-quotation.yml
  -> sequence.create-quotation.puml
  -> sequence.create-quotation.svg
```

---

# 3. Pipeline

```text
YAML diagram file
    ↓
YAML parser
    ↓
schema validator
    ↓
semantic validator
    ↓
renderer selector
    ↓
template / custom renderer
    ↓
diagram artifact
    ↓
image renderer
```

Ejemplo CLI:

```bash
diagram-render diagrams/sequence.create-quotation.yml --out build/
```

Salida esperada:

```text
build/
  sequence.create-quotation.puml
  sequence.create-quotation.svg
```

---

# 4. Estructura común de cada YAML

Todo archivo debe tener esta forma base:

```yaml
id: sequence.create-quotation
title: Create Quotation
type: sequence
version: 0.1

metadata:
  author: optional
  description: optional

style:
  theme: default

data:
  {}
```

Campos obligatorios:

```yaml
id: string
title: string
type: string
version: string
data: object
```

Campos opcionales:

```yaml
metadata: object
style: object
```

---

# 5. Tipos de diagramas soportados

Mínimo inicial:

```yaml
type: component
type: sequence
type: state
type: activity
type: deployment
type: component_view_matrix
```

Donde:

```text
component              -> UML component diagram
sequence               -> UML sequence diagram
state                  -> UML state machine
activity               -> UML activity diagram
deployment             -> UML deployment diagram
component_view_matrix  -> matriz bi-jerárquica custom
```

---

# 6. Component Diagram YAML

## 6.1 Propósito

Representar componentes, contenedores, boundaries y dependencias.

## 6.2 Schema conceptual

```yaml
id: component.quotation
title: Quotation Flow - Components
type: component
version: 0.1

data:
  nodes:
    QuotationFlow:
      label: QuotationFlow
      kind: core
      contains:
        - ClientSelection
        - Catalog
        - Basket
        - PricingEngine
        - ValidationSummary

    Store:
      kind: boundary

    Persistence:
      kind: boundary

  edges:
    - from: QuotationFlow
      to: Store
      relation: reads_writes
      label: reads/writes

    - from: QuotationFlow
      to: Persistence
      relation: persists
      label: persists
```

## 6.3 Reglas

Cada `node` debe tener ID único.

Cada `edge.from` y `edge.to` debe apuntar a un nodo existente.

`contains` define jerarquía conceptual.

`relation` debe ser semántico, no solo visual.

Ejemplos válidos:

```yaml
relation: calls
relation: reads
relation: writes
relation: persists
relation: publishes
relation: subscribes
relation: validates
relation: computes
relation: exports
```

---

# 7. Sequence Diagram YAML

## 7.1 Propósito

Representar interacción ordenada entre actores/componentes.

## 7.2 Schema conceptual

```yaml
id: sequence.create-quotation
title: Create Quotation
type: sequence
version: 0.1

data:
  participants:
    - id: User
      kind: actor

    - id: QuotationFlow
      kind: component

    - id: Store
      kind: boundary

    - id: PricingEngine
      kind: decision_engine

  messages:
    - from: User
      to: QuotationFlow
      message: open quotation flow

    - from: QuotationFlow
      to: Store
      message: load catalog

    - from: User
      to: QuotationFlow
      message: add item

    - from: QuotationFlow
      to: PricingEngine
      message: calculate price

    - from: QuotationFlow
      to: Persistence
      message: save draft
```

## 7.3 Reglas

Los participantes deben existir antes de ser usados.

Los mensajes son ordenados.

Cada mensaje debe tener:

```yaml
from
to
message
```

Opcionales:

```yaml
kind: sync | async | return
condition: string
group: string
```

Ejemplo:

```yaml
- from: QuotationFlow
  to: PricingEngine
  message: calculate price
  kind: sync
  condition: basket has items
```

---

# 8. State Diagram YAML

## 8.1 Propósito

Representar estados y transiciones de una entidad.

## 8.2 Schema conceptual

```yaml
id: state.quotation
title: Quotation State Machine
type: state
version: 0.1

data:
  entity: Quotation
  initial: browsing

  states:
    - browsing
    - client_selected
    - basket_editing
    - validating
    - completed

  transitions:
    - from: browsing
      to: client_selected
      on: select_client

    - from: client_selected
      to: basket_editing
      on: start_basket

    - from: basket_editing
      to: validating
      on: validate

    - from: validating
      to: completed
      on: complete
```

## 8.3 Reglas

`initial` debe existir en `states`.

Cada transición debe apuntar a estados existentes.

Cada transición debe tener:

```yaml
from
to
on
```

Opcionales:

```yaml
guard: string
action: string
```

Ejemplo:

```yaml
- from: validating
  to: completed
  on: complete
  guard: all validations passed
  action: persist final quotation
```

---

# 9. Activity Diagram YAML

## 9.1 Propósito

Representar flujo procedimental o workflow.

## 9.2 Schema conceptual

```yaml
id: activity.validation
title: Validate Quotation
type: activity
version: 0.1

data:
  start: load_basket

  steps:
    load_basket:
      label: Load basket
      next: calculate_price

    calculate_price:
      label: Calculate price
      next: check_validity

    check_validity:
      label: Is quotation valid?
      kind: decision
      branches:
        yes: export_summary
        no: show_errors

    export_summary:
      label: Export summary
      next: end

    show_errors:
      label: Show validation errors
      next: end

  end: end
```

## 9.3 Reglas

Cada step debe tener ID único.

`next` debe apuntar a un step existente o a `end`.

Un step `kind: decision` debe tener `branches`.

---

# 10. Deployment Diagram YAML

## 10.1 Propósito

Representar runtime, nodos, servicios y artefactos desplegados.

## 10.2 Schema conceptual

```yaml
id: deployment.quotation
title: Quotation Runtime Deployment
type: deployment
version: 0.1

data:
  nodes:
    browser:
      label: Browser
      kind: client
      contains:
        - quotation_ui

    app_server:
      label: App Server
      kind: server
      contains:
        - quotation_api

    database:
      label: Database
      kind: database
      contains:
        - quotation_store

  artifacts:
    quotation_ui:
      label: Quotation UI
      kind: frontend

    quotation_api:
      label: Quotation API
      kind: backend

    quotation_store:
      label: Quotation Store
      kind: database_schema

  connections:
    - from: quotation_ui
      to: quotation_api
      protocol: HTTPS

    - from: quotation_api
      to: quotation_store
      protocol: SQL
```

---

# 11. Component View Matrix YAML

## 11.1 Propósito

El **Component View Matrix** responde a una pregunta arquitectónica específica:

> **"¿En qué vista/etapa participa cada componente del sistema?"**

Es una matriz bi-jerárquica:

```
                    Vista A                    Vista B
                 ┌──────────────┐          ┌──────────────┐
Componente 1     │ ████████████ │          │              │
Componente 2     │      ████████│          │ ████████████ │
Componente 3     │ ████         │          │ ██████████   │
                 └──────────────┘          └──────────────┘
                   browse  edit  save        setup  config
```

- **Y axis**: jerarquía de componentes (con nesting)
- **X axis**: vistas, cada una con etapas ordenadas
- **Barras**: span de participación de cada componente

## 11.2 Cuándo usarlo

✅ **Arquitectura de microservicios o módulos** — qué servicio responde a qué pantalla

✅ **Bounded contexts** — delimitar qué dominio opera en qué flujo

✅ **Refactoring** — identificar componentes huérfanos o demasiado acoplados

✅ **Tech lead planning** — mapear ownership de features

## 11.3 Cuándo NO usarlo

❌ **Componentes UI atómicos** (Button, Input, Card) → usar component diagram simple o tabla

❌ **Relaciones entre componentes** (API calls, data flow) → usar component diagram o sequence diagram

❌ **Flujos de usuario** (secuencia de acciones) → usar sequence diagram o activity diagram

❌ **Estados de una entidad** → usar state diagram

## 11.4 Kinds disponibles

Cada componente tiene un `kind` semántico:

| kind | Uso típico | Color sugerido |
|------|-----------|---------------|
| `core` | Lógica de negocio principal | Naranja |
| `boundary` | Interfaces, adapters, gateways | Azul |
| `service` | Microservicios, workers | Gris |
| `database` | Persistencia | Verde |
| `ui` | Componentes de interfaz pesados | Gris claro |
| `external_system` | Integraciones externas | Púrpura |
| `decision_engine` | Reglas, validación | Rosa |

## 11.5 Schema conceptual

```yaml
id: matrix.quotation-view
title: Quotation Flow - Component View Matrix
type: component_view_matrix
version: 0.1

data:
  views:
    - id: quotation
      label: Quotation View
      stages:
        - id: browse
          label: browse
        - id: client
          label: client
        - id: basket
          label: basket
        - id: validation
          label: validation
        - id: completed
          label: completed
    - id: admin
      label: Administration Panel
      stages:
        - id: setup
          label: setup
        - id: config
          label: config
        - id: users
          label: users
        - id: logs
          label: logs

  components:
    - name: QuotationSystem
      kind: core
      stages:
        quotation: [browse, client, basket, validation, completed]
        admin: [setup, config, users, logs]
      children:
        - name: Frontend
          kind: boundary
          stages:
            quotation: [browse, client, basket]
          children:
            - name: WebUI
              kind: ui
              stages:
                quotation: [browse, client, basket]
            - name: MobileApp
              kind: ui
              stages:
                quotation: [browse, client]
        - name: Backend
          kind: core
          stages:
            quotation: [basket, validation, completed]
            admin: [config, users, logs]
          children:
            - name: OrderService
              kind: service
              stages:
                quotation: [basket, validation, completed]
            - name: AdminService
              kind: service
              stages:
                admin: [setup, config, users, logs]
            - name: Database
              kind: database
              stages:
                quotation: [completed]
```

## 11.6 Estructura de views

```yaml
views:
  - id: quotation          # ID único (snake_case)
    label: Quotation View  # Label para mostrar
    stages:
      - id: browse         # ID del stage
        label: browse      # Label para mostrar
      - id: client
        label: client
```

## 11.7 Estructura de components

```yaml
components:
  - name: OrderService     # ID único (PascalCase)
    kind: service          # categoría semántica
    label: Order Service   # opcional: label custom
    stages:                # en qué etapas participa
      quotation: [basket, validation, completed]
      admin: []            # vacío = no participa
    children: []           # componentes anidados
```

**Nota:** `name` debe ser único a nivel global (no solo por nivel).

## 11.8 Reglas

1. Cada view debe tener stages ordenadas (el renderer las muestra en orden)
2. Cada `stages[view]` en un component debe referenciar stages existentes
3. Componentes pueden participar en múltiples views
4. `children` heredan contexto pero declaran sus propias etapas
5. Un componente sin stages en una view = no aparece en esa columna

## 11.9 Anti-patrones

**❌ Matrix de componentes UI atómicos:**

```yaml
# ANTI-PATRÓN: esto no es lo que el matrix está diseñado para
components:
  - name: Button
    kind: ui
    stages:
      v1: [list, detail]
  - name: Input
    kind: ui
    stages:
      v1: [detail]
```

→ **Solución:** Usar una tabla markdown o un heatmap simple Vega

**❌ Matrix para flujos de datos:**

```yaml
# ANTI-PATRÓN: esto mezcla concerns
components:
  - name: UserService
    stages:
      auth: [login]
  - name: calls API
    # esto no es un componente
```

→ **Solución:** Usar sequence diagram para flujos, component diagram para relaciones

**❌ Jerarquía plana sin sentido:**

```yaml
# ANTI-PATRÓN: todos al mismo nivel sin jerarquía
components:
  - name: ComponentA
  - name: ComponentB
  - name: ComponentC
```

→ **Solución:** Si no hay jerarquía, usar component diagram simple

## 11.10 Comparación rápida

| Pregunta | Diagrama a usar |
|----------|-----------------|
| ¿Qué componentes existen? | `component` |
| ¿Qué componentes participan en qué flujos? | `component_view_matrix` |
| ¿Cómo se comunican los componentes? | `component` + `sequence` |
| ¿Qué componentes UI necesito? | Tabla / heatmap simple |
| ¿Qué estados tiene una entidad? | `state` |
| ¿Cuál es el flujo de un proceso? | `activity` |

## 11.11 Ejemplo completo de salida Vega

Ver `examples/matrix/example.vega.json` para el JSON generado.

---

# 12. Tipos visuales estándar

Los diagramas pueden usar `kind` para estilo semántico.

Valores recomendados:

```yaml
kind: core
kind: boundary
kind: decision_engine
kind: actor
kind: external_system
kind: database
kind: service
kind: ui
kind: api
```

Estilo sugerido:

```yaml
style:
  kinds:
    core:
      color: "#F59E0B"

    boundary:
      color: "#60A5FA"

    decision_engine:
      color: "#EC4899"

    external_system:
      color: "#A78BFA"

    database:
      color: "#10B981"
```

---

# 13. Reglas para LLM

## 13.1 El LLM debe preferir YAML

Cuando se le pida modificar un diagrama, el LLM debe modificar el YAML.

No debe editar directamente el PUML salvo que el usuario lo pida explícitamente.

---

## 13.2 El LLM no debe inventar semántica

Si una relación no está clara, debe usar una relación genérica:

```yaml
relation: uses
```

En vez de inventar algo más fuerte como:

```yaml
relation: owns
relation: persists
relation: validates
```

---

## 13.3 El LLM debe preservar IDs

Si modifica labels, no debe cambiar IDs innecesariamente.

Correcto:

```yaml
PricingEngine:
  label: Pricing Engine
```

Incorrecto:

```yaml
PriceCalculator:
  label: Pricing Engine
```

A menos que el usuario pida renombrar el componente.

---

## 13.4 El LLM debe separar semántica de render

No debería meter layout duro en el YAML salvo que el schema del diagrama lo permita.

Evitar:

```yaml
x: 120
y: 400
width: 300
height: 80
```

Preferir:

```yaml
kind: boundary
contains:
  - Store
```

---

# 14. Renderers

## 14.1 Renderer PlantUML

Usado para:

```text
component
sequence
state
activity
deployment
```

Entrada:

```yaml
type: sequence
```

Salida:

```text
.puml
.svg
.png
```

---

## 14.2 Renderer SVG custom

Usado para:

```text
component_view_matrix
```

Porque este diagrama no calza bien con UML/PUML.

Entrada:

```yaml
type: component_view_matrix
```

Salida:

```text
.svg
.png
```

---

# 15. CLI propuesta

## 15.1 Renderizar un diagrama

```bash
diagram-render diagrams/sequence.create-quotation.yml --out build/
```

## 15.2 Validar un diagrama

```bash
diagram-render validate diagrams/sequence.create-quotation.yml
```

## 15.3 Renderizar todos

```bash
diagram-render diagrams/*.yml --out build/
```

## 15.4 Elegir backend

```bash
diagram-render diagrams/component.quotation.yml --backend plantuml
diagram-render diagrams/sequence.create-quotation.yml --backend mermaid
diagram-render diagrams/matrix.quotation-view.yml --backend svg
```

---

# 16. Errores esperados

## 16.1 Referencia inexistente

```yaml
edges:
  - from: QuotationFlow
    to: MissingComponent
```

Error:

```text
Unknown node: MissingComponent
```

---

## 16.2 Stage inexistente

```yaml
stages:
  quotation:
    - payment
```

Error:

```text
Unknown stage "payment" in view "quotation"
```

---

## 16.3 Tipo de diagrama no soportado

```yaml
type: random_diagram
```

Error:

```text
Unsupported diagram type: random_diagram
```

---

# 17. Convención de nombres

Archivos:

```text
<type>.<domain-or-scenario>.yml
```

Ejemplos:

```text
component.quotation.yml
sequence.create-quotation.yml
state.quotation.yml
activity.validation.yml
deployment.runtime.yml
matrix.quotation-view.yml
```

IDs internos:

```yaml
id: sequence.create-quotation
```

IDs de nodos:

```yaml
QuotationFlow
PricingEngine
ValidationSummary
```

Labels humanos:

```yaml
label: Pricing Engine
label: Validation Summary
```

---

# 18. Non-goals

Esta spec no busca:

```text
- reemplazar PlantUML
- definir un nuevo estándar UML
- tener un YAML universal para toda la arquitectura
- controlar layout pixel-perfect desde YAML
- forzar todos los diagramas al mismo renderer
```

Sí busca:

```text
- hacer diagramas versionables
- hacer diagramas entendibles por LLMs
- separar modelo semántico de render
- permitir validación automática
- generar artefactos visuales reproducibles
```

---

# 19. Decisión principal

La decisión arquitectónica central es:

```text
YAML por grafo como fuente canónica.
PUML/Mermaid/D2/SVG como outputs generados.
```

En una frase:

> El YAML es el AST semántico del diagrama; PUML/Mermaid/D2 son backends de render.

