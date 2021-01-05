import inspect

import click
from chainchomplib.data import PathProvider
from click import style, echo

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.adapter.AdapterFolderHandler import AdapterFolderHandler
from chainchomp_cli.src.handlers.chainlink.ChainlinkFolderHandler import ChainlinkFolderHandler
from chainchomp_cli.src.handlers.environment.EnvironmentFolderHandler import EnvironmentFolderHandler
from chainchomp_cli.src.handlers.logs.LogsFolderHandler import LogsFolderHandler
from chainchomp_cli.src.handlers.logs.LogsWriterHandler import LogsWriterHandler
from chainchomp_cli.src.handlers.profiles.ProfilesFolderHandler import ProfilesFolderHandler
from chainchomp_cli.src.handlers.projects.ProjectsFolderHandler import ProjectsFolderHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@click.command('chainchomp:setup')
def setup():
    click.confirm(style('Welcome to Chainchomp. Do you want to run the setup?', fg=MessageColors.INFO), abort=True)

    with click.progressbar(
            length=len(inspect.getmembers(PathProvider, inspect.isfunction)) - 1,
            label='Running setup...'
    ) as bar:
        echo(style('Creating the base chainchomp folder if it does not already exist', fg=MessageColors.INFO))
        created_base_config_folder = SetupHandler.create_base_folder()
        if created_base_config_folder:
            echo(style('Created base chainchomp folder in path:', fg=MessageColors.INFO))
            echo(style(f'{PathProvider.base_config_folder()}', fg=MessageColors.INFO))
        if not created_base_config_folder:
            echo(style('Base config folder already exists. Moving on', fg=MessageColors.WARNING))
        bar.update(1)

        echo(style('Creating the projects folder if it does not already exist', fg=MessageColors.INFO))
        created_project_folder = ProjectsFolderHandler.create_projects_folder()
        if created_project_folder:
            echo(style('Created projects folder in path:', fg=MessageColors.INFO))
            echo(style(f'{PathProvider.projects_folder()}', fg=MessageColors.INFO))
        if not created_project_folder:
            echo(style('Projects folder already exists. Moving on', fg=MessageColors.WARNING))
        bar.update(1)

        echo(style('Creating folder for environments if it does not already exist', fg=MessageColors.INFO))
        created_environments_folder = EnvironmentFolderHandler.create_environments_folder()
        if created_environments_folder:
            echo(style('Created environments folder in path:', fg=MessageColors.INFO))
            echo(style(f'{PathProvider.environment_variables_folder()}', fg=MessageColors.INFO))
        if not created_environments_folder:
            echo(style('Environments folder already exists. Moving on', fg=MessageColors.WARNING))
        bar.update(1)

        echo(style('Creating folder for registered chainlinks if it does not already exist', fg=MessageColors.INFO))
        created_registered_chainlinks_folder = ChainlinkFolderHandler.create_chainlinks_folder()
        if created_registered_chainlinks_folder:
            echo(style('Registered chainlinks folder in path:', fg=MessageColors.INFO))
            echo(style(f'{PathProvider.chainlinks_folder()}', fg=MessageColors.INFO))
        if not created_registered_chainlinks_folder:
            echo(style('Registered chainlinks folder already exists. Moving on', fg=MessageColors.WARNING))
        bar.update(1)

        echo(style('Creating folder for profiles if it does not already exist', fg=MessageColors.INFO))
        created_profiles_folder = ProfilesFolderHandler.create_profiles_folder()
        if created_profiles_folder:
            echo(style('Created profiles folder in path:', fg=MessageColors.INFO))
            echo(style(f'{PathProvider.profiles_folder()}', fg=MessageColors.INFO))
        if not created_profiles_folder:
            echo(style('Profiles folder already exists. Moving on', fg=MessageColors.WARNING))
        bar.update(1)

        echo(
            style('Creating folder for installed adapters if it does not already exist', fg=MessageColors.INFO)
        )
        created_adapters_folder = AdapterFolderHandler.create_adapter_folder()
        if created_adapters_folder:
            echo(style('Created adapters folder in path:', fg=MessageColors.INFO))
            echo(style(f'{PathProvider.installed_adapters_folder()}', fg=MessageColors.INFO))
        if not created_adapters_folder:
            echo(style('Adapters folder already exists. Moving on', fg=MessageColors.WARNING))
        bar.update(1)

        echo(style('Creating logs folder if it does not already exist', fg=MessageColors.INFO))
        created_log_folder = LogsFolderHandler.create_log_folder()
        if created_log_folder:
            echo(style('Created log folder in path:', fg=MessageColors.INFO))
            echo(style(f'{PathProvider.log_folder()}', fg=MessageColors.INFO))
        if not created_log_folder:
            echo(style('Log folder already created. Moving on', fg=MessageColors.WARNING))
        bar.update(1)
        
        echo(style('Creating logs files if they don\'t already exist', fg=MessageColors.INFO))
        created_log_files = LogsWriterHandler.initiate_log_files()
        if created_log_files:
            echo(style('Created log files in path:', fg=MessageColors.INFO))
            echo(style(f'{PathProvider.log_folder()}', fg=MessageColors.INFO))
        if not created_log_files:
            echo(style(
                'Log folder seems to not exist. Please make sure it exists before running this.',
                fg=MessageColors.WARNING
            ))
        bar.update(1)

    echo(style('Setup concluded', fg=MessageColors.SUCCESS))
