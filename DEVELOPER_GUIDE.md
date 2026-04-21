# Developer Guide: Adding a New Diagram Type

This guide explains the process of adding a new diagram type to the `spec2viz` project. The pipeline follows a strict separation of concerns: **Model -> Compiler -> IR -> Renderer**.

---

## 1. Define the Data Model
The first step is to define the Pydantic schema for your YAML.

1.  **Add a new enum value**: In `spec2viz/models/base.py`, add your new type to `DiagramType`.
    ```python
    class DiagramType(str, Enum):
        my_new_diagram = "my_new_diagram"
    ```
2.  **Create the model file**: Create `spec2viz/models/my_new_diagram.py`.
    ```python
    from typing import Literal
    from pydantic import BaseModel
    from spec2viz.models.base import BaseDiagram, DiagramType

    class MyData(BaseModel):
        nodes: list[str]

    class MyNewDiagram(BaseDiagram):
        type: Literal[DiagramType.my_new_diagram] = DiagramType.my_new_diagram
        data: MyData
    ```
3.  **Register the model**: 
    - Add it to `spec2viz/models/__init__.py`.
    - Add it to `AnyDiagram` in `spec2viz/loader.py`.

---

## 2. Define the Intermediate Representation (IR)
The IR should be a graphics-ready, renderer-agnostic representation of your diagram.

1.  **Add to `spec2viz/ir.py`**: Create a new dataclass for your IR.
    ```python
    @dataclass
    class MyNewIR:
        title: str
        items: list[str]
    ```

---

## 3. Implement the Compiler
The compiler transforms the validated Pydantic model into the IR.

1.  **Create the compiler**: Create `spec2viz/compilers/my_new_diagram.py`.
    ```python
    from spec2viz.models.my_new_diagram import MyNewDiagram
    from spec2viz.ir import MyNewIR

    class MyNewCompiler:
        def compile(self, diagram: MyNewDiagram) -> MyNewIR:
            return MyNewIR(title=diagram.title, items=diagram.data.nodes)
    ```
2.  **Register the compiler**: In `spec2viz/compilers/__init__.py`, update `compile_ir` to include your new compiler.

---

## 4. Update the Renderers
Finally, teach the renderers how to turn your IR into a visual format.

1.  **Update PlantUML/Mermaid**: In `spec2viz/renderers/plantuml.py` (and/or `mermaid.py`), add a handler for your new IR.
    ```python
    def render(self, ir) -> str:
        match ir:
            case MyNewIR(): return self._my_new_render(ir)
    ```
2.  **Register Defaults**: Update `DEFAULT_RENDERER` in `spec2viz/renderers/__init__.py` to set the default backend for your new IR.

---

## 5. Add Tests
Verify your changes by adding a new test file in `tests/`.

1.  **Fixture**: Create a sample YAML in `tests/fixtures/`.
2.  **Test**: Create `tests/test_models_my_new_diagram.py` and add cases to `tests/test_compilers.py` and `tests/test_renderers.py`.

Run the suite to ensure everything works:
```bash
pytest
```
