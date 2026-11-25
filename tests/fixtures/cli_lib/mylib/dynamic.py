import argparse


def build(names):
    parser = argparse.ArgumentParser(prog="dyn")
    sub = parser.add_subparsers()
    for name in names:
        sub.add_parser(name)
    return parser
