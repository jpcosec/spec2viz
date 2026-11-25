import argparse

from .core import run_thing

parser = argparse.ArgumentParser(prog="mylib")
commands = parser.add_subparsers(dest="command")


def cmd_run(args):
    return run_thing(args.name)


run = commands.add_parser("run", help="Run a thing")
run.add_argument("name")
run.set_defaults(func=cmd_run)

# A subcommand with no handler of its own.
idle = commands.add_parser("idle", help="Do nothing")
