import json
import sys
import shlex
from typing import Optional

import click

from project_manager import CONFIG


def shell_task(command: str, comment: Optional[str] = None) -> None:
    if comment:
        click.echo('echo {}'.format(shlex.quote(comment)))
    click.echo(command)
    sys.exit(42)


def load_project(name):
    from project_manager.project import Project
    return Project.from_json(json.loads((CONFIG / (name + '.json')).open('r')))