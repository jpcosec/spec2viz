from copy import deepcopy
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz import load, validate, compile_ir, render, json_schema
from spec2viz.cli import main
from spec2viz.exceptions import ParseError, ValidationError
from spec2viz.ir import ClassIR
from spec2viz.linters.mermaid import lint_mermaid, mmdc_path
from spec2viz.models.class_diagram import ClassDiagram

EXAMPLE = Path('examples/class/runtime.yml')


def raw():
    return yaml.safe_load(EXAMPLE.read_text())


def test_schema_and_compiler_preserve_structured_signatures():
    diagram = load(EXAMPLE)
    validate(diagram)
    ir = compile_ir(diagram)
    assert isinstance(ir, ClassIR)
    method = ir.classes[0].methods[0]
    assert method.name == 'execute'
    assert [(p.name, p.type) for p in method.parameters] == [
        ('context', 'ExecutionContext'), ('input', 'PortValues')]
    assert method.returns == 'ExecutionResult'
    assert ir.classes[1].attributes[0].visibility == 'private'
    assert ir.relations[1].to_multiplicity == '1'
    schema = json_schema('class')
    assert schema['properties']['type']['const'] == 'class'
    assert schema['$defs']['ClassMethod']['additionalProperties'] is False
    assert 'class' in json_schema()['discriminator']['mapping']


def test_backends_preserve_realization_direction_and_generic_types():
    ir = compile_ir(load(EXAMPLE))
    mermaid = render(ir)
    plantuml = render(ir, 'plantuml')
    assert mermaid.startswith('classDiagram')
    assert 'DataNode ..|> ExecutableNode' in mermaid
    assert 'DataNode ..|> ExecutableNode' in plantuml
    assert '+List~InputPort~ inputs' in mermaid
    assert '+inputs: List<InputPort>' in plantuml
    assert '+execute(context: ExecutionContext, input: PortValues)* ExecutionResult' in mermaid
    assert '{abstract} +execute(context: ExecutionContext, input: PortValues): ExecutionResult' in plantuml


@pytest.mark.parametrize('mutate,match', [
    (lambda d: d['data']['relations'][0].update(to='Missing'), 'unknown class'),
    (lambda d: d['data']['relations'][0].update(to='NodeSpec'), 'interface or protocol'),
    (lambda d: d['data']['relations'][0].update(to='DataNode'), 'itself'),
    (lambda d: d['data']['relations'][0].update(to_multiplicity='1'), 'multiplicities'),
    (lambda d: d['data']['relations'][1].update(to_multiplicity='3..1'), 'Inverted'),
    (lambda d: d['data']['classes']['DataNode']['attributes'].append({'name':'spec','type':'Other'}), 'Duplicate attribute'),
    (lambda d: d['data']['classes']['DataNode']['methods'].append(deepcopy(d['data']['classes']['DataNode']['methods'][0])), 'Duplicate method'),
    (lambda d: d['data']['classes']['DataNode']['methods'][0]['parameters'].append({'name':'input','type':'Other'}), 'Duplicate parameter'),
    (lambda d: d['data']['classes']['ExecutableNode']['methods'][0].update(static=True), 'static and abstract'),
])
def test_semantic_errors_are_rejected(mutate, match):
    data = raw()
    mutate(data)
    with pytest.raises(ValidationError, match=match):
        validate(ClassDiagram.model_validate(data))


def test_inheritance_cycle_is_rejected_but_dependency_cycles_are_allowed():
    data = raw()
    data['data']['relations'] = [
        {'from':'DataNode', 'to':'NodeSpec', 'relation':'inheritance'},
        {'from':'NodeSpec', 'to':'DataNode', 'relation':'inheritance'},
    ]
    with pytest.raises(ValidationError, match='cycle'):
        validate(ClassDiagram.model_validate(data))
    for relation in data['data']['relations']:
        relation['relation'] = 'dependency'
    validate(ClassDiagram.model_validate(data))


def test_overloads_with_distinct_parameter_types_are_allowed():
    data = raw()
    overload = deepcopy(data['data']['classes']['DataNode']['methods'][0])
    overload['parameters'][1]['type'] = 'OtherInput'
    data['data']['classes']['DataNode']['methods'].append(overload)
    validate(ClassDiagram.model_validate(data))


@pytest.mark.parametrize('mutate', [
    lambda d: d['data']['classes'].update({'bad-id': {}}),
    lambda d: d['data']['classes']['DataNode']['methods'][0].update(returnz='Typo'),
    lambda d: d['data']['classes']['DataNode']['methods'][0].update(name='run\n}'),
    lambda d: d['data']['classes']['DataNode']['attributes'][0].update(type='Type\nOther'),
    lambda d: d['data']['relations'][0].update(relation='implements'),
    lambda d: d['data']['relations'][1].update(to_multiplicity='many'),
])
def test_invalid_schema_fails_at_load(tmp_path, mutate):
    data = raw()
    mutate(data)
    path = tmp_path / 'invalid.yml'
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ParseError, match='Invalid diagram schema'):
        load(path)


def test_cli_schema_validate_render_and_catalog(tmp_path, monkeypatch):
    # Real renderer integration is checked separately below.
    monkeypatch.setenv('SPEC2VIZ_MMDC', '0')
    runner = CliRunner()
    for args in [
        ['diagram', 'schema', '--type', 'class', '--out', str(tmp_path/'class.schema.json')],
        ['diagram', 'validate', str(EXAMPLE)],
        ['diagram', 'render', str(EXAMPLE), '--out', str(tmp_path)],
        ['diagram', 'render', str(EXAMPLE), '--backend', 'plantuml', '--out', str(tmp_path)],
    ]:
        result = runner.invoke(main, args)
        assert result.exit_code == 0, result.output
    assert (tmp_path/'runtime.mmd').exists()
    assert (tmp_path/'runtime.puml').exists()
    config = tmp_path/'catalog.yml'
    config.write_text(yaml.safe_dump({'diagram_store':{'items':[
        {'id':'runtime', 'type':'class', 'src':'runtime.mmd', 'specs':[str(EXAMPLE.resolve())]}
    ]}}))
    result = runner.invoke(main, ['catalog','build','--config',str(config),'--out',str(tmp_path/'index.html')])
    assert result.exit_code == 0, result.output
    assert 'data-type="class"' in (tmp_path/'index.html').read_text()


@pytest.mark.skipif(mmdc_path() is None, reason='Mermaid CLI is not installed')
def test_real_mermaid_engine_accepts_members_kinds_and_all_relations():
    data = raw()
    data['data']['classes']['DataNode']['attributes'].append(
        {'name':'instances','type':'Integer','static':True,'visibility':'protected'})
    data['data']['classes']['DataNode']['methods'].append(
        {'name':'create','static':True,'returns':'DataNode','visibility':'package'})
    for kind in ['class','interface','abstract','record','protocol','enum']:
        data['data']['classes'][f'Kind_{kind}'] = {'kind':kind}
    for relation in ['inheritance','composition','aggregation','association','dependency']:
        edge = {'from':'DataNode','to':'NodeSpec','relation':relation,'label':'contract & data'}
        if relation != 'inheritance':
            edge.update(from_multiplicity='1',to_multiplicity='0..*')
        data['data']['relations'].append(edge)
    diagram = ClassDiagram.model_validate(data)
    validate(diagram)
    assert lint_mermaid(render(compile_ir(diagram))) == []
