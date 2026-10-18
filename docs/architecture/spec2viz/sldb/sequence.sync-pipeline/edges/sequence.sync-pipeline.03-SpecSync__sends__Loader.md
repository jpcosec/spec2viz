---
source_id: SpecNodeDoc:sequence.sync-pipeline.SpecSync
target_id: SpecNodeDoc:sequence.sync-pipeline.Loader
relation_type: sends
condition: ''
attributes:
  group: loop for each spec
  message: load(path)
---

# SpecSync sends Loader

## Notes

load(path)
