import os
import subprocess
from time import sleep

import click
from chainchomplib.configlayer.ChainlinkResolver import ChainlinkResolver
from click import echo, style

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.handlers.adapter.AdapterResolver import AdapterResolver
from chainchomp_cli.src.handlers.chainlink.ChainlinkStartHandler import ChainlinkStartHandler
from chainchomp_cli.src.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainlink:start')
@click.argument('chainlinkname')
def chainlink_start(chainlinkname: str) -> None:
    """
    This command attempts to call the start script inside of a chainfile
    and start the necessary adapter as well

    params:

    chainlinkname: The name of the chainlink to be started
    """
    chainfile_model = ChainlinkResolver.resolve(chainlinkname)
    if chainfile_model is None:
        echo(style(f'No chainlink with the name "{chainlinkname}" seems to be registered', fg=MessageColors.ERROR))
        return

    adapter_data = AdapterResolver.resolve(chainfile_model.adapter)
    if adapter_data is None:
        echo(
            style(f'No adapter with the name {chainfile_model.adapter} seems to be registered', fg=MessageColors.ERROR))
        return

    echo(style(f'Now attempting to start necessary adapter for {chainlinkname}', fg=MessageColors.INFO))
    try:
        adapter_started = subprocess.run(adapter_data['start'].split(' '))
    except Exception:
        adapter_started = False
    if adapter_started:
        echo(style('The start script of the adapter ran through successfully', MessageColors.SUCCESS))
    else:
        echo(style('The start script of the adapter seems to have encountered a problem!', MessageColors.WARNING))

    echo(style(f'Now attempting to start the chainlink itself', fg=MessageColors.INFO))
    try:
        chainlink_started = os.system(chainfile_model.start)
    except Exception:
        chainlink_started = False
    if chainlink_started:
        echo(style('The start script of the chainlink ran through successfully', MessageColors.SUCCESS))
    else:
        echo(style('The start script of the chainlink seems to have encountered a problem!', MessageColors.WARNING))

    ChainlinkStartHandler.contact_local_adapter(chainfile_model)

    urls_done = {
        'next': [],
        'previous': [],
        'url_tries': {}
    }
    echo(style(f'Now attempting to contact other chainlinks...', fg=MessageColors.INFO))
    while len(urls_done['next']) != len(chainfile_model.next_links) or \
            len(urls_done['previous']) != len(chainfile_model.previous_links):
        urls_done = ChainlinkStartHandler.contact_remote_chainlinks(chainfile_model, urls_done)
        sleep(5)

    failed_contacts = [url for url in urls_done['url_tries'].keys() if urls_done['url_tries'][url] >= 10]
    echo(style(f'Contacted next\'s: {urls_done["next"]}', fg=MessageColors.SUCCESS))
    echo(style(f'Contacted previous: {urls_done["previous"]}', fg=MessageColors.SUCCESS))
    if len(failed_contacts) is not 0:
        echo(style(f'Of those, these have failed: {failed_contacts}', fg=MessageColors.ERROR))
