import os

from chainchomplib import LoggerInterface
from chainchomplib.data import PathProvider


class LogsFolderHandler:

    @staticmethod
    def create_log_folder():
        if PathProvider.log_folder().is_dir():
            return False

        try:
            os.mkdir(PathProvider.log_folder())
        except OSError as exception:
            LoggerInterface.error(f'Could not create log folder with os Error: {exception}')
        return True
