import os

import click
from click import style, echo

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.adapter.AdapterFolderHandler import AdapterFolderHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:adapter:register')
@click.argument('name')
@click.argument('path', default=os.getcwd())
def adapter_register(name: str, path: str):
    """
    Registers an adapter
    :param name: The name of the adapter
    :param path: The path to the adapters root folder. Default is current directory
    """
    pass
