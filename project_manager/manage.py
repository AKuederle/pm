import click

from project_manager.util import load_project, project_config


@click.group(name='_')
def manage():
    pass


def register_new_cli_command(pname, *args, **kwargs):
    p = load_project(pname)
    p._register_new_cli_command(*args, **kwargs)

    with project_config(pname).open('w') as f:
        f.write(p.to_json())


@manage.command()
@click.argument('name', nargs=1, required=True)
@click.argument('command', nargs=1, required=True)
@click.option('--use-project-pwd', '-pwd', is_flag=True)
@click.pass_obj
def new_cmd(obj, name, command, use_project_pwd):
    project = obj['project']
    register_new_cli_command(project, name, command, use_project_pwd=use_project_pwd)


@manage.command()
@click.pass_obj
def config_file(obj):
    project = obj['project']
    click.echo(project_config(project))
