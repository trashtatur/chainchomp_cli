import os

import click
from click import style, echo

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.environment.EnvironmentFolderHandler import EnvironmentFolderHandler
from chainchomp_cli.src.handlers.environment.EnvironmentWriterHandler import EnvironmentWriterHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:environment:create')
def list_environment_variables():
    """
    Registers an adapter
    :param name: The name of the adapter
    :param value: The path to the adapters root folder. Default is current directory
    """
    list_of_installed_adapters = EnvironmentFolderHandler.provide_list_of_environment_variables()
    echo(style('Configured environment variables: \n', fg=MessageColors.INFO))
    echo(style('\n'.join(map(str, list_of_installed_adapters)), fg=MessageColors.INFO))

