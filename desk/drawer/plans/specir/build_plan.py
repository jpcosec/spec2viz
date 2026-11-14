"""Refresh the specIR plan view from the DeskOps TaskDocs."""
from __future__ import annotations

from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[4]
PLAN = Path(__file__).resolve().parent
DAG = PLAN / "dag.yaml"


def short_id(task_id: str) -> str:
    match = re.match(r"task-ir(\d+[a-z]?)", task_id)
    if not match:
        raise ValueError(f"Unexpected task id: {task_id}")
    return "IR" + match.group(1)


def section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in text:
        return ""
    value = text.split(marker, 1)[1].split("\n## ", 1)[0].strip()
    return re.sub(r"^_.*?_\s*", "", value, flags=re.S).strip()


def build() -> None:
    dag = yaml.safe_load(DAG.read_text(encoding="utf-8"))
    records = []
    for task_doc in sorted((ROOT / "desk/tasks").glob("task-ir*.md")):
        text = task_doc.read_text(encoding="utf-8")
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        if "task-ir" not in frontmatter.get("id", ""):
            continue
        records.append((task_doc, text, frontmatter, short_id(frontmatter["id"])))
    ids = {frontmatter["id"]: node_id for _, _, frontmatter, node_id in records}
    old = {node["id"]: node for node in dag.get("tasks", [])}
    tasks = []
    for task_doc, text, fm, node_id in records:
        node = old.get(node_id, {})
        goal = section(text, "Goal")
        scope = section(text, "Scope")
        path = section(text, "Implementation Path")
        validation = section(text, "Validation")
        done = section(text, "Done When")
        title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), node_id)
        task_kind = fm.get("task_type", "task.code")
        node.update({
            "id": node_id,
            "task_doc": task_doc.relative_to(ROOT).as_posix(),
            "title": title,
            "kind": {"task.code": "code", "task.docs": "docs", "task.decision": "decision"}.get(task_kind, "code"),
            "node_role": "delivery",
            "parent_id": "ROOT",
            "owner_repo": "specIR",
            "depends_on": [ids[dependency] for dependency in fm.get("depends_on", [])],
            "requires": node.get("requires", []),
            "scope": f"Objetivo:\n{goal}\n\nAlcance:\n{scope}\n\nRuta:\n{path}".strip(),
            "acceptance": f"Terminado cuando:\n{done}\n\nValidación:\n{validation}".strip(),
            "output_scope": fm.get("files", []),
        })
        tasks.append(node)
    dag["tasks"] = tasks
    dag["hierarchy"]["root"]["children"] = [node["id"] for node in tasks]
    dag["source"] = "TaskDocs en desk/tasks son la fuente canónica de contratos y dependencias; build_plan.py regenera aquí su vista DAG y README."
    DAG.write_text(yaml.safe_dump(dag, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    write_readme(dag)


def write_readme(dag: dict) -> None:
    root = dag["hierarchy"]["root"]
    nodes = dag["tasks"]
    lines = [
        "# DAG de specIR", "", root["scope"], "",
        "Los TaskDocs son la fuente canónica de contratos y dependencias. Ejecuta `python desk/drawer/plans/specir/build_plan.py` tras editarlos para refrescar `dag.yaml` y este resumen.",
        "El cierre total también requiere resolver `G_SLDB_PRON_MCP` en el desk de SLDB. Cada tarea conserva sus gates de activación y cierre de DeskOps.",
        "", "## Grafo", "", "```mermaid", "graph TD", '  ROOT["specIR"]'
    ]
    for node in nodes:
        label = node["title"].replace('"', "'")
        lines.extend([f'  {node["id"]}["{node["id"]}: {label}"]', f'  ROOT --> {node["id"]}'])
    for node in nodes:
        for dependency in node["depends_on"]:
            lines.append(f'  {dependency} --> {node["id"]}')
    lines.extend([
        '  G_SLDB_PRON_MCP{{"G_SLDB_PRON_MCP: gate externo sldb"}}',
        "  G_SLDB_PRON_MCP -. requerido para cierre .-> ROOT", "```", "",
        "## Nodos y dependencias", "",
        "| Nodo | TaskDoc | Depende de | Entregables |", "|---|---|---|---|"
    ])
    for node in nodes:
        task_path = Path(node["task_doc"])
        files = "<br>".join(f"`{item}`" for item in node["output_scope"])
        dependencies = ", ".join(node["depends_on"]) or "—"
        link = f"../../../tasks/{task_path.name}"
        lines.append(f'| {node["id"]} | [`{node["task_doc"]}`]({link}) | {dependencies} | {files} |')
    lines.extend([
        "", "## Gate entre repositorios", "",
        "`G_SLDB_PRON_MCP` representa el trabajo de SLDB para integrar y exponer las capacidades de pron mediante la API pública/MCP de SLDB. IR01 registra el contrato faltante y prepara el handoff al desk propietario. specIR no importa pron ni implementa cambios de sldb. El gate condiciona el cierre del plan, sin bloquear tareas locales que puedan avanzar con la API actual.",
        "", "## Cierre del plan", "",
        "El plan está completo cuando todos los TaskDocs hijos están cerrados con su evidencia/closeout de DeskOps, IR13 demuestra cobertura y migración de consumidores antes de proponer retirar spec2viz, y `G_SLDB_PRON_MCP` tiene la evidencia declarada en `dag.yaml`. No se requiere un artefacto agregado aparte de los recibos de cierre y el acta IR13."
    ])
    (PLAN / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
