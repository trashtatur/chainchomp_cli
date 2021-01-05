import os

import click
from click import echo, style

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.chainlink.ChainlinkRegistrationHandler import ChainlinkRegistrationHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainlink:register')
@click.argument('chainlink_path', default=os.getcwd())
def chainlink_start(chainlink_path):
    """
    This command attempts to register a chainlink

    params:

    chainfile: The full path to the chainfile. Defaults to the current directory where it expects a chainfile.yml
    """
    echo(style(f'Now attempting to register the chainlink that sits at path {chainlink_path}', MessageColors.INFO))
    registered = ChainlinkRegistrationHandler.register_chainlink(chainlink_path)
    if registered:
        echo(style(f'Successfully registered the chainlink that is at {chainlink_path}', MessageColors.SUCCESS))
        return
    echo(style(f'Failed to register the chainlink that is at {chainlink_path}', MessageColors.ERROR))
