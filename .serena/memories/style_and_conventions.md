# Style and Conventions

## Python Coding Style
- **Type Hints**: Mandatory for new code. Use `from __future__ import annotations`.
- **Naming**: `snake_case` for variables, functions, and files. `PascalCase` for classes (Pydantic models, Compilers, Renderers).
- **Documentation**: Use docstrings for modules and complex functions.
- **Structure**: Follow the **Model -> Compiler -> IR -> Renderer** pipeline for adding new diagram types.

## Architecture
- **Pydantic Models**: Define all input schemas using Pydantic in `spec2viz/models/`.
- **Separation of Concerns**: Avoid putting rendering logic in compilers or parsing logic in renderers.
- **IR**: The Intermediate Representation should be as generic as possible to support multiple backends.

## Linting
- **Ruff**: Use `ruff` for linting. Note: Some existing code uses one-liner `match` cases which may trigger `E701`. Follow existing patterns if they are pervasive, or fix them if instructed.
