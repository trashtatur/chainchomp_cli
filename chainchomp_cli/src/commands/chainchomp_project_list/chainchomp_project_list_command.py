import click
from click import style, echo

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.projects.ProjectsFolderHandler import ProjectsFolderHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:project:list')
def project_list():
    """
    List all projects that are currently known
    """
    list_of_installed_projects = ProjectsFolderHandler.provide_list_of_projects()
    echo(style('Projects: \n', fg=MessageColors.INFO))
    echo(style('\n'.join(map(str, list_of_installed_projects)), MessageColors.INFO))
