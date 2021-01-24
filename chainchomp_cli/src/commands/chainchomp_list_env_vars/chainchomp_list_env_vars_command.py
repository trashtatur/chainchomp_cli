import click
from click import style, echo

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.environment.EnvironmentFolderHandler import EnvironmentFolderHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:environment:list')
def list_environment_variables():
    """
    Lists all environment variables currently registered with chainchomp
    """
    list_of_installed_adapters = EnvironmentFolderHandler.provide_list_of_environment_variables()
    echo(style('Configured environment variables: \n', fg=MessageColors.INFO))
    echo(style('\n'.join(map(str, list_of_installed_adapters)), fg=MessageColors.INFO))

