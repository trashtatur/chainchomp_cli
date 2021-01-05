import os

import click

from chainchomp_cli.src.handlers.environment.EnvironmentWriterHandler import EnvironmentWriterHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:environment:create')
@click.argument('name')
@click.argument('value')
def create_environment_variable(name: str, value: str):
    """
    Registers an adapter
    :param name: The name of the adapter
    :param value: The path to the adapters root folder. Default is current directory
    """
    EnvironmentWriterHandler.create_environment_variable(name, value)
