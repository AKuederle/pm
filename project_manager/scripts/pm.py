from pathlib import Path

import click

import sys

sys.path.append(str(Path(__file__).parent.parent))
from project_manager.register import register_new_project, register_new_cli_command


@click.group()
def pm():
    pass


@pm.command()
@click.argument('name', nargs=1, required=True)
@click.argument('path', nargs=1, required=False)
def register(name, path):
    register_new_project(name, path=path)


@pm.command()
@click.argument('project', nargs=1, required=True)
@click.argument('name', nargs=1, required=True)
@click.argument('command', nargs=1, required=True)
def register_command(project, name, command):
    register_new_cli_command(project, name, command)


def main():
    pm()


if __name__ == '__main__':
    main()
