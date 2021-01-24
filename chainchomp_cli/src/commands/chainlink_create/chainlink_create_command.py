import os
import click
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel
from click import echo, style

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.adapter.AdapterFolderHandler import AdapterFolderHandler
from chainchomp_cli.src.handlers.chainlink.ChainlinkRegistrationHandler import ChainlinkRegistrationHandler
from chainchomp_cli.src.handlers.config_file.ChainfileWriterHandler import ChainfileWriterHandler
from chainchomp_cli.src.handlers.projects.ProjectFileHandler import ProjectFileHandler
from chainchomp_cli.src.handlers.projects.ProjectsFolderHandler import ProjectsFolderHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainlink:create')
@click.argument('path', default=os.getcwd())
@click.option('--force/--soft',
              default=False,
              help='Force overwriting of an existing chainfile'
              )
def chainlink_create(path: str, force: bool):
    """
    This command creates a configuration file for your project.
    The configuration file will be stored at the current working directory
    (which should be your projects root directory) or at the path that you
    specify as a parameter.

    Through this, it gets registered as a chainlink.
    You get the options to let chainchomp handle and set most of the
    options, though you can always change them later.
    :param path: Absolute path to where the config file should be created. Defaults to current working directory
    :param force: If you want to overwrite a chainfile you should provide this parameter
    """

    echo(style('Welcome to Chainchomp. We can see that you want to add a new chainlink', fg=MessageColors.INFO))
    echo(style('What is the project that this chainlink is assigned to', fg=MessageColors.INFO))
    projects_list = ProjectsFolderHandler.provide_list_of_projects()
    user_wants_new_project = False
    project_name = None
    while project_name is None:
        if projects_list:
            output_string = f'Press 0 to make a new project \n'
            counter = 1
            for project in projects_list:
                output_string += f'{counter}) {project} \n'
            echo(style('You can choose from already existing projects, or make a new one', fg=MessageColors.INFO))
            project_name_index = click.prompt(output_string, default=0)
            if project_name_index == 0:
                user_wants_new_project = True
            if project_name_index != 0 and len(projects_list)-1 >= project_name_index:
                project_name = projects_list[project_name_index - 1]
        if not projects_list:
            project_name = click.prompt('Please type in the designated project name now')
    if user_wants_new_project or projects_list == []:
        project_name = click.prompt('Please type in the designated project name now')

    echo(style('Now please provide a name for your chainlink', fg=MessageColors.INFO))
    chainlink_name = click.prompt(style('Please type in the designated name now', MessageColors.PROMPT))
    chainfile_model = ChainfileModel(project_name, chainlink_name)

    more_information = click.confirm(style('Do you want to input further details?', fg=MessageColors.PROMPT),
                                     default=False)
    if not more_information:
        create_chainfile(chainfile_model, path, force)
        create_or_add_to_project(project_name, chainlink_name, user_wants_new_project)
        return

    start_script = click.confirm(
        style('Do you want to provide information about a start script', fg=MessageColors.PROMPT),
        default=False
    )
    if start_script:
        start_command = click.prompt(
            style('Please provide a full command to execute your start script now', fg=MessageColors.PROMPT),
            default=chainfile_model.start
        )
        chainfile_model.start = start_command

    stop_script = click.confirm(
        style('Do you want to provide information about a stop script', fg=MessageColors.PROMPT),
        default=False
    )
    if stop_script:
        stop_command = click.prompt(
            style('Please provide a full command to execute your stop script now', fg=MessageColors.PROMPT),
            default=chainfile_model.stop
        )
        chainfile_model.stop = stop_command

    adapter = click.confirm(
        style('Do you want to provide information about the adapter type', fg=MessageColors.PROMPT),
        default=False
    )
    if adapter:
        adapter_list = AdapterFolderHandler.provide_list_of_installed_adapters()
        counter = 1
        output_string = ''
        for adapter in adapter_list:
            output_string += f'{counter}) {adapter} \n'
        adapter_type = click.prompt(
            style(f'Please choose one of the following by number \n {output_string}', fg=MessageColors.PROMPT),
            default=1
        )
        chainfile_model.adapter = adapter_type

    create_or_add_to_project(project_name, chainlink_name, user_wants_new_project)
    create_chainfile(chainfile_model, path, force)

    echo(style(f'Now registering chainlink {chainlink_name} at path {path}...', MessageColors.INFO))
    registered = ChainlinkRegistrationHandler.register_chainlink(path)
    if registered:
        echo(style(
            'Chainlink was successfully registered. No need to run chainlink:register separately',
            MessageColors.SUCCESS
        ))
    else:
        echo(style(
            'Chainlink was not registered. Check the chainfile and run chainlink:register separately'
            'once the Chainfile is fixed.',
            MessageColors.ERROR
        ))


def create_or_add_to_project(project_name: str, chainlink_name: str, new: bool):
    if new:
        ProjectFileHandler.create_new_project(project_name, [chainlink_name])
    else:
        ProjectFileHandler.add_chainlink_to_project(chainlink_name, project_name)


def create_chainfile(chainlink_config_model: ChainfileModel, path: str, force: bool):
    echo(style('Now writing the chainfile...', fg=MessageColors.INFO))
    file_created = ChainfileWriterHandler.write_chainfile(chainlink_config_model, path, force)
    if file_created is None:
        echo(style(f'Could not write chainfile because it already exists at: {path}', fg=MessageColors.WARNING))
        echo(style('To overwrite an existing chainfile use the --force switch for this command',
                   fg=MessageColors.WARNING))
    if not file_created:
        echo(style(f'Failed to write the chainfile to: {path}', fg=MessageColors.ERROR))
    else:
        echo(style(f'Successfully wrote chainfile to: {path}', fg=MessageColors.SUCCESS))
