import click

from .core import _normalize


@click.group()
def main():
    pass


@main.command("greet")
@click.argument("name")
def greet(name):
    _normalize(name)
