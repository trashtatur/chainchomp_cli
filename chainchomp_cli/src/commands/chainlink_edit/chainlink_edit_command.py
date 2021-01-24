import os

import click
import yaml
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel
from chainchomplib.configlayer.resolver.ChainlinkResolver import ChainlinkResolver
from chainchomplib.data import PathProvider
from click import echo, style

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.adapter.AdapterFolderHandler import AdapterFolderHandler
from chainchomp_cli.src.handlers.config_file.ChainfileWriterHandler import ChainfileWriterHandler
from chainchomp_cli.src.handlers.projects.ProjectFileHandler import ProjectFileHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainlink:edit')
@click.argument('name',)
def chainlink_edit(name):
    """
    This command allows you to edit a chainlink.
    Chainchomp will look for a chainlink that is registered under the given name.
    If it can't be found the command won't do anything.

    If the file is found Chainchomp will allow you to edit it through command prompts
    :param name the name of the chainlink
    """
    echo(style('Attempting to read the provided path for the chainlink file', fg=MessageColors.INFO))

    config_model = ChainlinkResolver.resolve(name)

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

    name = click.prompt(
        style('If you want to rename the chainlink please type the name in now:', fg=MessageColors.PROMPT)
    )
    if name:
        config_model.chainlink_name = name

    project = click.prompt(
        style(
            'If you want to reassign the chainlink to another project please type the name in now:',
            fg=MessageColors.PROMPT
        )
    )

    if project:
        config_model.project_name = project
        ProjectFileHandler.remove_chainlink_from_all_projects(config_model.chainlink_name)
        if not ProjectFileHandler.project_exists(project):
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
                        'No suitable option chosen. The command will abort.',
                        fg=MessageColors.WARNING
                    )
                )
                return

        else:
            ProjectFileHandler.add_chainlink_to_project(config_model.chainlink_name, project)

    not_done_with_next_links = click.confirm(
        style('Do you want to set some next chainlinks?:', fg=MessageColors.PROMPT),
        default=False
    )
    next_links = []
    while not_done_with_next_links:
        name = click.prompt(
            style('Type in the name of the link')
        )
        ip_addr = click.prompt(
            style('Type in the address of the link')
        )
        next_links.append(f'{ip_addr}::{name}')

    if next_links:
        config_model.next_link = next_links

    not_done_with_previous_links = click.confirm(
        style('Do you want to set some previous chainlinks?:', fg=MessageColors.PROMPT),
        default=False
    )
    previous_links = []
    while not_done_with_previous_links:
        name = click.prompt(
            style('Type in the name of the link')
        )
        ip_addr = click.prompt(
            style('Type in the address of the link')
        )
        previous_links.append(f'{ip_addr}::{name}')

    if previous_links:
        config_model.previous_links = previous_links

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
    adapters = AdapterFolderHandler.provide_list_of_installed_adapters()
    while adapter not in adapters and adapter is not None:
        echo(style('That adapter is not registered. It must be one of: ', fg=MessageColors.PROMPT))
        adapter_list = "\n".join(adapters)
        echo(style(f'{adapter_list}'))
        adapter = click.prompt(
            style('Please provide the name of the adapter now:', fg=MessageColors.PROMPT)
        )

    if adapter:
        config_model.adapter = adapter

    profile = click.prompt(
        style('If you want to change the profile that is used please type that in now', fg=MessageColors.PROMPT)
    )

    if profile:
        config_model.profile = profile

    echo(style('Attempting to write new information to chainfile...', fg=MessageColors.INFO))
    edit_chainfile(config_model, name)


def edit_chainfile(chainlink_config_model: ChainfileModel, name: str):
    registrar_file = open(os.path.join(PathProvider.chainlinks_folder(), f'{name}.yml'))
    data = yaml.safe_load(registrar_file)
    echo(style('Now editing the chainfile...', fg=MessageColors.INFO))
    file_created = ChainfileWriterHandler.write_chainfile(chainlink_config_model, data.get('path', ''), True)
    if file_created is None:
        echo(style('Could not overwrite chainfile', fg=MessageColors.WARNING))
    if not file_created:
        echo(style('Failed to write the chainfile', fg=MessageColors.ERROR))
    else:
        echo(style('Successfully edited chainfile', fg=MessageColors.SUCCESS))
