import os
from time import sleep

import click
import requests
from click import echo, style

from chainchomp_cli.src.cli import MessageColors
from chainchomp_cli.src.core.handlers.adapter.AdapterResolver import AdapterResolver
from chainchomp_cli.src.core.handlers.chainlink.ChainlinkResolver import ChainlinkResolver
from chainchomp_cli.src.core.handlers.setup.SetupHandler import SetupHandler


@SetupHandler.is_setup
@click.command('chainlink:start')
@click.argument('chainlinkname')
def chainlink_start(chainlinkname):
    """
    This command attempts to call the start script inside of a chainfile
    and start the necessary adapter as well

    params:

    chainlinkname: The name of the chainlink to be started
    """
    chainfile_model = ChainlinkResolver.resolve(chainlinkname)
    adapter_data = AdapterResolver.resolve(chainfile_model.adapter)
    echo(style(f'Now attempting to start necessary adapter for {chainlinkname}', fg=MessageColors.INFO))
    adapter_started = os.system(adapter_data['start'])
    echo(style(f'Now attempting to start the chainlink itself', fg=MessageColors.INFO))
    chainlink_started = os.system(chainfile_model.start)

    urls_done = {
        'next': [],
        'previous': [],
    }
    echo(style(f'Now attempting to contact other chainlinks...', fg=MessageColors.INFO))
    while len(urls_done['next'] != chainfile_model.next_link) and len(urls_done['previous'] != chainfile_model.previous_link):
        for url in chainfile_model.next_link:
            if url in urls_done['next']:
                continue
            echo(style(f'Trying to next contact chainlink : {url}', fg=MessageColors.INFO))
            url = f"http://{url.split('::')[0]}:{4410}"
            params = {'chainfile': chainfile_model.get_serialized()}
            response = requests.get(url=url, params=params, timeout=1)
            if response.status_code == 200:
                echo(style(f'Successfully transmitted to chainlink : {url}', fg=MessageColors.SUCCESS))
                urls_done['next'].append(url)

        for url in chainfile_model.previous_link:
            if url in urls_done['previous']:
                continue
            echo(style(f'Trying to next contact chainlink : {url}', fg=MessageColors.INFO))
            url = f"http://{url.split('::')[0]}:{4410}"
            params = {'chainfile': chainfile_model.get_serialized()}
            response = requests.get(url=url, params=params, timeout=1)
            if response.status_code == 200:
                echo(style(f'Successfully transmitted to chainlink : {url}', fg=MessageColors.SUCCESS))
                urls_done['previous'].append(url)

        sleep(5)
