import json
import sys
import shlex
from typing import Optional, Dict

import click

from project_manager import PROJECT_CONFIG_DIR


def shell_task(command: str, comment: Optional[str] = None) -> None:
    if comment:
        click.echo('echo {}'.format(shlex.quote(comment)))
    click.echo(command)
    sys.exit(42)


def shell_command(name: str, command: str, comment: Optional[str] = None):
    @click.command(
        name=name,
        add_help_option=False,
        context_settings=dict(
            ignore_unknown_options=True,
        ))
    @click.argument('command-args', nargs=-1, type=click.UNPROCESSED)
    def out_command(command_args):
        command_with_args = command
        if command_args:
            command_with_args = '{} {}'.format(command, ' '.join(command_args))
        shell_task(command_with_args, comment)

    return out_command


def project_config(name):
    return PROJECT_CONFIG_DIR / (name + '.json')


def load_project(name):
    from project_manager.project import Project
    return Project.from_json(json.load(project_config(name).open('r')))


def load_all_projects() -> Dict[str, 'Project']:
    from project_manager.project import Project
    projects = dict()
    for pconf in PROJECT_CONFIG_DIR.glob('*.json'):
        with pconf.open('r') as f:
            config = json.load(f)
            p = Project.from_json(config)
            projects[p.name] = p
    return projects
