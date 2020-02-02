import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from project_manager.project import Projects


if __name__ == '__main__':
    Projects.load_projects()
    projects = Projects('This is a handy project manager')

    projects()