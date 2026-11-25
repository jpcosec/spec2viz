"""The rules of a Python library with a CLI (argparse, click) over the generic facts of sldb: the
module-level calls of argparse (`add_subparsers`, `add_parser`, `set_defaults`), the decorators of
click, the `calls` of a function, `__all__` and the classes with their `bases`.

It maps the existing types of specIR, it adds none: a CLI command is an InterfaceControlDoc and an
InterfaceActionDoc; a function of the public API of the package is an ApiOperationDoc (its method and
route are not HTTP, so they are unknown and named in `desconocidos`); the function a command runs is a
HandlerDoc; what the handler calls inside the package is a DomainOperationDoc; a Pydantic model or a
dataclass is a DomainEntityDoc. The layer of each node is the one its model declares.

What a rule reads as it stands is `observado`; what it assembles from several facts is `derivado`.
What the facts do not show is returned as not derived with the word `desconocido` and its reason,
never invented. Known gap of the facts: a call inside a function body carries only its name, so a
parser built inside a function (`def build(): ... sub.add_parser("run")`) shows no subcommand name nor
handler; it is reported as `desconocido`, one per builder function."""

from __future__ import annotations

from pathlib import Path

from sldb.api.code import code_facts

from specir.extract.django_drf import Plan
from specir.extract.facts import Fact, Facts, last, literal
from specir.extract.plan import Planned, node_name, sentence
from specir.extract.write import ExtractionReport, write_plan
from specir.install import package_pythonpath

COMMAND_CONTROL = "argparse-add-parser"
COMMAND_ACTION = "argparse-set-defaults-func"
CLICK_CONTROL = "click-command-decorator"
CLICK_ACTION = "click-command-function"
HANDLER = "cli-command-handler-function"
OPERATION = "handler-calls-package-function"
PUBLIC = "package-public-api"
MODEL = "pydantic-or-dataclass-model"
TRIGGERS = "cli-command-triggers-action"
INVOKES = "cli-action-invokes-public-function"
HANDLED_BY = "public-function-called-by-handler"
EXECUTES = "handler-executes-package-function"

#: Bases (last name segment) that make a class a model although they are not defined in the code read:
#: Pydantic's and sldb's, which is Pydantic-based.
MODEL_BASES = {"BaseModel", "StructuredNLDoc"}
NO_METHOD = "no es una operación HTTP: es una función de la API pública del paquete"
NO_ROUTE = "no es una operación HTTP: no tiene ruta"


def _unknown(text: str) -> str:
    return f"desconocido: {text}"


def _is_test(path: str) -> bool:
    parts = path.split("/")
    return "tests" in parts or "test" in parts or parts[-1].startswith("test_") or parts[-1] == "conftest.py"


def _call(fact: Fact) -> dict:
    return fact["attrs"].get("call") or {}


def _top(facts: Facts, fact: Fact) -> bool:
    owner = facts.owner(fact)
    return owner is not None and owner["kind"] == "module"


def _functions(facts: Facts) -> list[Fact]:
    return [f for f in facts.of_kind("function") if _top(facts, f)]


class Index:
    """The top-level functions of the tree by name, to resolve what a handler calls."""

    def __init__(self, facts: Facts) -> None:
        self.facts = facts
        self.by_name: dict[str, list[Fact]] = {}
        self.by_module: dict[tuple[str, str], Fact] = {}
        self.modules = {f["attrs"]["module"] for f in facts.of_kind("module")}
        for fact in _functions(facts):
            self.by_name.setdefault(fact["qualified_name"], []).append(fact)
            self.by_module[(fact["attrs"]["module"], fact["qualified_name"])] = fact

    def resolve(self, caller: Fact, name: str) -> tuple[Fact | None, str | None]:
        """The package function a call of `caller` names: (fact, None), or (None, reason) when it is
        ambiguous, or (None, None) when it is not a function of the package."""
        module = caller["attrs"]["module"]
        if "." in name:
            head, _, tail = name.rpartition(".")
            imported = {last(i) for i in self.facts.by_id[module]["attrs"].get("imports", [])}
            candidates = [m for m in self.modules if last(m) == last(head) and last(m) in imported and "." not in tail]
            found = [self.by_module[(m, tail)] for m in candidates if (m, tail) in self.by_module]
            return (found[0], None) if len(found) == 1 else (None, None)
        own = self.by_module.get((module, name))
        if own is not None:
            return own, None
        found = self.by_name.get(name, [])
        if len(found) == 1:
            return found[0], None
        return (None, f"{name!r} lo definen {len(found)} funciones del paquete") if found else (None, None)


