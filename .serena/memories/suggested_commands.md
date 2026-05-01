# Suggested Commands

## Installation
- **Standard Install**: `python3 -m pip install .`
- **Development Install**: `python3 -m pip install -e .[dev]`
- **Global Install (via pip)**: `pip install .` (or use `pipx install .` if available)

## Development
- **Run Tests**: `pytest`
- **Run Tests (Quiet)**: `pytest -q`
- **Lint Check**: `ruff check .`
- **Lint Fix**: `ruff check . --fix`

## CLI Usage
- **Help**: `spec2viz --help`
- **Validate Spec**: `spec2viz validate <path_to_yaml>`
- **Render Spec**: `spec2viz render <path_to_yaml> --out <dir>`
- **Render with Backend**: `spec2viz render <path_to_yaml> --backend mermaid --out <dir>`
- **Export Schema**: `spec2viz schema --type <type> --out <path>`

## Migration / Legacy
- **Legacy CLI**: `yaml-charts --help`
