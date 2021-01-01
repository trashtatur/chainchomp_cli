import click

from chainchomp_cli.src.handlers.setup import SetupHandler


@SetupHandler.is_setup
@click.command('chainlink:ping')
def chainlink_ping():
    pass
