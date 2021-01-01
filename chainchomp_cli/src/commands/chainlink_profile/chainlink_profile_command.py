import click

from chainchomp_cli.src.handlers.setup import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:profile')
def chainchomp_profile():
    pass
