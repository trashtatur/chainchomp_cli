import os

from chainchomplib import LoggerInterface
from chainchomplib.data import PathProvider


class FixturesFolderHandler:

    def provide_list_of_fixtures(self):
        pass

    @staticmethod
    def create_fixtures_folder():
        if PathProvider.fixtures_folder().is_dir():
            return False

        try:
            os.mkdir(PathProvider.fixtures_folder())
        except OSError as exception:
            LoggerInterface.error(f'Failed to create fixtures dir with exception: {exception}')
        return True
