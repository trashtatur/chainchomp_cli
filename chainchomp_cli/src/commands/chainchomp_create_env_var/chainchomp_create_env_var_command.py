import os

import click
from click import echo, style

from chainchomp_cli.src.cli import MessageColors
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
    echo(style('Creating new environment variable file...', MessageColors.INFO))
    created = EnvironmentWriterHandler.create_environment_variable(name, value)
    if not created:
        echo(style(f'Could not create environment variable {name}...', MessageColors.ERROR))
        return

    echo(style(f'Successfully created environment variable {name}', MessageColors.SUCCESS))
    activate_now = click.confirm(
        style(
            'Do you want to activate it immediately? Else it gets activated on chainchomps next start',
            MessageColors.PROMPT
        ),
        default=True
    )
    if activate_now:
        os.environ[name] = value
        echo(style(f'Successfully activated environment variable {name}', MessageColors.SUCCESS))
