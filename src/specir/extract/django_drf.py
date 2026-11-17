"""The rules of Django and Django REST Framework over the generic facts of sldb: classes with their
`bases`, decorators with their kwargs, `calls`, assignments and calls of module and class level.

Each rule names the facts it reads. What a rule reads as it stands is `observado` (a class, a
method, a table); what it assembles from several facts is `derivado` (a route from `register` and
`@action`, `handled_by`, `executes`, `governed_by`, `writes`, `persisted_in`). Nothing here is
`inferido` or `declarado`. What the facts do not show is returned as not derived, never invented."""

from __future__ import annotations

from dataclasses import dataclass, field

from specir.extract import sql
from specir.extract.facts import Fact, Facts, last, literal, literal_list
from specir.extract.plan import Planned, edge_name, node_name, sentence

PREDICATE_PREFIXES = ("can_", "is_", "has_", "may_")
CHOICES = ("TextChoices", "IntegerChoices", "Choices")
VERBS = {"get", "post", "put", "patch", "delete", "head", "options"}
ENTITY = "django-model"
STATE = "django-textchoices-state"
TABLE_OF = "django-meta-db-table"
ROUTE = "drf-router-register-action"
EXECUTES = "drf-handler-calls-model-method"
GOVERNED = "django-method-calls-predicate"
WRITES = "django-method-calls-save"
TRANSITION = "django-method-assigns-choice"


@dataclass
class Plan:
    nodes: dict[str, Planned] = field(default_factory=dict)
    edges: dict[str, Planned] = field(default_factory=dict)
    not_derived: list[str] = field(default_factory=list)
    members: dict[str, str] = field(default_factory=dict)

    def node(self, planned: Planned) -> Planned:
        kept = self.nodes.setdefault(planned.export_id, planned)
        kept.facts.extend(f for f in planned.facts if f not in kept.facts)
        return kept

    def edge(self, relation: str, source: Planned, target: Planned, rule: str, facts: list[Fact], what: str) -> Planned:
        name = edge_name(source, relation, target)
        used = list(facts)
        fields = {
            "title": f"{source.fields['title']} {relation} {target.fields['title']}", "source_id": source.export_id,
            "target_id": target.export_id, "relation_type": relation, "condition": "",
            "notes": f"{sentence(rule, used, derived=True)} {what}".strip(),
        }
        return self.edges.setdefault(f"RelationDoc:{name}", Planned("RelationDoc", name, fields, "derivado", rule, used))


def interpret(facts: Facts) -> Plan:
    plan = Plan()
    tables = sql.tables(facts)
    for planned in tables.values():
        plan.node(planned)
    entities = {c["id"]: _entity(plan, facts, c) for c in facts.of_kind("class") if _is_model(facts, c)}
    table_of = {cid: _persist(plan, facts, facts.by_id[cid], entity, tables) for cid, entity in entities.items()}
    for cid, entity in entities.items():
        _states(plan, facts, facts.by_id[cid], entity)
    operations = _routes(plan, facts, entities, table_of)
    _policies_writes_transitions(plan, facts, operations, entities, table_of)
    return plan


def _is_model(facts: Facts, cls: Fact) -> bool:
    return any(b in ("models.Model", "Model") for b in facts.bases(cls))


def _entity(plan: Plan, facts: Facts, cls: Fact) -> Planned:
    name = cls["qualified_name"]
    fields = {"title": name, "symbol": name, "description": sentence(ENTITY, [cls], derived=False)}
    return plan.node(Planned("DomainEntityDoc", node_name("DomainEntityDoc", name), fields, "observado", ENTITY, [cls]))


def _table_name(facts: Facts, cls: Fact) -> tuple[str | None, list[Fact]]:
    """The table a Django model is stored in: `Meta.db_table`, else Django's default `<app>_<model>`."""
    meta = facts.member(cls, "Meta", "class")
    declared = facts.member(meta, "db_table", "assignment") if meta else None
    if declared is not None and literal(declared["attrs"].get("value")):
        return literal(declared["attrs"]["value"]), [declared]
    app = cls["attrs"]["module"].split(".")[0]
    return f"{app}_{cls['qualified_name'].lower()}", []


