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

Representar una matriz bi-jerárquica:

```text
Y axis = component hierarchy
X axis = views -> stages
cells/spans = participation
```

## 11.2 Schema conceptual

```yaml
id: matrix.quotation-view
title: Quotation Flow - Component View Matrix
type: component_view_matrix
version: 0.1

data:
  views:
    quotation:
      label: Quotation View
      stages:
        - browse
        - client
        - basket
        - validation
        - completed

  components:
    - name: QuotationFlow
      kind: core
      stages:
        quotation:
          - browse
          - client
          - basket
          - validation
          - completed
      children:
        - name: Persistence
          kind: boundary
          stages:
            quotation:
              - browse
              - validation
              - completed

        - name: Store
          kind: boundary
          stages:
            quotation:
              - browse
              - client
              - basket

        - name: Basket
          kind: core
          stages:
            quotation:
              - basket
              - validation
          children:
            - name: BasketDay
              kind: core
              stages:
                quotation:
                  - basket
                  - validation
              children:
                - name: Item
                  label: Item (basket mode)
                  kind: core
                  stages:
                    quotation:
                      - basket
                      - validation
```

## 11.3 Reglas

Cada view debe tener stages ordenadas.

Cada component puede tener `children`.

Cada component puede declarar presencia en una o más views.

Un stage declarado por un component debe existir en la view correspondiente.

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

