from typing import List

import click
from click import echo, style

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.projects.ProjectFileHandler import ProjectFileHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:project:new')
@click.argument('project_name')
@click.option('--chainlinks', '-c', multiple=True, default=[])
def chainchomp_project_new(project_name: str, chainlinks: List[str]):
    echo(style('Creating new project...', fg=MessageColors.INFO))
    created = ProjectFileHandler.create_new_project(project_name, list(chainlinks))
    if not created:
        echo(style('Failed to create project', fg=MessageColors.ERROR))
        return
    echo(style(f'Created project {project_name}', fg=MessageColors.SUCCESS))