# -- commands -------------------------------------------------------------------------------------

class Command:
    def __init__(self, path: list[str], help: str, handler: str | None, kind: str, facts: list[Fact], module: str) -> None:
        self.path, self.help, self.handler, self.kind, self.facts, self.module = path, help, handler, kind, facts, module


def _argparse_commands(facts: Facts) -> list[Command]:
    """The commands of argparse parsers declared at module level (rule `argparse-add-parser`)."""
    commands: list[Command] = []
    for module in facts.of_kind("module"):
        scope = [f for f in facts.members(module, "assignment", "call")]
        parsers: dict[str, tuple[list[str], Fact]] = {}
        subparsers: dict[str, tuple[str, Fact]] = {}
        parser_facts = {}
        for fact in scope:
            call, var = _call(fact), fact["qualified_name"]
            func = call.get("func", "")
            if fact["kind"] == "assignment" and last(func) == "ArgumentParser":
                prog = literal(call.get("kwargs", {}).get("prog")) or module["name"]
                parsers[var] = ([prog], fact)
            elif fact["kind"] == "assignment" and last(func) == "add_subparsers" and "." in func:
                subparsers[var] = (func.rsplit(".", 1)[0], fact)
        handlers: dict[str, tuple[str, Fact]] = {}
        for fact in scope:
            call = _call(fact)
            func = call.get("func", "")
            name = literal((call.get("args") or [None])[0]) if call.get("args") else None
            if fact["kind"] == "assignment" and last(func) == "add_parser" and "." in func and func.rsplit(".", 1)[0] in subparsers and name:
                owner, sub_fact = subparsers[func.rsplit(".", 1)[0]]
                if owner in parsers:
                    path = [*parsers[owner][0], name]
                    parsers[fact["qualified_name"]] = (path, fact)
                    parser_facts[fact["qualified_name"]] = [fact, sub_fact, parsers[owner][1]]
            elif fact["kind"] == "call" and last(func) == "set_defaults" and "func" in call.get("kwargs", {}) and "." in func:
                handlers[func.rsplit(".", 1)[0]] = (call["kwargs"]["func"], fact)
        for var, (path, fact) in parsers.items():
            if var not in parser_facts:
                continue
            help_text = literal(_call(fact).get("kwargs", {}).get("help")) or ""
            handler, used = handlers.get(var, (None, None))
            commands.append(Command(path, help_text, handler, "argparse", parser_facts[var] + ([used] if used else []), module["attrs"]["module"]))
    return commands


def _click_commands(facts: Facts) -> list[Command]:
    """The commands of click declared with `@<x>.command(...)` or `@click.command(...)` on a top-level function."""
    groups = {f["qualified_name"] for f in _functions(facts) if any(last(d["name"]) == "group" for d in f["attrs"].get("decorators", []))}
    commands = []
    for fact in _functions(facts):
        for deco in fact["attrs"].get("decorators", []):
            if last(deco["name"]) != "command":
                continue
            args = deco.get("args") or []
            name = (literal(args[0]) if args else None) or literal(deco.get("kwargs", {}).get("name")) or fact["qualified_name"].replace("_", "-")
            owner = deco["name"].rsplit(".", 1)[0] if "." in deco["name"] else ""
            path = [owner, name] if owner in groups else [name]
            commands.append(Command(path, fact.get("doc") or "", fact["qualified_name"], "click", [fact], fact["attrs"]["module"]))
    return commands


