import os

import click


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
    pass
