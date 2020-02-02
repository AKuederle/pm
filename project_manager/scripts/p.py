import os

from project_manager.project import Projects
from project_manager.util import load_project


def main():
    activated_project = os.getenv('_P_CURRENT_PROJECT')
    if activated_project:
        load_project(activated_project)(prog_name='p')
    else:
        Projects('This is a handy project manager')(prog_name='p')


if __name__ == '__main__':
    main()
