import os
import click
from chainchomplib.configlayer.model.ChainlinkConfigModel import ChainlinkConfigModel
from click import echo, style

from chainchomp_cli.src.core.handlers.config_file.ConfigWriterHandler import ConfigWriterHandler
from chainchomp_cli.src.core.handlers.projects.ProjectFileHandler import ProjectFileHandler
from chainchomp_cli.src.core.handlers.projects.ProjectsFolderHandler import ProjectsFolderHandler
from chainchomp_cli.src.core.handlers.setup.SetupHandler import SetupHandler


@click.command('chainlink:create')
@click.argument('path', default=os.getcwd())
@click.option('--force/--soft',
              default=False,
              help='Force overwriting of an existing chainfile'
              )
def chainlink_create(path, force):
    """
    parameters:
    path: Absolute path to where the config file should be created. Defaults to current working directory

    This command creates a configuration file for your project.
    The configuration file will be stored at the current working directory
    (which should be your projects root directory) or at the path that you
    specify as a parameter.

    Through this, it gets registered as a chainlink.
    You get the options to let chainchomp handle and set most of the
    options, though you can always change them later.
    :param path: Absolute path to where the config file should be created. Defaults to current working directory
    :return:
    """

    if not SetupHandler.is_setup():
        echo(style('Oh no it looks like you haven\'t set up chainchomp on this machine yet. Please run '
                   'chainchomp:setup before you continue', fg='red'))
        return

    echo(style('Welcome to Chainchomp. We can see that you want to add a new chainlink', fg='cyan'))
    echo(style('What is the project that this chainlink is assigned to', fg='cyan'))
    projects_list = ProjectsFolderHandler.provide_list_of_projects()
    user_wants_new_project = False
    if projects_list is not []:
        output_string = f'Press 0 to make a new project \n'
        counter = 1
        for project in projects_list:
            output_string += f'{counter}) {project} \n'
        echo(style('You can choose from already existing projects, or make a new one', fg='cyan'))
        project_name_index = click.prompt(output_string, default=0)
        if project_name_index == 0:
            user_wants_new_project = True
        if project_name_index != 0:
            project_name = projects_list[project_name_index - 1]
    if user_wants_new_project:
        project_name = click.prompt('Please type in the designated project name now')

    echo(style('Now please provide a name for your chainlink', fg='cyan'))
    chainlink_name = click.prompt('Please type in the designated name now')
    chainlink_config_model = ChainlinkConfigModel(project_name, chainlink_name)

    more_information = click.confirm(style('Do you want to input further details?', fg='cyan'), default=False)
    if not more_information:
        create_chainfile(chainlink_config_model, path, force)
        create_or_add_to_project(project_name, chainlink_name, user_wants_new_project)
        return

    master_link = click.confirm('Is this chainlink a Master link?', default=chainlink_config_model.is_master_link)
    if not master_link:
        master_location = click.prompt('Do you want to provide information about the master link location?',
                                       default=False)
        if master_location:
            master_location = click.prompt('Please provide an ip address for the master chainlink',
                                           default=chainlink_config_model.master_location)
            chainlink_config_model.master_location = master_location

    start_script = click.confirm(style('Do you want to provide information about a start script', fg='cyan'),
                                 default=False)
    if start_script:
        start_command = click.prompt('Please provide a full command to execute your start script now',
                                     default=chainlink_config_model.start)
        chainlink_config_model.start = start_command

    stop_script = click.confirm(style('Do you want to provide information about a stop script', fg='cyan'),
                                default=False)
    if stop_script:
        stop_command = click.prompt('Please provide a full command to execute your stop script now',
                                    default=chainlink_config_model.stop)
        chainlink_config_model.stop = stop_command

    mq = click.confirm(style('Do you want to provide information about the message queue type', fg='cyan'),
                       default=False)
    if mq:
        default = 1 if chainlink_config_model.mq_type == 'rabbitmq' else 2
        mq_type = click.prompt('Please choose one of the following by number \n'
                               '1) RabbitMQ\n'
                               '2) Apache Kafka\n',
                               default=default)
        chainlink_config_model.mq_type = mq_type

    create_or_add_to_project(project_name, chainlink_name, user_wants_new_project)
    create_chainfile(chainlink_config_model, path, force)


def create_or_add_to_project(project_name: str, chainlink_name: str, new: bool):
    project_file_handler = ProjectFileHandler()
    if new:
        project_file_handler.create_new_project(project_name, [chainlink_name])
    else:
        project_file_handler.add_chainlink_to_project(chainlink_name, project_name)


def create_chainfile(chainlink_config_model: ChainlinkConfigModel, path: str, force: bool):
    echo(style('Now writing the chainlink file...', fg='cyan'))
    file_created = ConfigWriterHandler.write_config_file(chainlink_config_model, path, force)
    if file_created is None:
        echo(style(f'Could not write chainfile because it already exists at: {path}', fg='yellow'))
        echo(style('To overwrite an existing chainfile use the --force switch for this command', fg='yellow'))
    if not file_created:
        echo(style(f'Failed to write the chainlink file to: {path}', fg='red'))
    else:
        echo(style(f'Successfully wrote chainlink file to: {path}', fg='green'))
