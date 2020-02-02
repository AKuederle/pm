from pathlib import Path

import click

import sys

sys.path.append(str(Path(__file__).parent.parent))
from project_manager.register import register_new_project


@click.group()
def pm():
    pass


@pm.command()
@click.argument('name', nargs=1, required=True)
@click.argument('path', nargs=1, required=False)
def register(name, path):
    register_new_project(name, path=None)


def main():
    pm()


if __name__ == '__main__':
    main()
