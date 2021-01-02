import os

import click
from chainchomplib.configlayer.resolver.ChainfileResolver import ChainfileResolver

from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainlink:stop')
@click.argument('chainfile', default=os.path.join(os.getcwd(), 'chainfile.yml'))
def chainlink_stop(chainfile):
    """
    This command attempts to call the stop script inside of a chainfile

    params:

    chainfile: The full path to the chainfile. Defaults to the current directory where it expects a chainfile.yml
    """
    chainfile_model = ChainfileResolver().resolve_config_file(chainfile)

    if chainfile_model.stop is None:
        return

    os.system(chainfile_model.stop)
