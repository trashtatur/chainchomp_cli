import os
from collections import Callable

import click
from chainchomplib.data import PathProvider
from click import style, echo

from chainchomp_cli.src.MessageColorEnum import MessageColorEnum


class SetupHandler:

    @staticmethod
    def is_setup(func: Callable) -> Callable:
        is_setup = PathProvider.base_config_folder().is_dir() \
               and PathProvider.projects_folder().is_dir() \
               and PathProvider.env_var_folder().is_dir() \
               and PathProvider.profiles_folder().is_dir()

        @click.command(hidden=True)
        def is_not_setup():
            echo(style('Oh no it looks like you haven\'t set up chainchomp on this machine yet. Please run '
                       'chainchomp:setup before you continue', fg=MessageColorEnum.ERROR))

        if is_setup:
            return func

        return is_not_setup

    @staticmethod
    def create_base_folder():
        if PathProvider.base_config_folder().is_dir():
            return False
        try:
            os.mkdir(PathProvider.base_config_folder())
        except OSError:
            # TODO Proper exception
            print('Failed to create base dir')

        return True
