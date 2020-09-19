import inspect

import click
from chainchomplib.data import PathProvider
from click import echo, style

from chainchomp_cli.src.core.handlers.environmnent.EnvironmentFolderHandler import EnvironmentFolderHandler
from chainchomp_cli.src.core.handlers.profiles.ProfilesFolderHandler import ProfilesFolderHandler
from chainchomp_cli.src.core.handlers.projects.ProjectsFolderHandler import ProjectsFolderHandler
from chainchomp_cli.src.core.handlers.setup.SetupHandler import SetupHandler


@click.command('chainchomp:setup')
def chainchomp_setup():
    setup = click.confirm(style('Welcome to Chainchomp. Do you want to run the setup?', fg='cyan'), abort=True)

    with click.progressbar(
            length=len(inspect.getmembers(PathProvider, inspect.ismethod)),
            label='Running setup...'
    ) as bar:
        click.echo(style('Creating the base chainchomp folder if it does not already exist', fg='cyan'))
        created_base_config_folder = SetupHandler.create_base_folder()
        if created_base_config_folder:
            click.echo(style('Created base chainchomp folder in path:', fg='cyan'))
            click.echo(style(f'{PathProvider.base_config_folder()}', fg='cyan'))
        if not created_base_config_folder:
            click.echo(style('Base config folder already exists. Moving on', fg='blue'))
        bar.update(1)
        
        click.echo(style('Creating the projects folder if it does not already exist', fg='cyan'))
        created_project_folder = ProjectsFolderHandler.create_projects_folder()
        if created_project_folder:
            click.echo(style('Created projects folder in path:', fg='cyan'))
            click.echo(style(f'{PathProvider.projects_folder()}', fg='cyan'))
        if not created_project_folder:
            click.echo(style('Projects folder already exists. Moving on', fg='blue'))
        bar.update(2)
        
        click.echo(style('Creating folder for environments if it does not already exist', fg='cyan'))
        created_environments_folder = EnvironmentFolderHandler.create_environments_folder()
        if created_environments_folder:
            click.echo(style('Created environments folder in path:', fg='cyan'))
            click.echo(style(f'{PathProvider.env_var_folder()}', fg='cyan'))
        if not created_environments_folder:
            click.echo(style('Environments folder already exists. Moving on', fg='blue'))
        bar.update(3)

        click.echo(style('Creating folder for profiles if it does not already exist', fg='cyan'))
        created_profiles_folder = ProfilesFolderHandler.create_profiles_folder()
        if created_profiles_folder:
            click.echo(style('Created profiles folder in path:', fg='cyan'))
            click.echo(style(f'{PathProvider.profiles_folder()}', fg='cyan'))
        if not created_profiles_folder:
            click.echo(style('Profiles folder already exists. Moving on', fg='blue'))
        bar.update(4)
