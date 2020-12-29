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
    if chainfile_model is None:
        echo(style(f'No chainlink with the name "{chainlinkname}" seems to be registered', fg=MessageColors.ERROR))
        return

    adapter_data = AdapterResolver.resolve(chainfile_model.adapter)
    if adapter_data is None:
        echo(style(f'No adapter with the name {chainfile_model.adapter} seems to be registered', fg=MessageColors.ERROR))
        return

    echo(style(f'Now attempting to start necessary adapter for {chainlinkname}', fg=MessageColors.INFO))
    adapter_started = os.system(adapter_data['start'])
    echo(style(f'Now attempting to start the chainlink itself', fg=MessageColors.INFO))
    chainlink_started = os.system(chainfile_model.start)

    urls_done = {
        'next': [],
        'previous': [],
        'url_tries': {}
    }
    echo(style(f'Now attempting to contact other chainlinks...', fg=MessageColors.INFO))
    while len(urls_done['next'] != chainfile_model.next_link) and len(urls_done['previous'] != chainfile_model.previous_link):
        for url in chainfile_model.next_link:
            if url not in urls_done['url_tries'].keys():
                urls_done['url_tries'][url] = 0
            if urls_done['url_tries'][url] >= 10 and url not in urls_done['next']:
                urls_done['next'].append(url)
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
            if url not in urls_done['url_tries'].keys():
                urls_done['url_tries'][url] = 0
            if urls_done['url_tries'][url] >= 10 and url not in urls_done['previous']:
                urls_done['previous'].append(url)
            if url in urls_done['previous']:
                continue
            echo(style(f'Trying to next contact chainlink : {url}', fg=MessageColors.INFO))
            url = f"http://{url.split('::')[0]}:{4410}/adapter/assign/link"
            params = {'chainfile': chainfile_model.get_serialized()}
            response = requests.get(url=url, params=params, timeout=1)
            if response.status_code == 200:
                echo(style(f'Successfully transmitted to chainlink : {url}', fg=MessageColors.SUCCESS))
                urls_done['previous'].append(url)
            urls_done['url_tries'][url] += 1
        sleep(5)

    failed_contacts = [url for url in urls_done['url_tries'].keys() if urls_done['url_tries'][url] >= 10]
    echo(style(f'Contacted next\'s: {urls_done["next"]}', fg=MessageColors.SUCCESS))
    echo(style(f'Contacted previous: {urls_done["previous"]}', fg=MessageColors.SUCCESS))
    if len(failed_contacts) is not 0:
        echo(style(f'Of those, these have failed: {failed_contacts}', fg=MessageColors.ERROR))
