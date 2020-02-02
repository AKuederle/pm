import json
import shlex
from pathlib import Path
from typing import Dict, TypeVar, Type, Optional

import click as click

from project_manager import CONFIG
from project_manager.manage import management
from project_manager.util import shell_task

T = TypeVar('T')


class Project(click.Group):
    name: str
    path: str

    custom_cli_commands: Dict[str, Dict]

    _fields = ['name', 'path', 'custom_cli_commands']

    def __init__(self, name: str, path: str = None, custom_cli_commands: Optional[Dict[str, Dict]] = None):
        # Set context defaults for subcommands to get current project name
        context_settings = dict(obj={'project': name})
        super().__init__(chain=False, name=name, context_settings=context_settings)

        self.path = path
        self.custom_cli_commands = {}
        custom_cli_commands = custom_cli_commands or {}
        for k, v in custom_cli_commands.items():
            self._register_new_cli_command(k, **v)

        commands = {
            'cd': self.cd,
        }
        for name, c in commands.items():
            self.add_command(click.command(name, help=c.__doc__)(c))

        # register management group
        self.add_command(management, name='_')

    def _register_new_cli_command(self, name: str, command: str, help=None, use_project_pwd: bool = False):
        if name in self.custom_cli_commands:
            raise ValueError('A command with this name already exists.')
        full_command = command
        if use_project_pwd is True:
            full_command = self._assemble_cd_command() + ' && ' + command
        self.add_command(click.command(name)(lambda: shell_task(full_command)))
        self.custom_cli_commands[name] = dict(command=command, use_project_pwd=use_project_pwd)

    @classmethod
    def from_json(cls: Type[T], data: Dict) -> T:
        instance = cls(**data)
        return instance

    def to_json(self) -> str:
        dump_dict = {k: getattr(self, k, None) for k in self._fields}
        return json.dumps(dump_dict, indent=4)

    def _assemble_cd_command(self) -> str:
        return "cd " + shlex.quote(str(Path(self.path).expanduser().resolve(strict=True)))

    def cd(self):
        """Switch to the base dir of the project."""
        comment = 'Switching to project dir ({}): "{}"'.format(self.name, self.path)
        shell_task(self._assemble_cd_command(), comment=comment)


class Projects(click.MultiCommand):
    projects: Dict[str, Project]

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