def _persist(plan: Plan, facts: Facts, cls: Fact, entity: Planned, tables: dict[str, Planned]) -> tuple[Planned, list[Fact]] | None:
    table_name, used = _table_name(facts, cls)
    table = tables.get(table_name or "")
    if table is None:
        plan.not_derived.append(f"{entity.export_id} persisted_in: el SQL leído no tiene la tabla {table_name!r} de {cls['qualified_name']}")
        return None
    source = [cls, *used, table.facts[0]]
    plan.edge("persisted_in", entity, table, TABLE_OF, source, f"La tabla sale de {'Meta.db_table' if used else 'la convención <app>_<modelo> de Django'}.")
    return table, [*used, table.facts[0]]


def _states(plan: Plan, facts: Facts, cls: Fact, entity: Planned) -> None:
    for nested in facts.members(cls, "class"):
        if not any(last(b) in CHOICES for b in facts.bases(nested)):
            continue
        for member in facts.members(nested, "assignment"):
            items = member["attrs"].get("items") or []
            label = literal(items[1]["value"]) if len(items) > 1 else None
            title = label or last(member["qualified_name"])
            used = [nested, member]
            fields = {"title": title, "entity": entity.export_id, "description": sentence(STATE, used, derived=False)}
            state = plan.node(Planned("StateDoc", node_name("StateDoc", member["qualified_name"]), fields, "observado", STATE, used))
            plan.members[state.export_id] = last(member["qualified_name"])


# -- routes: urlpatterns, router.register, @action ------------------------------------------------

def _prefixes(facts: Facts, module: str, seen: tuple[str, ...] = ()) -> list[tuple[str, list[Fact]]]:
    """The URL prefixes `module` is mounted under by `path(prefix, include('<module>'))` in the
    `urlpatterns` of other modules (with the facts they come from); `[("", [])]` for a root module."""
    mounts: list[tuple[str, list[Fact]]] = []
    for fact in facts.of_kind("assignment"):
        if fact["qualified_name"] != "urlpatterns" or fact["attrs"]["module"] in seen:
            continue
        for item in fact["attrs"].get("items") or []:
            args = item.get("args") or []
            if item.get("func", "").endswith("path") and len(args) > 1 and args[1] in (f"include('{module}')", f'include("{module}")'):
                for above, used in _prefixes(facts, fact["attrs"]["module"], (*seen, module)):
                    mounts.append((join(above, literal(args[0]) or ""), [*used, fact]))
    return mounts or [("", [])]


def join(*parts: str) -> str:
    return "/".join(p.strip("/") for p in parts if p.strip("/"))


def _router(facts: Facts, register: Fact) -> tuple[Fact | None, list[Fact]]:
    """The router variable of `<router>.register(...)`, the `<router>.urls` assignment of its
    module that exposes it, and the router's own assignment (for `trailing_slash`)."""
    var = register["attrs"]["call"]["func"].rsplit(".", 1)[0]
    module = register["attrs"]["module"]
    router = next((f for f in facts.of_kind("assignment") if f["qualified_name"] == var and f["attrs"]["module"] == module and f["attrs"].get("call")), None)
    exposed = [f for f in facts.of_kind("assignment") if f["qualified_name"] == "urlpatterns" and f["attrs"]["module"] == module and _mentions(f, f"{var}.urls")]
    return router, exposed


def _mentions(patterns: Fact, text: str) -> bool:
    attrs = patterns["attrs"]
    return attrs.get("value") == text or any(text in a for i in attrs.get("items") or [] for a in i.get("args") or [])


def _viewset(facts: Facts, name: str, module: str) -> Fact | None:
    imported = facts.by_id.get(module, {}).get("attrs", {}).get("imports", [])
    found = [c for c in facts.classes(name) if any(last(b).endswith("ViewSet") for b in facts.bases(c))]
    near = [c for c in found if c["attrs"]["module"] in imported]
    return (near or found)[0] if len(near or found) == 1 else None


def _action(method: Fact) -> dict | None:
    return next((d for d in method["attrs"].get("decorators") or [] if last(d["name"]) == "action"), None)


