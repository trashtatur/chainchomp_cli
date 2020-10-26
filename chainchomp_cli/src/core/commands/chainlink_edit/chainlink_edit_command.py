import os

import click
from chainchomplib.configlayer.model.ChainlinkConfigModel import ChainlinkConfigModel
from click import echo, style

from chainchomp_cli.src.MessageColorEnum import MessageColorEnum
from chainchomp_cli.src.core.handlers.config_file.ConfigReadHandler import ConfigReadHandler
from chainchomp_cli.src.core.handlers.config_file.ConfigWriterHandler import ConfigWriterHandler
from chainchomp_cli.src.core.handlers.projects.ProjectFileHandler import ProjectFileHandler
from chainchomp_cli.src.core.handlers.setup.SetupHandler import SetupHandler


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
    echo(style('Attempting to read the provided path for the chainlink file', fg=MessageColorEnum.INFO))

    config_model = ConfigReadHandler.read_config_file(path)

    if config_model is None:
        echo(style('Could not read the provided chainfile or could not find it in the provided path',
                   fg=MessageColorEnum.ERROR))
        return

    echo(
        style(
            'You will now be asked about individual changes you might want to make. '
            'To skip one just press enter when asked to change something',
            fg=MessageColorEnum.INFO
        )
    )

    project = click.prompt(
        style(
            'If you want to reassing the chainlink to another project please type the name in now:',
            fg=MessageColorEnum.PROMPT
        )
    )

    if project:
        config_model.project_name = project
        # TODO Remove from old project
        add_to_project(project, config_model.chainlink_name)

    name = click.prompt(
        style('If you want to rename the chainlink please type the name in now:', fg=MessageColorEnum.PROMPT)
    )
    if name:
        config_model.chainlink_name = name

    next_link = click.prompt(
        style('If you want to set a next chainlink please type it in now:', fg=MessageColorEnum.PROMPT)
    )

    if next_link:
        config_model.next_link = next_link

    previous_link = click.prompt(
        style('If you want to set a previous chainlink please type it in now:', fg=MessageColorEnum.PROMPT)
    )

    if previous_link:
        config_model.previous_link = previous_link

    start = click.prompt(
        style('If you want to set a start script please type it in now:', fg=MessageColorEnum.PROMPT)
    )

    if start:
        config_model.start = start

    stop = click.prompt(
        style('If you want to set a stop script please type it in now:', fg=MessageColorEnum.PROMPT)
    )

    if stop:
        config_model.stop = stop

    master_link = click.confirm(
        style('Is this a master link', fg=MessageColorEnum.PROMPT),
        default=config_model.is_master_link
    )

    if master_link != config_model.is_master_link:
        config_model.is_master_link = master_link

    adapter = click.prompt(
        style('If you want to change the adapter that is used please type that in now', fg=MessageColorEnum.PROMPT)
    )

    if adapter:
        config_model.mq_type = adapter

    profile = click.prompt(
        style('If you want to change the profile that is used please type that in now', fg=MessageColorEnum.PROMPT)
    )

    if profile:
        config_model.profile = profile

    echo(style('Attempting to write new information to chainfile...', fg=MessageColorEnum.INFO))
    edit_chainfile(config_model, path)


def add_to_project(project_name: str, chainlink_name: str):
    project_file_handler = ProjectFileHandler()
    project_file_handler.add_chainlink_to_project(chainlink_name, project_name)


def edit_chainfile(chainlink_config_model: ChainlinkConfigModel, path: str):
    actual_path = path
    if os.path.isfile(path):
        actual_path = os.path.dirname(path)
    echo(style('Now editing the chainfile...', fg=MessageColorEnum.INFO))
    file_created = ConfigWriterHandler.write_config_file(chainlink_config_model, actual_path, True)
    if file_created is None:
        echo(style(f'Could not overwrite chainfile', fg=MessageColorEnum.WARNING))
    if not file_created:
        echo(style(f'Failed to write the chainfile to: {path}', fg=MessageColorEnum.ERROR))
    else:
        echo(style(f'Successfully edited chainfile in: {actual_path}', fg=MessageColorEnum.SUCCESS))
