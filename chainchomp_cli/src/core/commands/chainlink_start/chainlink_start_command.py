import os

import click
from chainchomplib.configlayer.resolver.ChainfileResolver import ChainfileResolver


@click.command('chainlink:start')
@click.argument('chainfile', default=os.path.join(os.getcwd(), 'chainfile.yml'))
def chainlink_start(chainfile):
    """
    This command attempts to call the start script inside of a chainfile

    params:

    chainfile: The full path to the chainfile. Defaults to the current directory where it expects a chainfile.yml
    """
    chainfile_model = ChainfileResolver().resolve_config_file(chainfile)

    if chainfile_model.start is None:
        return

    os.system(chainfile_model.start)