def _model_of(facts: Facts, viewset: Fact, entities: dict[str, Planned]) -> tuple[Fact, list[Fact]] | None:
    """The model class a viewset serves: the `X` of `queryset = X.objects...`, else the
    `Meta.model` of its `serializer_class`."""
    by_name = {e.fields["symbol"]: cid for cid, e in entities.items()}
    queryset = facts.member(viewset, "queryset", "assignment")
    func = (queryset["attrs"].get("call") or {}).get("func", "") if queryset else ""
    if func.split(".")[0] in by_name and ".objects" in func:
        return facts.by_id[by_name[func.split(".")[0]]], [queryset]
    serializer = facts.member(viewset, "serializer_class", "assignment")
    named = serializer["attrs"].get("value") if serializer else None
    for cls in facts.classes(named) if named else []:
        meta = facts.member(cls, "Meta", "class")
        model = facts.member(meta, "model", "assignment") if meta else None
        if model and model["attrs"].get("value") in by_name:
            return facts.by_id[by_name[model["attrs"]["value"]]], [serializer, cls, meta, model]
    return None


def _routes(plan: Plan, facts: Facts, entities: dict[str, Planned], table_of: dict) -> list[tuple[Planned, Fact, Fact]]:
    """ApiOperationDoc, HandlerDoc, DomainOperationDoc and `handled_by`/`executes` of each
    `@action` of each viewset registered on a router; the domain operations found, with their entity."""
    operations: list[tuple[Planned, Fact, Fact]] = []
    for register in facts.of_kind("call"):
        call = register["attrs"].get("call") or {}
        args = call.get("args") or []
        if not call.get("func", "").endswith(".register") or len(args) < 2 or literal(args[0]) is None:
            continue
        viewset = _viewset(facts, args[1], register["attrs"]["module"])
        router, exposed = _router(facts, register)
        if viewset is None:
            plan.not_derived.append(f"{register['path']}:{register['span']['start_line']} register({args[1]}): no hay un viewset único con ese nombre entre los facts")
            continue
        if router is None or not exposed:
            plan.not_derived.append(f"{viewset['qualified_name']}: ningún urlpatterns del módulo expone el router de {register['path']}:{register['span']['start_line']}")
            continue
        slash = "" if (router["attrs"]["call"].get("kwargs") or {}).get("trailing_slash") == "False" else "/"
        model = _model_of(facts, viewset, entities)
        plan.not_derived.append(f"{viewset['qualified_name']}: rutas CRUD heredadas de {', '.join(facts.bases(viewset))}: sin método handler en los facts")
        for method in facts.members(viewset, "method"):
            action = _action(method)
            if action is None:
                continue
            for prefix, mount in _prefixes(facts, register["attrs"]["module"]):
                operations += _action_routes(plan, facts, viewset, method, action, register, router, exposed, mount, prefix, slash, model, entities)
    return operations


def _action_routes(plan, facts, viewset, method, action, register, router, exposed, mount, prefix, slash, model, entities):
    kwargs = action.get("kwargs") or {}
    verbs = [v.upper() for v in (literal_list(kwargs.get("methods")) or ["get"]) if v.lower() in VERBS]
    detail = kwargs.get("detail") == "True"
    segment = literal(kwargs.get("url_path")) or last(method["qualified_name"])
    route = "/" + join(prefix, literal(register["attrs"]["call"]["args"][0]), "{id}" if detail else "", segment) + slash
    handler_facts = [method]
    handler = plan.node(Planned("HandlerDoc", node_name("HandlerDoc", method["qualified_name"]), {
        "title": method["qualified_name"], "framework": "django-rest-framework", "symbol": method["qualified_name"],
        "description": sentence("drf-viewset-method", handler_facts, derived=False)}, "observado", "drf-viewset-method", handler_facts))
    sources = [register, router, *exposed, *mount, method]
    found: list = []
    for verb in verbs:
        title = f"{verb} {route}"
        fields = {"title": title, "method": verb, "route": route, "description": sentence(ROUTE, sources, derived=True)}
        api = plan.node(Planned("ApiOperationDoc", node_name("ApiOperationDoc", title), fields, "derivado", ROUTE, sources))
        plan.edge("handled_by", api, handler, ROUTE, [register, method], "")
    if model is not None:
        found = _executes(plan, facts, method, handler, model, entities)
    return found


