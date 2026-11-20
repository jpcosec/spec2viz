"""The rules of React and of HTTP clients over the generic facts of sldb for TS, TSX, JS and JSX:
`attrs.handlers` of a component (element, attribute, handler) and `attrs.calls` of a function or
component (name, first_arg, canonical). One mapping for the four extensions: it reads facts, never code.

What a rule reads as it stands is `observado` (the control a handler sits on, the action a handler
is); what it assembles is `derivado` (`triggers` control -> action, `invokes` action -> API operation).
Nothing here is `inferido` or `declarado`. A call that cannot be resolved is returned as not derived:
a declared gap (the facts do not show the method or the URL) or a breach (no operation in the graph)."""

from __future__ import annotations

from specir.extract.django_drf import Plan
from specir.extract.facts import Fact, Facts, last
from specir.extract.plan import Planned, node_name, sentence

#: The extensions whose facts this module maps (the same code for every one of them).
FRONTEND_SUFFIXES = (".ts", ".tsx", ".js", ".jsx")
HTTP_VERBS = {"get", "post", "put", "patch", "delete"}
CONTROL = "react-jsx-handler-element"
ACTION = "react-jsx-handler-function"
TRIGGERS = "react-handler-triggers-action"
INVOKES = "http-call-resolves-to-api-operation"


def normalize(route: str) -> tuple[str, ...]:
    """A route as segments, without query nor trailing slash, every `{x}` the same parameter."""
    path = route.split("?", 1)[0].split("#", 1)[0]
    return tuple("{}" if s.startswith("{") and s.endswith("}") else s for s in path.strip("/").split("/") if s)


def http_method(call: dict) -> str | None:
    """The method of an HTTP call (rule c): a canonical call whose last name segment is an HTTP verb
    and whose first argument is a literal route starting with `/`; else None."""
    first = call.get("first_arg")
    if call.get("canonical") and last(call["name"]).lower() in HTTP_VERBS and isinstance(first, str) and first.startswith("/"):
        return last(call["name"]).upper()
    return None


def _is_hole(call: dict) -> bool:
    """A call that looks like an HTTP call by its name but gives no literal route (a template with
    expressions, a variable, a non canonical callee)."""
    first = call.get("first_arg")
    verb = last(call["name"]).lower() in HTTP_VERBS and "." in call["name"]
    if last(call["name"]) == "fetch":
        return True  # the method is not in the facts, even when the URL is a literal
    return verb and not (call.get("canonical") and isinstance(first, str) and first.startswith("/"))


def interpret_frontend(facts: Facts, operations: list[Planned]) -> Plan:
    """Controls, actions, `triggers` and `invokes` of the frontend facts, resolved against `operations`
    (the ApiOperationDoc of the graph, as Planned without facts)."""
    plan = Plan()
    code = [f for f in facts.all if f["path"].endswith(FRONTEND_SUFFIXES)]
    frontend = Facts(code)
    functions: dict[str, list[Fact]] = {}
    for fact in frontend.of_kind("function", "component"):
        functions.setdefault(fact["qualified_name"], []).append(fact)
    for component in frontend.of_kind("component"):
        handlers = component["attrs"].get("handlers") or []
        seen: dict[str, int] = {}
        for entry in handlers:
            key = f"{entry['element']}.{entry['attribute']}"
            seen[key] = seen.get(key, 0) + 1
            _handler(plan, frontend, functions, operations, component, entry, seen[key], len(handlers))
    return plan


def _handler(plan, facts, functions, operations, component, entry, index, total) -> None:
    where = f"{component['path']}:{component['span']['start_line']}"
    element, attribute, name = entry["element"], entry["attribute"], entry["handler"]
    suffix = "" if index == 1 else f".{index}"
    control = plan.node(Planned("InterfaceControlDoc", node_name("InterfaceControlDoc", f"{component['id']}.{element}.{attribute}{suffix}"), {
        "title": f"{component['qualified_name']} {element}", "kind": element, "component": component["qualified_name"],
        "description": sentence(CONTROL, [component], derived=False)}, "observado", CONTROL, [component]))
    own = [f for f in functions.get(name, []) if f["attrs"]["module"] == component["attrs"]["module"] and f is not component]
    handler = own[0] if len(own) == 1 else None
    used = [component, *([handler] if handler else [])]
    event = attribute[2:].lower() if attribute.startswith("on") else attribute.lower()
    action = plan.node(Planned("InterfaceActionDoc", node_name("InterfaceActionDoc", f"{component['id']}.{name}"), {
        "title": name, "event": event, "description": sentence(ACTION, used, derived=False)}, "observado", ACTION, used))
    plan.edge("triggers", control, action, TRIGGERS, [component], f"El elemento {element} liga {attribute} a {name} (línea {component['span']['start_line']}).")
    if handler is not None:
        calls, owner = handler["attrs"].get("calls") or [], handler
    elif not own and total == 1:
        # the handler is declared inside the component: sldb gives its calls with the component's own
        calls, owner = component["attrs"].get("calls") or [], component
    else:
        plan.not_derived.append(f"{where} {name}: el handler no es un fact único y el componente tiene más de un handler; no se sabe qué llamadas son suyas")
        return
    for call in calls:
        _call(plan, facts, functions, operations, action, component, owner, call, depth=0)


def _call(plan, facts, functions, operations, action, component, owner, call, depth) -> None:
    here = f"{owner['path']}:{call['line']}"
    method = http_method(call)
    if method is not None:
        _resolve(plan, operations, action, component, owner, call, method, here)
    elif _is_hole(call):
        why = "fetch no da el método en los facts (hueco declarado)" if last(call["name"]) == "fetch" else "la URL no es un literal con / inicial (hueco declarado: template con expresiones, variable o llamada no canónica)"
        plan.not_derived.append(f"{here} {call['name']}: {why}")
    elif depth == 0 and call.get("canonical") and "." not in call["name"]:
        found = functions.get(call["name"], [])
        if len(found) != 1:
            plan.not_derived.append(f"{here} {call['name']}: {'ninguna función' if not found else 'más de una función'} de los facts del frontend con ese nombre; no se sigue la llamada")
            return
        for inner in found[0]["attrs"].get("calls") or []:
            _call(plan, facts, functions, operations, action, component, found[0], inner, depth=1)


def _resolve(plan, operations, action, component, owner, call, method, here) -> None:
    wanted = normalize(call["first_arg"])
    matches = [o for o in operations if o.fields["method"] == method and normalize(o.fields["route"]) == wanted]
    if len(matches) != 1:
        reason = "ninguna ApiOperationDoc del grafo con ese método y ruta (brecha hacia un endpoint ausente)" if not matches else "más de una ApiOperationDoc del grafo casa"
        plan.not_derived.append(f"{here} {call['name']}({call['first_arg']!r}): {reason}: {method} {call['first_arg']}")
        return
    facts = [owner] if owner is component else [component, owner]
    plan.edge("invokes", action, matches[0], INVOKES, facts, f"La llamada {call['name']} (línea {call['line']}) es {method} {call['first_arg']}, que casa con {matches[0].fields['title']}.")
