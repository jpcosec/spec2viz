"""How specIR's renderers draw what the IRs project: the kind scale of `vega`, the selector of renderers,
and a transition whose source state is not named (`ANY_STATE`, the state projection of IR11).

- `vega` lists the kinds in order of first appearance.
- The selector has nine renderers.
- A transition whose source state is not named leaves one dashed pseudostate labelled `*` in mermaid,
  plantuml and d2; it is never the initial state, and a state IR without an initial state draws no
  initial arrow."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "models"))  # blog.py, for conftest's blog fixtures

from specir.visual.ir import ANY_STATE, StateIR, StateNode, Transition  # noqa: E402
from specir.visual.lint_mermaid import lint_mermaid  # noqa: E402
from specir.visual.renderers import EXT_MAP, RENDERER_MAP, render  # noqa: E402
from specir.visual.renderers.mermaid import ANY_STATE_ID  # noqa: E402


def test_vega_lists_the_kinds_in_order_of_first_appearance():
    from sldb.api.notations import load_spec

    from specir.visual.compilers import compile_ir

    ir = compile_ir(load_spec(HERE / "fixtures" / "spec2viz" / "examples" / "matrix" / "example.yml"))
    scale = next(s for s in render(ir, "vega")["scales"] if s["name"] == "kindColor")
    assert scale["domain"] == list(dict.fromkeys(span.kind for span in ir.spans))


def test_the_selector_has_the_nine_renderers():
    from specir.visual.commands import DIAGRAM_RENDERERS

    nine = ("plantuml", "mermaid", "vega", "d2", "antonia-html", "tree", "graph", "bpmn", "json")
    assert tuple(DIAGRAM_RENDERERS) == nine
    assert set(RENDERER_MAP) == set(EXT_MAP) == set(nine)


# ── a transition without a source state (ANY_STATE) ──────────────────────────────────────────────


def _any_state_ir(initial: str = "draft") -> StateIR:
    return StateIR(
        title="Post", entity="Post", initial=initial,
        states=[StateNode(id="draft", label="Draft"), StateNode(id="published", label="Published")],
        transitions=[Transition(from_=ANY_STATE, to="published", on="PublishPost"), Transition(from_="published", to="draft", on="Unpublish")],
    )


def test_mermaid_draws_any_state_as_one_dashed_pseudostate():
    out = render(_any_state_ir(), "mermaid")
    lines = [l.strip() for l in out.splitlines()]
    assert f'state "*" as {ANY_STATE_ID}' in lines and f"class {ANY_STATE_ID} anyState" in lines
    assert any(l.startswith("classDef anyState") and "stroke-dasharray" in l for l in lines)
    assert f"{ANY_STATE_ID} --> published : PublishPost" in lines and "published --> draft : Unpublish" in lines
    assert "[*] --> draft" in lines and not any(l.startswith("* ") for l in lines)
    assert lint_mermaid(out) == []


def test_plantuml_and_d2_draw_any_state_as_one_dashed_pseudostate():
    puml = render(_any_state_ir(), "plantuml").splitlines()
    assert f'state "*" as {ANY_STATE_ID} ##[dashed]' in puml and f"{ANY_STATE_ID} --> published : PublishPost" in puml
    assert "[*] --> draft" in puml and "published --> draft : Unpublish" in puml
    d2 = render(_any_state_ir(), "d2").splitlines()
    assert f'{ANY_STATE_ID}: "*" {{style.stroke-dash: 3}}' in d2 and f"{ANY_STATE_ID} -> published: PublishPost" in d2


def test_mermaid_state_ids_with_a_hyphen_become_ids_the_real_engine_accepts():
    ir = StateIR(
        title="Post", entity="Post", initial="post-draft",
        states=[StateNode(id="post-draft", label="Draft"), StateNode(id="post-published", label="Published"),
                StateNode(id="post_published", label="Taken")],
        transitions=[Transition(from_=ANY_STATE, to="post-published", on="PublishPost"),
                     Transition(from_="post-published", to="post-draft", on="Unpublish")],
    )
    lines = [l.strip() for l in render(ir, "mermaid").splitlines()]
    assert 'state "Draft" as post_draft' in lines and 'state "Taken" as post_published' in lines
    assert 'state "Published" as post_published_2' in lines  # no collision with an id already safe
    assert "[*] --> post_draft" in lines and f"{ANY_STATE_ID} --> post_published_2 : PublishPost" in lines
    assert "post_published_2 --> post_draft : Unpublish" in lines
    assert lint_mermaid("\n".join(lines)) == []


def test_without_any_state_or_initial_nothing_extra_is_drawn():
    ir = _any_state_ir(initial="")
    ir.transitions = [Transition(from_="draft", to="published", on="PublishPost")]
    for name in ("mermaid", "plantuml", "d2"):
        out = render(ir, name)
        assert ANY_STATE_ID not in out and "[*]" not in out, name


def test_the_projected_states_of_the_blog_render(blog, blog_root: Path):
    """The state projection of IR11 over the blog of IR06 (ViewDoc:post-states) draws in every state
    renderer, with PublishPost leaving the `*` pseudostate."""
    from specir.visual import state_from_view

    ir = state_from_view(blog_root / ".sldb", "ViewDoc:post-states")
    assert [t.from_ for t in ir.transitions] == [ANY_STATE]
    mermaid = render(ir, "mermaid")
    # mermaid's state lexer does not accept '-' in an id: the renderer writes post_published (mmdc)
    assert f"{ANY_STATE_ID} --> post_published : PublishPost" in mermaid and "[*] --> post_draft" in mermaid
    assert 'state "*" as __any_state' in mermaid and "post-" not in mermaid.split("\n", 1)[1].replace('"', "")
    assert lint_mermaid(mermaid) == []
    assert f"{ANY_STATE_ID} --> post-published : PublishPost" in render(ir, "plantuml")
    assert f"{ANY_STATE_ID} -> post-published: PublishPost" in render(ir, "d2")
    assert "PublishPost" in render(ir, "antonia-html")
