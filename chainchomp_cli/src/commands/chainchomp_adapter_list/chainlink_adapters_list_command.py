import click
from click import style, echo

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.adapter.AdapterFolderHandler import AdapterFolderHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:adapter:list')
def adapter_list():
    """
    List all adapters that are currently known
    to be installed for chainchomp
    """
    list_of_installed_adapters = AdapterFolderHandler.provide_list_of_installed_adapters()
    echo(style('Installed Adapters: \n', fg=MessageColors.INFO))
    echo(style('\n'.join(map(str, list_of_installed_adapters)), MessageColors.INFO))
