---
source_id: SpecNodeDoc:sequence.build-pipeline.Deskops
target_id: SpecNodeDoc:sequence.build-pipeline.VistasYML
relation_type: sends
condition: ''
attributes:
  message: yaml.safe_load(config_path)
---

# Deskops sends VistasYML

## Notes

yaml.safe_load(config_path)
