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
def adapter_list(name: str, path: str):
    """
    Registers an adapter
    :param name: The name of the adapter
    :param path: The path to the adapters root folder. Default is current directory
    """
    list_of_installed_adapters = AdapterFolderHandler.provide_list_of_installed_adapters()
    echo(style('Installed Adapters: \n', fg=MessageColors.INFO))
    echo(style('\n'.join(map(str, list_of_installed_adapters)), fg='cyan'))
