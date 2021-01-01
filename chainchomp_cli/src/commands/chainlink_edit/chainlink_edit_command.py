import os

import click
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel
from chainchomplib.data import PathProvider
from click import echo, style

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.config_file.ConfigReadHandler import ConfigReadHandler
from chainchomp_cli.src.handlers.config_file.ChainfileWriterHandler import ChainfileWriterHandler
from chainchomp_cli.src.handlers.projects.ProjectFileHandler import ProjectFileHandler
from chainchomp_cli.src.handlers.setup import SetupHandler


@SetupHandler.is_setup
@click.command('chainlink:edit')
@click.argument('path', default=os.getcwd())
def chainlink_edit(path):
    """
    parameters:
    path: Absolute path to the config file. Defaults to current working directory

    This command allows you to edit a Chainfile at a given location.
    Chainchomp will look for a file called "chainfile.yml" here.
    If you provide the file directly, through a path, it will also work.
    If it can't be found the command won't do anything.

    If the file is found Chainchomp will allow you to edit it through command prompts
    :return:
    """
    echo(style('Attempting to read the provided path for the chainlink file', fg=MessageColors.INFO))

    config_model = ConfigReadHandler.read_config_file(path)

    if config_model is None:
        echo(style('Could not read the provided chainfile or could not find it in the provided path',
                   fg=MessageColors.ERROR))
        return

    echo(
        style(
            'You will now be asked about individual changes you might want to make. '
            'To skip one just press enter when asked to change something',
            fg=MessageColors.INFO
        )
    )

    project = click.prompt(
        style(
            'If you want to reassign the chainlink to another project please type the name in now:',
            fg=MessageColors.PROMPT
        )
    )

    if project:
        config_model.project_name = project
        ProjectFileHandler.remove_chainlink_from_all_projects(config_model.chainlink_name)
        if not os.path.isfile(os.path.join(PathProvider.projects_folder(), project)):
            new_project = click.confirm(
                style(
                    'The project you chose does not exist yet. Should chainchomp create it?:',
                    fg=MessageColors.PROMPT
                )
            )
            if new_project:
                echo(
                    style('The project is being created and the chainlink will be added to it', fg=MessageColors.INFO)
                )
                project_created = ProjectFileHandler.create_new_project(project, [config_model.chainlink_name])
                if project_created:
                    echo(
                        style(
                            'The project has been created successfully and the chainlink was added.',
                            fg=MessageColors.SUCCESS
                        )
                    )
                if not project_created:
                    echo(style(f'Chainchomp could not create the project "{project}".', fg=MessageColors.ERROR))
            else:
                echo(
                    style(
                        f'Chainchomp will ignore all project settings now. '
                        f'Please consider this and maybe rerun this command or another more suited command',
                        fg=MessageColors.WARNING
                    )
                )

        else:
            ProjectFileHandler.add_chainlink_to_project(config_model.chainlink_name, project)

    name = click.prompt(
        style('If you want to rename the chainlink please type the name in now:', fg=MessageColors.PROMPT)
    )
    if name:
        config_model.chainlink_name = name

    next_link = click.prompt(
        style('If you want to set a next chainlink please type it in now:', fg=MessageColors.PROMPT)
    )

    if next_link:
        config_model.next_link = next_link

    previous_link = click.prompt(
        style('If you want to set a previous chainlink please type it in now:', fg=MessageColors.PROMPT)
    )

    if previous_link:
        config_model.previous_link = previous_link

    start = click.prompt(
        style('If you want to set a start script please type it in now:', fg=MessageColors.PROMPT)
    )

    if start:
        config_model.start = start

    stop = click.prompt(
        style('If you want to set a stop script please type it in now:', fg=MessageColors.PROMPT)
    )

    if stop:
        config_model.stop = stop

    adapter = click.prompt(
        style('If you want to change the adapter that is used please type that in now', fg=MessageColors.PROMPT)
    )

    if adapter:
        config_model.adapter = adapter

    profile = click.prompt(
        style('If you want to change the profile that is used please type that in now', fg=MessageColors.PROMPT)
    )

    if profile:
        config_model.profile = profile

    echo(style('Attempting to write new information to chainfile...', fg=MessageColors.INFO))
    edit_chainfile(config_model, path)


def edit_chainfile(chainlink_config_model: ChainfileModel, path: str):
    actual_path = path
    if os.path.isfile(path):
        actual_path = os.path.dirname(path)
    echo(style('Now editing the chainfile...', fg=MessageColors.INFO))
    file_created = ChainfileWriterHandler.write_chainfile(chainlink_config_model, actual_path, True)
    if file_created is None:
        echo(style(f'Could not overwrite chainfile', fg=MessageColors.WARNING))
    if not file_created:
        echo(style(f'Failed to write the chainfile to: {path}', fg=MessageColors.ERROR))
    else:
        echo(style(f'Successfully edited chainfile in: {actual_path}', fg=MessageColors.SUCCESS))
