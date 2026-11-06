"""Intermediate representation (IR) dataclasses — one per diagram type.

Each IR is a graphics-ready, renderer-agnostic view of a diagram.
Compilers produce IRs; renderers consume them.
"""

from __future__ import annotations
from dataclasses import dataclass, field


# Class members remain structured through compilation; renderers own syntax.
@dataclass
class ClassParameterIR:
    name: str
    type: str


@dataclass
class ClassAttributeIR:
    name: str
    type: str
    visibility: str
    static: bool


@dataclass
class ClassMethodIR:
    name: str
    parameters: list[ClassParameterIR]
    returns: str
    visibility: str
    abstract: bool
    static: bool


@dataclass
class ClassNodeIR:
    id: str
    label: str
    kind: str
    attributes: list[ClassAttributeIR]
    methods: list[ClassMethodIR]


@dataclass
class ClassRelationIR:
    from_: str
    to: str
    relation: str
    label: str | None
    from_multiplicity: str | None
    to_multiplicity: str | None


@dataclass
class ClassPackageIR:
    id: str
    label: str
    kind: str
    contains: list[str] = field(default_factory=list)


@dataclass
class ClassIR:
    title: str
    direction: str
    classes: list[ClassNodeIR]
    relations: list[ClassRelationIR]
    packages: list[ClassPackageIR] = field(default_factory=list)
    style_kinds: dict[str, dict] = field(default_factory=dict)

    def package_path(self, package_id: str) -> list[str]:
        """Los paquetes desde la raiz hasta `package_id` (incluido)."""
        parent = {child: p.id for p in self.packages for child in p.contains}
        path = [package_id]
        while path[0] in parent:
            path.insert(0, parent[path[0]])
        return path

    def package_of(self, class_id: str) -> str | None:
        return next((p.id for p in self.packages if class_id in p.contains), None)


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
    contains: list[str] | None = None


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
    href: str | None = None


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
    partition: str | None = None
    notes: str | None = None
    tone: str | None = None
    detail: str | None = None
    group: str | None = None


@dataclass
class ActivityGroup:
    id: str
    label: str
    tone: str | None = None
    detail: str | None = None


@dataclass
class ActivityIR:
    title: str
    start: str
    steps: list[ActivityStep]
    end: str
    style_kinds: dict[str, dict] = field(default_factory=dict)
    groups: dict[str, ActivityGroup] = field(default_factory=dict)


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
    kind: str = "communication"
    label: str | None = None

    @property
    def text(self) -> str:
        """Rotulo de la conexion: label y protocolo; con «deploy»/«manifest» el estereotipo delante."""
        parts = [p for p in (self.label, self.protocol) if p]
        text = " · ".join(parts)
        if self.kind in ("deploy", "manifest"):
            text = f"«{self.kind}» {text}".strip()
        return text


@dataclass
class DeploymentIR:
    title: str
    nodes: list[DeploymentNode]
    artifacts: list[DeploymentArtifact]
    connections: list[DeploymentConnection]
    style_kinds: dict[str, dict] = field(default_factory=dict)


__all__ = [
    "ClassParameterIR", "ClassAttributeIR", "ClassMethodIR", "ClassNodeIR",
    "ClassRelationIR", "ClassIR", "ClassPackageIR",
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
    "ActivityGroup",
    "ActivityIR",
    "DeploymentNode",
    "DeploymentArtifact",
    "DeploymentConnection",
    "DeploymentIR",
]