def _builders(facts: Facts) -> list[str]:
    """Functions that build argparse subparsers in their body: the facts show no subcommand name nor handler there."""
    out = []
    for fact in _functions(facts):
        names = [c["name"] for c in fact["attrs"].get("calls", [])]
        if any(last(n) == "add_parser" and "." in n for n in names):
            at = f"{fact['path']}:{fact['span']['start_line']} {fact['id']}"
            out.append(_unknown(
                f"los comandos de argparse que arma {at} en el cuerpo de la función; los hechos de sldb traen de cada llamada solo su nombre "
                "y su línea (sin argumentos), así que no muestran el nombre del subcomando ni su handler; pedido a sldb en su inbox"))
    return out


# -- models and public API --------------------------------------------------------------------------

def _models(facts: Facts) -> list[Fact]:
    classes = [c for c in facts.of_kind("class") if _top(facts, c) and not c["qualified_name"].startswith("_")]
    known = {c["qualified_name"] for c in classes if _direct_model(c)}
    changed = True
    while changed:
        changed = False
        for c in classes:
            if c["qualified_name"] not in known and any(last(b) in known for b in facts.bases(c)):
                known.add(c["qualified_name"])
                changed = True
    return [c for c in classes if c["qualified_name"] in known]


def _direct_model(cls: Fact) -> bool:
    bases = cls["attrs"].get("bases") or []
    return any(last(b) in MODEL_BASES for b in bases) or any(last(d["name"]) == "dataclass" for d in cls["attrs"].get("decorators", []))


def _public(facts: Facts, index: Index) -> tuple[dict[str, Fact], list[str]]:
    """The functions the top-level packages export (`__all__`, else their own names without underscore)."""
    public: dict[str, Fact] = {}
    notes: list[str] = []
    for module in facts.of_kind("module"):
        if "." in module["attrs"]["module"] or not module["path"].endswith("__init__.py"):
            continue
        declared = facts.member(module, "__all__", "assignment")
        if declared is not None:
            names = [literal(i["value"]) for i in declared["attrs"].get("items") or []]
            names = [n for n in names if n]
        else:
            names = [f["qualified_name"] for f in _functions(facts) if f["attrs"]["module"] == module["attrs"]["module"] and not f["qualified_name"].startswith("_")]
        for name in names:
            found = index.by_name.get(name, [])
            if len(found) == 1:
                public[found[0]["id"]] = found[0]
            elif len(found) > 1:
                notes.append(_unknown(f"la función pública {name!r} de {module['attrs']['module']} la definen {len(found)} funciones; no se sabe cuál exporta"))
    return public, notes


# -- the plan -------------------------------------------------------------------------------------

def _text(*parts: str) -> str:
    return ".".join(p for p in parts if p)


def interpret_python_cli(facts: Facts) -> Plan:
    plan = Plan()
    index = Index(facts)
    public, notes = _public(facts, index)
    plan.not_derived.extend(notes)
    commands = [*_argparse_commands(facts), *_click_commands(facts)]
    plan.not_derived.extend(_builders(facts))
    callers: dict[str, set[str]] = {}
    for command in commands:
        _command(plan, facts, index, public, command, callers)
    for api_id, handlers in sorted(callers.items()):
        api_node = plan.nodes[api_id]
        if len(handlers) == 1:
            handler = plan.nodes[next(iter(handlers))]
            plan.edge("handled_by", api_node, handler, HANDLED_BY, [*api_node.facts, *handler.facts], "La función pública la llama este handler y solo él.")
        else:
            plan.not_derived.append(_unknown(f"{api_node.export_id} handled_by: la llaman {len(handlers)} handlers y una operación tiene uno solo"))
    for cls in _models(facts):
        if _is_test(cls["path"]):
            continue
        symbol = cls["id"]
        fields = {"title": symbol, "symbol": symbol, "description": sentence(MODEL, [cls], derived=False)}
        plan.node(Planned("DomainEntityDoc", node_name("DomainEntityDoc", symbol), fields, "observado", MODEL, [cls]))
    return plan


