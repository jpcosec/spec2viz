# Project Overview: spec2viz

`spec2viz` is a Python-based tool that transforms semantic YAML specifications into various diagram and chart formats, including PlantUML, Mermaid, and Vega. It is designed to allow users to define structured specifications once and render them into multiple visual outputs.

## Tech Stack
- **Language**: Python 3.11+
- **Validation**: Pydantic v2
- **Parsing**: PyYAML
- **CLI Framework**: Click
- **Testing**: Pytest
- **Linting**: Ruff (noted by `.ruff_cache` and current violations)

## Key Concepts
- **Diagram-as-Data**: Using YAML to define the semantics of a diagram rather than its visual layout.
- **IR (Intermediate Representation)**: A renderer-agnostic representation of the diagram.
- **Pipeline**: Model (YAML -> Pydantic) -> Compiler (Model -> IR) -> Renderer (IR -> Output).

## Codebase Structure
- `spec2viz/models/`: Pydantic schemas for different diagram types (Sequence, State, Component, Activity, Deployment, Matrix).
- `spec2viz/compilers/`: Logic to transform validated models into IR.
- `spec2viz/renderers/`: Logic to transform IR into specific backends (Mermaid, PlantUML, Vega).
- `spec2viz/ir.py`: Definitions for the Intermediate Representation.
- `spec2viz/loader.py`: Handles loading and parsing YAML files.
- `spec2viz/validator.py`: Handles validation logic.
- `spec2viz/cli.py`: The Click-based CLI entrypoint.
- `yaml_charts/`: Legacy compatibility layer for the old project name.
