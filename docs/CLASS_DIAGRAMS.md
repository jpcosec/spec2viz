# Class diagrams

`type: class` models language-neutral classes, interfaces, abstract classes, records, protocols and enums. It follows the native pipeline: YAML → Pydantic model → validated ClassIR → Mermaid (default) or PlantUML.

```bash
spec2viz diagram schema --type class --out class.schema.json
spec2viz diagram validate examples/class/runtime.yml
spec2viz diagram render examples/class/runtime.yml --out out
spec2viz diagram render examples/class/runtime.yml --backend plantuml --out out
```

See [the complete example](../examples/class/runtime.yml) and [JSON Schema](../examples/schema/class.schema.json).

## Data contract

- `direction`: `TB` (default) or `LR`.
- `classes`: nonempty map keyed by stable identifiers (letters, digits and underscores; no leading digit).
- Each class has optional `label`, `kind`, `attributes` and `methods`.
- `kind`: `class`, `interface`, `abstract`, `record`, `protocol`, `enum`.
- Attributes have `name`, `type`, `visibility` and `static`.
- Methods have `name`, `parameters: [{name, type}]`, `returns`, `visibility`, `static` and `abstract`.
- Visibility: `public`, `private`, `protected`, `package`. Defaults are public visibility, nonstatic members and nonabstract methods.
- Member names may contain hyphens, `?` and `!` for protocol-oriented languages. Parameter lists omit implicit receivers (`self`, `this`, protocol dispatch arguments).
- `type` and `returns` are display expressions, not resolved type definitions. External types can be referenced without adding boxes. Simple generics such as `List<InputPort>` become Mermaid's `List~InputPort~` notation. Complex language-specific types can be named aliases; the rendering engine still checks Mermaid syntax.
- Unknown structural fields and invalid identifiers are rejected instead of silently discarded.

## Relationship direction

| `relation` | Meaning of `from → to` | UML glyph |
|---|---|---|
| `inheritance` | subtype → parent | solid line, hollow triangle at parent |
| `realization` | implementation → interface/protocol | dashed line, hollow triangle at contract |
| `composition` | owner → owned part | filled diamond at owner |
| `aggregation` | aggregate → shared part | hollow diamond at aggregate |
| `association` | source → target | directed solid line |
| `dependency` | client → supplier | directed dashed line |

Relations may declare `label`, `from_multiplicity` and `to_multiplicity`. Multiplicities use `1`, `*`, `0..1`, `0..*`, etc. Inheritance/realization have no multiplicities. Validation rejects unknown endpoints, duplicate attributes/parameter names/method signatures, inverted multiplicities, inheritance/realization cycles and realization targets that are not interfaces or protocols. Distinct parameter-type overloads and ordinary dependency cycles are supported.

## Catalogs

Render the YAML, then register the `.mmd` as `src` and the YAML under `specs`. The existing catalog builder displays and filters `type: class` views without a custom template.

```yaml
diagram_store:
  template: template.html
  items:
    - id: runtime-contract
      title: Runtime contract
      type: class
      src: out/runtime.mmd
      specs: [examples/class/runtime.yml]
```

This is a diagram schema; it does not generate implementations or require an object-oriented inheritance hierarchy. For Clojure, `protocol` and `record` describe `defprotocol` and `defrecord` contracts.
