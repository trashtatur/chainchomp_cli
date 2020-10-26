import inspect

import click
from chainchomplib.data import PathProvider
from click import echo, style

from chainchomp_cli.src.MessageColorEnum import MessageColorEnum
from chainchomp_cli.src.core.handlers.adapter.AdapterFolderHandler import AdapterFolderHandler
from chainchomp_cli.src.core.handlers.environmnent.EnvironmentFolderHandler import EnvironmentFolderHandler
from chainchomp_cli.src.core.handlers.fixtures.FixturesFolderHandler import FixturesFolderHandler
from chainchomp_cli.src.core.handlers.profiles.ProfilesFolderHandler import ProfilesFolderHandler
from chainchomp_cli.src.core.handlers.projects.ProjectsFolderHandler import ProjectsFolderHandler
from chainchomp_cli.src.core.handlers.setup.SetupHandler import SetupHandler


@click.command('setup')
def setup():
    click.confirm(style('Welcome to Chainchomp. Do you want to run the setup?', fg=MessageColorEnum.INFO), abort=True)

    with click.progressbar(
            length=len(inspect.getmembers(PathProvider, inspect.isfunction)),
            label='Running setup...'
    ) as bar:
        click.echo(style('Creating the base chainchomp folder if it does not already exist', fg=MessageColorEnum.INFO))
        created_base_config_folder = SetupHandler.create_base_folder()
        if created_base_config_folder:
            click.echo(style('Created base chainchomp folder in path:', fg=MessageColorEnum.INFO))
            click.echo(style(f'{PathProvider.base_config_folder()}', fg=MessageColorEnum.INFO))
        if not created_base_config_folder:
            click.echo(style('Base config folder already exists. Moving on', fg=MessageColorEnum.WARNING))
        bar.update(1)

        click.echo(style('Creating the projects folder if it does not already exist', fg=MessageColorEnum.INFO))
        created_project_folder = ProjectsFolderHandler.create_projects_folder()
        if created_project_folder:
            click.echo(style('Created projects folder in path:', fg=MessageColorEnum.INFO))
            click.echo(style(f'{PathProvider.projects_folder()}', fg=MessageColorEnum.INFO))
        if not created_project_folder:
            click.echo(style('Projects folder already exists. Moving on', fg=MessageColorEnum.WARNING))
        bar.update(1)

        click.echo(style('Creating folder for environments if it does not already exist', fg=MessageColorEnum.INFO))
        created_environments_folder = EnvironmentFolderHandler.create_environments_folder()
        if created_environments_folder:
            click.echo(style('Created environments folder in path:', fg=MessageColorEnum.INFO))
            click.echo(style(f'{PathProvider.env_var_folder()}', fg=MessageColorEnum.INFO))
        if not created_environments_folder:
            click.echo(style('Environments folder already exists. Moving on', fg=MessageColorEnum.WARNING))
        bar.update(1)

        click.echo(style('Creating folder for profiles if it does not already exist', fg=MessageColorEnum.INFO))
        created_profiles_folder = ProfilesFolderHandler.create_profiles_folder()
        if created_profiles_folder:
            click.echo(style('Created profiles folder in path:', fg=MessageColorEnum.INFO))
            click.echo(style(f'{PathProvider.profiles_folder()}', fg=MessageColorEnum.INFO))
        if not created_profiles_folder:
            click.echo(style('Profiles folder already exists. Moving on', fg=MessageColorEnum.WARNING))
        bar.update(1)

        click.echo(
            style('Creating folder for installed adapters if it does not already exist', fg=MessageColorEnum.INFO)
        )
        created_adapters_folder = AdapterFolderHandler.create_adapter_folder()
        if created_adapters_folder:
            click.echo(style('Created adapters folder in path:', fg=MessageColorEnum.INFO))
            click.echo(style(f'{PathProvider.installed_adapters_folder()}', fg=MessageColorEnum.INFO))
        if not created_adapters_folder:
            click.echo(style('Adapters folder already exists. Moving on', fg=MessageColorEnum.WARNING))
        bar.update(1)

        click.echo(style('Creating folder for fixtures if it does not already exist', fg=MessageColorEnum.INFO))
        created_fixtures_folder = FixturesFolderHandler.create_fixtures_folder()
        if created_fixtures_folder:
            click.echo(style('Created fixtures folder in path:', fg=MessageColorEnum.INFO))
            click.echo(style(f'{PathProvider.fixtures_folder()}', fg=MessageColorEnum.INFO))
        if not created_fixtures_folder:
            click.echo(style('Fixtures folder already exists. Moving on', fg=MessageColorEnum.WARNING))
        bar.update(1)

    click.echo(style('Setup concluded', fg=MessageColorEnum.SUCCESS))
