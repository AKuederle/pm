import json
import shlex
from pathlib import Path
from typing import Dict, TypeVar, Type, Optional

import click as click

from project_manager import ACTIVATE_SHELL_VAR
from project_manager.manage import manage
from project_manager.util import shell_task, load_all_projects

T = TypeVar('T')

swap_script = shlex.quote(str((Path(__file__).parent / 'scripts/swap_prompt.sh').expanduser().resolve(strict=True)))


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
            'activate': self.activate,
            'deactivate': self.deactivate,
        }
        for name, c in commands.items():
            self.add_command(click.command(name, help=c.__doc__)(c))

        # register management group
        self.add_command(manage, name='_')

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

    def activate(self):
        """Activate the current project, so that it is used for all further commands."""
        command = 'export {}={} && . {}'.format(ACTIVATE_SHELL_VAR, shlex.quote(self.name), swap_script)
        comment = 'Activating project "{}"\nUse "p deactivate" to deactivate.'.format(self.name)
        shell_task(command, comment=comment)

    def deactivate(self):
        """Deactivate the current project."""
        command = 'unset {} && . {}'.format(ACTIVATE_SHELL_VAR, swap_script)
        shell_task(command)


class Projects(click.Group):
    projects: Dict[str, Project]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # register management group
        from project_manager.project_management import project_manage
        self.add_command(project_manage, name='_')

        self.load_projects()

    def load_projects(self):
        self.projects = load_all_projects()
        for p in self.projects.values():
            self.add_command(p)
