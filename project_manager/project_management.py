from pathlib import Path

import click

from project_manager import CONFIG
from project_manager.project import Project


def register_new_project(name, path):
    p = Project(name, path=path)
    pconf = p.to_json()

    config_file = CONFIG / Path(name + '.json')
    if config_file.is_file():
        raise ValueError('A project with this name already exists')

    with config_file.open('w') as f:
        f.write(pconf)


@click.group(name='_' )
def project_manage():
    pass


@project_manage.command()
@click.argument('name', nargs=1, required=True)
@click.argument('path', nargs=1, required=False)
def register(name, path):
    register_new_project(name, path=path)