def _command(plan: Plan, facts: Facts, index: Index, public: dict[str, Fact], command: Command, callers: dict[str, set[str]]) -> None:
    title = " ".join(command.path)
    control_rule, action_rule = (COMMAND_CONTROL, COMMAND_ACTION) if command.kind == "argparse" else (CLICK_CONTROL, CLICK_ACTION)
    key = f"{command.module}:{title}"
    control = plan.node(Planned("InterfaceControlDoc", node_name("InterfaceControlDoc", key), {
        "title": title, "kind": "cli_command", "component": command.module,
        "description": " ".join(x for x in (command.help, sentence(control_rule, command.facts, derived=False)) if x)}, "observado", control_rule, command.facts))
    action = plan.node(Planned("InterfaceActionDoc", node_name("InterfaceActionDoc", key), {
        "title": title, "event": "cli_invocation", "description": sentence(action_rule, command.facts, derived=False)}, "observado", action_rule, command.facts))
    plan.edge("triggers", control, action, TRIGGERS, command.facts, "El comando de la CLI ejecuta su acción.")
    if command.handler is None:
        plan.not_derived.append(_unknown(f"{control.export_id}: el subcomando no declara handler con set_defaults(func=...) en los hechos"))
        return
    start = command.facts[0]
    anchor = next((f for f in facts.of_kind("function") if f["attrs"]["module"] == command.module and f["qualified_name"] == command.handler and _top(facts, f)), None)
    if anchor is None:
        plan.not_derived.append(_unknown(f"{control.export_id}: el handler {command.handler!r} no es una función de primer nivel de {command.module}"))
        return
    handler = plan.node(Planned("HandlerDoc", node_name("HandlerDoc", anchor["id"]), {
        "title": anchor["id"], "framework": command.kind, "symbol": anchor["id"], "description": sentence(HANDLER, [anchor], derived=False)},
        "observado", HANDLER, [anchor]))
    seen: set[str] = set()
    for call in anchor["attrs"].get("calls", []):
        target, why = index.resolve(anchor, call["name"])
        if target is None:
            if why:
                plan.not_derived.append(_unknown(f"{handler.export_id} executes: {why}"))
            continue
        if target["id"] in seen or target["id"] == anchor["id"] or _is_test(target["path"]):
            continue
        seen.add(target["id"])
        operation = plan.node(Planned("DomainOperationDoc", node_name("DomainOperationDoc", target["id"]), {
            "title": target["id"], "symbol": target["id"], "description": sentence(OPERATION, [anchor, target], derived=False)},
            "observado", OPERATION, [target]))
        plan.edge("executes", handler, operation, EXECUTES, [anchor, target], "El handler llama a la función dentro del paquete.")
        if target["id"] in public:
            api_node = plan.node(Planned("ApiOperationDoc", node_name("ApiOperationDoc", target["id"]), {
                "title": target["id"], "method": None, "route": None,
                "desconocidos": {"method": NO_METHOD, "route": NO_ROUTE},
                "description": sentence(PUBLIC, [target], derived=False)}, "observado", PUBLIC, [target]))
            plan.edge("invokes", action, api_node, INVOKES, [start, anchor, target], "La acción llama, por su handler, a la función pública.")
            callers.setdefault(api_node.export_id, set()).add(handler.export_id)


def extract_python_cli(root: str | Path, store: str | Path | None = None, paths: list[str] | None = None) -> ExtractionReport:
    """Extract the CLI, public API, handlers, operations and models of the Python code under `root`
    into `store` (default `<root>/.sldb`); idempotent. `report.not_derived` holds what stayed
    `desconocido`, each with its reason.

    Raises:
        ValueError: A fact's anchor does not match the fact; nothing is written.
    """
    root = Path(root).resolve()
    store_path = Path(store).resolve() if store is not None else root / ".sldb"
    result = code_facts(root, paths)
    code = [f for f in result["facts"] if f["path"].endswith(".py") and not _is_test(f["path"])]
    plan = interpret_python_cli(Facts(code))
    report = write_plan(store_path, root, package_pythonpath(), list(plan.nodes.values()), list(plan.edges.values()), list(dict.fromkeys(plan.not_derived)))
    report.skipped = [s for s in result.get("skipped", []) if s.endswith(".py")]
    return report
