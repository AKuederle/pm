import json
import shlex
from pathlib import Path
from typing import Dict, TypeVar, Type, Optional

import click as click

from project_manager import CONFIG
from project_manager.util import shell_task

T = TypeVar('T')


class Project(click.Group):
    name: str
    path: str

    custom_cli_commands: Dict[str, str]

    _fields = ['name', 'path', 'custom_cli_commands']

    def __init__(self, name: str, path: str = None, custom_cli_commands: Optional[Dict[str, str]] = None):
        super().__init__(chain=False)

        self.name = name
        self.path = path

        if custom_cli_commands:
            self.custom_cli_commands = custom_cli_commands

        custom_cli_commands = getattr(self, 'custom_cli_commands', {})
        custom_cli_commands_objs = {k: lambda: shell_task(v) for k, v in custom_cli_commands.items()}


        commands = {
            'cd': self.cd,
            **custom_cli_commands_objs
        }
        for name, c in commands.items():
            self.add_command(click.command(name, help=c.__doc__)(c))

    @classmethod
    def from_json(cls: Type[T], data: Dict) -> T:
        instance = cls(**data)
        return instance

    def to_json(self) -> str:
        dump_dict = {k: getattr(self, k, None) for k in self._fields}
        return json.dumps(dump_dict, indent=4)

    def cd(self):
        """Switch to the base dir of the project."""
        comment = 'Switching to project dir ({}): "{}"'.format(self.name, self.path)
        shell_task("cd " + shlex.quote(str(Path(self.path).resolve(strict=True))), comment=comment)


class Projects(click.MultiCommand):
    projects: Dict[str, Project]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'p'

    @classmethod
    def load_projects(cls):
        cls.projects = dict()
        for pconf in Path(CONFIG).glob('*.json'):
            with pconf.open('r') as f:
                config = json.load(f)
                p = Project.from_json(config)
                cls.projects[p.name] = p

    def list_commands(self, ctx):
        if not getattr(self, 'projects', None):
            self.load_projects()

        return list(self.projects.keys())

    def get_command(self, ctx, name):
        return self.projects[name]
