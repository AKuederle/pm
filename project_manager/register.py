from pathlib import Path

from project_manager import CONFIG
from project_manager.project import Project
from project_manager.util import load_project, project_config


def register_new_project(name, path):
    p = Project(name, path=path)
    pconf = p.to_json()

    config_file = CONFIG / Path(name + '.json')
    if config_file.is_file():
        raise ValueError('A project with this name already exists')

    with config_file.open('w') as f:
        f.write(pconf)
