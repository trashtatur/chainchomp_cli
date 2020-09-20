import click
from click import style, echo

from chainchomp_cli.src.core.handlers.adapter.AdapterFolderHandler import AdapterFolderHandler


@click.command('adapter:list')
def adapter_list():
    """
    List all adapters that are currently known
    to be installed for chainchomp
    """
    list_of_installed_adapters = AdapterFolderHandler.provide_list_of_installed_adapters()
    echo(style('Installed Adapters: \n', fg='cyan'))
    echo(style('\n'.join(map(str, list_of_installed_adapters)), fg='cyan'))
