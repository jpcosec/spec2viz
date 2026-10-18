---
source_id: SpecNodeDoc:sequence.sync-pipeline.SpecSync
target_id: SpecNodeDoc:sequence.sync-pipeline.StoreAPI
relation_type: sends
condition: ''
attributes:
  group: loop for each spec
  message: upsert SpecNodeDoc, SpecDoc, RelationDoc (attributes)
---

# SpecSync sends StoreAPI

## Notes

upsert SpecNodeDoc, SpecDoc, RelationDoc (attributes)
