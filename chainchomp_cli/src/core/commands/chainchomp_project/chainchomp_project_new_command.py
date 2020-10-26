import click
from click import echo, style

from chainchomp_cli.src.MessageColorEnum import MessageColorEnum
from chainchomp_cli.src.core.handlers.projects.ProjectFileHandler import ProjectFileHandler
from chainchomp_cli.src.core.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:project:new')
@click.argument('project_name')
def chainchomp_project_new(project_name: str):
    echo(style('Creating new project...', fg=MessageColorEnum.INFO))
    created = ProjectFileHandler.create_new_project(project_name)
    if not created:
        echo(style('Failed to create project', fg=MessageColorEnum.ERROR))

    echo(style(f'Created project {project_name}', fg=MessageColorEnum.SUCCESS))

