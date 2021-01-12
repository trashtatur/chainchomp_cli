import os

import click
from chainchomplib.configlayer.model.AdapterFileModel import AdapterFileModel
from click import style, echo

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.adapter.AdapterRegistrationHandler import AdapterRegistrationHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainchomp:adapter:register')
@click.argument('name')
@click.argument('path', default=os.getcwd())
def adapter_register(name: str, path: str):
    """
    Registers an adapter
    :param name: The name of the adapter
    :param path: The path to the adapters root folder. Default is current directory
    """
    echo(style('Starting adapter registration process...', fg=MessageColors.INFO))

    start_script_set = False
    start_script = ''
    if os.path.isfile(os.path.join(path, 'start.sh')):
        set_found_start_script = click.confirm(
            style(
                'A start script has been found at the path you provided. '
                'Do you want to set it as the start script for the adapter?',
                fg=MessageColors.PROMPT
            )
        )

        if set_found_start_script:
            start_script = os.path.join(path, 'start.sh')
    else:
        while start_script_set is False:
            start_script_preliminary = click.prompt(
                style(
                    'Please provide an absolute path to a start script for your adapter now',
                    MessageColors.PROMPT
                )
            )
            if not os.path.isfile(start_script):
                is_correct = click.confirm(
                    style(
                        'The provided path is not a file. Are you certain this was correct?',
                        MessageColors.WARNING
                    )
                )
                if is_correct:
                    start_script = start_script_preliminary
                    start_script_set = True
            else:
                start_script = start_script_preliminary
                start_script_set = True

    stop_script_set = False
    stop_script = ''
    if os.path.isfile(os.path.join(path, 'start.sh')):
        set_found_stop_script = click.confirm(
            style(
                'A stop script has been found at the path you provided. '
                'Do you want to set it as the stop script for the adapter?',
                fg=MessageColors.PROMPT
            )
        )

        if set_found_stop_script:
            stop_script = os.path.join(path, 'stop.sh')
    else:
        while stop_script_set is False:
            stop_script_preliminary = click.prompt(
                style(
                    'Please provide an absolute path to a stop script for your adapter now',
                    MessageColors.PROMPT
                )
            )
            if not os.path.isfile(stop_script):
                is_correct = click.confirm(
                    style(
                        'The provided path is not a file. Are you certain this was correct?',
                        MessageColors.WARNING
                    )
                )
                if is_correct:
                    stop_script = stop_script_preliminary
                    stop_script_set = True
            else:
                stop_script = stop_script_preliminary
                stop_script_set = True

    adapter_file_model = AdapterFileModel(name, path, start_script, stop_script)
    registered = AdapterRegistrationHandler.register_adapter(adapter_file_model)
    if registered:
        echo(style(f'Adapter {name} successfully registered', MessageColors.SUCCESS))
        return

    echo(style(f'Adapter {name} could not be registered registered', MessageColors.ERROR))