def _executes(plan, facts, method, handler, model, entities):
    cls, served = model
    found = []
    for call in method["attrs"].get("calls") or []:
        owner, _, name = call["name"].rpartition(".")
        target = facts.member(cls, name, "method") if owner and "." not in owner and owner not in ("self", "cls") else None
        if target is None:
            continue
        fields = {"title": target["qualified_name"], "symbol": target["qualified_name"], "description": sentence("django-model-method", [target], derived=False)}
        operation = plan.node(Planned("DomainOperationDoc", node_name("DomainOperationDoc", target["qualified_name"]), fields, "observado", "django-model-method", [target]))
        plan.edge("executes", handler, operation, EXECUTES, [method, *served, target], f"La llamada {call['name']} (línea {call['line']}) es a un método del modelo servido por el viewset.")
        found.append((operation, target, cls))
    return found


def _policies_writes_transitions(plan: Plan, facts: Facts, operations: list, entities: dict, table_of: dict) -> None:
    done: set[str] = set()
    for operation, method, cls in operations:
        if operation.export_id in done:
            continue
        done.add(operation.export_id)
        module = method["attrs"]["module"]
        for call in method["attrs"].get("calls") or []:
            if "." not in call["name"]:
                if call["name"].startswith(PREDICATE_PREFIXES):
                    for function in facts.functions(module, call["name"]):
                        _policy(plan, operation, method, function, call)
                else:
                    _unfiltered(plan, facts, operation, method, module, call)
            if call["name"] in ("self.save", "self.delete") and table_of.get(cls["id"]):
                table, used = table_of[cls["id"]]
                plan.edge("writes", operation, table, WRITES, [method, *used], f"La llamada {call['name']} (línea {call['line']}) escribe en la tabla del modelo.")
        _transitions(plan, facts, operation, method, cls, entities)


def _unfiltered(plan: Plan, facts: Facts, operation: Planned, method: Fact, module: str, call: dict) -> None:
    """A call to a module function of the analyzed tree (this module or one it imports) that the
    predicate-prefix convention does not take as a policy is reported, never dropped in silence."""
    imported = facts.by_id.get(module, {}).get("attrs", {}).get("imports", [])
    for function in [f for m in (module, *imported) for f in facts.functions(m, call["name"])]:
        note = (f"{operation.export_id} governed_by: llamada a función del proyecto sin señal de política: {call['name']} "
                f"({function['path']}:{function['span']['start_line']}, llamada en {method['qualified_name']} línea {call['line']}); "
                f"solo se toman como política las funciones con prefijo {'/'.join(PREDICATE_PREFIXES)}")
        if note not in plan.not_derived:
            plan.not_derived.append(note)


def _policy(plan: Plan, operation: Planned, method: Fact, function: Fact, call: dict) -> None:
    statement = function.get("doc") or None
    fields = {
        "title": function["qualified_name"], "statement": statement,
        "description": sentence("django-predicate-function", [function], derived=False),
    }
    if statement is None:
        fields["desconocidos"] = {"statement": "la función no tiene docstring"}
    policy = plan.node(Planned("PolicyDoc", node_name("PolicyDoc", function["qualified_name"]), fields, "observado", "django-predicate-function", [function]))
    what = (f"La llamada {call['name']} (línea {call['line']}) es a una función predicado por la convención de specIR de que un nombre con prefijo {'/'.join(PREDICATE_PREFIXES)} "
            "es un predicado de política (no es un fact del código); "
            "los facts no dan la condición que decide el raise, así que la regla usa solo la llamada.")
    plan.edge("governed_by", operation, policy, GOVERNED, [method, function], what)


def _transitions(plan: Plan, facts: Facts, operation: Planned, method: Fact, cls: Fact, entities: dict) -> None:
    """`transitions` only when a fact shows the operation assigning a member of the entity's choices;
    the facts of assignment are of module and class level, so a body assignment is not one."""
    entity = entities[cls["id"]]
    states = [n for n in plan.nodes.values() if n.model == "StateDoc" and n.fields["entity"] == entity.export_id]
    shown = [f for f in facts.members(method, "assignment")]
    if not states:
        return
    reached = [(f, s) for f in shown for s in states if (f["attrs"].get("value") or "").endswith(f".{plan.members[s.export_id]}")]
    if not reached:
        plan.not_derived.append(f"{operation.export_id} transitions: ningún fact de assignment dentro de {method['qualified_name']} muestra el estado al que pasa ({', '.join(s.fields['title'] for s in states)})")
        return
    for fact, state in reached:
        plan.edge("transitions", operation, state, TRANSITION, [method, fact], "")
