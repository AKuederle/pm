from project_manager.project import Projects


def main():
    Projects.load_projects()
    projects = Projects('This is a handy project manager')

    projects()

if __name__ == '__main__':
    main()