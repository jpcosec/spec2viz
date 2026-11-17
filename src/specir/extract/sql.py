"""Rule `sql-create-table`: the tables of the SQL files, with their columns and keys, read from the
`table`, `column` and `constraint` facts of sldb (a primary key is `attrs.primary_key` of its
column, the others `constraint_type` facts with `columns` and `references`)."""

from __future__ import annotations

from specir.extract.facts import Fact, Facts
from specir.extract.plan import Planned, node_name, sentence

RULE = "sql-create-table"
SCHEMA_UNKNOWN = "el SQL leído no dice el esquema de la tabla"


def column_text(column: Fact) -> str:
    attrs = column["attrs"]
    extras = [word for key, word in (("primary_key", "PK"), ("identity", "identity")) if attrs.get(key)]
    return " ".join([column["qualified_name"].split(".", 1)[1], attrs.get("type", ""), *extras]).strip()


def constraint_text(constraint: Fact) -> str:
    attrs = constraint["attrs"]
    text = f"{attrs['constraint_type']} {constraint['qualified_name'].split('.', 1)[1]} ({', '.join(attrs.get('columns') or [])})"
    reference = attrs.get("references")
    return f"{text} -> {reference['table']} ({', '.join(reference['columns'])})" if reference else text


def tables(facts: Facts) -> dict[str, Planned]:
    """One TableDoc per `table` fact, by table name; observado, because a table, its columns and its
    keys are read as they are written."""
    planned: dict[str, Planned] = {}
    for table in facts.of_kind("table"):
        columns = facts.members(table, "column")
        constraints = facts.members(table, "constraint")
        used = [table, *columns, *constraints]
        detail = "; ".join([*(column_text(c) for c in columns), *(constraint_text(c) for c in constraints)])
        name = table["qualified_name"]
        description = f"{sentence(RULE, used, derived=False)} Columnas y claves: {detail}."
        fields = {
            "title": name, "description": description, "schema_name": None, "desconocidos": {"schema_name": SCHEMA_UNKNOWN},
            "columns": [c["qualified_name"].split(".", 1)[1] for c in columns],
        }
        planned[name] = Planned("TableDoc", node_name("TableDoc", name), fields, "observado", RULE, used)
    return planned
