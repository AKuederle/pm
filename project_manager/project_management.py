from pathlib import Path

import click

from project_manager import PROJECT_CONFIG_DIR
from project_manager.project import Project


def register_new_project(name, path):
    p = Project(name, path=str(Path(path).expanduser().resolve()))
    pconf = p.to_json()

    config_file = PROJECT_CONFIG_DIR / Path(name + '.json')
    if config_file.is_file():
        raise ValueError('A project with this name already exists')

    with config_file.open('w') as f:
        f.write(pconf)


@click.group(name='_')
def project_manage():
    pass


@project_manage.command()
@click.argument('name', nargs=1, required=True)
@click.argument('path', nargs=1, required=False)
def register(name, path):
    register_new_project(name, path=path)
