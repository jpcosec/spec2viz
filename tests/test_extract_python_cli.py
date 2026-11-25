"""The Python CLI extractor over tests/fixtures/cli_lib: an argparse command with its handler, a click
command, a public function, a model of Pydantic and a dataclass, and a builder the facts cannot read."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parent / "extract"))

from conftest import REPO  # noqa: E402
from extraction import documents, rules_findings, triples  # noqa: E402

from specir.models import domain  # noqa: F401
from specir.cli import main  # noqa: E402
from specir.extract import extract_python_cli  # noqa: E402
from specir.install import package_pythonpath  # noqa: E402

LAYERS = {"InterfaceControlDoc": "interface", "InterfaceActionDoc": "interface", "ApiOperationDoc": "api", "HandlerDoc": "backend", "DomainOperationDoc": "domain", "DomainEntityDoc": "domain"}
FIXTURE = REPO / "tests" / "fixtures" / "cli_lib"


@pytest.fixture(scope="module")
def project(tmp_path_factory: pytest.TempPathFactory):
    from conftest import sldb

    root = tmp_path_factory.mktemp("cli_lib") / "cli_lib"
    shutil.copytree(FIXTURE, root, ignore=shutil.ignore_patterns("__pycache__"))
    sldb("stores", "init", "--path", str(root), cwd=root)
    done = subprocess.run([sys.executable, "-m", "specir.install", "--store", str(root / ".sldb")], cwd=root, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    return root, extract_python_cli(root)


def payloads(root: Path, model: str) -> dict[str, dict]:
    return {d.payload["title"]: d.payload for k, d in documents(root).items() if k.startswith(f"{model}:")}


def test_argparse_command_is_control_and_action(project):
    root, _ = project
    controls, actions = payloads(root, "InterfaceControlDoc"), payloads(root, "InterfaceActionDoc")
    assert controls["mylib run"]["kind"] == "cli_command" and "mylib run" in actions
    assert "mylib idle" in controls
    assert "mylib.cli.cmd_run" not in controls


def test_handler_operation_and_public_api(project):
    root, _ = project
    assert payloads(root, "HandlerDoc")["mylib.cli.cmd_run"]["framework"] == "argparse"
    assert {"mylib.core.run_thing", "mylib.core._normalize"} >= set(payloads(root, "DomainOperationDoc"))
    assert "mylib.core.run_thing" in payloads(root, "DomainOperationDoc")
    api = payloads(root, "ApiOperationDoc")
    assert set(api) == {"mylib.core.run_thing"}
    assert api["mylib.core.run_thing"].get("method") is None
    assert set(api["mylib.core.run_thing"]["desconocidos"]) == {"method", "route"}


def test_click_command(project):
    root, _ = project
    assert "main greet" in payloads(root, "InterfaceControlDoc")
    assert payloads(root, "HandlerDoc")["mylib.clicmd.greet"]["framework"] == "click"


def test_models_are_entities(project):
    root, _ = project
    assert set(payloads(root, "DomainEntityDoc")) == {"mylib.models.Thing", "mylib.models.Settings"}


def test_edges(project):
    root, _ = project
    assert {
        ("InterfaceControlDoc", "triggers", "InterfaceActionDoc"),
        ("InterfaceActionDoc", "invokes", "ApiOperationDoc"),
        ("ApiOperationDoc", "handled_by", "HandlerDoc"),
        ("HandlerDoc", "executes", "DomainOperationDoc"),
    } <= triples(root)


def test_provenance_layer_and_anchors(project):
    root, _ = project
    nodes = [d for k, d in documents(root).items() if d.model_name in LAYERS]
    assert nodes and all(d.payload["origen"] == "observado" and d.payload["verificacion"] == "sin_verificar" for d in nodes)
    assert all("mylib/" in d.payload["description"] and ".py:" in d.payload["description"] for d in nodes)
    assert {d.model_name for d in nodes} == set(LAYERS)
    for model, layer in LAYERS.items():
        assert domain.__dict__[model].__semantics__["layer"] == [layer]


def test_unknowns_are_named_and_counted(project):
    _, report = project
    text = "\n".join(report.not_derived)
    assert all(item.startswith("desconocido:") for item in report.not_derived)
    assert "mylib/dynamic.py" in text and "sin argumentos" in text
    assert "InterfaceControlDoc:control-" in text and "set_defaults" in text  # `idle` has no handler
    assert len(report.not_derived) == 2


def test_idempotent_and_seeded_rules_run(project):
    root, first = project
    again = extract_python_cli(root)
    assert not again.created and not again.changed and len(again.unchanged) == len(first.created)
    findings = rules_findings(root)
    assert not [f for f in findings if f.get("severity") == "error"], findings


def test_cli_prints_unknowns(project):
    root, _ = project
    result = CliRunner().invoke(main, ["extract", "python-cli", str(root)])
    assert result.exit_code == 0, result.output
    assert "desconocidos: 2" in result.output and "desconocido:" in result.output
