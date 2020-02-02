from pathlib import Path

import click

import sys

from project_manager.manage import register_new_cli_command

sys.path.append(str(Path(__file__).parent.parent))
from project_manager.register import register_new_project


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
@click.option('--use-project-pwd', '-pwd', is_flag=True)
def register_command(project, name, command, use_project_pwd):
    register_new_cli_command(project, name, command, use_project_pwd=use_project_pwd)


def main():
    pm()


if __name__ == '__main__':
    main()
