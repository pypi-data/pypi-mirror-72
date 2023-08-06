import importlib
import pkgutil
import sys

import log

def main():
    log.init()

    target = sys.argv[-1]

    while True:
        module = get_module(target)
        if module:
            break
        target = input(": ")

    module.main()


def get_module(target):
    package = importlib.import_module(__package__)
    modules = list(pkgutil.iter_modules(package.__path__))

    choices = [m.name for m in modules]
    if target == __package__:
        print(f"<package> not provided, choices: {choices}")
        return None

    if target not in choices:
        print(f"{target!r} not found, choices: {choices}")
        return None

    return importlib.import_module(f'{__package__}.{target}')


if __name__ == "__main__":
    main()
