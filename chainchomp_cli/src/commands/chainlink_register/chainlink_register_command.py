import os

import click
from chainchomp_cli.src.handlers.chainlink import ChainlinkRegistrationHandler
from chainchomp_cli.src.handlers.setup import SetupHandler


@SetupHandler.is_setup
@click.command('chainlink:register')
@click.argument('chainlink_path', default=os.getcwd())
def chainlink_start(chainlink_path):
    """
    This command attempts to register a chainlink

    params:

    chainfile: The full path to the chainfile. Defaults to the current directory where it expects a chainfile.yml
    """
    ChainlinkRegistrationHandler.register_chainlink(chainlink_path)
