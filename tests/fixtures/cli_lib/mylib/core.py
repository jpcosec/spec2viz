from .models import Thing


def _normalize(name):
    return name.strip()


def run_thing(name):
    return Thing(name=_normalize(name))
