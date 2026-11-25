---
subject: model <= RelationDoc
where: relation_type in ["triggers", "invokes", "handled_by", "executes", "governed_by",
  "transitions", "writes", "persisted_in", "bound_to", "field_of"]
condition: attributes.origen in ["observado", "derivado", "inferido", "declarado"]
  and attributes.verificacion in ["sin_verificar", "verificado", "refutado"]
severity: error
moment: on_write
message: An edge of a specIR relation type declares origen and verificacion in its
  attributes (IR05 D1-B).
---

# A specIR edge carries its provenance