# UC-06: Python API pipeline

El usuario quiere integrar spec2viz en un script Python: cargar specs, validarlos, compilar a IR, y renderizar programáticamente sin pasar por el CLI.

## Pasos

1. `from spec2viz import load, validate, compile_ir, render`
2. `load("diagram.yml")` → BaseDiagram
3. `validate(diagram)` → None
4. `compile_ir(diagram)` → IR object
5. `render(ir, renderer="mermaid")` → str
6. `render_to_file("diagram.yml", out=".", renderer="plantuml")` → Path

## Preguntas de estrés

- ¿La función `load()` acepta Path y str?
- ¿`validate()` lanza excepción o devuelve resultado?
- ¿`compile_ir()` retorna tipos específicos (SequenceIR, StateIR) o Union?
- ¿`render()` detecta automáticamente el renderer según el tipo de IR?
- ¿Hay type hints en todas las funciones públicas?
- ¿Los modelos de IR son dataclasses o Pydantic?
- ¿Hay backward compatibility con `yaml_charts` imports?
