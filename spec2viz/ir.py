"""Intermediate representation (IR) dataclasses — one per diagram type.

Each IR is a graphics-ready, renderer-agnostic view of a diagram.
Compilers produce IRs; renderers consume them.
"""

from __future__ import annotations
from dataclasses import dataclass, field


# ── Matrix ────────────────────────────────────────────────────────────────────


@dataclass
class Stage:
    id: str
    index: int
    label: str
    view: str | None = None


@dataclass
class Row:
    id: str
    label: str
    row: int
    depth: int


@dataclass
class Span:
    component: str
    row: int
    start: int
    end: int
    kind: str


@dataclass
class MatrixIR:
    title: str
    stages: list[Stage]
    rows: list[Row]
    spans: list[Span]


# ── Sequence ──────────────────────────────────────────────────────────────────


@dataclass
class Participant:
    id: str
    kind: str = "component"


@dataclass
class Message:
    index: int = 0
    from_: str = ""
    to: str = ""
    message: str = ""
    kind: str = "sync"
    condition: str | None = None
    group: str | None = None


@dataclass
class SequenceIR:
    title: str
    participants: list[Participant]
    messages: list[Message]


# ── State ─────────────────────────────────────────────────────────────────────


@dataclass
class StateNode:
    id: str
    label: str


@dataclass
class Transition:
    from_: str
    to: str
    on: str
    guard: str | None = None
    action: str | None = None


@dataclass
class StateIR:
    title: str
    entity: str
    initial: str
    states: list[StateNode]
    transitions: list[Transition]


# ── Component ─────────────────────────────────────────────────────────────────


@dataclass
class ComponentNode:
    id: str
    label: str
    kind: str
    contains: list[str] = field(default_factory=list)


@dataclass
class ComponentEdge:
    from_: str
    to: str
    relation: str
    label: str | None = None


@dataclass
class ComponentIR:
    title: str
    nodes: list[ComponentNode]
    edges: list[ComponentEdge]
    style_kinds: dict[str, dict] = field(default_factory=dict)


# ── Activity ──────────────────────────────────────────────────────────────────


@dataclass
class ActivityStep:
    id: str
    label: str
    kind: str = "action"
    next: str | None = None
    branches: dict[str, str] = field(default_factory=dict)


@dataclass
class ActivityIR:
    title: str
    start: str
    steps: list[ActivityStep]
    end: str


# ── Deployment ────────────────────────────────────────────────────────────────


@dataclass
class DeploymentNode:
    id: str
    label: str
    kind: str
    contains: list[str] = field(default_factory=list)


@dataclass
class DeploymentArtifact:
    id: str
    label: str
    kind: str


@dataclass
class DeploymentConnection:
    from_: str
    to: str
    protocol: str | None = None


@dataclass
class DeploymentIR:
    title: str
    nodes: list[DeploymentNode]
    artifacts: list[DeploymentArtifact]
    connections: list[DeploymentConnection]


__all__ = [
    "Stage",
    "Row",
    "Span",
    "MatrixIR",
    "Participant",
    "Message",
    "SequenceIR",
    "StateNode",
    "Transition",
    "StateIR",
    "ComponentNode",
    "ComponentEdge",
    "ComponentIR",
    "ActivityStep",
    "ActivityIR",
    "DeploymentNode",
    "DeploymentArtifact",
    "DeploymentConnection",
    "DeploymentIR",
]
