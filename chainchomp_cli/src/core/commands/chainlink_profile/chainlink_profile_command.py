import click

from chainchomp_cli.src.core.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:profile')
def chainchomp_profile():
    pass
